# Запуск приложения

## Требования

- Node.js версии 18 или выше
- npm или yarn

## Установка зависимостей

```bash
npm install
```

## Запуск в режиме разработки

```bash
npm run dev
```

Приложение будет доступно по адресу `http://localhost:3001` (или другому порту, указанному в консоли).

## Сборка для production

```bash
npm run build
```

Собранные файлы будут находиться в директории `dist/`.

## Предпросмотр production сборки

```bash
npm run preview
```

## Настройка API

По умолчанию приложение подключается к API по адресу `http://localhost:8080`. 

Для изменения адреса API отредактируйте файл `src/api/client.js`:

```javascript
const api = axios.create({
  baseURL: 'http://your-api-url:8080',
  // ...
});
```

