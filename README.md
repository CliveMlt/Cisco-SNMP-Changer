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
    git clone https://github.com/your-username/network-configuration-script.git
    cd network-configuration-script
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

4. **Run the Script:**

    ```bash
    python network_config_script.py
    ```

5. **View Logs:**

    Check the `script_log.txt` file for detailed logs of script execution.
