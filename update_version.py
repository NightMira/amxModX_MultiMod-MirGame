#!/usr/bin/env python3
import re, datetime, os, sys, json, subprocess

VERSION_FILE = "scripting/include/version.inc"
BUILD_HISTORY_FILE = ".build_history.json"

def get_build_history():
    """Загружает историю сборок"""
    if os.path.exists(BUILD_HISTORY_FILE):
        with open(BUILD_HISTORY_FILE, 'r') as f:
            return json.load(f)
    return {
        "major_version": 1,
        "branch_builds": {},
        "total_builds": 0,
        "last_build_date": ""
    }

def save_build_history(history):
    """Сохраняет историю сборок"""
    with open(BUILD_HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def get_current_version_info():
    if not os.path.exists(VERSION_FILE):
        return None
    
    try:
        with open(VERSION_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        def find_define(pattern):
            match = re.search(pattern, content, re.MULTILINE)
            return match.group(1) if match else None
        
        return {
            'version': find_define(r'#define PROJECT_VERSION\s+"([^"]+)"'),
            'suffix': find_define(r'#define PROJECT_VERSION_SUFFIX\s+"([^"]*)"'),
            'build': find_define(r'#define PROJECT_BUILD\s+"([^"]+)"'),
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
    try:
        with open(VERSION_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content, success = safe_update_define(content, define_name, new_value, is_string)
        
        if not success:
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
def update_version_num(major, minor, patch):
    """Обновляет PROJECT_VERSION_NUM в формате MMMmmmppp"""
    version_num = (major * 10000) + (minor * 100) + patch
    return update_version_define('PROJECT_VERSION_NUM', version_num, False)

def update_build_date():
    return update_version_define('PROJECT_BUILD_DATE', datetime.datetime.now().strftime('%Y-%m-%d'))

def get_git_info():
    """Получает информацию о git коммите"""
    git_info = {
        'commit_hash': '',
        'commit_short_hash': '',
        'commit_author': '',
        'commit_date': ''
    }
    
    try:
        git_info['commit_hash'] = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], 
            stderr=subprocess.DEVNULL
        ).decode().strip()
        
        git_info['commit_short_hash'] = subprocess.check_output(
            ['git', 'rev-parse', '--short', 'HEAD'],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        
        git_info['commit_author'] = subprocess.check_output(
            ['git', 'log', '-1', '--pretty=format:%an'],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        
        git_info['commit_date'] = subprocess.check_output(
            ['git', 'log', '-1', '--pretty=format:%cd', '--date=short'],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        
    except Exception as e:
        print(f"⚠️ Could not get git info: {e}")
        git_info['commit_hash'] = 'unknown'
        git_info['commit_short_hash'] = 'unknown'
        git_info['commit_author'] = os.getenv('GITHUB_ACTOR', 'unknown')
        git_info['commit_date'] = datetime.datetime.now().strftime('%Y-%m-%d')
    
    return git_info

def update_git_info():
    """Обновляет информацию о git коммите в version.inc"""
    git_info = get_git_info()
    
    success = True
    success &= update_version_define('PROJECT_COMMIT_HASH', git_info['commit_hash'])
    success &= update_version_define('PROJECT_COMMIT_SHORT_HASH', git_info['commit_short_hash'])
    success &= update_version_define('PROJECT_COMMIT_AUTHOR', git_info['commit_author'])
    success &= update_version_define('PROJECT_COMMIT_DATE', git_info['commit_date'])
    
    if success:
        print("✅ Git commit information updated")
        print(f"   Hash: {git_info['commit_short_hash']}")
        print(f"   Author: {git_info['commit_author']}")
        print(f"   Date: {git_info['commit_date']}")
    else:
        print("❌ Failed to update git commit information")
    
    return success

def generate_mirgame_build_number(branch_code, build_suffix):
    """Генерирует номер сборки в стиле MirGame"""
    history = get_build_history()
    
    info = get_current_version_info()
    major_version = int(info['major'] or 1)
    
    # Логируем текущее состояние
    print(f"🔧 Build history for branch {branch_code}: {history['branch_builds'].get(branch_code, 0)}")
    
    if branch_code not in history["branch_builds"]:
        history["branch_builds"][branch_code] = 0
    
    history["branch_builds"][branch_code] += 1
    history["total_builds"] += 1
    history["major_version"] = major_version
    history["last_build_date"] = datetime.datetime.now().isoformat()
    
    build_number = history["branch_builds"][branch_code]
    
    formatted_build = f"{build_number:04d}"
    mirgame_build_number = f"{major_version:02d}{branch_code}{formatted_build}{build_suffix}"
    
    save_build_history(history)
    
    print(f"🔧 Generated build {mirgame_build_number} (counter: {build_number})")
    return mirgame_build_number, build_number

def get_branch_code(branch_name):
    """Определяет код ветки по имени ветки Git"""
    branch_name = branch_name.lower()
    
    exact_matches = {
        'main': 'R',
        'dev': 'D',
    }
    
    pattern_matches = {
        'hotfix/': 'H',
        'alpha/': 'A',
        'beta/': 'B',
        'rc/': 'C',
        'feature/': 'F',
        'bugfix/': 'X',
    }
    
    for exact_branch, code in exact_matches.items():
        if branch_name == exact_branch:
            return code
    
    for pattern, code in pattern_matches.items():
        if branch_name.startswith(pattern):
            return code
    
    if branch_name == 'pr':
        return 'P'
    
    return 'U'

def get_build_suffix(build_type):
    """Определяет суффикс типа сборки"""
    suffix_mapping = {
        'internal': 'i',
        'developer': 'd',
        'beta': 'b',
        'release': 'r',
        'nightly': 'n',
        'snapshot': 's',
        'ci': 'c',
        'local': 'l'
    }
    return suffix_mapping.get(build_type.lower(), 'x')

def detect_build_type():
    """Автоматически определяет тип сборки по окружению"""
    if os.getenv('GITHUB_ACTIONS'):
        ref = os.getenv('GITHUB_REF', '')
        
        if ref.startswith('refs/tags/'):
            return 'release'
        elif ref == 'refs/heads/main':
            return 'release'
        elif ref == 'refs/heads/dev':
            return 'developer'
        elif '/alpha/' in ref:
            return 'internal'
        elif '/beta/' in ref:
            return 'beta'
        elif '/rc/' in ref:
            return 'beta'
        elif '/hotfix/' in ref:
            return 'internal'
        else:
            return 'ci'
    else:
        return 'local'

def update_build_number():
    """Обновляет номер сборки в стиле MirGame"""
    info = get_current_version_info()
    if not info:
        return False
    
    branch_name = get_current_branch_name()
    branch_code = get_branch_code(branch_name)
    build_type = detect_build_type()
    build_suffix = get_build_suffix(build_type)
    
    mirgame_build_number, build_counter = generate_mirgame_build_number(branch_code, build_suffix)
    
    success = True
    success &= update_version_define('PROJECT_BUILD', mirgame_build_number)
    success &= update_version_define('PROJECT_BUILD_NUM', build_counter, False)
    success &= update_version_define('PROJECT_BUILD_TYPE', build_type)
    success &= update_version_define('PROJECT_BRANCH_CODE', branch_code)
    success &= update_version_define('PROJECT_BUILD_SUFFIX', build_suffix)
    success &= update_build_date()
    success &= update_git_info()
    
    if success:
        print(f"✅ Номер сборки обновлен: {mirgame_build_number}")
        print(f"   Ветка: {branch_name} ({branch_code})")
        print(f"   Тип: {build_type} ({build_suffix})")
        print(f"   Счетчик: {build_counter}")
        return mirgame_build_number
    return False

def get_current_branch_name():
    """Получает имя текущей ветки Git"""
    try:
        if os.getenv('GITHUB_ACTIONS'):
            ref = os.getenv('GITHUB_REF', '')
            
            if ref.startswith('refs/tags/'):
                return 'main'
            elif ref.startswith('refs/heads/'):
                branch_name = ref[11:]
                
                patterns = ['hotfix/', 'alpha/', 'beta/', 'rc/', 'feature/', 'bugfix/']
                for pattern in patterns:
                    if branch_name.startswith(pattern):
                        return branch_name
                
                if branch_name in ['main', 'dev']:
                    return branch_name
                
                return branch_name
            elif ref.startswith('refs/pull/'):
                return 'pr'
        
        result = subprocess.check_output(['git', 'branch', '--show-current'], 
                                        stderr=subprocess.DEVNULL)
        branch_name = result.decode().strip()
        
        patterns = ['hotfix/', 'alpha/', 'beta/', 'rc/', 'feature/', 'bugfix/']
        for pattern in patterns:
            if branch_name.startswith(pattern):
                return branch_name
        
        return branch_name
        
    except:
        return 'unknown'

def decode_build_number(build_number):
    """Декодирует номер сборки в стиле MirGame"""
    if len(build_number) < 7:
        return None
    
    try:
        major = int(build_number[0:2])
        branch_code = build_number[2]
        build_counter = int(build_number[3:7])
        suffix = build_number[7] if len(build_number) > 7 else ''
        
        branch_names = {
            'R': 'main (Релиз)',
            'D': 'dev (Разработка)', 
            'H': 'hotfix/* (Исправление)',
            'A': 'alpha/* (Альфа)',
            'B': 'beta/* (Бета)',
            'C': 'rc/* (Кандидат)',
            'F': 'feature/* (Функция)',
            'X': 'bugfix/* (Баги)',
            'P': 'PR (Pull Request)',
            'U': 'Unknown (Неизвестная)'
        }
        
        suffix_names = {
            'i': 'Internal (Внутренняя)',
            'd': 'Developer (Разработчика)', 
            'b': 'Beta (Бета)',
            'r': 'Release (Релиз)',
            'n': 'Nightly (Ночная)',
            's': 'Snapshot (Снапшот)',
            'c': 'CI (Непрерывная интеграция)',
            'l': 'Local (Локальная)',
            'x': 'Experimental (Экспериментальная)'
        }
        
        return {
            'major_version': major,
            'branch_code': branch_code,
            'branch_name': branch_names.get(branch_code, 'Unknown'),
            'build_counter': build_counter,
            'suffix': suffix,
            'suffix_name': suffix_names.get(suffix, 'Unknown'),
            'full_decode': f"Версия {major}, ветка {branch_names.get(branch_code, 'Unknown')}, сборка #{build_counter} ({suffix_names.get(suffix, 'Unknown')})"
        }
    except:
        return None

def get_branch_stats():
    """Статистика по использованию веток"""
    history = get_build_history()
    
    print("📊 Статистика по веткам:")
    for branch_code, count in sorted(history["branch_builds"].items()):
        branch_names = {
            'R': 'main', 'D': 'dev', 'H': 'hotfix/*', 'A': 'alpha/*',
            'B': 'beta/*', 'C': 'rc/*', 'F': 'feature/*', 'X': 'bugfix/*',
            'P': 'PR', 'U': 'unknown'
        }
        print(f"   {branch_code} ({branch_names.get(branch_code, 'unknown')}): {count} сборок")
    
    return True

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
    
    # Обновляем ВСЕ версионные поля
    success1 = update_version_define('PROJECT_VERSION', new_version)
    success2 = update_version_define('PROJECT_VERSION_MAJOR', str(major))
    success3 = update_version_define('PROJECT_VERSION_MAJOR_NUM', major, False)
    success4 = update_version_define('PROJECT_VERSION_MINOR', str(minor))
    success5 = update_version_define('PROJECT_VERSION_MINOR_NUM', minor, False)
    success6 = update_version_define('PROJECT_VERSION_PATCH', str(patch))
    success7 = update_version_define('PROJECT_VERSION_PATCH_NUM', patch, False)  # ДОБАВЛЕНО
    success8 = update_version_num(major, minor, patch)  # ДОБАВЛЕНО
    success9 = update_build_date()
    success10 = update_version_define('PROJECT_VERSION_SUFFIX', "")
    success11 = update_version_define('PROJECT_VERSION_TAG', "")
    success12 = update_git_info()
    
    if all([success1, success2, success3, success4, success5, success6, 
            success7, success8, success9, success10, success11, success12]):
        print(f"✅ Version updated successfully to {new_version}")
        return True
    else:
        print("❌ Failed to update version")
        return False

def update_version_suffix(suffix_type, number=""):
    info = get_current_version_info()
    if not info:
        return False
    
    if suffix_type == "release":
        new_suffix = ""
        new_tag = ""
    elif suffix_type == "snapshot":
        new_suffix = f"-SNAPSHOT.{number}" if number else "-SNAPSHOT"
        new_tag = f"SNAPSHOT.{number}" if number else "SNAPSHOT"
    elif suffix_type in ["alpha", "beta", "rc", "hotfix"]:
        new_suffix = f"-{suffix_type}.{number}" if number else f"-{suffix_type}.1"
        new_tag = f"{suffix_type.upper()}.{number}" if number else f"{suffix_type.upper()}.1"
    else:
        new_suffix = info['suffix'] or ""
        new_tag = info.get('tag', '')
    
    success1 = update_version_define('PROJECT_VERSION_SUFFIX', new_suffix)
    success2 = update_version_define('PROJECT_VERSION_TAG', new_tag)
    success3 = update_build_date()
    success4 = update_git_info()
    
    if success1 and success2 and success3 and success4:
        action = "removed" if not new_suffix else f"set to {new_suffix}"
        print(f"✅ Version suffix {action}")
        return True
    return False

def validate_version_consistency():
    """Проверяет согласованность версионных данных"""
    info = get_current_version_info()
    if not info:
        return False
    
    issues = []
    
    # Проверяем соответствие строковых и числовых значений
    if info.get('major') and info.get('major_num'):
        if int(info['major']) != int(info['major_num']):
            issues.append(f"MAJOR mismatch: {info['major']} vs {info['major_num']}")
    
    if info.get('minor') and info.get('minor_num'):
        if int(info['minor']) != int(info['minor_num']):
            issues.append(f"MINOR mismatch: {info['minor']} vs {info['minor_num']}")
    
    if info.get('patch') and info.get('patch_num'):
        if int(info['patch']) != int(info['patch_num']):
            issues.append(f"PATCH mismatch: {info['patch']} vs {info['patch_num']}")
    
    # Проверяем PROJECT_VERSION_NUM
    expected_num = (int(info.get('major', 0)) * 10000 + 
                   int(info.get('minor', 0)) * 100 + 
                   int(info.get('patch', 0)))
    actual_num = int(info.get('version_num', 0))
    if expected_num != actual_num:
        issues.append(f"VERSION_NUM mismatch: expected {expected_num}, got {actual_num}")
    
    if issues:
        print("⚠️ Version consistency issues found:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    
    print("✅ Version data is consistent")
    return True

def handle_command(args):
    if not args or args[0] in ['-h', '--help']:
        show_help()
        return True
    
    command = args[0].lower()
    
    if command in ['build-mirgame', 'bm']:
        result = update_build_number()
        return result is not None
        
    elif command in ['decode-build', 'db']:
        if len(args) > 1:
            build_number = args[1]
            decoded = decode_build_number(build_number)
            if decoded:
                print("🔍 Анализ номера сборки:")
                print(f"   Полный номер: {build_number}")
                print(f"   Мажорная версия: {decoded['major_version']}")
                print(f"   Ветка: {decoded['branch_code']} ({decoded['branch_name']})")
                print(f"   Счетчик сборки: {decoded['build_counter']}")
                print(f"   Суффикс: {decoded['suffix']} ({decoded['suffix_name']})")
                print(f"   Расшифровка: {decoded['full_decode']}")
            else:
                print("❌ Неверный формат номера сборки")
        else:
            info = get_current_version_info()
            if info and info.get('build'):
                decoded = decode_build_number(info['build'])
                if decoded:
                    print("🔍 Анализ текущей сборки:")
                    for key, value in decoded.items():
                        print(f"   {key.replace('_', ' ').title()}: {value}")
            else:
                print("❌ Номер сборки не найден")
        return True
        
    elif command in ['build-history', 'bh']:
        history = get_build_history()
        print("📊 История сборок:")
        print(f"   Мажорная версия: {history['major_version']}")
        print(f"   Всего сборок: {history['total_builds']}")
        print(f"   Последняя сборка: {history['last_build_date']}")
        get_branch_stats()
        return True
        
    elif command in ['branch-stats', 'bs']:
        return get_branch_stats()
    
    elif command in ['info', '-i']:
        info = get_current_version_info()
        if info:
            full_version = f"{info['version'] or '0.1.0'}{info['suffix'] or ''}"
            
            print("📋 Информация о версии:")
            print(f"   Проект: {info['name'] or 'MirGame Multi-Mod'}")
            print(f"   Автор: {info['author'] or 'MirGame'}")
            print(f"   Версия: {full_version}")
            print(f"   Сборка: {info['build'] or '1'}")
            print(f"   Дата: {info['build_date'] or 'N/A'}")
            
            if info.get('build') and len(info['build']) >= 7:
                decoded = decode_build_number(info['build'])
                if decoded:
                    print(f"   Тип сборки: {decoded['suffix_name']}")
                    print(f"   Ветка: {decoded['branch_name']}")
        return True
        
    elif command in ['major', '--major']:
        return increment_version("major")
    elif command in ['validate', '-v']:
        return validate_version_consistency()
        
    elif command in ['minor', '--minor']:
        return increment_version("minor")
        
    elif command in ['patch', '--patch']:
        return increment_version("patch")
        
    elif command in ['build', '-b']:
        result = update_build_number()
        return result is not None
        
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
    elif command in ['git-info']:
        update_git_info()
        return True
        
    else:
        print(f"❌ Unknown command: {command}")
        show_help()
        return False

def show_help():
    print("🚀 MirGame Build System - Система нумерации сборок")
    print("Usage: python update_version.py [COMMAND] [OPTIONS]")
    print("\n📋 Поддерживаемые ветки:")
    print("  main, dev, hotfix/*, alpha/*, beta/*, rc/*, feature/*, bugfix/*")
    print("\n🔧 Команды системы сборок:")
    print("  build-mirgame (bm)       Генерировать номер сборки MirGame")
    print("  decode-build (db) [NUM]  Расшифровать номер сборки")
    print("  build-history (bh)       Показать историю сборок")
    print("  branch-stats (bs)        Статистика по веткам")
    print("\n🔄 Стандартные команды версий:")
    print("  info                     Показать информацию о версии")
    print("  major                    Увеличить мажорную версию (X.0.0)")
    print("  minor                    Увеличить минорную версию (0.Y.0)")  
    print("  patch                    Увеличить патч версию (0.0.Z)")
    print("  build                    Увеличить номер сборки")
    print("  snapshot [N]             Установить SNAPSHOT.N суффикс")
    print("  release                  Убрать суффикс для финального релиза")
    print("  alpha [N]                Установить alpha.N суффикс")
    print("  beta [N]                 Установить beta.N суффикс")
    print("  rc [N]                   Установить rc.N суффикс")
    print("  hotfix [N]               Установить hotfix.N суффикс")
    print("  get-version              Получить базовую версию (X.Y.Z)")
    print("  get-suffix               Получить суффикс версии")
    print("  get-full-version         Получить полную версию с суффиксом")

if __name__ == "__main__":
    try:
        if not os.path.exists(VERSION_FILE):
            print(f"❌ Version file not found: {VERSION_FILE}")
            sys.exit(1)
        
        success = handle_command(sys.argv[1:])
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        sys.exit(1)