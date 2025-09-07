# Changelog

## [0.0.1] - 2025-09-05

### 🚀 Added
- **Complete build system** for AMXX plugins compilation
- **Centralized configuration** in `config.sh` with path management
- **Version management system** with `update_version.py` script:
  - Semantic versioning with pre-releases (alpha, beta, rc)
  - Automatic build number increment
  - Branch-based suffix detection

### 📊 Enhanced
- **Plugin validation** for required defines (PLUGIN_NAME, PLUGIN_VERSION, PLUGIN_AUTHOR)
- **Detailed compilation reporting** with color-coded status table
- **Comprehensive logging** to `compile.log` with timestamps
- **Statistics tracking** (successful/warnings/errors counts)

### 🤖 Automated
- **CI/CD pipeline** with GitHub Actions:
  - Automatic branch-based version suffixes:
    - `main` → release (1.0.0)
    - `develop` → alpha.1 (1.0.0-alpha.1)
    - `pre-release/alpha/*` → alpha.X
    - `pre-release/beta/*` → beta.X  
    - `pre-release/rc/*` → rc.X
  - Artifact upload with suffix naming
  - 32-bit library dependencies installation

### 🛡️ Reliability
- **Error handling** for compiler failures
- **Timeout protection** (30s per plugin)
- **Fallback mechanisms** for missing components
- **Requirements checking** before compilation

### 🎯 Usage
``` bash
# Compile all plugins
./compile.sh

# Version management
python3 update_version.py info      # Show current version
python3 update_version.py build     # Increment build number
python3 update_version.py alpha 1   # Set alpha release
python3 update_version.py release   # Final release
```
## [0.1.0] - 2025-09-07
### **🚀 Initial Release: Complete AMXX Build System**
**📦 Core System Architecture**
- **Полная система сборки** AMXX плагинов с SemVer версионированием
- **Централизованная конфигурация** через `config.sh`
- **Автоматическое создание структуры** проекта при инициализации
- **Поддержка всех веток** Git workflow: `main`, `dev`, `feature/*`, `pre-release/*`, `hotfix/*`

**🏷️ Semantic Versioning System**
- **Полное соответствие SemVer 2.0.0**
- **Автоматическое определение версий** по веткам:
  - `main` → релизные версии (1.0.0)
  - `dev` → SNAPSHOT версии (1.0.0-SNAPSHOT)
  - `pre-release/alpha/*` → alpha-версии (1.0.0-alpha.1)
  - `pre-release/beta/*` → beta-версии (1.0.0-beta.1)
  - `pre-release/rc/*` → release candidate (1.0.0-rc.1)
  - `hotfix/*` → хотфиксы (1.0.1-hotfix.1)

**🤖 CI/CD Automation**
- **GitHub Actions workflow** с полной автоматизацией
- **Автоматическая сборка** при пуше в любую ветку
- **Умное версионирование** на основе веток и тегов
- **Артефакты сборки** с автоматическим именованием:

  - amxx-plugins-stable - для main ветки
  - amxx-plugins-dev - для dev ветки
  - amxx-plugins-alpha-N - для alpha версий
  - amxx-plugins-beta-N - для beta версий
  - amxx-plugins-rc-N - для release candidate


**📊 Advanced Reporting**
- **Детальная таблица результатов** компиляции
- **Цветовая индикация статусов** (✅ Success, ⚠️ Warnings, ❌ Errors)
- **Подсчет статистики:** успешные/с предупреждениями/с ошибками
- **Подробное логирование** в `compile.log` с timestamp
- **Автоматические summary** в GitHub Actions

**🎯 Plugin Validation System**

- **Валидация метаданных** плагинов:
  - Проверка `PLUGIN_NAME`
  - Проверка `PLUGIN_VERSION`
  - Проверка `PLUGIN_AUTHOR`
- **Автоматическое использование** `PROJECT_AUTHOR` из version.inc
- **Предупреждения** о missing defines

**📁 Project Structure**

```
amxModX_MultiMod/
├── 📄 amxxpc                 # Компилятор
├── 📄 compile.sh             # Главный скрипт компиляции
├── 📄 config.sh              # Центральная конфигурация
├── 📄 update_version.py      # Управление версиями
├── 📁 compiled/              # Скомпилированные плагины
└── 📁 scripting/
    ├── 📁 include/
    │   └── 📄 version.inc    # Версии проекта (SemVer)
    └── 📄 *.sma              # Исходники плагинов
```
**🔧 Version Management**
- **Python скрипт** `update_version.py` с командами:
  ``` bash
  python3 update_version.py info      # Информация о версии
  python3 update_version.py major     # Инкремент мажорной версии
  python3 update_version.py minor     # Инкремент минорной версии  
  python3 update_version.py patch     # Инкремент патч версии
  python3 update_version.py build     # Инкремент номера сборки
  python3 update_version.py alpha N   # Установка alpha версии
  python3 update_version.py beta N    # Установка beta версии
  python3 update_version.py rc N      # Установка rc версии
  python3 update_version.py release   # Релизная версия
  ```
**🏷️ Labels & Project Management**
- **Система меток** для GitHub Issues:
  - `🐛 bug` - Ошибки компиляции
  - `✨ feature` - Новые функции
  - `🔧 refactor` - Рефакторинг
  - `🚨 priority-critical` - Критический приоритет
  - `⚡ priority-high` - Высокий приоритет
  - `📋 priority-medium` - Средний приоритет
- **Автоматическое добавление** issues в GitHub Projects
- **Синхронизация меток** через CI/CD

**💻 Usage Examples**
``` bash
# Компиляция всех плагинов
./compile.sh

# Управление версиями
python3 update_version.py minor      # 0.0.1 → 0.1.0
python3 update_version.py alpha 1    # 0.1.0-alpha.1
python3 update_version.py build      # Инкремент сборки

# Создание issue с метками
gh issue create --title "Ошибка компиляции" --label "bug,priority-high"
```
