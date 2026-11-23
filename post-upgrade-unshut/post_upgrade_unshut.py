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

# Unshut interfaces
def unshut_interfaces() -> None:
    cmds = []
    for interface in interfaces:
        cmds.extend([
            "enable",
            "configure",
            f"interface {interface}",
            "no shutdown",
            "exit"
        ])
    ctx.runDeviceCmds(cmds)
    ctx.alog(f"Enabled interfaces: {','.join(interfaces)}")

# Get route count
def get_count() -> List[str]:
    try:
        response = ctx.runDeviceCmds(["show ip route"])[0]["response"]
        # Extract routes from the output
        routes = [line.strip() for line in response.get("output", "").split('\n') if line.strip()]
        return routes
    except Exception as e:
        ctx.alog(f"Failed to fetch route count: {str(e)}")
        raise ActionFailed("Unable to retrieve route count")

# Compare route count
def compare_count(before: List[str], after: List[str]) -> bool:
    if len(before) != len(after):
        ctx.alog("Route count changed after upgrade")
        return False

    for i, (route_before, route_after) in enumerate(zip(before, after)):
        if route_before != route_after:
            ctx.alog(f"Route mismatch at line {i + 1}:")
            ctx.alog(f"  Before: {route_before}")
            ctx.alog(f"  After:  {route_after}")
            return False

    ctx.alog("Route count match before and after upgrade")
    return True

# Main function
def main():
    try:
        # Step 1: Unshut the interfaces
        ctx.alog("Unshutting interfaces...")
        unshut_interfaces()

        # Step 2: Wait for the network to stabilize again
        ctx.alog("Waiting for network stabilization...")
        time.sleep(10) 

        ctx.alog("DONE")

        '''# Step 3: Get the route count after unshutting interfaces
        ctx.alog("Fetching route count after unshut...")

        count_after = ctx.retrieve(path=['DeviceID:/Smash/routing/status/_counts'])

        # Step 4: Compare route count
        ctx.alog("Comparing route count...")
        if compare_count(count_before, count_after):
            ctx.alog("SUCCESS: Route count match. No changes detected.")
            
            ctx.clear(path=[''])
            ctx.alog("Deleted temporary comparison route count.")
        else:
            ctx.alog("FAILURE: Route count differ. Changes detected after shutdown/unshut.")
'''
    except Exception as e:
        ctx.alog(f"Script failed: {str(e)}")
        raise ActionFailed(f"Script execution failed: {str(e)}")

if __name__ == "__main__":
    main()
