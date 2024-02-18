# Cisco SNMP Changer
 Change Cisco SNMP community strings on IOS and IOS XR

## Overview

This Python script is designed to automate the modification of SNMP configurations on Cisco IOS and XR devices. It utilizes the Netmiko library for network automation and supports concurrent execution on multiple devices.

## Features

- **SNMP Configuration Modification:** The script connects to Cisco devices and modifies SNMP configuration strings, replacing old strings with new ones.

- **Concurrency:** Utilizes concurrent execution to efficiently process multiple devices simultaneously.

- **Logging:** Logs important events and errors to a file (`script_log.txt`).

- **Device Reachability Check:** Checks if a device is reachable before attempting to connect.

## Prerequisites

- Python 3.x
- Netmiko library (`pip install netmiko`)

## Usage

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/CliveMlt/Cisco-SNMP-Changer/
    cd Cisco-SNMP-Changer
    ```

2. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Edit Devices File:**

    Update the `Devices.txt` file with the details of your devices in the following format:

    ```plaintext
    hostname:device_type:username:password:enable_password
    ```

4. **Change SNMP Community Strings:**

    Update the `cisco_snmp_changer.py` python script with the details of your SNMP community strings by changing the items below:

    ```plaintext
    Current SNMP read only string = old_snmp_ro 
    Current SNMP read write string = old_snmp_rw
    New SNMP read only string = NEW1RO
    New SNMP read only string = NEW2RW
    ```

5. **Run the Script:**

    ```bash
    python cisco_snmp_changer.py
    ```

6. **View Logs:**

    Check the `script_log.txt` file for detailed logs of script execution.
