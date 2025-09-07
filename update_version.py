#!/usr/bin/env python3
import re, datetime, os, sys, json

VERSION_FILE = "scripting/include/version.inc"

def show_help():
    print("🚀 AMXX Version Management Tool - SemVer")
    print("Usage: python update_version.py [COMMAND] [OPTIONS]")
    print("\nCommands:")
    print("  info                     Show current version information")
    print("  major                    Increment major version (X.0.0)")
    print("  minor                    Increment minor version (0.Y.0)")  
    print("  patch                    Increment patch version (0.0.Z)")
    print("  build                    Increment build number")
    print("  snapshot                 Set SNAPSHOT suffix")
    print("  release                  Remove suffix for final release")
    print("  alpha [N]                Set alpha.N suffix")
    print("  beta [N]                 Set beta.N suffix")
    print("  rc [N]                   Set rc.N suffix")
    print("  hotfix [N]               Set hotfix.N suffix")
    print("  get-version              Get base version (X.Y.Z)")
    print("  get-suffix               Get version suffix")
    print("  get-full-version         Get full version with suffix")

def get_current_version_info():
    if not os.path.exists(VERSION_FILE):
        return {
            'version': "1.0.0",
            'suffix': "",
            'build': "1",
            'name': "MirGame Multi-Mod",
            'author': "MirGame",
            'date': datetime.datetime.now().strftime("%Y-%m-%d")
        }
    
    try:
        with open(VERSION_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        version = re.search(r'#define PROJECT_VERSION "([^"]+)"', content)
        suffix = re.search(r'#define PROJECT_VERSION_SUFFIX "([^"]*)"', content)
        build = re.search(r'#define PROJECT_BUILD "(\d+)"', content)
        name = re.search(r'#define PROJECT_NAME "([^"]+)"', content)
        author = re.search(r'#define PROJECT_AUTHOR "([^"]+)"', content)
        date = re.search(r'#define PROJECT_BUILD_DATE "([^"]+)"', content)
        
        return {
            'version': version.group(1) if version else "1.0.0",
            'suffix': suffix.group(1) if suffix else "",
            'build': build.group(1) if build else "1",
            'name': name.group(1) if name else "MirGame Multi-Mod",
            'author': author.group(1) if author else "MirGame",
            'date': date.group(1) if date else datetime.datetime.now().strftime("%Y-%m-%d")
        }
    except Exception as e:
        print(f"❌ Error reading version file: {e}")
        return None

def update_version_file(content):
    try:
        with open(VERSION_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"❌ Error writing version file: {e}")
        return False

def increment_version(version_type):
    info = get_current_version_info()
    if not info:
        return False
    
    major, minor, patch = map(int, info['version'].split('.'))
    
    if version_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif version_type == "minor":
        minor += 1
        patch = 0
    elif version_type == "patch":
        patch += 1
    else:
        return False
    
    new_version = f"{major}.{minor}.{patch}"
    
    content = f"""#if defined _version_included
    #endinput
#endif
#define _version_included

#define PROJECT_NAME "{info['name']}"
#define PROJECT_AUTHOR "{info['author']}"
#define PROJECT_VERSION "{new_version}"
#define PROJECT_VERSION_SUFFIX "{info['suffix']}"
#define PROJECT_BUILD "{info['build']}"
#define PROJECT_BUILD_DATE "{datetime.datetime.now().strftime('%Y-%m-%d')}"

#define PRINT_PROJECT_INFO() \\
    server_print("[%s] Project v%s (build %s, %s)", \\
    PROJECT_NAME, PROJECT_VERSION PROJECT_VERSION_SUFFIX, PROJECT_BUILD, PROJECT_BUILD_DATE)

#define PROJECT_FULL_VERSION PROJECT_VERSION PROJECT_VERSION_SUFFIX
"""
    
    return update_version_file(content)

def update_build_number():
    info = get_current_version_info()
    if not info:
        return False
    
    try:
        new_build = str(int(info['build']) + 1)
    except:
        new_build = "1"
    
    content = f"""#if defined _version_included
    #endinput
#endif
#define _version_included

#define PROJECT_NAME "{info['name']}"
#define PROJECT_AUTHOR "{info['author']}"
#define PROJECT_VERSION "{info['version']}"
#define PROJECT_VERSION_SUFFIX "{info['suffix']}"
#define PROJECT_BUILD "{new_build}"
#define PROJECT_BUILD_DATE "{datetime.datetime.now().strftime('%Y-%m-%d')}"

#define PRINT_PROJECT_INFO() \\
    server_print("[%s] Project v%s (build %s, %s)", \\
    PROJECT_NAME, PROJECT_VERSION PROJECT_VERSION_SUFFIX, PROJECT_BUILD, PROJECT_BUILD_DATE)

#define PROJECT_FULL_VERSION PROJECT_VERSION PROJECT_VERSION_SUFFIX
"""
    
    if update_version_file(content):
        print(f"✅ Build number updated: {info['build']} → {new_build}")
        return new_build
    return False

def update_version_suffix(suffix_type, number=""):
    info = get_current_version_info()
    if not info:
        return False
    
    if suffix_type == "release":
        new_suffix = ""
    elif suffix_type == "snapshot":
        new_suffix = "-SNAPSHOT"
    elif suffix_type in ["alpha", "beta", "rc", "hotfix"]:
        new_suffix = f"-{suffix_type}.{number}" if number else f"-{suffix_type}.1"
    elif suffix_type == "keep":
        new_suffix = info['suffix']
    else:
        new_suffix = info['suffix']
    
    content = f"""#if defined _version_included
    #endinput
#endif
#define _version_included

#define PROJECT_NAME "{info['name']}"
#define PROJECT_AUTHOR "{info['author']}"
#define PROJECT_VERSION "{info['version']}"
#define PROJECT_VERSION_SUFFIX "{new_suffix}"
#define PROJECT_BUILD "{info['build']}"
#define PROJECT_BUILD_DATE "{datetime.datetime.now().strftime('%Y-%m-%d')}"

#define PRINT_PROJECT_INFO() \\
    server_print("[%s] Project v%s (build %s, %s)", \\
    PROJECT_NAME, PROJECT_VERSION PROJECT_VERSION_SUFFIX, PROJECT_BUILD, PROJECT_BUILD_DATE)

#define PROJECT_FULL_VERSION PROJECT_VERSION PROJECT_VERSION_SUFFIX
"""
    
    if update_version_file(content):
        action = "removed" if not new_suffix else f"set to {new_suffix}"
        print(f"✅ Version suffix {action}")
        return new_suffix
    return False

# Добавить в существующий код:

def set_commit_info(commit_hash, author):
    """Обновляет информацию о коммите в version.inc"""
    info = get_current_version_info()
    if not info:
        return False
    
    short_hash = commit_hash[:7] if commit_hash else ""
    
    content = f"""#if defined _version_included
    #endinput
#endif
#define _version_included

#define PROJECT_NAME "{info['name']}"
#define PROJECT_AUTHOR "{info['author']}"
#define PROJECT_VERSION "{info['version']}"
#define PROJECT_VERSION_SUFFIX "{info['suffix']}"
#define PROJECT_BUILD "{info['build']}"
#define PROJECT_BUILD_DATE "{datetime.datetime.now().strftime('%Y-%m-%d')}"

#define PROJECT_COMMIT_HASH "{commit_hash}"
#define PROJECT_COMMIT_SHORT_HASH "{short_hash}"
#define PROJECT_COMMIT_AUTHOR "{author}"
#define PROJECT_COMMIT_DATE "{datetime.datetime.now().strftime('%Y-%m-%d')}"

#define PRINT_PROJECT_INFO() \\
    server_print("[%s] Project v%s%s (build %s, %s)", \\
    PROJECT_NAME, PROJECT_VERSION, PROJECT_VERSION_SUFFIX, PROJECT_BUILD, PROJECT_BUILD_DATE)

#define PRINT_PROJECT_INFO_DETAILED() \\
    server_print("[%s] Project Information:", PROJECT_NAME); \\
    server_print("  Version: v%s%s", PROJECT_VERSION, PROJECT_VERSION_SUFFIX); \\
    server_print("  Build: %s (%s)", PROJECT_BUILD, PROJECT_BUILD_DATE); \\
    server_print("  Author: %s", PROJECT_AUTHOR); \\
    if(strlen(PROJECT_COMMIT_SHORT_HASH) > 0) {{ \\
        server_print("  Commit: %s", PROJECT_COMMIT_SHORT_HASH); \\
    }}
"""
    
    return update_version_file(content)

def get_build():
    """Получить номер сборки"""
    info = get_current_version_info()
    return info['build'] if info else "1"



def handle_command(args):
    if not args or args[0] in ['-h', '--help']:
        show_help()
        return True
    
    command = args[0].lower()
    
    if command in ['info', '-i']:
        info = get_current_version_info()
        if info:
            full_version = f"{info['version']}{info['suffix']}"
            print("📋 Version Information:")
            print(f"   Project: {info['name']}")
            print(f"   Author: {info['author']}")
            print(f"   Version: {full_version}")
            print(f"   Build: {info['build']}")
            print(f"   Date: {info['date']}")
        return True
        
    elif command in ['major', '--major']:
        return increment_version("major")
        
    elif command in ['minor', '--minor']:
        return increment_version("minor")
        
    elif command in ['patch', '--patch']:
        return increment_version("patch")
        
    elif command in ['build', '-b']:
        return update_build_number() is not None
        
    elif command in ['snapshot', '-s']:
        return update_version_suffix("snapshot")
        
    elif command in ['release', '-r']:
        return update_version_suffix("release")
        
    elif command in ['alpha', '-a']:
        number = args[1] if len(args) > 1 else "1"
        return update_version_suffix("alpha", number)
        
    elif command in ['beta', '-be']:
        number = args[1] if len(args) > 1 else "1"
        return update_version_suffix("beta", number)
        
    elif command in ['rc', '-rc']:
        number = args[1] if len(args) > 1 else "1"
        return update_version_suffix("rc", number)
        
    elif command in ['hotfix', '-hf']:
        number = args[1] if len(args) > 1 else "1"
        return update_version_suffix("hotfix", number)
        
    elif command in ['get-version']:
        info = get_current_version_info()
        print(info['version'] if info else "1.0.0")
        return True
        
    elif command in ['get-suffix']:
        info = get_current_version_info()
        print(info['suffix'] if info else "")
        return True
        
    elif command in ['get-full-version']:
        info = get_current_version_info()
        full_version = f"{info['version']}{info['suffix']}" if info else "1.0.0"
        print(full_version)
        return True
    elif command in ['set-commit', '--set-commit']:
        commit_hash = args[1] if len(args) > 1 else ""
        author = args[2] if len(args) > 2 else ""
        return set_commit_info(commit_hash, author)
    elif command in ['get-build', '--get-build']:
        print(get_build())
        return True
    else:
        print(f"❌ Unknown command: {command}")
        show_help()
        return False

if __name__ == "__main__":
    try:
        success = handle_command(sys.argv[1:])
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        sys.exit(1)