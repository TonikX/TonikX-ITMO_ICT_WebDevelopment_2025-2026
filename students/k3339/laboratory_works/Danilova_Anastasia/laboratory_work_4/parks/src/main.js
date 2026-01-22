import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import vuetify from "./plugins/vuetify";
import { useAuthStore } from "@/store/auth";

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(vuetify);

const authStore = useAuthStore();
authStore.fetchUser().finally(() => {
  app.use(router);
  app.mount("#app");
});
