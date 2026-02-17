# Публикация документации на GitHub Pages

## Способ 1: Автоматическая публикация через mkdocs gh-deploy

Самый простой способ - использовать встроенную команду MkDocs:

```bash
cd lab3/docs
source ../venv/bin/activate
mkdocs gh-deploy
```

Эта команда:
1. Соберет документацию
2. Создаст ветку `gh-pages` (если её нет)
3. Загрузит документацию на GitHub
4. Активирует GitHub Pages в настройках репозитория

После выполнения документация будет доступна по адресу:
`https://Cherepnya-Yaroslav.github.io/web-itmo/`

## Способ 2: GitHub Actions (автоматическая публикация при каждом коммите)

Создайте файл `.github/workflows/docs.yml` в корне репозитория для автоматической публикации.

## Настройка GitHub Pages

1. Перейдите в настройки репозитория: `Settings` → `Pages`
2. В разделе "Source" выберите:
   - Branch: `gh-pages`
   - Folder: `/ (root)`
3. Сохраните изменения

## Локальный просмотр перед публикацией

```bash
cd lab3/docs
source ../venv/bin/activate
mkdocs serve
```

Документация будет доступна по адресу: `http://127.0.0.1:8000`
