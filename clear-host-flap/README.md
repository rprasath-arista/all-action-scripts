# Clear Host Flap

CloudVision action script to clear BGP EVPN host-flap counters on a device.

## What It Does

- Runs `clear bgp evpn host-flaps` on the target device
- Resets host-flap detection counters, useful after resolving a flapping host or during maintenance windows

## Inputs

| Name | Type | Default |
|------|------|---------|
| DeviceID | Dynamic | |

## Output

- Logs success or failure of the clear command
- Raises an exception if the command fails