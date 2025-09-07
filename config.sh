#!/bin/bash
# 📋 Central configuration for AMXX build system

# ==================== 📁 PATHS ====================
ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
SCRIPTING_DIR="$ROOT_DIR/scripting"
COMPILED_DIR="$ROOT_DIR/compiled"
INCLUDE_DIR="$SCRIPTING_DIR/include"
PLUGINS_DIR="$SCRIPTING_DIR"

# ==================== ⚙️ EXECUTABLES ====================
COMPILER="$ROOT_DIR/amxxpc"
COMPILE_SCRIPT="$ROOT_DIR/compile.sh"
UPDATE_SCRIPT="$ROOT_DIR/update_version.py"

# ==================== 📄 FILES ====================
VERSION_FILE="$SCRIPTING_DIR/include/version.inc"
CONFIG_FILE="$ROOT_DIR/config.sh"
LOG_FILE="$ROOT_DIR/compile.log"

# ==================== ⚙️ SETTINGS ====================
COMPILER_FLAGS="-i$INCLUDE_DIR"
DEFAULT_OUTPUT="$COMPILED_DIR"

# ==================== 🔧 FUNCTIONS ====================
get_define_value() {
    local file="$1" define_name="$2"
    grep -E "^#define[[:space:]]+$define_name" "$file" 2>/dev/null | head -1 | awk -F '"' '{print $2}'
}

create_project_structure() {
    mkdir -p "$SCRIPTING_DIR" "$COMPILED_DIR" "$INCLUDE_DIR"
}

check_requirements() {
    local missing=0
    [ ! -f "$COMPILER" ] && echo "❌ Compiler not found: $COMPILER" && missing=1
    [ ! -d "$INCLUDE_DIR" ] && echo "❌ Include directory not found: $INCLUDE_DIR" && missing=1
    return $missing
}

# ==================== 🚀 EXPORT VARIABLES ====================
export ROOT_DIR SCRIPTING_DIR COMPILED_DIR INCLUDE_DIR PLUGINS_DIR
export COMPILER COMPILE_SCRIPT UPDATE_SCRIPT
export VERSION_FILE CONFIG_FILE LOG_FILE
export COMPILER_FLAGS DEFAULT_OUTPUT

# ==================== 📝 INITIALIZATION ====================
create_project_structure