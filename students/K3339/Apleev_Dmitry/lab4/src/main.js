import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import App from './App.vue'
import { routes, setupRouterGuards } from './router'

const router = createRouter({
  history: createWebHistory(),
  routes
})

// подключаем защиту маршрутов
setupRouterGuards(router)

// базовая настройка vuetify
const vuetify = createVuetify({
  components,
  directives
})

createApp(App).use(router).use(vuetify).mount('#app')

