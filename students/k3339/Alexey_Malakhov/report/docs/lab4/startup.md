## Запуск фронтенд приложения

### Предварительные требования

- Node.js версии 16 или выше
- npm или yarn
- Бэкенд API должен работать на `http://localhost:8000`

### Инструкции по запуску

#### 1. Переход в директорию фронтенда

```bash
cd students/k3339/Alexey_Malakhov/lab_4/frontend
```

#### 2. Установка зависимостей

```bash
npm install
```

или если используете yarn:

```bash
yarn install
```

#### 3. Запуск в режиме разработки

```bash
npm run dev
```

или

```bash
yarn dev
```

После запуска приложение будет доступно по адресу: [http://localhost:5173/](http://localhost:5173/)

**Примечание:** Vite будет отслеживать изменения в файлах и автоматически перезагружать приложение (Hot Module Replacement).

#### 4. Сборка для продакшена

```bash
npm run build
```

или

```bash
yarn build
```

Скомпилированные файлы будут находиться в папке `dist/`.

#### 5. Предпросмотр собранного приложения

```bash
npm run preview
```

или

```bash
yarn preview
```

---

## Полный процесс запуска всего проекта

Если вы хотите запустить и бэкенд, и фронтенд одновременно:

### Терминал 1: Запуск бэкенда

```bash
cd students/k3339/Alexey_Malakhov/lab_3/
sudo docker compose up -d                     # запуск контейнера с postgresql
cd backend
python -m venv .venv                          # создание виртуального окружения
source .venv/bin/activate                     # активация виртуального окружения
pip install -r requirements.txt               # установка зависимостей
uvicorn src.main:app --port 8000 --reload     # запуск веб-сервера
```

### Терминал 2: Запуск фронтенда

```bash
cd students/k3339/Alexey_Malakhov/lab_4/frontend
npm install
npm run dev
```

После запуска обоих приложений:

- **Фронтенд** будет доступен по адресу: [http://localhost:5173/](http://localhost:5173/)
- **Бэкенд API** будет доступен по адресу: [http://localhost:8000/](http://localhost:8000/)
- **Документация API (Swagger)** будет доступна по адресу: [http://localhost:8000/docs](http://localhost:8000/docs)
