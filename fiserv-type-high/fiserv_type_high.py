from cloudvision.cvlib import ActionFailed

# Retrieve filename from CVP
filename = ctx.action.args.get("filename")
if not filename:
    raise ActionFailed("Filename must be provided.")

def copy_file(destination: str, content: str):
    if not destination or not content:
        raise ActionFailed("Filename and content must be provided.")
    
    ctx.debug(f"Copying content to {destination}")
    
    # Prepare the command to copy content
    cmds = [
        "enable",
        {"cmd": f"copy terminal: file:{destination}", "input": content},
    ]
    
    # Run the copy command on the device
    response = ctx.runDeviceCmds(cmds)
    errors = [resp.get('error') for resp in response if resp.get('error')]
    if errors:
        raise ActionFailed(f"Copy failed: {errors[0]}")
    
    ctx.info(f"Content copied to {destination}")
    
# Predefined content to copy
content = """
{
   int i = 0;
   for( i = 0; i < 10; i ++ ) {
      if ( bcm_unit_valid( i ) ) {
         bshell( i, "mod IHP_UNKNOWN_DA_MAP 18 1 DESTINATION=0x3f6" );
      }
   }
}
"""

# Call the copy_file function
copy_file(filename, content)
