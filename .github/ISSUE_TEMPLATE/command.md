# Сценарии использования
## Сценарий 1: Разработка новой функции
```bash
# 1. Создание задачи
gh issue create --title "✨ Добавить систему скилов" --label "feature,priority-medium" --milestone "v1.3.0"

# 2. Создание ветки
git checkout -b feature/skills-system dev

# 3. Разработка и коммиты
git commit -m "Добавление базовой системы скилов #789"

# 4. Создание PR
gh pr create --base dev --head feature/skills-system --label "feature" --reviewer "team-lead"

# 5. После ревью - мерж
gh pr merge 789 --squash --delete-branch
```
## Сценарий 2: Исправление критического бага
```bash
# 1. Создание hotfix ветки от main
git checkout -b hotfix/compile-error main

# 2. Экстренный фикс
git commit -m "🚨 Исправление segmentation fault #999"

# 3. Создание PR в main и dev
gh pr create --base main --head hotfix/compile-error --label "bug,priority-critical"
gh pr create --base dev --head hotfix/compile-error --label "bug,priority-critical"

# 4. Быстрый мерж после тестирования
gh pr merge 999 --squash --delete-branch
```
## Сценарий 3: Подготовка релиза
```bash
# 1. Создание release ветки
git checkout -b release/v1.2.0 dev

# 2. Финальное тестирование
gh workflow run "Build and Test" --ref release/v1.2.0

# 3. Мерж в main
git checkout main
git merge release/v1.2.0
git tag v1.2.0
git push origin main v1.2.0

# 4. Мерж обратно в dev
git checkout dev
git merge release/v1.2.0
git push origin dev
```
# 💻 Команды и примеры
## Управление issues
```bash
# Создание issue с метками
gh issue create --title "🐛 Баг компиляции" --label "bug,priority-high" --body "Ошибка в plugin_admin.sma"

# Просмотр issues по меткам
gh issue list --label "bug,priority-critical" --state open

# Назначение вехи
gh issue edit 123 --milestone "v1.2.0-release"
```
## Управление ветками
```bash
# Создание feature ветки
git checkout -b feature/new-plugin dev

# Создание hotfix ветки
git checkout -b hotfix/urgent-fix main

# Удаление merged веток
git branch --merged dev | grep -v "dev" | xargs git branch -d
```
## Управление релизами
```bash
# Создание релиза
gh release create v1.2.0 --title "Релиз v1.2.0" --notes "Добавлена система телепортации"

# Просмотр релизов
gh release list

# Откат релиза
git revert <commit-hash>
git push origin main
```
## Автоматизация
```bash
# Запуск workflow вручную
gh workflow run "Build and Test" --ref dev

# Просмотр логов workflow
gh run list --workflow=build.yml
gh run view <run-id> --log

# Синхронизация меток
gh workflow run "Sync Labels" --ref main
```
# 📊 Мониторинг и аналитика
## Отслеживание прогресса
``` bash
# Прогресс по вехам
gh milestone list --state open

# Статистика по меткам
gh issue list --label "bug" --state open | wc -l
gh issue list --label "feature" --state closed | wc -l

# Эффективность разработки
gh issue list --assignee @me --state closed --json closedAt,createdAt
```
## Дашборд проекта
```bash
# Обзор открытых issues
gh issue list --state open --limit 10

# Просмотр recent PR
gh pr list --state open --limit 5

# Статус workflows
gh run list --limit 5
```