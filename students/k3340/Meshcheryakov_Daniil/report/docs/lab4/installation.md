# Установка и запуск фронтенда

Пошаговая инструкция по установке и запуску клиентской части приложения.

## Предварительные требования

- **Node.js** 18.x или выше
- **npm** 9.x или выше (входит в Node.js)
- **Backend API** должен быть запущен на `http://localhost:8000`

### Проверка установки Node.js

```bash
node --version
# v18.17.0 или выше

npm --version
# 9.6.7 или выше
```

### Установка Node.js

Если Node.js не установлен:

**Windows:**
- Скачайте с [nodejs.org](https://nodejs.org/)
- Установите LTS версию

**Linux (Ubuntu/Debian):**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**macOS:**
```bash
brew install node
```

---

## Установка проекта

### Шаг 1: Переход в папку фронтенда

```bash
cd students/k3340/Meshcheryakov_Daniil/lab3/frontend
```

### Шаг 2: Установка зависимостей

```bash
npm install
```

**Вывод:**
```
added 245 packages, and audited 246 packages in 15s

45 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
```

**Основные зависимости:**
```json
{
  "dependencies": {
    "vue": "^3.4.0",
    "vue-router": "^4.2.5",
    "vuetify": "^3.5.0",
    "pinia": "^2.1.7",
    "axios": "^1.6.0",
    "dayjs": "^1.11.10",
    "@mdi/font": "^7.4.47"
  }
}
```

**Dev зависимости:**
```json
{
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "vite": "^5.0.8",
    "vite-plugin-vuetify": "^2.0.0"
  }
}
```

---

## Конфигурация

### Проверка vite.config.js

Файл `vite.config.js` должен содержать:

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'
import path from 'path'

export default defineConfig({
  plugins: [
    vue(),
    vuetify({ autoImport: true })
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
```

### Проверка package.json

```json
{
  "name": "reading-room-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }
}
```

---

## Запуск Development Server

### Команда запуска

```bash
npm run dev
```

**Вывод:**
```
VITE v5.0.8  ready in 432 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

### Открытие в браузере

Откройте:
```
http://localhost:3000
```

Вы должны увидеть страницу входа в систему! ✅

---

## Проверка работоспособности

### 1. Backend должен быть запущен

В другом терминале:

```bash
cd students/k3340/Meshcheryakov_Daniil/lab3
python manage.py runserver
```

### 2. Проверка подключения к API

Откройте консоль браузера (F12) и убедитесь что нет ошибок CORS.

### 3. Тестовый вход

Используйте учетные данные суперпользователя:
```
Username: admin
Password: admin123
```

Если вход успешен → всё работает! 🎉

---

## Структура проекта после установки

```
frontend/
├── node_modules/         # Установленные пакеты (не коммитятся)
├── public/              # Статические файлы
├── src/                 # Исходный код
│   ├── assets/         # Изображения, стили
│   ├── components/     # Vue компоненты
│   ├── views/          # Страницы
│   ├── stores/         # Pinia stores
│   ├── services/       # API сервисы
│   ├── router/         # Маршруты
│   ├── plugins/        # Плагины (Vuetify)
│   ├── App.vue        # Корневой компонент
│   └── main.js        # Точка входа
├── index.html          # HTML шаблон
├── package.json        # Зависимости проекта
├── package-lock.json   # Lockfile зависимостей
└── vite.config.js      # Vite конфигурация
```

---

## Полезные команды

### Development

```bash
# Запуск dev сервера
npm run dev

# Запуск на конкретном порту
npm run dev -- --port 3001

# Открыть в сети (для тестирования на других устройствах)
npm run dev -- --host
```

### Build

```bash
# Production сборка
npm run build

# Вывод будет в папке dist/
# Сборка оптимизирована и минимизирована
```

### Preview

```bash
# Просмотр production сборки локально
npm run preview
```

### Обновление зависимостей

```bash
# Проверить устаревшие пакеты
npm outdated

# Обновить все пакеты
npm update

# Установить конкретную версию
npm install vue@latest
```

### Очистка

```bash
# Удалить node_modules и package-lock.json
rm -rf node_modules package-lock.json

# Переустановить зависимости
npm install
```

---

## Отладка (Debugging)

### Vue DevTools

Установите расширение для браузера:

**Chrome:**
[Vue.js devtools](https://chrome.google.com/webstore/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)

**Firefox:**
[Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)

**Использование:**
1. Откройте DevTools (F12)
2. Вкладка "Vue"
3. Просмотр компонентов, состояния, событий

### Vite Inspector

В режиме разработки:
- Наведите на элемент + Alt + Click
- Откроется исходный код компонента в редакторе

### Console Logging

```javascript
// В компоненте
console.log('Current user:', authStore.user)
console.log('Rooms:', rooms.value)
```

---

## Hot Module Replacement (HMR)

Vite поддерживает HMR "из коробки":

- ✅ Изменения в `.vue` файлах применяются мгновенно
- ✅ Состояние компонента сохраняется
- ✅ Не требуется перезагрузка страницы

**Пример:**
1. Откройте `src/views/Dashboard.vue`
2. Измените текст
3. Сохраните файл
4. Изменения применятся сразу в браузере

---

## Environment Variables

### Создание .env файла

Создайте файл `.env` в корне `frontend/`:

```env
VITE_API_BASE_URL=http://localhost:8000/api/
VITE_APP_TITLE=Читальный Зал
```

### Использование в коде

```javascript
// src/services/api.js
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

const api = axios.create({
  baseURL: API_BASE_URL
})
```

### Разные окружения

**Development** (`.env.development`):
```env
VITE_API_BASE_URL=http://localhost:8000/api/
```

**Production** (`.env.production`):
```env
VITE_API_BASE_URL=https://api.example.com/api/
```

---

## Возможные проблемы и решения

### ❌ Проблема: CORS errors

**Ошибка в консоли:**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Решение:**

1. Проверьте Django settings.py:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

2. Убедитесь что `corsheaders` в `INSTALLED_APPS` и `MIDDLEWARE`

---

### ❌ Проблема: Port already in use

**Ошибка:**
```
Port 3000 is already in use
```

**Решение 1 - Использовать другой порт:**
```bash
npm run dev -- --port 3001
```

**Решение 2 - Убить процесс:**

**Windows:**
```bash
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
lsof -ti:3000 | xargs kill
```

---

### ❌ Проблема: Module not found

**Ошибка:**
```
Error: Cannot find module '@/components/MyComponent.vue'
```

**Решение:**

1. Проверьте путь к файлу
2. Проверьте алиас `@` в `vite.config.js`:
```javascript
resolve: {
  alias: {
    '@': path.resolve(__dirname, 'src')
  }
}
```

---

### ❌ Проблема: Vuetify styles not loading

**Ошибка:** Компоненты выглядят "сломанными"

**Решение:**

1. Проверьте импорт в `main.js`:
```javascript
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
```

2. Переустановите зависимости:
```bash
npm install vuetify @mdi/font --force
```

---

### ❌ Проблема: API requests fail with 401

**Ошибка:** Все запросы возвращают 401 Unauthorized

**Решение:**

1. Проверьте что токен сохраняется:
```javascript
// В DevTools Console
console.log(localStorage.getItem('access_token'))
```

2. Проверьте Axios interceptor:
```javascript
// src/services/api.js
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

---

## Production Build

### Создание production сборки

```bash
npm run build
```

**Вывод:**
```
vite v5.0.8 building for production...
✓ 145 modules transformed.
dist/index.html                   0.45 kB │ gzip:  0.29 kB
dist/assets/index-abc123.js     142.15 kB │ gzip: 45.67 kB
dist/assets/index-def456.css     12.34 kB │ gzip:  3.21 kB
✓ built in 3.52s
```

### Структура dist/

```
dist/
├── index.html
├── assets/
│   ├── index-[hash].js
│   ├── index-[hash].css
│   └── [other assets]
└── favicon.ico
```

### Развертывание

**Статический хостинг (Netlify, Vercel, GitHub Pages):**

1. Загрузите содержимое `dist/` на хостинг
2. Настройте перенаправление для SPA:
```
/* /index.html 200
```

**Nginx:**

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/frontend/dist;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

---

## VS Code Extensions (Рекомендуемые)

Для улучшения опыта разработки:

1. **Volar** - Vue 3 language support
2. **ESLint** - Линтинг кода
3. **Prettier** - Форматирование кода
4. **Vue VSCode Snippets** - Сниппеты для Vue

---

## Следующие шаги

1. ✅ Фронтенд установлен и запущен
2. 📖 [Изучите компоненты](components.md)
3. 🛤️ [Изучите маршрутизацию](routing.md)
4. 🗄️ [Изучите state management](state.md)
5. 🔌 [Изучите API интеграцию](api-integration.md)

---

## Справка

**Frontend:** http://localhost:3000  
**Backend API:** http://localhost:8000/api/  
**Swagger UI:** http://localhost:8000/api/schema/swagger-ui/

**Студент:** Мещеряков Даниил  
**Группа:** K3340

