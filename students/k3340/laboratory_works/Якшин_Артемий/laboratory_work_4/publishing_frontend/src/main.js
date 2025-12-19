import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'publishingTheme',
    themes: {
      publishingTheme: {
        dark: false,
        colors: {
          primary: '#2D3E50',
          secondary: '#C9A959',
          accent: '#8B4513',
          background: '#F5F2EB',
          surface: '#FFFFFF',
          error: '#B71C1C',
          info: '#1565C0',
          success: '#2E7D32',
          warning: '#F57F17',
          'on-background': '#2D3E50',
          'on-surface': '#2D3E50',
        }
      },
      darkTheme: {
        dark: true,
        colors: {
          primary: '#C9A959',
          secondary: '#2D3E50',
          accent: '#D4A574',
          background: '#1A1A2E',
          surface: '#252540',
          error: '#CF6679',
          info: '#64B5F6',
          success: '#81C784',
          warning: '#FFD54F',
          'on-background': '#E8E6E3',
          'on-surface': '#E8E6E3',
        }
      }
    }
  },
  defaults: {
    VBtn: {
      variant: 'elevated',
      rounded: 'lg',
    },
    VCard: {
      rounded: 'lg',
      elevation: 2,
    },
    VTextField: {
      variant: 'outlined',
      density: 'comfortable',
    },
    VSelect: {
      variant: 'outlined',
      density: 'comfortable',
    },
  }
})

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(vuetify)

app.mount('#app')

