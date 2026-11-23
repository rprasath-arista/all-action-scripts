# WinRM DNS Update

CloudVision action script that automatically registers an Arista switch hostname and management IP as a DNS A record in Active Directory via WinRM and PowerShell.

## What It Does

1. Retrieves the device management IP and hostname from the switch
2. Copies a helper Python script to the switch flash storage
3. The helper installs the `winrm` package, opens an NTLM-authenticated session to the AD server, and runs `Add-DnsServerResourceRecordA` via PowerShell to create the DNS entry
4. Cleans up by uninstalling the `winrm` package after completion

## Inputs

| Name | Type | Default |
|------|------|---------|
| DeviceID | Dynamic | |
| AD Server | Static | `1.1.1.1` |
| Username | Static | `abc` |
| Password | Static | `abc` |
| DNS Zone | Static | `1` |

## Output

- Logs management IP and hostname retrieval
- Logs success or failure of the DNS record creation
- Raises an exception if script execution fails on the switch