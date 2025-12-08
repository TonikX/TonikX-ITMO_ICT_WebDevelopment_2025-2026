import {createApp} from 'vue'
import {createPinia} from 'pinia'
import App from './App.vue'
import './styles/main.scss'
import router from './router'
import {uiStore} from "@/stores/ui.js";
import Icon from '@/components/ui/Icon.vue'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.component('Icon', Icon)
const ui = uiStore()
ui.initTheme()
app.mount('#app')
