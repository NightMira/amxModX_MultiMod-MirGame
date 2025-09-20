#!/bin/bash
source "$(dirname "$0")/config.sh"

# 📊 Counters
PLUGINS_WITH_WARNINGS=0
PLUGINS_WITH_ERRORS=0
PLUGINS_SUCCESSFUL=0
TOTAL_WARNINGS=0
declare -A PLUGINS_DATA

# 🔍 Functions
get_define_value() {
    local file="$1" define_name="$2"
    grep -E "^#define[[:space:]]+$define_name" "$file" 2>/dev/null | head -1 | awk -F '"' '{print $2}'
}

uses_project_author() {
    # Проверяем использование PROJECT_AUTHOR в register_plugin
    grep -E "register_plugin\([^,]+,[^,]+,PROJECT_AUTHOR" "$1" >/dev/null 2>&1 ||
    # Или использование PROJECT_AUTHOR в любом другом контексте
    grep -E "PROJECT_AUTHOR" "$1" >/dev/null 2>&1
}

get_plugin_status() {
    [ "$2" -eq 0 ] && { [ "$1" -eq 0 ] && echo "0" || echo "1"; } || echo "2"
}

# 🏷️ Project information
PROJECT_NAME=$(get_define_value "$VERSION_FILE" "PROJECT_NAME")
PROJECT_AUTHOR=$(get_define_value "$VERSION_FILE" "PROJECT_AUTHOR")
PROJECT_BUILD=$(get_define_value "$VERSION_FILE" "PROJECT_BUILD")
PROJECT_VERSION=$(get_define_value "$VERSION_FILE" "PROJECT_VERSION")
PROJECT_SUFFIX=$(get_define_value "$VERSION_FILE" "PROJECT_VERSION_SUFFIX")
FULL_VERSION="${PROJECT_VERSION}${PROJECT_SUFFIX}"

PROJECT_NAME=${PROJECT_NAME:-"MirGame Multi-Mod"}
PROJECT_AUTHOR=${PROJECT_AUTHOR:-"MirGame"}
PROJECT_BUILD=${PROJECT_BUILD:-"1"}
PROJECT_VERSION=${PROJECT_VERSION:-"1.0.0"}

echo "🔨 [$PROJECT_NAME] Starting compilation..."
echo "🏷️ Version: $FULL_VERSION (build $PROJECT_BUILD)"
echo "==========================================" > "$LOG_FILE"
echo "🏗️ Project: $PROJECT_NAME" >> "$LOG_FILE"
echo "👤 Author: $PROJECT_AUTHOR" >> "$LOG_FILE"
echo "🔄 Version: $FULL_VERSION" >> "$LOG_FILE"
echo "🔢 Build: $PROJECT_BUILD" >> "$LOG_FILE"
echo "📅 Date: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

mkdir -p "$COMPILED_DIR"

# 📦 Plugin compilation function
compile_plugin() {
    local sma_file="$1"
    local base_name=$(basename "$sma_file" .sma)
    local plugin_name=$(get_define_value "$sma_file" PLUGIN_NAME)
    local plugin_version=$(get_define_value "$sma_file" PLUGIN_VERSION)
    local plugin_author=$(get_define_value "$sma_file" PLUGIN_AUTHOR)
    
    local warnings="" local_warnings=0 has_warnings=0 compile_result=1

    [ -z "$plugin_name" ] && { warnings+="PLUGIN_NAME "; local_warnings=$((local_warnings + 1)); plugin_name="Not name"; }
    [ -z "$plugin_version" ] && { warnings+="PLUGIN_VERSION "; local_warnings=$((local_warnings + 1)); plugin_version=""; }
    
    # ОСНОВНОЕ ИСПРАВЛЕНИЕ: проверяем использование PROJECT_AUTHOR
    if [ -z "$plugin_author" ] && ! uses_project_author "$sma_file"; then
        warnings+="PLUGIN_AUTHOR "; local_warnings=$((local_warnings + 1)); plugin_author="Not author"
    elif [ -z "$plugin_author" ] && uses_project_author "$sma_file"; then
        # Если используется PROJECT_AUTHOR, используем автора проекта
        plugin_author="$PROJECT_AUTHOR"
        echo "📝 Using PROJECT_AUTHOR: $plugin_author" >> "$LOG_FILE"
    fi
    
    local version_display=""; [ -n "$plugin_version" ] && version_display="v$plugin_version" || version_display="Not version"
    local display_compiling_name="$plugin_name"; [ "$plugin_name" = "Not name" ] && display_compiling_name="$base_name"
    
    echo "📦 Compiling: $display_compiling_name $version_display"
    echo "🔧 Plugin: $display_compiling_name $version_display (file: $base_name.sma)" >> "$LOG_FILE"
    echo "👤 Author: $plugin_author" >> "$LOG_FILE"
    
    if [ -n "$warnings" ]; then
        warning_msg="Plugin $base_name: Not found ${warnings% }"
        echo "⚠️ [WARNING] $warning_msg"
        echo "⚠️ [WARNING] $warning_msg" >> "$LOG_FILE"
        TOTAL_WARNINGS=$((TOTAL_WARNINGS + local_warnings))
        has_warnings=1
    fi
    
    "$COMPILER" "$sma_file" -o"$COMPILED_DIR/$base_name.amxx" -i"$INCLUDE_DIR" 2>> "$LOG_FILE"
    compile_result=$?
    
    if [ $compile_result -eq 0 ]; then
        echo "✅ Success: $base_name.amxx"
        echo "✅ Status: Success" >> "$LOG_FILE"
        [ $has_warnings -eq 1 ] && PLUGINS_WITH_WARNINGS=$((PLUGINS_WITH_WARNINGS + 1)) || PLUGINS_SUCCESSFUL=$((PLUGINS_SUCCESSFUL + 1))
    else
        echo "❌ Failed: $plugin_name (see compile.log)"
        echo "❌ Status: Failed" >> "$LOG_FILE"
        PLUGINS_WITH_ERRORS=$((PLUGINS_WITH_ERRORS + 1))
        tail -5 "$LOG_FILE" | grep -i error
    fi
    
    local status_code=$(get_plugin_status $has_warnings $compile_result)
    PLUGINS_DATA["$base_name"]="$plugin_name|$plugin_version|$plugin_author|$status_code"
    echo "------------------------------------------" >> "$LOG_FILE"
}

# 🔄 Compile all plugins
if [ -d "$SCRIPTING_DIR" ]; then
    echo "🔍 Searching for .sma files in: $SCRIPTING_DIR"
    sma_files=()
    while IFS= read -r -d '' file; do
        sma_files+=("$file")
    done < <(find "$SCRIPTING_DIR" -name "*.sma" -type f -print0 2>/dev/null)
    
    total_files=${#sma_files[@]}
    echo "📋 Found $total_files .sma files to compile"
    
    if [ $total_files -eq 0 ]; then
        echo "❌ No .sma files found in $SCRIPTING_DIR"
        exit 1
    fi
    
    for sma_file in "${sma_files[@]}"; do
        compile_plugin "$sma_file"
    done
else
    echo "❌ Scripting directory not found: $SCRIPTING_DIR"
    exit 1
fi

# 📊 Summary
TOTAL_PLUGINS=$((PLUGINS_SUCCESSFUL + PLUGINS_WITH_WARNINGS + PLUGINS_WITH_ERRORS))

echo ""; echo "=========================================="
echo "📊 [$PROJECT_NAME] Compilation summary:"
echo "✅ Successful: $PLUGINS_SUCCESSFUL (without warnings)"
echo "⚠️ With warnings: $PLUGINS_WITH_WARNINGS"
echo "❌ Failed: $PLUGINS_WITH_ERRORS"
echo "📋 Total warnings: $TOTAL_WARNINGS"
echo "🏷️ Version: $FULL_VERSION (build $PROJECT_BUILD)"
echo "📋 Details saved to: $LOG_FILE"

# 📋 Table function
print_table_row() {
    local base_name="$1" plugin_name="$2" plugin_version="$3" plugin_author="$4" status_code="$5"
    local version_display="$plugin_version"
    [ -n "$plugin_version" ] && [ "$plugin_version" != "Not version" ] && version_display="v$plugin_version" || version_display="-"
    
    case "$status_code" in
        "0") status_display="✅ Success" ;;
        "1") status_display="⚠️ Success (warnings)" ;;
        "2") status_display="❌ Failed" ;;
        *) status_display="❓ Unknown" ;;
    esac
    
    printf "%-20s | %-15s | %-10s | %-15s | %s\n" "$base_name" "$plugin_name" "$version_display" "$plugin_author" "$status_display"
}

# 📋 Print plugins table
echo ""; echo "📦 Plugins details:"
echo "------------------------------------------------------------"
printf "%-20s | %-15s | %-10s | %-15s | %s\n" "File" "Name" "Version" "Author" "Status"
echo "------------------------------------------------------------"

for base_name in "${!PLUGINS_DATA[@]}"; do
    IFS='|' read -r plugin_name plugin_version plugin_author status_code <<< "${PLUGINS_DATA[$base_name]}"
    print_table_row "$base_name" "$plugin_name" "$plugin_version" "$plugin_author" "$status_code"
done

echo "------------------------------------------------------------"