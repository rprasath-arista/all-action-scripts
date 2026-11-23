# Field Notice 0142

CloudVision action scripts for identifying and remediating devices affected by Field Notice 0142 (1042-day uptime issue).

## Tasks

### Task 1: Identify Affected Devices
**Script:** `task1-identify-affected-devices.py`

Identifies affected devices based on model and uptime. Checks if the device model matches any affected CCS-720 or DCS-7000 series SKUs and calculates how many days remain before the 1042-day uptime threshold is reached.

**Input:**
| Name | Type | Description |
|------|------|-------------|
| DeviceID | Dynamic | Automatically populated with the target device ID at runtime |

**Output:**
- Devices not in the affected model list are logged as info
- Devices approaching 1042 days show remaining days
- Devices at exactly 1042 days trigger a warning
- Devices past 1042 days trigger an error

### Task 2: Save Config and Copy Patch
*Coming soon*

Save running config and copy the remediation patch file to flash.

### Task 3: Install Patch and Finish Checks
*Coming soon*

Install the patch and run post-installation verification checks.