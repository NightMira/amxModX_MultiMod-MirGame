#!/bin/bash
# 🚀 Setup script for AMXX build system
# 📋 Initializes project structure and dependencies

set -e  # Exit on error

echo "🎯 Setting up AMXX Build System v0.0.6..."
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для цветного вывода
print_status() {
    echo -e "${BLUE}🔧 ${1}${NC}"
}

print_success() {
    echo -e "${GREEN}✅ ${1}${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  ${1}${NC}"
}

print_error() {
    echo -e "${RED}❌ ${1}${NC}"
}

# Функция проверки наличия файла
check_file_exists() {
    local file="$1"
    local description="$2"
    
    if [ -f "$file" ]; then
        echo "   - $description: ✅ $file"
        return 0
    else
        echo "   - $description: ❌ $file (MISSING)"
        return 1
    fi
}

# Функция проверки прав доступа
check_file_executable() {
    local file="$1"
    local description="$2"
    
    if [ -f "$file" ]; then
        if [ -x "$file" ]; then
            echo "   - $description: ✅ Executable"
            return 0
        else
            echo "   - $description: ⚠️  Not executable (run: chmod +x $file)"
            return 1
        fi
    else
        echo "   - $description: ❌ File not found"
        return 1
    fi
}

# Функция проверки hooks
check_hooks_setup() {
    print_status "Checking Git hooks setup..."
    
    local hooks_ok=0
    
    # Проверяем папку hooks
    if [ -d ".githooks" ]; then
        print_success "Hooks directory exists: .githooks/"
    else
        print_error "Hooks directory missing: .githooks/"
        return 1
    fi
    
    # Проверяем pre-commit hook
    echo "🔍 Checking pre-commit hook:"
    check_file_exists ".githooks/pre-commit" "pre-commit hook" && \
    check_file_executable ".githooks/pre-commit" "pre-commit hook"
    if [ $? -eq 0 ]; then
        ((hooks_ok++))
    fi
    
    # Проверяем pre-push hook  
    echo "🔍 Checking pre-push hook:"
    check_file_exists ".githooks/pre-push" "pre-push hook" && \
    check_file_executable ".githooks/pre-push" "pre-push hook"
    if [ $? -eq 0 ]; then
        ((hooks_ok++))
    fi
    
    # Проверяем Git конфигурацию
    echo "🔍 Checking Git configuration:"
    local git_hooks_path=$(git config --get core.hooksPath 2>/dev/null)
    if [ "$git_hooks_path" = ".githooks" ]; then
        echo "   - Git hooks path: ✅ .githooks"
        ((hooks_ok++))
    else
        echo "   - Git hooks path: ❌ Not configured (run: git config core.hooksPath .githooks)"
    fi
    
    if [ $hooks_ok -eq 3 ]; then
        print_success "All Git hooks are properly configured"
        return 0
    else
        print_warning "Some hooks need configuration ($hooks_ok/3 checks passed)"
        return 1
    fi
}

# Загружаем конфигурацию если есть
if [ -f "config.sh" ]; then
    source config.sh
    print_success "Loaded configuration from config.sh"
else
    print_warning "config.sh not found, using default paths"
    ROOT_DIR=$(pwd)
    SCRIPTING_DIR="$ROOT_DIR/scripting"
    COMPILED_DIR="$ROOT_DIR/compiled"
    INCLUDE_DIR="$SCRIPTING_DIR/include"
    VERSION_FILE="$INCLUDE_DIR/version.inc"
    COMPILER="$ROOT_DIR/amxxpc"
fi

# Функция создания структуры проекта
create_project_structure() {
    print_status "Creating project structure..."
    
    mkdir -p "$SCRIPTING_DIR"
    mkdir -p "$COMPILED_DIR"
    mkdir -p "$INCLUDE_DIR"
    
    print_success "Project structure created"
    echo "   - Scripting: $SCRIPTING_DIR"
    echo "   - Compiled: $COMPILED_DIR"
    echo "   - Include: $INCLUDE_DIR"
}

# Функция загрузки компилятора
download_compiler() {
    print_status "Downloading AMXX compiler..."
    
    if [ -f "$COMPILER" ]; then
        print_warning "Compiler already exists: $COMPILER"
        return 0
    fi
    
    # Пробуем скачать из вашего репозитория
    if curl --silent --output /dev/null --head --fail "https://github.com/NightMira/amxmodx_1-9/releases/download/v1.9/amxmodx19.tar"; then
        print_status "Downloading from GitHub Releases..."
        wget -q "https://github.com/NightMira/amxmodx_1-9/releases/download/v1.9/amxmodx19.tar" -O amxmodx19.tar
        
        if [ -f "amxmodx19.tar" ]; then
            tar -xf amxmodx19.tar
            rm -f amxmodx19.tar
            
            if [ -f "amxxpc" ] && [ -f "amxxpc32.so" ]; then
                chmod +x amxxpc
                print_success "Compiler downloaded successfully"
                echo "   - amxxpc: $(file amxxpc | cut -d: -f2-)"
                echo "   - amxxpc32.so: $(file amxxpc32.so | cut -d: -f2-)"
                return 0
            else
                print_error "Compiler files not found in archive"
                return 1
            fi
        else
            print_error "Failed to download compiler archive"
            return 1
        fi
    else
        print_warning "GitHub Releases not accessible, trying official source..."
        wget -q "https://www.amxmodx.org/amxxpack/amxxpc.linux" -O "$COMPILER"
        
        if [ -f "$COMPILER" ]; then
            chmod +x "$COMPILER"
            print_success "Compiler downloaded from official source"
            echo "   - amxxpc: $(file "$COMPILER" | cut -d: -f2-)"
            return 0
        else
            print_error "Failed to download compiler from any source"
            return 1
        fi
    fi
}

# Функция создания version.inc с новой структурой
create_version_file() {
    print_status "Creating version file with MirGame build system..."
    
    if [ -f "$VERSION_FILE" ]; then
        print_warning "Version file already exists: $VERSION_FILE"
        echo "   Keeping existing version file"
        return 0
    fi
    
    mkdir -p "$INCLUDE_DIR"
    
    cat > "$VERSION_FILE" << 'EOF'
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

// Semantic Versioning (SemVer) - ✅ В репозитории (управляется вручную)
#define PROJECT_VERSION_MAJOR "0"
#define PROJECT_VERSION_MAJOR_NUM 0
#define PROJECT_VERSION_MINOR "0"
#define PROJECT_VERSION_MINOR_NUM 0
#define PROJECT_VERSION_PATCH "6"
#define PROJECT_VERSION_PATCH_NUM 6
#define PROJECT_VERSION "0.0.6"
#define PROJECT_VERSION_NUM 6

// Version Suffix (Pre-release tags) - ✅ В репозитории (управляется вручную)
#define PROJECT_VERSION_TAG "SNAPSHOT"
#define PROJECT_VERSION_SUFFIX "-SNAPSHOT"

// MirGame Build System Information - ❌ Генерируется автоматически в CI
#define PROJECT_BUILD               "TEMPLATE"
#define PROJECT_BUILD_NUM           0
#define PROJECT_BUILD_TYPE          "local"
#define PROJECT_BRANCH_CODE         "U"
#define PROJECT_BUILD_SUFFIX        "x"
#define PROJECT_BUILD_DATE          "2025-09-29"
#define PROJECT_BUILD_TIME          __TIME__
#define PROJECT_BUILD_TIMESTAMP     __DATE__ " " __TIME__

// Git Commit Information - ✅ Обновляется автоматически
#define PROJECT_COMMIT_HASH         "0000000000000000000000000000000000000000"
#define PROJECT_COMMIT_SHORT_HASH   "0000000"
#define PROJECT_COMMIT_AUTHOR       "Developer"
#define PROJECT_COMMIT_DATE         "2025-09-29"

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
EOF

    if [ -f "$VERSION_FILE" ]; then
        print_success "Version file created: $VERSION_FILE"
        echo "   - MirGame build system ready"
        echo "   - Semantic versioning: 0.0.6-SNAPSHOT"
        return 0
    else
        print_error "Failed to create version file"
        return 1
    fi
}

# Функция создания build history файла
create_build_history() {
    print_status "Initializing build history..."
    
    if [ -f ".build_history.json" ]; then
        print_warning "Build history already exists"
        return 0
    fi
    
    cat > .build_history.json << 'EOF'
{
  "major_version": 0,
  "branch_builds": {},
  "total_builds": 0,
  "last_build_date": ""
}
EOF

    if [ -f ".build_history.json" ]; then
        print_success "Build history initialized"
    else
        print_error "Failed to create build history"
        return 1
    fi
}

# Функция настройки Git ignore
setup_git_ignore() {
    print_status "Setting up .gitignore..."
    
    if [ ! -f ".gitignore" ]; then
        cat > .gitignore << 'EOF'
# Build artifacts
compiled/
compile.log

# Build system files
.build_history.json
*.build_history.json

# Compiler and temporary files
amxxpc
amxxpc32.so
amxmodx19.tar

# OS files
.DS_Store
Thumbs.db

# IDE files
.vscode/
.idea/
*.swp
*.swo
EOF
        print_success ".gitignore created"
    else
        print_warning ".gitignore already exists"
    fi
}

# Функция создания Git hooks
setup_git_hooks() {
    print_status "Setting up Git hooks..."
    
    # Создаем папку для hooks если её нет
    if [ ! -d ".githooks" ]; then
        mkdir -p .githooks
        print_success "Created .githooks directory"
    fi
    
    # Создаем pre-commit hook
    cat > .githooks/pre-commit << 'EOF'
#!/bin/bash
echo "🔧 Pre-commit: Updating version.inc..."

# Обновляем git информацию
if python3 update_version.py git-info; then
    git add scripting/include/version.inc
    echo "✅ version.inc updated with git information"
else
    echo "❌ Failed to update version.inc"
    exit 1
fi

# Дополнительные проверки
echo "🔍 Running validations..."
if ! python3 update_version.py validate 2>/dev/null; then
    echo "⚠️ Version consistency issues detected"
    echo "   Run: python3 update_version.py validate for details"
fi

echo "✅ Pre-commit checks completed"
exit 0
EOF

    # Создаем pre-push hook
    cat > .githooks/pre-push << 'EOF'
#!/bin/bash
echo "🚀 Pre-push: Running build verification..."

# Проверяем что проект компилируется
if ./compile.sh > /dev/null 2>&1; then
    echo "✅ Build verification passed"
else
    echo "❌ Build failed - fix issues before pushing"
    exit 1
fi

exit 0
EOF

    # Даем права на выполнение
    chmod +x .githooks/pre-commit
    chmod +x .githooks/pre-push
    
    # Настраиваем Git для использования наших hooks
    if git config core.hooksPath .githooks; then
        print_success "Git hooks configured to use .githooks/"
        echo "   - pre-commit: Updates version.inc automatically"
        echo "   - pre-push: Verifies build before pushing"
    else
        print_warning "Failed to configure git hooks path"
        echo "   You can manually run: git config core.hooksPath .githooks"
    fi
    
    print_success "Git hooks setup completed"
}

# Функция проверки системных файлов
check_system_files() {
    print_status "Checking system files and permissions..."
    
    local files_ok=0
    local total_files=0
    
    # Проверяем основные скрипты
    echo "🔍 Checking main scripts:"
    
    check_file_exists "compile.sh" "Compile script" && \
    check_file_executable "compile.sh" "Compile script"
    if [ $? -eq 0 ]; then
        ((files_ok++))
    fi
    ((total_files++))
    
    check_file_exists "update_version.py" "Version management" && \
    check_file_executable "update_version.py" "Version management"
    if [ $? -eq 0 ]; then
        ((files_ok++))
    fi
    ((total_files++))
    
    check_file_exists "config.sh" "Configuration"
    if [ $? -eq 0 ]; then
        ((files_ok++))
    fi
    ((total_files++))
    
    # Проверяем компилятор
    echo "🔍 Checking compiler:"
    check_file_exists "amxxpc" "AMXX compiler" && \
    check_file_executable "amxxpc" "AMXX compiler"
    if [ $? -eq 0 ]; then
        ((files_ok++))
    fi
    ((total_files++))
    
    # Проверяем version.inc
    echo "🔍 Checking version files:"
    check_file_exists "scripting/include/version.inc" "Version information"
    if [ $? -eq 0 ]; then
        ((files_ok++))
    fi
    ((total_files++))
    
    check_file_exists ".build_history.json" "Build history"
    if [ $? -eq 0 ]; then
        ((files_ok++))
    fi
    ((total_files++))
    
    # Проверяем setup_hooks.sh
    echo "🔍 Checking setup scripts:"
    check_file_exists "setup_hooks.sh" "Hooks setup script" && \
    check_file_executable "setup_hooks.sh" "Hooks setup script"
    if [ $? -eq 0 ]; then
        ((files_ok++))
    fi
    ((total_files++))
    
    if [ $files_ok -eq $total_files ]; then
        print_success "All system files are present and properly configured ($files_ok/$total_files)"
        return 0
    else
        print_warning "Some files need attention ($files_ok/$total_files files OK)"
        return 1
    fi
}

# Функция настройки прав доступа
setup_permissions() {
    print_status "Setting up permissions..."
    
    # Делаем скрипты исполняемыми
    chmod +x compile.sh 2>/dev/null || true
    chmod +x update_version.py 2>/dev/null || true
    chmod +x setup.sh 2>/dev/null || true
    
    # Создаем скрипт для настройки hooks если нужно
    if [ ! -f "setup_hooks.sh" ]; then
        cat > setup_hooks.sh << 'EOF'
#!/bin/bash
echo "Setting up git hooks..."
git config core.hooksPath .githooks
echo "✅ Git hooks configured to use .githooks/"
chmod +x .githooks/*
echo "✅ Hooks made executable"
EOF
        chmod +x setup_hooks.sh
    fi
    
    print_success "Permissions set up"
}

# Функция проверки зависимостей
check_dependencies() {
    print_status "Checking system dependencies..."
    
    local missing=0
    local deps=("wget" "tar" "python3")
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            print_warning "Missing dependency: $dep"
            missing=$((missing + 1))
        fi
    done
    
    if [ $missing -eq 0 ]; then
        print_success "All dependencies found"
    else
        print_warning "$missing dependencies missing - some features may not work"
    fi
}

# Функция создания примера плагина
create_example_plugin() {
    print_status "Creating example plugin..."
    
    local example_plugin="$SCRIPTING_DIR/example_plugin.sma"
    
    if [ -f "$example_plugin" ]; then
        print_warning "Example plugin already exists"
        return 0
    fi
    
    cat > "$example_plugin" << 'EOF'
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
EOF

    if [ -f "$example_plugin" ]; then
        print_success "Example plugin created: $(basename "$example_plugin")"
    else
        print_error "Failed to create example plugin"
    fi
}

# Функция показа итоговой информации
show_summary() {
    echo ""
    echo "=========================================="
    echo "🎉 AMXX BUILD SYSTEM SETUP COMPLETED!"
    echo "=========================================="
    echo ""
    
    echo "📁 Project Structure:"
    echo "   - Root:          $(pwd)"
    echo "   - Scripting:     $SCRIPTING_DIR"
    echo "   - Compiled:      $COMPILED_DIR"
    echo "   - Include:       $INCLUDE_DIR"
    [ -d ".githooks" ] && echo "   - Git Hooks:     .githooks/"
    echo ""
    
    # Проверяем системные файлы
    check_system_files
    echo ""
    
    # Проверяем hooks если есть git репозиторий
    if [ -d ".git" ]; then
        check_hooks_setup
        echo ""
    fi
    
    echo "🚀 Next Steps:"
    echo "   1. Add your .sma files to: $SCRIPTING_DIR/"
    echo "   2. Run: ./compile.sh to compile plugins"
    echo "   3. Check: $COMPILED_DIR/ for compiled .amxx files"
    echo ""
    
    echo "🔧 Version Management:"
    echo "   python3 update_version.py info      # Show version info"
    echo "   python3 update_version.py build-mirgame  # Generate build number"
    echo "   python3 update_version.py patch     # Bump patch version"
    echo "   python3 update_version.py validate  # Check version consistency"
    echo ""
    
    if [ -d ".git" ] && [ -d ".githooks" ]; then
        echo "🪝 Git Hooks:"
        echo "   - pre-commit: Auto-updates version.inc with git info"
        echo "   - pre-push:   Verifies build before pushing"
        echo "   - Manual:     ./setup_hooks.sh (if hooks not working)"
        echo ""
    fi
    
    echo "📚 Documentation:"
    echo "   See README.md for detailed usage instructions"
    echo ""
}

# Главная функция
main() {
    echo "=========================================="
    echo "🛠️  AMXX Build System Setup"
    echo "=========================================="
    echo ""
    
    # Проверяем зависимости
    check_dependencies
    echo ""
    
    # Создаем структуру проекта
    create_project_structure
    echo ""
    
    # Загружаем компилятор
    if ! download_compiler; then
        print_error "Failed to download compiler"
        exit 1
    fi
    echo ""
    
    # Создаем файл версий с новой структурой
    if ! create_version_file; then
        print_error "Failed to create version file"
        exit 1
    fi
    echo ""
    
    # Создаем build history
    create_build_history
    echo ""
    
    # Настраиваем git ignore
    setup_git_ignore
    echo ""
    
    # Настраиваем Git hooks (только если это git репозиторий)
    if [ -d ".git" ]; then
        setup_git_hooks
        echo ""
    else
        print_warning "Not a git repository - skipping hooks setup"
        echo "   Initialize git: git init"
        echo "   Then run: ./setup.sh again for hooks"
        echo ""
    fi
    
    # Создаем пример плагина
    create_example_plugin
    echo ""
    
    # Настраиваем права доступа
    setup_permissions
    echo ""
    
    # Показываем итоговую информацию
    show_summary
    
    print_success "AMXX Build System v0.0.6 setup completed! 🎉"
}

# Запускаем главную функцию
main "$@"