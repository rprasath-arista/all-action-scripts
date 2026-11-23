# Mismatch Neighbor

CloudVision change control action that compares a device current LLDP neighbors against an expected baseline and reports any discrepancies.

## What It Does

- Queries the device live LLDP neighbor table via the CloudVision resource API
- Compares each interface neighbor against the provided baseline JSON
- Reports **missing** neighbors (expected but not found or changed) and **unexpected** neighbors (present but not in the baseline)
- In non-dry-run mode, annotates the device in CloudVision when mismatches are found

## Inputs

| Name | Type | Default |
|------|------|---------|
| DeviceID | Static | `710-1-JT` |
| baseline | Static | `{ "Ethernet1": "leaf01", "Ethernet2": "leaf02" }` |
| dryRun | Static | `true` |

## Output

- **All neighbors match** — info log, no action taken
- **Mismatches found** — warning with details of missing and unexpected neighbors; device annotated if dryRun is false