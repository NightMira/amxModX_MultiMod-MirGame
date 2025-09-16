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
    print("  snapshot [N]             Set SNAPSHOT.N suffix")
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
        
        # Упрощенные регулярные выражения
        def find_define(pattern):
            match = re.search(pattern, content, re.MULTILINE)
            return match.group(1) if match else None
        
        return {
            'version': find_define(r'#define PROJECT_VERSION\s+"([^"]+)"'),
            'suffix': find_define(r'#define PROJECT_VERSION_SUFFIX\s+"([^"]*)"'),
            'build': find_define(r'#define PROJECT_BUILD\s+"(\d+)"'),
            'build_num': find_define(r'#define PROJECT_BUILD_NUM\s+(\d+)'),
            'build_date': find_define(r'#define PROJECT_BUILD_DATE\s+"([^"]+)"'),
            'major': find_define(r'#define PROJECT_VERSION_MAJOR\s+"([^"]+)"'),
            'minor': find_define(r'#define PROJECT_VERSION_MINOR\s+"([^"]+)"'),
            'patch': find_define(r'#define PROJECT_VERSION_PATCH\s+"([^"]+)"'),
            'major_num': find_define(r'#define PROJECT_VERSION_MAJOR_NUM\s+(\d+)'),
            'minor_num': find_define(r'#define PROJECT_VERSION_MINOR_NUM\s+(\d+)'),
            'patch_num': find_define(r'#define PROJECT_VERSION_PATCH_NUM\s+(\d+)'),
            'name': find_define(r'#define PROJECT_NAME\s+"([^"]+)"'),
            'author': find_define(r'#define PROJECT_AUTHOR\s+"([^"]+)"'),
            'tag': find_define(r'#define PROJECT_VERSION_TAG\s+"([^"]*)"')
        }
    except Exception as e:
        print(f"❌ Error reading version file: {e}")
        return None

def safe_update_define(content, define_name, new_value, is_string=True):
    """Безопасно обновляет define в содержимом файла"""
    if is_string:
        pattern = rf'#define {define_name}\s+"[^"]*"'
        replacement = f'#define {define_name} "{new_value}"'
    else:
        pattern = rf'#define {define_name}\s+\d+'
        replacement = f'#define {define_name} {new_value}'
    
    new_content, count = re.subn(pattern, replacement, content, flags=re.MULTILINE)
    
    if count == 0:
        print(f"⚠️ Define {define_name} not found in pattern")
        return content, False
    
    return new_content, True

def update_version_define(define_name, new_value, is_string=True):
    """Обновляет одно определение в файле"""
    try:
        with open(VERSION_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content, success = safe_update_define(content, define_name, new_value, is_string)
        
        if not success:
            print(f"⚠️ Define {define_name} not found, adding at the end")
            # Добавляем перед последним #endif
            if '#endif // _version_included' in new_content:
                new_content = new_content.replace('#endif // _version_included', 
                                                 f'#define {define_name} "{new_value}"\n#endif // _version_included' 
                                                 if is_string else 
                                                 f'#define {define_name} {new_value}\n#endif // _version_included')
        
        with open(VERSION_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    except Exception as e:
        print(f"❌ Error updating {define_name}: {e}")
        return False

def update_build_date():
    """Обновляет дату сборки"""
    return update_version_define('PROJECT_BUILD_DATE', datetime.datetime.now().strftime('%Y-%m-%d'))

def update_version_num(major, minor, patch):
    version_num = f"{major}{minor}{patch}"
    return update_version_define('PROJECT_VERSION_NUM', version_num, False)


def update_numeric_version(major, minor, patch):
    """Обновляет числовые представления версии"""
    success = True
    success &= update_version_define('PROJECT_VERSION_MAJOR', str(major))
    success &= update_version_define('PROJECT_VERSION_MAJOR_NUM', str(major), False)
    success &= update_version_define('PROJECT_VERSION_MINOR', str(minor))
    success &= update_version_define('PROJECT_VERSION_MINOR_NUM', str(minor), False)
    success &= update_version_define('PROJECT_VERSION_PATCH', str(patch))
    success &= update_version_define('PROJECT_VERSION_PATCH_NUM', str(patch), False)
    success &= update_version_num(major, minor, patch)  # Обновляем PROJECT_VERSION_NUM
    return success

def increment_version(version_type):
    info = get_current_version_info()
    if not info:
        print("❌ Cannot get version info")
        return False
    
    try:
        major = int(info['major'] or 0)
        minor = int(info['minor'] or 1)
        patch = int(info['patch'] or 0)
    except (ValueError, TypeError):
        major, minor, patch = 0, 1, 0
    
    old_version = info['version'] or "0.1.0"
    
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
    
    print(f"🔄 Updating version: {old_version} → {new_version}")
    print("📌 Removing version suffix (as per SemVer rules)")
    
    # Обновляем все связанные определения
    success1 = update_version_define('PROJECT_VERSION', new_version)
    success2 = update_numeric_version(major, minor, patch)
    success3 = update_build_date()
    
    # Убираем суффикс и тег при изменении версии
    success4 = update_version_define('PROJECT_VERSION_SUFFIX', "")
    success5 = update_version_define('PROJECT_VERSION_TAG', "")
    
    if success1 and success2 and success3 and success4 and success5:
        print(f"✅ Version updated successfully to {new_version}")
        return True
    else:
        print("❌ Failed to update version")
        return False

def update_build_number():
    info = get_current_version_info()
    if not info:
        return False
    
    try:
        current_build = int(info['build'] or 1)
        new_build = str(current_build + 1)
    except (ValueError, TypeError):
        new_build = "1"
    
    # Обновляем номер сборки и дату
    success1 = update_version_define('PROJECT_BUILD', new_build)
    success2 = update_version_define('PROJECT_BUILD_NUM', new_build, False)
    success3 = update_build_date()
    
    if success1 and success2 and success3:
        print(f"✅ Build number updated: {info.get('build', 'N/A')} → {new_build}")
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
        # Простая нумерация снапшотов без файла
        new_suffix = f"-SNAPSHOT.{number}" if number else "-SNAPSHOT"
        new_tag = f"SNAPSHOT.{number}" if number else "SNAPSHOT"
        
    elif suffix_type in ["alpha", "beta", "rc", "hotfix"]:
        new_suffix = f"-{suffix_type}.{number}" if number else f"-{suffix_type}.1"
        new_tag = f"{suffix_type.upper()}.{number}" if number else f"{suffix_type.upper()}.1"
    else:
        new_suffix = info['suffix'] or ""
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
            full_version = f"{info['version'] or '0.1.0'}{info['suffix'] or ''}"
            
            print("📋 Version Information:")
            print(f"   Project: {info['name'] or 'MirGame Multi-Mod'}")
            print(f"   Author: {info['author'] or 'MirGame'}")
            print(f"   Version: {full_version}")
            print(f"   Build: {info['build'] or '1'} (Num: {info.get('build_num', 'N/A')})")
            print(f"   Date: {info['build_date'] or 'N/A'}")
            print(f"   Suffix: '{info['suffix'] or ''}'")
            print(f"   Tag: '{info.get('tag', 'N/A')}'")
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
        number = args[1] if len(args) > 1 else ""
        return update_version_suffix("snapshot", number)
        
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
        print(info['version'] if info and info['version'] else "0.1.0")
        return True
        
    elif command in ['get-suffix']:
        info = get_current_version_info()
        print(info['suffix'] if info and info['suffix'] else "")
        return True
        
    elif command in ['get-full-version']:
        info = get_current_version_info()
        version = info['version'] if info and info['version'] else "0.1.0"
        suffix = info['suffix'] if info and info['suffix'] else ""
        print(f"{version}{suffix}")
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