import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

export default defineConfig({
    plugins: [vue()],
    server: {
        host: true,
        port: 3000,
        proxy: {
            '/api': {
                target: 'http://127.0.0.1:8000',  // ← твой локальный бэкенд Django
                changeOrigin: true,
            },
            '/media': {
                target: 'http://127.0.0.1:8000',  // ← тоже на Django
                changeOrigin: true,
            }
        }
    }
})