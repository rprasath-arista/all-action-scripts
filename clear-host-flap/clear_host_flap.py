from cloudvision.cvlib import ActionFailed
from typing import List, Dict

def clear_bgp_evpn_host_flaps():
    ctx.alog("Running 'clear bgp evpn host-flaps' command")

    try:
        cmds = ["enable", "clear bgp evpn host-flaps"]
        responses = ctx.runDeviceCmds(cmds)

        errors = [resp.get("error") for resp in responses if resp.get("error")]
        if errors:
            ctx.alog(f"Error executing command: {errors[0]}")
            raise Exception(errors[0])

        ctx.alog("Successfully cleared BGP EVPN host-flaps on this device")

    except Exception as e:
        ctx.alog(f"Failed to clear BGP EVPN host-flaps: {str(e)}")
        raise

    ctx.alog("Action completed")

if __name__ == "__main__":
    clear_bgp_evpn_host_flaps()
