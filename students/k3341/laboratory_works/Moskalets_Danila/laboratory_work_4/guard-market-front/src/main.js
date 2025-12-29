import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import pinia from './stores'
import vuetify from './plugins/vuetify'
import './assets/main.css'

const app = createApp(App)

app.use(router)
app.use(pinia)
app.use(vuetify)

app.mount('#app')