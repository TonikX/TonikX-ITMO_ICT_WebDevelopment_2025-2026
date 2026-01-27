import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './vuetify'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'
import api from './api'

const resizeObserverError = /ResizeObserver loop completed with undelivered notifications|ResizeObserver loop limit exceeded/
window.addEventListener('error', event => {
  if (resizeObserverError.test(event.message)) {
    event.stopImmediatePropagation()
    event.preventDefault()
  }
})

const app = createApp(App)

app.use(router)
app.use(store)
app.use(vuetify)
app.use(Toast, {
  position: 'top-right',
  timeout: 3000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: true,
  closeButton: 'button',
  icon: true,
  rtl: false
})

app.config.globalProperties.$api = api

app.mount('#app')