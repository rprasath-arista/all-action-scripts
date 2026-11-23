from typing import List, Dict

ad_server = ctx.changeControl.args["AD Server"]
ad_username = ctx.changeControl.args["Username"]
ad_password = ctx.changeControl.args["Password"]
dns_zone = ctx.changeControl.args["DNS Zone"]

def get_switch_info():
    ctx.alog("Getting Management IP")
    mgmt_ip = ctx.device.ip
    ctx.alog(f"Retrieved Management IP: {mgmt_ip}")

    ctx.alog("Getting Hostname")
    cmds = ["enable", "show hostname"]
    cmdResponses: List[Dict] = ctx.runDeviceCmds(cmds)

    errs = [resp.get('error') for resp in cmdResponses if resp.get('error')]
    if errs:
        raise Exception(f"Failed to retrieve hostname: {errs[0]}")

    hostname = str(cmdResponses[1]["response"]["hostname"])

    ctx.alog(f"Retrieved Hostname: {hostname}")
    return mgmt_ip, hostname


# Get switch info
ctx.alog("Getting switch info")
mgmt_ip, hostname = get_switch_info()

# Python script for the switch
python_script = '''
import subprocess
import argparse
import sys

def install_package(package, mgmt_vrf="default"):
    # Installs a pip package from within a Python script.
    subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)

def uninstall_package(package):
    # Uninstalls a pip package from within a Python script.
    subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", package], check=True)

# Parse arguments
parser = argparse.ArgumentParser(description="Add Network Device to AD DNS via WinRM")
parser.add_argument("--ad-server", required=True, help="Active Directory Server IP/FQDN")
parser.add_argument("--ad-username", required=True, help="Username for AD server")
parser.add_argument("--ad-password", required=True, help="Password for AD server")
parser.add_argument("--dns-zone", required=True, help="DNS Zone for AD")
args = parser.parse_args()

install_package("winrm")

import winrm

powershell_cmd = (
    'Add-DnsServerResourceRecordA -Name "{hostname}" '
    '-ZoneName "{args.dns_zone}" -IPv4Address "{mgmt_ip}" '
    '-ComputerName "{args.ad_server}"'
)

session = winrm.Session(
    "{args.ad_server}",
    auth=("{args.ad_username}", "{args.ad_password}"),
    transport="ntlm"
)

try:
    result = session.run_ps(powershell_cmd)

    if result.status_code == 0:
        print(f"Successfully added DNS record: {hostname} -> {mgmt_ip}")
    else:
        print(f"Failed to add DNS record: {result.std_err.decode('utf-8', errors='ignore')}")
except Exception as e:
    print(f"Error executing remote PowerShell: {str(e)}")


uninstall_package("winrm")
'''

ctx.alog("Executing script on the switch")
try:
    # Execute the Python script on the switch
    call_script = f"bash timeout 90 python3 /mnt/flash/dns_update.py --ad-server={ad_server} --ad-username={ad_username} --ad-password={ad_password} --dns-zone={dns_zone}"
    ctx.runDeviceCmds(["enable",
                      {"cmd": f"copy terminal: file:/mnt/flash/dns_update.py", "input": python_script},
                       call_script
                    ]) 
except Exception as e:
    ctx.alog(f"Error executing script: {e}")
    raise Exception(f"Script execution failed: {e}")

ctx.alog("Action completed successfully")
