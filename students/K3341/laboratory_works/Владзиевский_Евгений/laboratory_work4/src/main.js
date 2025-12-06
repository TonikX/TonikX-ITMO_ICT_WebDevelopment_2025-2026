import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

import App from './App.vue'
import router from './router'
import './style.css'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#0058e6',
          secondary: '#14213d',
          accent: '#fca311',
          surface: '#f7f7fb',
        },
      },
    },
  },
})

createApp(App).use(router).use(vuetify).mount('#app')
