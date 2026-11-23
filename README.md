# All Action Scripts

Collection of CloudVision action scripts for network automation tasks on Arista devices.

## Scripts

| Script | Description |
|--------|-------------|
| [add-device-to-clearpass](add-device-to-clearpass/) | Register an Arista switch as a NAD in Aruba ClearPass |
| [affected-by-bug1018819](affected-by-bug1018819/) | Identify devices affected by BUG1018819 (Smart eMMC) |
| [bandwidth-check](bandwidth-check/) | Monitor interface packet rates against a 50% threshold |
| [bandwidth-threshold-check](bandwidth-threshold-check/) | Check interface bandwidth utilization against a 1% threshold |
| [bug-997432](bug-997432/) | Check device susceptibility to BUG997432 (VRM firmware) |
| [clear-host-flap](clear-host-flap/) | Clear BGP EVPN host-flap counters |
| [field-notice-0142](field-notice-0142/) | Identify and remediate FN0142 (1042-day uptime issue) |
| [find-emmc-devices](find-emmc-devices/) | Find devices with Smart eMMC storage |
| [fiserv-type-high](fiserv-type-high/) | Copy BCM shell script for Gen3-258990 workaround (high) |
| [fiserv-type-low](fiserv-type-low/) | Copy BCM shell script for Gen3-258990 workaround (low) |
| [mismatch-neighbor](mismatch-neighbor/) | Compare LLDP neighbors against a baseline |
| [op-status-check](op-status-check/) | Pre-upgrade readiness check (interface status) |
| [post-upgrade-unshut](post-upgrade-unshut/) | Unshut interfaces after an upgrade |
| [pre-upgrade-shut](pre-upgrade-shut/) | Shut interfaces before an upgrade |
| [winrm-dns-update](winrm-dns-update/) | Register switch DNS A record in AD via WinRM |