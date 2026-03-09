import { createApp } from 'vue';
import App from './App.vue';
import router from "./router";
import './assets/main.css';

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import * as icons from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css'

const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    icons,
  }
})

const app = createApp(App);
app.use(router);
app.use(vuetify);
app.mount('#app');
