# Установка и настройка

## Требования

- Node.js 18+ 
- npm или yarn
- Работающий бэкенд (laboratory_work_3)

## Установка

### 1. Клонирование репозитория

```bash
cd laboratory_work_4/frontend
```

### 2. Установка зависимостей

```bash
npm install
```

### 3. Настройка переменных окружения

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Отредактируйте `.env`:

```env
VITE_API_URL=http://localhost:8000
```

### 4. Запуск приложения

#### Режим разработки

```bash
npm run dev
```

Приложение будет доступно по адресу [http://localhost:3000](http://localhost:3000)

#### Сборка для продакшена

```bash
npm run build
```

Собранные файлы будут в папке `dist/`

#### Предпросмотр продакшен-сборки

```bash
npm run preview
```

## Настройка бэкенда

Убедитесь, что бэкенд из лабораторной работы №3 запущен и доступен.

### CORS

Бэкенд уже настроен для работы с CORS. В файле `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

!!! warning "Предупреждение"
    В продакшене рекомендуется указать конкретные origins вместо `"*"`.

## Структура файлов конфигурации

| Файл | Описание |
|------|----------|
| `vite.config.ts` | Конфигурация Vite |
| `tailwind.config.js` | Конфигурация Tailwind CSS |
| `tsconfig.json` | Конфигурация TypeScript |
| `postcss.config.js` | Конфигурация PostCSS |
| `.env` | Переменные окружения |

## Устранение проблем

### CORS ошибки

Убедитесь что:
1. Бэкенд запущен
2. URL в `VITE_API_URL` правильный
3. CORS настроен в бэкенде

### Ошибки TypeScript

```bash
# Проверка типов
npx tsc --noEmit
```

### Проблемы с зависимостями

```bash
# Удалите node_modules и переустановите
rm -rf node_modules package-lock.json
npm install
```
