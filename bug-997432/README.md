# BUG 997432

CloudVision action script to check if a device is susceptible to BUG997432 based on model and VRM firmware version.

## What It Does

- Retrieves device model and serial number via `show inventory`
- Checks if the model is in the affected list (DCS-7280SR3 variants)
- For affected models, reads VRM firmware version from `show version detail`
- Reports whether the device is susceptible (firmware version < 6) or not

## Affected Models

| Model | Firmware Component |
|-------|-------------------|
| DCS-7280SR3-48YC8 | vrm2 |
| DCS-7280SR3K-48YC8 | vrm2 |
| 7280SR3K-48YC8A | vrm2 |
| DCS-7280SR3M-48YC8 | vrm4 |
| DCS-7280SR3MK-48YC8A-S | vrm4 |

## Inputs

| Name | Type | Default |
|------|------|---------|
| DeviceID | Dynamic | |

## Output

- **Not affected** — device model is not in the susceptible list
- **SUSCEPTIBLE** — firmware version is below 6
- **NOT susceptible** — firmware version is 6 or above