/// <reference types="vite/client" />

// Интерфейс для переменных окружения, доступных через import.meta.env
interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string // Базовый URL API сервера
  // add more env variables as needed (можно добавить больше переменных окружения по необходимости)
}

// Интерфейс для расширения глобального объекта ImportMeta
interface ImportMeta {
  readonly env: ImportMetaEnv // Объект с переменными окружения
}

