# Copyright (c) 2024 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0

import time

TARGET_DAYS = 1042
DAY_SEC = 86400

# Set of affected model SKUs and Series prefixes
AFFECTED_MODELS = {
    # CCS-720 Series
    "CCS-720DF-48Y", "CCS-720DF-48Y-2", "CCS-720DF-48Y-DC", "CCS-720DF-48Y-DC-2", "CCS-720DF-48Y-HVDC-2", "CCS-720DF-48Y-M-S-2",
    "CCS-720DP-24", "CCS-720DP-24S-2", "CCS-720DP-24S", "CCS-720DP-24S-M-S-2", "CCS-720DP-24ZS", "CCS-720DP-ZS-2",
    "CCS-720DP-48", "CCS-720DP-48S-2", "CCS-720DP-48S", "CCS-720DP-48S-M-S-2", "CCS-720DP-48ZS-2", "CCS-720DP-48ZS",
    "CCS-720DT-24S", "CCS-720DT-24S-2", "CCS-720DT-24S-M-S-2",
    "CCS-720DT-48S", "CCS-720DT-48S-2", "CCS-720DT-48S-HV-2", "CCS-720DT-48S-MGX-2",
    "CCS-720XDM-48T", "CCS-720XDM-48T-6SY",
    "CCS-720XP-48TXH", "CCS-720XP-48TXH-2C-S",
    "CCS-720XPM-48TH", "CCS-720XPM-48TH-6S",
    # DCS Series
    "DCS-7010TX-48C", "DCS-7010TX-48C-DC", "DCS-7010TX-48C-DC-RV3",
    "DCS-7020R4-24Y", "DCS-7020R4-24Y-4QC", "DCS-7020R4-24Y-6QDF",
    "DCS-7020R4-48Y", "DCS-7020R4-48Y-4QC", "DCS-7020R4-48Y-8QC",
    "DCS-7020R4M-24Y", "DCS-7020R4M-24Y-4QC", "DCS-7020R4M-24Y-6QDF",
    "DCS-7020R4M-48Y", "DCS-7020R4M-48Y-4QC", "DCS-7020R4M-48Y-8QC",
    "DCS-7020R4-48TX", "DCS-7020R4-48TX-4QC",
    "DCS-7050CX3", "DCS-7050CX3-32C",
    "DCS-7050CX4", "DCS-7050CX4-24D8",
    "DCS-7050CX4M", "DCS-7050CX4M-48D8",
    "DCS-7050SDX4", "DCS-7050SDX4-48D8",
    "DCS-7050SPX4", "DCS-7050SPX4-48D8",
    "DCS-7050SX3", "DCS-7050SX3-24YC4C-S", "DCS-7050SX3-48C8C",
    "DCS-7050X4", "DCS-7050X4-48Y-4DF",
    "DCS-7060CX5", "DCS-7060CX5-56D8"
}

# 1. Gather device version and uptime via eAPI
cmds = ["enable", "show version", "show uptime"]
cmd_out = ctx.runDeviceCmds(cmds)

show_version = cmd_out[1]["response"]
show_uptime = cmd_out[2]["response"]

model_name = show_version.get("modelName", "")
uptime_sec = show_uptime.get("upTime", 0)

# 2. Check if model is affected
is_affected = any(
    model_name == affected or model_name.startswith(affected) or affected.startswith(model_name)
    for affected in AFFECTED_MODELS
)

if not is_affected:
    ctx.info("Device model not affected")
else:
    # 3. Calculate uptime and output log for affected devices
    up_days = uptime_sec / DAY_SEC
    days_left = TARGET_DAYS - up_days
    boot_ts = time.time() - uptime_sec
    cross_date = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime(boot_ts + (TARGET_DAYS * DAY_SEC)))

    if up_days == TARGET_DAYS:
        msg, log = "Device at 1042 days", ctx.warning
    elif up_days > TARGET_DAYS:
        msg, log = "Device crossed 1042 days", ctx.error
    else:
        msg, log = f"Days till 1042 days is {days_left:.1f}", ctx.info

    log(f"{msg} | Uptime: {up_days:.1f}d | Target: {cross_date}")