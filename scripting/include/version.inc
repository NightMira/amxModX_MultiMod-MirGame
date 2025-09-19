#if defined _version_included
    #endinput
#endif
#define _version_included

/* ========================================================================== */
/*                          PROJECT VERSION INFORMATION                       */
/* ========================================================================== */

// Project Identification
#define PROJECT_NAME                "MirGame Multi-Mod"
#define PROJECT_AUTHOR              "MirGame"
#define PROJECT_DESCRIPTION         "Advanced AMXX Modification Framework"

// Semantic Versioning (SemVer)
#define PROJECT_VERSION_MAJOR "0"
#define PROJECT_VERSION_MAJOR_NUM 0
#define PROJECT_VERSION_MINOR "0"
#define PROJECT_VERSION_MINOR_NUM 0
#define PROJECT_VERSION_PATCH "5"
#define PROJECT_VERSION_PATCH_NUM 5
#define PROJECT_VERSION "0.0.5"
#define PROJECT_VERSION_NUM 005

// Version Suffix (Pre-release tags)
#define PROJECT_VERSION_TAG "RC.1"
#define PROJECT_VERSION_SUFFIX "-rc.1"

// Build Information
#define PROJECT_BUILD "122"
#define PROJECT_BUILD_NUM 122
#define PROJECT_BUILD_DATE "2025-09-19"
#define PROJECT_BUILD_TIME          __TIME__
#define PROJECT_BUILD_TIMESTAMP     __DATE__ " " __TIME__

// Git Commit Information
#define PROJECT_COMMIT_HASH         ""
#define PROJECT_COMMIT_SHORT_HASH   ""
#define PROJECT_COMMIT_AUTHOR       ""
#define PROJECT_COMMIT_DATE         ""

/* ========================================================================== */
/*                            COMPATIBILITY MACROS                            */
/* ========================================================================== */

// Full version string for display
#define PROJECT_FULL_VERSION        PROJECT_VERSION PROJECT_VERSION_SUFFIX

// Numeric version for comparisons
#define PROJECT_VERSION_ID          (PROJECT_VERSION_MAJOR_NUM * 10000 + \
                                     PROJECT_VERSION_MINOR_NUM * 100 + \
                                     PROJECT_VERSION_PATCH_NUM)

// Backward compatibility with original version system
#define PROJECT_VERSION_LEGACY      PROJECT_VERSION

/* ========================================================================== */
/*                              UTILITY MACROS                                */
/* ========================================================================== */

// Print project information to server console
#define PRINT_PROJECT_INFO() \
    server_print("[%s] v%s%s (build %s, %s)", \
        PROJECT_NAME, \
        PROJECT_VERSION, \
        PROJECT_VERSION_SUFFIX, \
        PROJECT_BUILD, \
        PROJECT_BUILD_DATE)

// Print detailed project information  
#define PRINT_PROJECT_INFO_DETAILED() \
    server_print("[%s] Project Information:", PROJECT_NAME); \
    server_print("  Version: v%s%s", PROJECT_VERSION, PROJECT_VERSION_SUFFIX); \
    server_print("  Build: %s (%s)", PROJECT_BUILD, PROJECT_BUILD_DATE); \
    server_print("  Author: %s", PROJECT_AUTHOR); \
    if(strlen(PROJECT_COMMIT_SHORT_HASH) > 0) { \
        server_print("  Commit: %s", PROJECT_COMMIT_SHORT_HASH); \
    }

// Check version compatibility
#define IS_VERSION_COMPATIBLE(major, minor) \
    (PROJECT_VERSION_MAJOR_NUM == major && PROJECT_VERSION_MINOR_NUM >= minor)

// Version comparison macros
#define VERSION_EQUAL(major, minor, patch) \
    (PROJECT_VERSION_MAJOR_NUM == major && \
     PROJECT_VERSION_MINOR_NUM == minor && \
     PROJECT_VERSION_PATCH_NUM == patch)

#define VERSION_GREATER_THAN(major, minor, patch) \
    (PROJECT_VERSION_MAJOR_NUM > major || \
     (PROJECT_VERSION_MAJOR_NUM == major && PROJECT_VERSION_MINOR_NUM > minor) || \
     (PROJECT_VERSION_MAJOR_NUM == major && PROJECT_VERSION_MINOR_NUM == minor && PROJECT_VERSION_PATCH_NUM > patch))

#define VERSION_LESS_THAN(major, minor, patch) \
    (PROJECT_VERSION_MAJOR_NUM < major || \
     (PROJECT_VERSION_MAJOR_NUM == major && PROJECT_VERSION_MINOR_NUM < minor) || \
     (PROJECT_VERSION_MAJOR_NUM == major && PROJECT_VERSION_MINOR_NUM == minor && PROJECT_VERSION_PATCH_NUM < patch))

/* ========================================================================== */
/*                            DEPRECATION WARNINGS                            */
/* ========================================================================== */

// Mark deprecated features
#define DEPRECATED___(message) \
    #pragma warning _%_DEPRECATED: message _%_

// Usage: DEPRECATED___("Use new_function() instead")

/* ========================================================================== */
/*                               API VERSIONING                               */
/* ========================================================================== */

// API Version (increment when breaking changes occur)
#define API_VERSION_MAJOR           "1"
#define API_VERSION_MINOR           "0"
#define API_VERSION                 "1.0"

// API Compatibility
#define IS_API_COMPATIBLE(version) \
    (strcmp(API_VERSION, version) >= 0)