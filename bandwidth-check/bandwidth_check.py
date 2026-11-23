from typing import List, Dict
from cloudvision.cvlib import ActionFailed

THRESHOLD = 50

def get_bandwidth() -> Dict:
    cmds: List[str] = ["show interfaces counters rates"]
    resp = ctx.runDeviceCmds(cmds)
    if not resp or "response" not in resp[0]:
        raise ActionFailed("No valid bandwidth response from device")
    
    return resp[0].get("response", {}).get("interfaces", {}) or {}

ints = get_bandwidth()
fail = []

for name, d in ints.items():
    in_percent = d.get("inPktsRate", 0)
    out_percent = d.get("outPktsRate", 0)
    util = max(in_percent, out_percent)
    
    result = "PASS" if util <= THRESHOLD else "FAIL"
    
    if result == "FAIL":
        fail.append((name, util))

if fail:
    for iface, u in fail:
        ctx.alog(f" - {iface}: {u:.1f}% utilization which exceeds threshold")
    raise ActionFailed(f"{len(fail)} interfaces exceeded {THRESHOLD}% utilization")
else:
    ctx.alog("All interfaces within utilization limit.")
