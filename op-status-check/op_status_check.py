from cloudvision.cvlib import ActionFailed

def count_disconnected_interfaces():
    resp = ctx.runDeviceCmds(["show interfaces status"])
    interface_statuses = resp[0]["response"]["interfaceStatuses"]
    disconnected = 0
    total_count = 0
    for data in interface_statuses.values():
        if data.get("linkStatus") != "connected":
            disconnected += 1
        total_count += 1
    return disconnected, total_count

def main():
    try:
        ctx.alog("Device Action started")

        # To add checking for tags. Issue : Can't read them. 
        # Location : analytics/tagsV2/interfaces/device/system/desc/
        # Ideas : try to find a way / manual result for tag query is input to the action

        ''' ctx.alog(f"Tag evaluation result received: {tag_matched}")

        if tag_matched is not True:
            ctx.alog("❌ Device does not match required tag (desc=bob). Aborting.")
            return
        '''
        
        disconnected_count, total_count = count_disconnected_interfaces()

        if disconnected_count == 0:
            ctx.alog("✅ Ready to go. Proceed with upgrade ✅")
        else:
            ctx.alog(
                f"⚠️ Warning: {disconnected_count} out of {total_count} interfaces are not connected. Do not upgrade ⚠️"
            )

    except ActionFailed as e:
        ctx.alog(f"ActionFailed: {e}")
    except Exception as e:
        ctx.alog(f"Unhandled exception: {e}")

if __name__ == "__main__":
    main()
