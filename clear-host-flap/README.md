# Clear Host Flap

CloudVision action script to clear BGP EVPN host-flap counters on a device.

## What It Does

- Runs `clear bgp evpn host-flaps` on the target device
- Resets host-flap detection counters, useful after resolving a flapping host or during maintenance windows

## Input

| Name | Type | Description |
|------|------|-------------|
| DeviceID | Dynamic | Target device ID, automatically populated at runtime |

## Output

- Logs success or failure of the clear command
- Raises an exception if the command fails
