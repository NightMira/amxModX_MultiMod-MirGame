#include <amxmodx>
#include <version>

#define PLUGIN_NAME "Test Build"
#define PLUGIN_VERSION "1.0.0"

public plugin_init() {
    register_plugin(PLUGIN_NAME, PLUGIN_VERSION, PROJECT_AUTHOR);
    PRINT_PROJECT_INFO();
    server_print("Plugin: %s v%s", PLUGIN_NAME, PLUGIN_VERSION);
}