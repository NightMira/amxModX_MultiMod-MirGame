#!/bin/bash
# 🚀 Setup script for AMXX build system
# 📋 Initializes project structure and dependencies

set -e  # Exit on error

echo "🎯 Setting up AMXX build system..."
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

# Загружаем конфигурацию если есть
if [ -f "config.sh" ]; then
    source config.sh
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

# Функция создания version.inc
create_version_file() {
    print_status "Creating version file..."
    
    if [ -f "$VERSION_FILE" ]; then
        print_warning "Version file already exists: $VERSION_FILE"
        return 0
    fi
    
    mkdir -p "$INCLUDE_DIR"
    
    cat > "$VERSION_FILE" << 'EOF'
#if defined _version_included
    #endinput
#endif
#define _version_included

#define PROJECT_NAME "MirGame Multi-Mod"
#define PROJECT_AUTHOR "MirGame"
#define PROJECT_VERSION "1.0.0"
#define PROJECT_VERSION_SUFFIX ""
#define PROJECT_BUILD "1"
#define PROJECT_BUILD_DATE "2024-02-08"

#define PRINT_PROJECT_INFO() \
    server_print("[%s] Project v%s (build %s, %s)", \
    PROJECT_NAME, PROJECT_VERSION PROJECT_VERSION_SUFFIX, PROJECT_BUILD, PROJECT_BUILD_DATE)

#define PROJECT_FULL_VERSION PROJECT_VERSION PROJECT_VERSION_SUFFIX
EOF

    if [ -f "$VERSION_FILE" ]; then
        print_success "Version file created: $VERSION_FILE"
        return 0
    else
        print_error "Failed to create version file"
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
#define PLUGIN_AUTHOR PROJECT_AUTHOR

public plugin_init()
{
    register_plugin(PLUGIN_NAME, PLUGIN_VERSION, PLUGIN_AUTHOR);
    
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
    echo "🎉 SETUP COMPLETED SUCCESSFULLY!"
    echo "=========================================="
    echo ""
    
    echo "📁 Project Structure:"
    echo "   - Root:          $(pwd)"
    echo "   - Scripting:     $SCRIPTING_DIR"
    echo "   - Compiled:      $COMPILED_DIR"
    echo "   - Include:       $INCLUDE_DIR"
    echo ""
    
    echo "⚙️  Files:"
    [ -f "amxxpc" ] && echo "   - Compiler:      ✅ amxxpc"
    [ -f "amxxpc32.so" ] && echo "   - Library:       ✅ amxxpc32.so"
    [ -f "$VERSION_FILE" ] && echo "   - Version:       ✅ $(basename "$VERSION_FILE")"
    [ -f "compile.sh" ] && echo "   - Build script:  ✅ compile.sh"
    [ -f "config.sh" ] && echo "   - Config:        ✅ config.sh"
    echo ""
    
    echo "🚀 Next steps:"
    echo "   1. Add your .sma files to: $SCRIPTING_DIR/"
    echo "   2. Run: ./compile.sh to compile plugins"
    echo "   3. Check: $COMPILED_DIR/ for compiled .amxx files"
    echo ""
    
    echo "🔧 Useful commands:"
    echo "   ./compile.sh                 # Compile all plugins"
    echo "   python3 update_version.py    # Update build number"
    echo "   python3 update_version.py info  # Show version info"
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
    
    # Создаем структуру проекта
    create_project_structure
    
    # Загружаем компилятор
    if ! download_compiler; then
        print_error "Failed to download compiler"
        exit 1
    fi
    
    # Создаем файл версий
    if ! create_version_file; then
        print_error "Failed to create version file"
        exit 1
    fi
    
    # Создаем пример плагина
    create_example_plugin
    
    # Настраиваем права доступа
    setup_permissions
    
    # Показываем итоговую информацию
    show_summary
    
    print_success "Setup completed successfully! 🎉"
}

# Запускаем главную функцию
main "$@"