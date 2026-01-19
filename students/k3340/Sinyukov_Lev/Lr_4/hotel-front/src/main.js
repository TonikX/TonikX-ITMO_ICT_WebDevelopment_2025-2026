import { createApp } from "vue";
import App from "./App.vue";

import "vuetify/styles";
import "@mdi/font/css/materialdesignicons.css";

import { createPinia } from "pinia";
import router from "./router";

import vuetify from "./plugins/vuetify";

createApp(App)
  .use(createPinia())
  .use(router)
  .use(vuetify)
  .mount("#app");