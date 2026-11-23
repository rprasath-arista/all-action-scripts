# Post-Upgrade Unshut

CloudVision action script to unshut selected interfaces on a device after an upgrade, then wait for network stabilization.

## What It Does

- Takes a comma-separated list of interfaces as input
- Runs `no shutdown` on each specified interface via eAPI
- Waits 10 seconds for network stabilization
- Includes scaffolding for route count comparison (pre/post unshut) for future use

## Inputs

| Name | Type | Default |
|------|------|---------|
| DeviceID | Dynamic | |
| interfaces | Dynamic | |

## Output

- Logs each interface being enabled
- Confirms completion after stabilization wait
- Raises `ActionFailed` if the interface list is empty or script execution fails