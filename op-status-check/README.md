# Op Status Check

CloudVision action script that performs pre-upgrade readiness checks on a device before proceeding with an upgrade.

## What It Does

1. Checks if the `desc` tag is present on the device (scaffolded for future implementation)
2. Queries `show interfaces status` and counts how many interfaces are not in a "connected" state
3. If all interfaces are connected, signals the device is ready for upgrade
4. If any interfaces are disconnected, throws a warning and blocks the upgrade

## Input

| Name | Type | Description |
|------|------|-------------|
| DeviceID | Dynamic | Target device ID, automatically populated at runtime |

## Output

- **Ready to go** — all interfaces are connected, safe to proceed with upgrade
- **Warning** — reports the count of disconnected interfaces and advises not to upgrade
