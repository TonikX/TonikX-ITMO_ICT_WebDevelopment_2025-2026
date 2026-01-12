// Импортируем стили Vuetify
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css' // Иконки Material Design

// Импортируем компоненты Vuetify
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// Настройка темы
const myCustomLightTheme = {
  dark: false,
  colors: {
    background: '#FFFFFF',
    surface: '#FFFFFF',
    primary: '#1976D2',
    'primary-darken-1': '#1565C0',
    secondary: '#424242',
    'secondary-darken-1': '#212121',
    error: '#D32F2F',
    info: '#2196F3',
    success: '#4CAF50',
    warning: '#FB8C00',
    fuel: '#FF9800', // Кастомный цвет для темы АЗС
    fuelDark: '#F57C00',
  }
}

// Создаем экземпляр Vuetify
const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'myCustomLightTheme',
    themes: {
      myCustomLightTheme,
    }
  },
  defaults: {
    VBtn: {
      color: 'primary',
      variant: 'flat',
      rounded: 'md',
    },
    VTextField: {
      variant: 'outlined',
      density: 'comfortable',
    },
    VSelect: {
      variant: 'outlined',
      density: 'comfortable',
    },
    VCard: {
      elevation: 2,
      rounded: 'lg',
    },
    VTable: {
      density: 'comfortable',
    }
  }
})

export default vuetify