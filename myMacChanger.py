import subprocess
import argparse
import re
import platform

def get_user_input():
   
    parser = argparse.ArgumentParser(description="Change MAC address of a network interface.")
    parser.add_argument("-i", "--interface", dest="interface", required=True, help="Network interface for MAC address changing")
    parser.add_argument("-m", "--mac", dest="mac_address", required=True, help="New MAC address")
    
    
    args = parser.parse_args()
    return args

def change_mac_address(interface, mac_address):
    print(f"[+] Changing MAC address for {interface} to {mac_address}")

    
    os_type = platform.system()

    if os_type == "Linux":
        
        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(["ifconfig", interface, "hw", "ether", mac_address])
        subprocess.call(["ifconfig", interface, "up"])
    elif os_type == "Darwin":  # macOS
        
        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(["ifconfig", interface, "ether", mac_address])  
        subprocess.call(["ifconfig", interface, "up"])
    else:
        print(f"[-] Unsupported OS: {os_type}")

def get_mac_address(interface):
    ifconfig = subprocess.check_output(["ifconfig", interface]).decode('utf-8')
    new_mac = re.search(r"([0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5})", ifconfig)
    if new_mac:
        return new_mac.group(0)
    else:
        return None

def check_mac_address(interface, mac_address):
    finalize_mac = get_mac_address(interface)
    if finalize_mac == mac_address:
        print("[+] MAC address changed successfully!")
    else:
        print("[-] MAC address did not change. Please check permissions or syntax.")


user_input = get_user_input()

print("MAC changer started!")
change_mac_address(user_input.interface, user_input.mac_address)
check_mac_address(user_input.interface, user_input.mac_address)
