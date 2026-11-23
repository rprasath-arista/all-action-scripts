# WinRM

CloudVision action script that automatically registers an Arista switch's hostname and management IP as a DNS A record in Active Directory via WinRM and PowerShell.

## What It Does

1. Retrieves the device's management IP and hostname from the switch
2. Copies a helper Python script to the switch's flash storage
3. The helper installs the `winrm` package, opens an NTLM-authenticated session to the AD server, and runs `Add-DnsServerResourceRecordA` via PowerShell to create the DNS entry
4. Cleans up by uninstalling the `winrm` package after completion

## Inputs

| Name | Type | Default | Description |
|------|------|---------|-------------|
| DeviceID | Dynamic | — | Target device ID, automatically populated at runtime |
| AD Server | Static | `1.1.1.1` | Active Directory server IP or FQDN |
| Username | Static | `abc` | AD account username for WinRM authentication |
| Password | Static | `abc` | AD account password for WinRM authentication |
| DNS Zone | Static | `1` | DNS zone in AD where the A record will be created |

## Output

- Logs management IP and hostname retrieval
- Logs success or failure of the DNS record creation
- Raises an exception if script execution fails on the switch
