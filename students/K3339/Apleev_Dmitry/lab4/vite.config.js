import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'

// простая конфигурация vite для vue 3 и vuetify

export default defineConfig({
  plugins: [
    vue(),
    vuetify({
      autoImport: true
    })
  ],
  server: {
    port: 5173,
    // проксируем запросы к api и auth на django, чтобы не было cors
    proxy: {
      '/api': {
        target: 'http://localhost:8003',
        changeOrigin: true
      },
      '/auth': {
        target: 'http://localhost:8003',
        changeOrigin: true
      }
    }
  }
})

