# Fiserv - Type High

CloudVision action script to copy a predefined BCM shell script (cint) file to a device flash storage for the Gen3-258990 workaround.

## What It Does

- Takes a filename/path as input
- Copies a predefined BCM shell script to the specified path on the device using `copy terminal:`
- The script modifies `IHP_UNKNOWN_DA_MAP` entries across all valid BCM units

## Inputs

| Name | Type | Default |
|------|------|---------|
| DeviceID | Dynamic | |
| filename | Static | `/mnt/flash/gen3-258990.cint` |

## Output

- Logs confirmation that content was copied to the destination
- Raises `ActionFailed` if the filename is missing or the copy command fails