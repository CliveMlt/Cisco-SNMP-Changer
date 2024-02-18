import concurrent.futures
from netmiko import ConnectHandler
import netmiko
import logging
import subprocess

#################################################################################################
# Configure logging to write to a file
logging.basicConfig(filename='script_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#################################################################################################
#Banner Intro
def banner():
    print(
    """
   _____ _   ____  _______     ________  _____    _   __________________ 
  / ___// | / /  |/  / __ \   / ____/ / / /   |  / | / / ____/ ____/ __ \\
  \__ \/  |/ / /|_/ / /_/ /  / /   / /_/ / /| | /  |/ / / __/ __/ / /_/ /
 ___/ / /|  / /  / / ____/  / /___/ __  / ___ |/ /|  / /_/ / /___/ _, _/ 
/____/_/ |_/_/  /_/_/       \____/_/ /_/_/  |_/_/ |_/\____/_____/_/ |_|                                                                      
                                                                                                                                                                                                                     
    """
    )
    
#################################################################################################
def ping_device(ip):
    """Check if device is reachable."""
    try:
        ping_response = subprocess.run(['ping', '-n', '2', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return ping_response.returncode == 0  # Return True if ping succeeds, False otherwise
    except Exception as e:
        logging.error(f"Error during ping check: {str(e)}")
        return False

#################################################################################################
def get_device_info(device_line):
    """Extracts device info from a line in the Devices.txt file."""
    hostname, device_type, username, password, enable_password = device_line.strip().split(':')
    return {
        'device_type': device_type,
        'ip': hostname,
        'username': username,
        'password': password,
        'secret': enable_password  
    }

#################################################################################################
def modify_snmp_config(device_info):
    try:
        """Modify snmp community strings."""

        # Check if the device is reachable
        if not ping_device(device_info['ip']):
            logging.error(f"Device {device_info['ip']} is not reachable.")
            return f"Device {device_info['ip']} is not reachable."

        print(f"Connecting to {device_info['ip']}")
        
        connection = ConnectHandler(**device_info)

        if device_info['device_type'] == 'cisco_ios':
            # Enter enable mode
            print(f"Entering Enable Mode in {device_info['ip']}")
            connection.enable()

            # Check if enable mode has been entered successfully
            if not connection.check_enable_mode():
                logging.error(f"Failed to enter enable mode on {device_info['ip']}")
                return f"Failed to enter enable mode on {device_info['ip']}"


        # Check for old_snmp_ro
        snmp_output_old_snmp_ro = connection.send_command("sh run | inc old_snmp_ro")
        logging.info(f"Searching for SNMP RO string' from {device_info['ip']}:{snmp_output_old_snmp_ro}")

        # Check for old_snmp_rw
        snmp_output_old_snmp_rw = connection.send_command("sh run | inc old_snmp_rw")
        logging.info(f"Searching for SNMP RW string' from {device_info['ip']}:{snmp_output_old_snmp_rw}")

        lines_to_remove = [line for line in snmp_output_old_snmp_ro.splitlines() if 'old_snmp_ro' in line] + \
                        [line for line in snmp_output_old_snmp_rw.splitlines() if 'old_snmp_rw' in line]
        
        if lines_to_remove:
            # Enter configuration mode
            connection.config_mode()
            
            # Remove old config lines
            for line in lines_to_remove:
                print(f"Sending command to {device_info['ip']}: no {line}")
                connection.send_config_set(f"no {line}", exit_config_mode=False)
                logging.info(f"Removing old SNMP string from {device_info['ip']}")

            if device_info['device_type'] == 'cisco_ios':
                # Save configuration after removing old config
                print(f"Sending command to {device_info['ip']}: wr mem")
                connection.send_command("wr mem")
                logging.info(f"Saving configuration on {device_info['ip']}")

                # Re-enter configuration mode for new commands
                connection.config_mode()

            elif device_info['device_type'] == 'cisco_xr':
                # Commit changes after removing old config
                print(f"Sending command to {device_info['ip']}: commit")
                connection.send_command("commit")
                logging.info(f"Saving configuration on {device_info['ip']}")

            # Add new config lines
            for line in lines_to_remove:
                new_line = line.replace('old_snmp_ro', 'NEW1RO').replace('old_snmp_rw', 'NEW2RW')
                print(f"Sending command to {device_info['ip']}: {new_line}")
                connection.send_config_set(new_line, exit_config_mode=False)
                logging.info(f"Configuring new SNMP strings on {device_info['ip']}:{new_line}")

            # Save configuration after adding new config
            if device_info['device_type'] == 'cisco_ios':
                print(f"Sending command to {device_info['ip']}: wr mem")
                connection.send_command("wr mem")
                logging.info(f"Saving configuration on {device_info['ip']}")

            elif device_info['device_type'] == 'cisco_xr':
                print(f"Sending command to {device_info['ip']}: commit")
                connection.send_command("commit")
                logging.info(f"Saving configuration on {device_info['ip']}")

            result = f"Configuration modified and saved for: {device_info['ip']}"
        else:
            result = f"No old SNMP strings found for: {device_info['ip']}"

        connection.disconnect()

        return result
    except netmiko.NetmikoTimeoutException:
        logging.error(f"Timeout connecting to {device_info['ip']}")
        return f"Timeout connecting to {device_info['ip']}"
    except netmiko.NetmikoAuthenticationException:
        logging.error(f"Authentication failed for {device_info['ip']}")
        return f"Authentication failed for {device_info['ip']}"
    except Exception as e:
        logging.error(f"Error processing {device_info['ip']}: {str(e)}")
        return f"Error processing {device_info['ip']}: {str(e)}"


#################################################################################################
def main():
    with open('Devices.txt', 'r') as f:
        # Exclude commented-out lines and blank lines
        device_lines = [line for line in f.readlines() if not line.strip().startswith('#') and line.strip()]

    # Extract the device information from the file
    devices = [get_device_info(line) for line in device_lines]

    # ThreadPoolExecutor is used to send the commands to devices concurrently
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(devices)) as executor:
            results = list(executor.map(modify_snmp_config, devices))
            for result in results:
                print(result)
    except Exception as e:
        logging.error(f"Error in thread execution: {str(e)}")
        print(f"Error in thread execution: {str(e)}")

#################################################################################################
if __name__ == '__main__':
    banner()
    main()