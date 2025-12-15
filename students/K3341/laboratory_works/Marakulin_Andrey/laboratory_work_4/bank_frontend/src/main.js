import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// 1. Импорт Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'

// 2. Инициализация Vuetify
const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
  },
})

// 3. Создание приложения и использование маршрутизатора и Vuetify
createApp(App)
  .use(router)
  .use(vuetify)
  .mount('#app')