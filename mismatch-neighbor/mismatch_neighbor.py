# Copyright (c) 2025 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the COPYING file.

# CVP Custom Action: Neighbor Mismatch Finder
# Action Type: Change Control

import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_current_neighbors(client, device_id):
    path = f"/Device/{device_id}/lldp/neighbors"
    neighbors = {}
    for notif in client.get(path):
        for update in notif.updates:
            intf = update.path_elements[-1]
            neighbors[intf] = update.values.get("systemName", "UNKNOWN")
    return neighbors

def run(ctx, inputs):
    """
    ctx: CVP execution context
    inputs: dict from CVP UI
    """
    device_id = inputs.get("deviceId")
    baseline = json.loads(inputs.get("baseline", "{}"))
    dry_run = str(inputs.get("dryRun", "true")).lower() == "true"

    if not device_id or not baseline:
        ctx.error("Missing deviceId or baseline in parameters")
        return

    client = ctx.getCvClient()
    current = get_current_neighbors(client, device_id)

    missing = {intf: nbr for intf, nbr in baseline.items()
               if intf not in current or current[intf] != nbr}
    unexpected = {intf: nbr for intf, nbr in current.items()
                  if intf not in baseline or baseline[intf] != nbr}

    if missing or unexpected:
        msg = f"Missing: {missing}, Unexpected: {unexpected}"
        ctx.warning(msg)
        if not dry_run:
            ctx.annotateDevice(device_id, "Neighbor mismatch detected", msg)
    else:
        ctx.info("All neighbors match baseline.")
