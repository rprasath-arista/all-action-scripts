from cloudvision.cvlib import ActionFailed
from typing import List, Dict

def check_smart_emmc(cmdResponses: List[Dict]) -> bool:
    """Check if the device uses Smart eMMC (08GP1A/16GP1A)."""
    for response in cmdResponses:
        if "response" in response and "storageDevices" in response["response"]:
            storage_devices = response["response"]["storageDevices"]
            for device_info in storage_devices.values():
                model = device_info.get("model", "")
                if "08GP1A" in model or "16GP1A" in model:
                    ctx.alog("Smart eMMC detected: Model {model}")
                    return True
    return False

def main():
    """Main function to check for SMART eMMC storage."""
    try:
        inventory_response = ctx.runDeviceCmds(["show inventory"])
        cmdResponse = ctx.runDeviceCmds(["show hostname"])
        
        if cmdResponse and 'response' in cmdResponse[0]:
            hostname = cmdResponse[0]["response"]["hostname"]

        if not check_smart_emmc(inventory_response):
            ctx.alog(f"RESULT: No Smart eMMC (08GP1A/16GP1A) detected in {hostname}")
            return

        ctx.alog(f"RESULT: Smart eMMC (08GP1A/16GP1A detected in {hostname}!!!")

    except ActionFailed as e:
        ctx.alog(f"Failed to execute command: {e}")

if __name__ == "__main__":
    main()