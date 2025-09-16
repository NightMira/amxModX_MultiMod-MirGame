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
        return None
    
    try:
        with open(VERSION_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Основные версионные определения
        version = re.search(r'#define PROJECT_VERSION\s+"([^"]+)"', content)
        suffix = re.search(r'#define PROJECT_VERSION_SUFFIX\s+"([^"]*)"', content)
        build = re.search(r'#define PROJECT_BUILD\s+"(\d+)"', content)
        build_date = re.search(r'#define PROJECT_BUILD_DATE\s+"([^"]+)"', content)
        
        # Детальные компоненты версии
        major = re.search(r'#define PROJECT_VERSION_MAJOR\s+"([^"]+)"', content)
        minor = re.search(r'#define PROJECT_VERSION_MINOR\s+"([^"]+)"', content)
        patch = re.search(r'#define PROJECT_VERSION_PATCH\s+"([^"]+)"', content)
        
        # Дополнительная информация
        name = re.search(r'#define PROJECT_NAME\s+"([^"]+)"', content)
        author = re.search(r'#define PROJECT_AUTHOR\s+"([^"]+)"', content)
        
        return {
            'version': version.group(1) if version else "0.1.0",
            'suffix': suffix.group(1) if suffix else "",
            'build': build.group(1) if build else "1",
            'build_date': build_date.group(1) if build_date else datetime.datetime.now().strftime("%Y-%m-%d"),
            'major': major.group(1) if major else "0",
            'minor': minor.group(1) if minor else "1", 
            'patch': patch.group(1) if patch else "0",
            'name': name.group(1) if name else "MirGame Multi-Mod",
            'author': author.group(1) if author else "MirGame"
        }
    except Exception as e:
        print(f"❌ Error reading version file: {e}")
        return None

def update_version_define(define_name, new_value):
    """Обновляет одно определение версии в файле"""
    try:
        with open(VERSION_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Шаблон для поиска define
        pattern = rf'^(#define {define_name}\s+")([^"]*)(")'
        replacement = rf'\g<1>{new_value}\g<3>'
        
        new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        if new_content == content:
            print(f"⚠️ Define {define_name} not found, but continuing")
            return False
        
        with open(VERSION_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    except Exception as e:
        print(f"❌ Error updating {define_name}: {e}")
        return False

def update_build_date():
    """Обновляет дату сборки"""
    return update_version_define('PROJECT_BUILD_DATE', datetime.datetime.now().strftime('%Y-%m-%d'))

def update_numeric_version(major, minor, patch):
    """Обновляет числовые представления версии"""
    success = True
    success &= update_version_define('PROJECT_VERSION_MAJOR', str(major))
    success &= update_version_define('PROJECT_VERSION_MAJOR_NUM', str(major))
    success &= update_version_define('PROJECT_VERSION_MINOR', str(minor))
    success &= update_version_define('PROJECT_VERSION_MINOR_NUM', str(minor))
    success &= update_version_define('PROJECT_VERSION_PATCH', str(patch))
    success &= update_version_define('PROJECT_VERSION_PATCH_NUM', str(patch))
    return success

def increment_version(version_type):
    info = get_current_version_info()
    if not info:
        return False
    
    try:
        major = int(info['major'])
        minor = int(info['minor'])
        patch = int(info['patch'])
    except:
        major, minor, patch = 0, 1, 0
    
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
    
    # Обновляем все связанные определения
    success1 = update_version_define('PROJECT_VERSION', new_version)
    success2 = update_numeric_version(major, minor, patch)
    success3 = update_build_date()
    
    # Обновляем PROJECT_VERSION_NUM (трехзначный числовой код)
    version_num = major * 10000 + minor * 100 + patch
    success4 = update_version_define('PROJECT_VERSION_NUM', str(version_num))
    
    return success1 and success2 and success3 and success4

def update_build_number():
    info = get_current_version_info()
    if not info:
        return False
    
    try:
        new_build = str(int(info['build']) + 1)
        new_build_num = str(int(info['build']) + 1)
    except:
        new_build = "1"
        new_build_num = "1"
    
    # Обновляем номер сборки и дату
    success1 = update_version_define('PROJECT_BUILD', new_build)
    success2 = update_version_define('PROJECT_BUILD_NUM', new_build_num)
    success3 = update_build_date()
    
    if success1 and success2 and success3:
        print(f"✅ Build number updated: {info['build']} → {new_build}")
        return new_build
    return False

def update_version_suffix(suffix_type, number=""):
    info = get_current_version_info()
    if not info:
        return False
    
    if suffix_type == "release":
        new_suffix = ""
        new_tag = ""
    elif suffix_type == "snapshot":
        new_suffix = "-SNAPSHOT"
        new_tag = "SNAPSHOT"
    elif suffix_type in ["alpha", "beta", "rc", "hotfix"]:
        new_suffix = f"-{suffix_type}.{number}" if number else f"-{suffix_type}.1"
        new_tag = f"{suffix_type.upper()}.{number}" if number else f"{suffix_type.upper()}.1"
    elif suffix_type == "keep":
        new_suffix = info['suffix']
        new_tag = info.get('tag', '')
    else:
        new_suffix = info['suffix']
        new_tag = info.get('tag', '')
    
    # Обновляем суффикс, тег и дату
    success1 = update_version_define('PROJECT_VERSION_SUFFIX', new_suffix)
    success2 = update_version_define('PROJECT_VERSION_TAG', new_tag)
    success3 = update_build_date()
    
    if success1 and success2 and success3:
        action = "removed" if not new_suffix else f"set to {new_suffix}"
        print(f"✅ Version suffix {action}")
        return new_suffix
    return False

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
            print(f"   Version: {full_version} (v{info['major']}.{info['minor']}.{info['patch']})")
            print(f"   Build: {info['build']} (Date: {info['build_date']})")
            print(f"   Suffix: '{info['suffix']}'")
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
        print(info['version'] if info else "0.1.0")
        return True
        
    elif command in ['get-suffix']:
        info = get_current_version_info()
        print(info['suffix'] if info else "")
        return True
        
    elif command in ['get-full-version']:
        info = get_current_version_info()
        full_version = f"{info['version']}{info['suffix']}" if info else "0.1.0"
        print(full_version)
        return True
        
    else:
        print(f"❌ Unknown command: {command}")
        show_help()
        return False

if __name__ == "__main__":
    try:
        # Проверяем существование файла
        if not os.path.exists(VERSION_FILE):
            print(f"❌ Version file not found: {VERSION_FILE}")
            print("💡 Please create the file first or check the path")
            sys.exit(1)
        
        success = handle_command(sys.argv[1:])
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        sys.exit(1)