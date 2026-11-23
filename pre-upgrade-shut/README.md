# Pre-Upgrade Shut

CloudVision action script to shut down selected interfaces on a device before an upgrade.

## What It Does

- Takes a comma-separated list of interfaces as input
- Runs `shutdown` on each specified interface via eAPI
- Waits 10 seconds for network stabilization
- Signals readiness to proceed with the upgrade

## Inputs

| Name | Type | Default |
|------|------|---------|
| DeviceID | Dynamic | |
| interfaces | Dynamic | |

## Output

- Logs each interface being shut down
- Confirms readiness to proceed with upgrade
- Raises `ActionFailed` if the interface list is empty or script execution fails