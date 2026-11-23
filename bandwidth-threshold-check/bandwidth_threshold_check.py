# Run this Action only with sufficient device privileges (enable access)

from typing import List, Dict
from cloudvision.cvlib import ActionFailed

# Bandwidth percentage threshold
THRESHOLD = 1 

# Get Bandwidth 
def get_bandwidth() -> Dict:
    cmds: List[str] = ["show interfaces counters rates"]
    resp = ctx.runDeviceCmds(cmds)
    if not resp or "response" not in resp[0]:
        raise ActionFailed("No valid bandwidth response from device")
    return resp[0]["response"].get("interfaces", {})

ctx.alog(f"Checking bandwidth utilization with {THRESHOLD}% threshold")

# Run Get Bandwidth
ints = get_bandwidth()

fail = []

# Parse Output Dictionary
for name, d in ints.items():
    bw = d.get("bandwidth", 0)
    rx = d.get("inBpsRate", 0)
    tx = d.get("outBpsRate", 0)
    if not bw:
        continue
    util = max(rx, tx) * 100 / bw
    result = "PASS" if util <= THRESHOLD else "FAIL"
    ctx.alog(f"{name}: {util:.1f}% -> {result}")
    if result == "FAIL":
        fail.append((name, util))

# Output
if fail:
    ctx.alog(f"Interfaces above {THRESHOLD}% utilization:")
    for i, u in fail:
        ctx.alog(f" - {i}: {u:.1f}%")
    raise ActionFailed(f"Bandwidth utilization check failed")
else:
    ctx.alog("All interfaces within utilization limit.")