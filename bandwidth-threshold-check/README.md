# Bandwidth Threshold Check

CloudVision action script that checks interface bandwidth utilization against a configurable threshold and flags any interfaces exceeding it.

## What It Does

- Queries all interface counters and rates via `show interfaces counters rates`
- Calculates utilization as the higher of inbound/outbound rate relative to interface bandwidth
- Logs each interface with PASS/FAIL status
- Raises `ActionFailed` if any interface exceeds the threshold (default: 1%)

## Input

| Name | Type | Description |
|------|------|-------------|
| DeviceID | Dynamic | Target device ID, automatically populated at runtime |

## Output

- Per-interface utilization percentage with PASS/FAIL
- Summary of failing interfaces if any exceed the threshold
- Action fails if any interface is above the threshold