#include <amxmodx>
#include <version>

#define PLUGIN_NAME "Example Plugin"
#define PLUGIN_VERSION "1.0.0"

public plugin_init()
{
    register_plugin(PLUGIN_NAME, PLUGIN_VERSION, PROJECT_AUTHOR);
    
    // Show project info in server console
    PRINT_PROJECT_INFO();
    server_print("Plugin: %s v%s", PLUGIN_NAME, PLUGIN_VERSION);
    
    // Register example command
    register_clcmd("say /example", "cmd_example");
}

public cmd_example(id)
{
    client_print(id, print_chat, "🎉 %s v%s is working!", PLUGIN_NAME, PLUGIN_VERSION);
    return PLUGIN_HANDLED;
}
