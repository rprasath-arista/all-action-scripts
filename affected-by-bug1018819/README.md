# Affected by BUG1018819

CloudVision action script to identify devices affected by BUG1018819 by checking for Smart eMMC storage models (08GP1A/16GP1A).

## What It Does

- Runs `show inventory` to inspect storage devices on the target switch
- Checks if any storage device model contains **08GP1A** or **16GP1A** (Smart eMMC)
- Retrieves the device hostname via `show hostname` for reporting
- Logs whether the device is affected by BUG1018819

## Input

| Name | Type | Description |
|------|------|-------------|
| DeviceID | Dynamic | Target device ID, automatically populated at runtime |

## Output

- **No Smart eMMC detected** — device is not affected by BUG1018819
- **Smart eMMC detected** — device is affected by BUG1018819
