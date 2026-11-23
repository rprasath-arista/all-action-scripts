# Add Device to Clearpass

CloudVision action script to automatically register an Arista switch as a Network Access Device (NAD) in Aruba ClearPass and map it to a device group.

## What It Does

1. Retrieves the device's management IP, hostname, and FQDN from the switch
2. Copies a Python helper script to the switch's flash storage
3. The helper script installs `pyclearpass`, registers the switch as a NAD in ClearPass with RADIUS and CoA settings, and maps it to the specified device group
4. Cleans up by uninstalling `pyclearpass` after completion

## Inputs

| Name | Type | Default | Description |
|------|------|---------|-------------|
| DeviceID | Dynamic | — | Target device ID, automatically populated at runtime |
| Clearpass Server | Static | `1.1.1.1` | ClearPass server IP or hostname |
| Clearpass Api Token | Static | — | API token for ClearPass authentication |
| Clearpass Radius Secret | Static | `abc` | RADIUS shared secret for the device |
| Clearpass Group Name | Dynamic | `Arista_Access_Switches` | ClearPass network device group to add the switch to |

## Output

- Logs management IP, hostname, and FQDN retrieval
- Logs ClearPass registration and group mapping steps
- Raises an exception if script execution fails on the switch
