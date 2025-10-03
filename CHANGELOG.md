# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.6] - 2025-10-03

### Добавлено
- **Новая система нумерации сборок MirGame** - автоматическая генерация номеров сборок в формате `XXYZZZZs`
- **Git hooks** - автоматическое обновление версии и проверка сборки через pre-commit и pre-push
- **Build History** - отслеживание истории сборок в `.build_history.json`
- **Автоматическое определение типа сборки** по окружению (CI/локальная/релиз)
- **Команды анализа сборок** - `decode-build`, `build-history`, `branch-stats`
- **Пример плагина** - `example_plugin.sma` с использованием новой системы версий
- **Скрипт настройки hooks** - `setup_hooks.sh` для быстрой настройки git hooks

### Изменено
- **Обновлена структура version.inc** - разделение на ручные и автоматические поля
- **Упрощенная логика версионирования в CI** - убрана сложная логика определения веток
- **Улучшенная система версионирования** - семантическое версионирование с поддержкой пре-релизов
- **Обновлен setup.sh** (v0.0.6) - улучшенная настройка системы с проверкой файлов
- **Именование артефактов** - по номеру сборки вместо суффикса

### Исправлено
- **Проверка автора плагина** в compile.sh - корректная обработка PROJECT_AUTHOR
- **Обработка merge-коммитов** в CI - улучшенное определение целевой ветки
- **Права доступа** к скриптам и hooks
- **Кэширование в CI** - ускорение сборок через кэш истории

### Технические улучшения
- **Валидация согласованности версий** через `python3 update_version.py validate`
- **Автоматическое обновление git информации** в pre-commit hook
- **Расшифровка номеров сборок** - анализ структуры сборки
- **Статистика по веткам** - отслеживание количества сборок по типам веток

## Известные проблемы
- **Project Automation Action отключен** - временно не работает из-за проблем с разрешениями GitHub Projects
- **Требуется ручная настройка hooks** при первом использовании (`./setup_hooks.sh`)

## [Unreleased]
### Added
- Полная система шаблонов issues (8 категорий)
- Автоматическая ретроактивная проверка существующих issues/PR
- Git commit информация в version.inc
- Поддержка автоматической нумерации снапшотов

### Changed
- Улучшена система автоматического назначения меток
- Переработана структура меток (type-, priority-, component-)
- Обновлена логика определения веток для merge-коммитов
- Улучшено распознавание PROJECT_AUTHOR в плагинах

### Fixed
- Исправление обработки merge-веток в CI/CD
- Корректное определение авторства плагинов
- Оптимизация работы с GitHub API

## [0.0.5] - 2025-09-20
### Added
- Поддержка SemVer с автоматическими снапшотами
- Система автоматического назначения меток
- GitHub Actions для CI/CD
- Интеграция с GitHub Projects

### Changed
- Обновлена структура проекта
- Улучшена система версионирования
- Оптимизированы скрипты сборки

### Fixed
- Баги компиляции плагинов
- Проблемы с путями в config.sh
- Обработка ошибок в скриптах

## [0.0.4] - 2025-09-07
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

## Версия 0.0.3
**Дата:** 16 сентября 2025
**Тип релиза:** Патч (bug fixes и улучшения)

### 🚀 Новые возможности
- **Автоматическое назначение меток:** Улучшенный алгоритм анализа issue/PR с созданием детальных summary
- **Версионирование:** Добавлена поддержка нумерованных снапшотов (SNAPSHOT.N)
- **Логирование:** Детальные отчеты о сборке в GitHub Actions

### 🐛 Исправления ошибок
- **Версионный файл:** Исправлены числовые значения версий (0.1.0 → 0.0.3)
- **Метки проекта:** Исправлено добавление в проекты организации NightMira
- **Обработка ошибок:** Улучшена обработка отсутствующих меток и конфигураций

### 🔧 Технические улучшения
- **Скрипты:** Упрощенные регулярные выражения для чтения defines
- **Безопасное обновление:** Добавлена функция `safe_update_define`
- **Валидация:** Проверка существования меток перед назначением
- **Документация:** Детальные summary в workflow steps

### ⚠️ Известные проблемы
- **Сборка в main ветке:** Workflow `build.yml` завершается с ошибкой в main ветке
- **Автоматические метки:** Система создает новые метки вместо использования существующих
- **Ошибки в summary:** Некорректные отчеты в некоторых workflow steps
- **Нумерация снапшотов:** Требуется удаление нумерации для снапшотов (должны быть только SNAPSHOT)
- **Шаблоны issues:** Требуется переписывание шаблонов для корректной работы
- **Автоматизация проектов:** Добавляет элементы в проект, но в summary сообщает о неудаче
- **Обнаружение автора:** Сборка не видит `PROJECT_AUTHOR` вместо `PLUGIN_AUTHOR` в плагинах
- **Сборка PR:** Build system не настроена для работы с merge-ветками при Pull Requests

### 📊 Статистика изменений
- **Файлов изменено:** 8
- **Добавлено строк:** 257
- **Удалено строк:** 153
- **Нет кардинальных изменений**

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