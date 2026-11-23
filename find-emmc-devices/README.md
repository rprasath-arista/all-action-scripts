# Find eMMC Devices

CloudVision action script to identify devices with Smart eMMC storage that can be affected by BUG1018819.

## What It Does

- Runs `show inventory` to inspect storage devices on the target switch
- Checks for Smart eMMC models containing **08GP1A** or **16GP1A**
- Logs whether the device has affected eMMC storage or not

## Input

| Name | Type | Description |
|------|------|-------------|
| DeviceID | Dynamic | Target device ID, automatically populated at runtime |

## Output

- **No Smart eMMC detected** — device is not affected
- **Smart eMMC detected** — device may be susceptible to BUG1018819