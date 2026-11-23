# python3 pyclearpass.py --clearpass-server 1.1.1.1 --clearpass-api-token abc --clearpass-radius-secret abc --clearpass-group-name group1 --hostname HQ-LEAF-3 --managementip 10.92.62.2
import subprocess
import sys
import argparse
from typing import List, Dict

clearpass_server = ctx.changeControl.args["Clearpass Server"]
clearpass_api_token = ctx.changeControl.args["Clearpass Api Token"]
ctx.alog(f"{clearpass_api_token}")
clearpass_radius_secret = ctx.changeControl.args["Clearpass Radius Secret"]
group_name = ctx.changeControl.args["Clearpass Group Name"]
mgmt_vrf = "default"

def get_switch_info():
    ctx.alog("Getting Management IP")
    mgmt_ip = ctx.device.ip
    ctx.alog(f"Retrieved Management IP: {mgmt_ip}")

    ctx.alog("Getting Hostname and FQDN")
    cmds = ["enable", "show hostname"]
    cmdResponses: List[Dict] = ctx.runDeviceCmds(cmds)

    errs = [resp.get('error') for resp in cmdResponses if resp.get('error')]
    if errs:
        raise Exception(f"Failed to retrieve hostname: {errs[0]}")

    hostname = str(cmdResponses[1]["response"]["hostname"])
    fqdn = str(cmdResponses[1]["response"].get("fqdn", ""))

    ctx.alog(f"Retrieved Hostname: {hostname}")
    ctx.alog(f"Retrieved FQDN: {fqdn}")
    return mgmt_ip, hostname, fqdn

# Get switch info
ctx.alog("Getting switch info")
mgmt_ip, hostname, fqdn = get_switch_info()

# Python script for the switch
python_script = '''
import subprocess
import sys
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Script to configure switch in ClearPass")
    parser.add_argument("--clearpass-server", required=True, help="ClearPass Server IP or hostname")
    parser.add_argument("--clearpass-api-token", required=True, help="API token for ClearPass")
    parser.add_argument("--clearpass-radius-secret", required=True, help="Radius secret for the device")
    parser.add_argument("--clearpass-group-name", required=True, help="ClearPass Group Name")
    parser.add_argument("--vrf", default="default", help="Management VRF for package installation")
    parser.add_argument("--hostname", required=True, help="HostName")
    parser.add_argument("--managementip", required=True, help="MGMT IP")
    return parser.parse_args()

# Parse arguments
args = parse_arguments()
clearpass_server = args.clearpass_server
clearpass_api_token = args.clearpass_api_token
clearpass_radius_secret = args.clearpass_radius_secret
group_name = args.clearpass_group_name
mgmt_vrf = args.vrf
hostname = args.hostname
mgmt_ip = args.managementip

def install_package(package, mgmt_vrf="default"):
    # Installs a pip package from within a Python script.
    subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)

def uninstall_package(package):
    # Uninstalls a pip package from within a Python script.
    subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", package], check=True)

# Install pyclearpass
print("Installing pyclearpass")
install_package("pyclearpass", mgmt_vrf)

from pyclearpass import *

# Login to ClearPass
print(f"Logging into ClearPass ({clearpass_server})")
login = ClearPassAPILogin(server=f"https://{clearpass_server}:443/api",
                          api_token=clearpass_api_token, 
                          verify_ssl=False)

# Add new network access device
print(f"Adding {hostname} ({mgmt_ip}) to ClearPass")
newNAD = {{
    "description": "{hostname}",
    "name": "{hostname}",
    "ip_address": "{mgmt_ip}",
    "radius_secret": "{clearpass_radius_secret}",
    "vendor_name": "Arista",
    "coa_capable": True,
    "coa_port": 3799,
}}
ApiPolicyElements.new_network_device(login, body=newNAD)

# Map new device to group
print(f"Mapping {hostname} ({mgmt_ip}) to group {group_name} in ClearPass")
getcurrentnads = ApiPolicyElements.get_network_device_group_name_by_name(login, name="{group_name}")
newnads = {{"value": "{mgmt_ip}"}}
newnads["value"] = getcurrentnads['value'] + ", " + newnads["value"]
ApiPolicyElements.update_network_device_group_name_by_name(login, name="{group_name}", body=newnads)

# Uninstall
print("Uninstalling pyclearpass")
uninstall_package("pyclearpass")
'''

# Push the script to the switch and execute it
ctx.alog("Executing script on the switch")
try:
    call_script = f"bash timeout 90 python3 pyclearpass.py --clearpass-server={clearpass_server} --clearpass-api-token={clearpass_api_token} --clearpass-radius-secret={clearpass_radius_secret} --clearpass-group-name={group_name} --vrf={mgmt_vrf} --hostname={hostname} --managementip={mgmt_ip}"
    # Execute the Python script on the switch
    ctx.runDeviceCmds(["enable",
                       {"cmd": f"copy terminal: file:/mnt/flash/pyclearpass.py", "input": python_script},
                       call_script
                    ]) 
except Exception as e:
    ctx.alog(f"Error executing script: {e}")
    raise Exception(f"Script execution failed: {e}")

ctx.alog("Action completed successfully")
