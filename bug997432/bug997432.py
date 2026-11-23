from cloudvision.cvlib import ActionFailed

def get_device_info():
    """Retrieve the device model and serial number from the command response."""
    try:
        response = ctx.runDeviceCmds(["enable", "show inventory | json"])
        ctx.alog(f"DEBUG: Device inventory response: {response}")
        
        for entry in response:
            if "response" in entry and "systemInformation" in entry["response"]:
                system_info = entry["response"]["systemInformation"]
                model = system_info.get("name", "Unknown Model")
                serial = system_info.get("serialNum", "Unknown Serial")
                return model, serial
    except Exception as e:
        ctx.alog(f"ERROR: Failed to get device info: {e}")
    return None, None

def get_firmware_version(model):
    """Retrieve the firmware version based on the model-specific keyword."""
    model_keywords = {
        "DCS-7280SR3-48YC8": "vrm2",
        "DCS-7280SR3K-48YC8": "vrm2",
        "7280SR3K-48YC8A": "vrm2",
        "DCS-7280SR3M-48YC8": "vrm4",
        "DCS-7280SR3MK-48YC8A-S": "vrm4"
    }
    keyword = model_keywords.get(model, None)
    if not keyword:
        ctx.alog(f"INFO: Model {model} is not in the affected list. No firmware check required.")
        return "Not Applicable"
    
    try:
        response = ctx.runDeviceCmds(["enable", "show version detail | json"])
        ctx.alog(f"DEBUG: Firmware response: {response}")
        
        if response and "response" in response[0] and "details" in response[0]["response"]:
            components = response[0]["response"].get("details", {}).get("components", [])
            
            for component in components:
                if keyword in component.get("name", "").lower():
                    version_str = component.get("version", "")
                    ctx.alog(f"DEBUG: Found firmware version string: {version_str}")
                    
                    try:
                        version_num = float(version_str.split(".")[0])
                        return version_num
                    except ValueError:
                        ctx.alog(f"ERROR: Unable to parse firmware version: {version_str}")
                        return None
    except Exception as e:
        ctx.alog(f"ERROR: Failed to get firmware version: {e}")
    
    return None

def main():
    try:
        # Step 1: Get device model and serial
        model, serial = get_device_info()
        if not model or not serial:
            ctx.alog("ERROR: Could not determine device model or serial number.")
            return
        
        ctx.alog(f"INFO: Identified device model: {model}, Serial: {serial}")
        
        # Step 2: Get firmware version
        firmware_version = get_firmware_version(model)
        if firmware_version == "Not Applicable":
            ctx.alog(f"INFO: Device {model} (Serial: {serial}) is not affected by this issue.")
            return
        
        if firmware_version is None:
            ctx.alog("ERROR: Could not determine firmware version.")
            return
        
        # Step 3: Check if the device is susceptible
        if firmware_version < 6:
            ctx.alog(f"RESULT: Device {model} (Serial: {serial}) is SUSCEPTIBLE (firmware version: {firmware_version}).")
        else:
            ctx.alog(f"RESULT: Device {model} (Serial: {serial}) is NOT susceptible (firmware version: {firmware_version}).")
    
    except ActionFailed as e:
        ctx.alog(f"ERROR: Command execution failed: {e}")

if __name__ == "__main__":
    main()
