# Add Device to Clearpass

CloudVision action script to automatically register an Arista switch as a Network Access Device (NAD) in Aruba ClearPass and map it to a device group.

## What It Does

1. Retrieves the device management IP, hostname, and FQDN from the switch
2. Copies a Python helper script to the switch flash storage
3. The helper script installs `pyclearpass`, registers the switch as a NAD in ClearPass with RADIUS and CoA settings, and maps it to the specified device group
4. Cleans up by uninstalling `pyclearpass` after completion

## Inputs

| Name | Type | Default |
|------|------|---------|
| DeviceID | Dynamic | |
| Clearpass Server | Static | `1.1.1.1` |
| Clearpass Api Token | Static | |
| Clearpass Radius Secret | Static | `abc` |
| Clearpass Group Name | Dynamic | `Arista_Access_Switches` |

## Output

- Logs management IP, hostname, and FQDN retrieval
- Logs ClearPass registration and group mapping steps
- Raises an exception if script execution fails on the switch