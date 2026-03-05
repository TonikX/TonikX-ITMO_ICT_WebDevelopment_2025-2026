import {createApp} from 'vue'
import {createPinia} from 'pinia'
import App from './App.vue'
import '@mdi/font/css/materialdesignicons.css'
import piniaPluginPersistedState from "pinia-plugin-persistedstate"

import 'vuetify/styles'
import {createVuetify} from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import router from "@/utils/router.js";
import axios from "axios";

const pinia = createPinia()
pinia.use(piniaPluginPersistedState)

const vuetify = createVuetify({
    components,
    directives,
    theme: {
        defaultTheme: 'light',
    },
})

axios.defaults.baseURL = 'http://localhost:8000'

createApp(App).use(pinia).use(router).use(vuetify).mount('#app')
