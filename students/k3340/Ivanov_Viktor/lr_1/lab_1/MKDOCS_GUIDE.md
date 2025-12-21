# руководство по использованию MkDocs

## что такое MkDocs?

MkDocs - это быстрый, простой и очаровательный генератор статической документации, созданный для проектов. он создает документацию из файлов Markdown.

## быстрый старт

**1. активация виртуального окружения**
```bash
cd /Users/viktorivanov/Studying/web/lab_1
source venv/bin/activate
```

**2. запуск локального сервера**
```bash
mkdocs serve
```

**3. открытие в браузере**
перейдите по адресу: http://127.0.0.1:8000

## структура проекта

```
lab_1/
├── mkdocs.yml          # конфигурация MkDocs
├── docs/               # папка с документацией
│   ├── index.md        # главная страница
│   ├── about.md        # о проекте
│   └── ex_1/           # папки с заданиями
│       └── index.md
├── site/               # собранная документация (создается автоматически)
└── venv/               # виртуальное окружение
```

## основные команды

**запуск сервера разработки**
```bash
mkdocs serve
```
запускает локальный сервер, автоматически обновляет при изменениях, доступен по адресу http://127.0.0.1:8000.

**сборка статической документации**
```bash
mkdocs build
```
создает статические файлы в папке `site/`, можно загрузить на любой веб-сервер.

**очистка и сборка**
```bash
mkdocs build --clean
```
удаляет старые файлы перед сборкой.

**публикация на GitHub Pages**
```bash
mkdocs gh-deploy
```
публикует документацию на GitHub Pages, требует настройки репозитория.

## редактирование документации

**добавление новой страницы**
1. создайте файл `.md` в папке `docs/`
2. добавьте его в навигацию в `mkdocs.yml`:
```yaml
nav:
  - Главная: index.md
  - Новая страница: new-page.md
```

**редактирование существующих страниц**
откройте файл `.md` в папке `docs/`, используйте Markdown синтаксис, сохраните файл, сервер автоматически обновится.

**структура Markdown файла**
```markdown
# заголовок 1
## заголовок 2
### заголовок 3

**жирный текст**
*курсив*

`код`

```python
# блок кода
print("Hello, World!")
```

- список
- элемент 1
- элемент 2

[ссылка](https://example.com)
```

## настройка темы

**Material тема**
в файле `mkdocs.yml` настроена Material тема с темной/светлой темой, поиском, навигацией, подсветкой кода.

**изменение цветовой схемы**
```yaml
theme:
  name: material
  palette:
    - scheme: default
      primary: indigo  # цвет темы
      accent: indigo   # акцентный цвет
```

## конфигурация

**основные настройки в mkdocs.yml**
```yaml
site_name: название сайта
site_description: описание
site_author: автор
site_url: https://example.com

theme:
  name: material
  # настройки темы

nav:
  - Главная: index.md
  # структура навигации

plugins:
  - search
  # плагины

markdown_extensions:
  - codehilite
  # расширения markdown
```

## полезные расширения Markdown

**Material тема поддерживает**
admonitions - блоки с предупреждениями, code highlighting - подсветка синтаксиса, tables - таблицы, math - математические формулы, emoji - эмодзи, tabs - вкладки.

**пример admonition**
```markdown
!!! note "заметка"
    это важная информация.

!!! warning "предупреждение"
    будьте осторожны!

!!! tip "совет"
    полезный совет.
```

## устранение неполадок

**проблема: "command not found: mkdocs"**
```bash
# активируйте виртуальное окружение
source venv/bin/activate

# проверьте установку
pip list | grep mkdocs
```

**проблема: "Config value error"**
```bash
# проверьте синтаксис YAML
mkdocs config

# проверьте наличие всех файлов
mkdocs build --verbose
```

**проблема: "Port already in use"**
```bash
# используйте другой порт
mkdocs serve --dev-addr 127.0.0.1:8001
```

## публикация

**GitHub Pages**
1. создайте репозиторий на GitHub
2. обновите настройки в `mkdocs.yml`:
   ```yaml
   repo_name: username/repository-name
   repo_url: https://github.com/username/repository-name
   ```
3. запустите:
   ```bash
   mkdocs gh-deploy
   ```

**другие хостинги**
1. соберите документацию:
   ```bash
   mkdocs build
   ```
2. загрузите содержимое папки `site/` на хостинг

## дополнительные ресурсы

официальная документация MkDocs, Material for MkDocs, Markdown Guide, YAML Tutorial.

это руководство поможет вам эффективно использовать MkDocs для создания красивой документации.