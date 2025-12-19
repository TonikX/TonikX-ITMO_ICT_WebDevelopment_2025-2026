import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path, // Убрали замену, передаём путь как есть
      },
    },
    // Добавляем разрешенные хосты
    host: '0.0.0.0', // Разрешаем доступ с любого IP
    allowedHosts: ['miracle-love.online', 'miracle-love.ru', 'localhost'],
  },
})
