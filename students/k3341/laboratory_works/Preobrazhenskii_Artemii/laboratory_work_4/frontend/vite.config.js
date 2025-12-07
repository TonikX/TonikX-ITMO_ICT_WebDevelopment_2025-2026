import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: true,
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://host.docker.internal:8082',
        changeOrigin: true,
      },
      '/media': {
        target: 'http://host.docker.internal:8080', // nginx, который раздаёт media
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/media/, '/media') // оставляем путь без изменений
      }
    }
  }
})