# Bandwidth Check

CloudVision action script that monitors interface packet rates and flags any interfaces exceeding a 50% utilization threshold.

## What It Does

- Queries interface counter rates via `show interfaces counters rates`
- Evaluates the higher of inbound/outbound packet rate per interface
- Fails the action if any interface exceeds the 50% threshold, listing all offenders
- Passes silently when all interfaces are within limits

## Input

| Name | Type | Description |
|------|------|-------------|
| DeviceID | Dynamic | Target device ID, automatically populated at runtime |

## Output

- Lists each interface exceeding the threshold with its utilization percentage
- Raises `ActionFailed` with a count of failing interfaces if any exceed 50%
- Logs success message if all interfaces pass
