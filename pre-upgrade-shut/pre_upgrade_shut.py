from cloudvision.cvlib import ActionFailed
from typing import List, Dict
import time

# Input from user: Interfaces
ctx.alog("Enter interfaces as a list separated by a comma")
interfacesStr: str = ctx.action.args.get("interfaces")
# Split the comma-separated string on the comma and strip any whitespace
interface_list = [intf.strip() for intf in interfacesStr.split(',')]
# Filter out empty values from the split
interfaces = list(filter(None, interface_list))
# If the list is empty, raise an error
if not interfaces:
    raise ActionFailed("Interface list passed to script is empty")

'''
# Use a flag variable to determine if routing table change is expected or not during the update
# False means routing table is NOT expected to change because of the update
flag = ctx.action.args.get("flag", "false").lower() == "true"
'''

# Shutdown interfaces
def shutdown_interfaces() -> None:
    cmds = []
    for interface in interfaces:
        cmds.extend([
            "enable",
            "configure",
            f"interface {interface}",
            "shutdown",
            "exit"
        ])
    ctx.runDeviceCmds(cmds)
    ctx.alog(f"Shutdown interfaces: {','.join(interfaces)}")

# Main function
def main():
    try:
        '''Step 1: Get the route count before shutting down interfaces
        ctx.alog("Fetching route count before shutdown...")
        count_before = ctx.retrieve(path=['DeviceID:/Smash/routing/status/_counts/route'])
        ctx.alog(count_before)
'''
        # Step 2: Shut down the specified interfaces
        ctx.alog("Shutting down interfaces...")
        shutdown_interfaces()

        time.sleep(10)

        # Step 3: Assume update function
        ctx.alog("Proceed with Upgrade.")
        
    except Exception as e:
        ctx.alog(f"Script failed: {str(e)}")
        raise ActionFailed(f"Script execution failed: {str(e)}")

if __name__ == "__main__":
    main()
