import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify'
import 'vuetify/styles';
import '@mdi/font/css/materialdesignicons.css';
import store from './store'

const app = createApp(App);

app.use(router);
app.use(vuetify);
app.use(store);
app.mount('#app');