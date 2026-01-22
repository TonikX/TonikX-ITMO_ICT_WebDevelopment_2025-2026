<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon
        @click="drawer = !drawer"
        v-if="auth.isAuthenticated"
      ></v-app-bar-nav-icon>
      <v-toolbar-title>
        <router-link to="/" class="text-white text-decoration-none"
          >Parks</router-link
        >
      </v-toolbar-title>
      <v-spacer></v-spacer>

      <template v-if="auth.isAuthenticated">
        <v-btn :to="{ name: 'dashboard' }" icon title="Дашборд">
          <v-icon>mdi-view-dashboard</v-icon>
        </v-btn>
        <v-btn :to="{ name: 'UserSettings' }" icon title="Настройки">
          <v-icon>mdi-cog</v-icon>
        </v-btn>
        <v-btn @click="handleLogout" icon title="Выход">
          <v-icon>mdi-logout</v-icon>
        </v-btn>
      </template>
      <template v-else>
        <v-btn :to="{ name: 'login' }" variant="text" class="text-white">
          <v-icon left>mdi-login</v-icon>
          Войти
        </v-btn>
        <v-btn
          :to="{ name: 'register' }"
          variant="outlined"
          color="white"
          class="ml-2"
        >
          Регистрация
        </v-btn>
      </template>
    </v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      app
      temporary
      v-if="auth.isAuthenticated"
    >
      <v-list density="compact" nav>
        <v-list-item
          :to="{ name: 'home' }"
          prepend-icon="mdi-home"
          title="Главная"
        ></v-list-item>
        <v-list-item
          :to="{ name: 'dashboard' }"
          prepend-icon="mdi-view-dashboard"
          title="Дашборд"
        ></v-list-item>
        <v-list-item
          :to="{ name: 'object-create' }"
          prepend-icon="mdi-plus-circle"
          title="Создать объект"
        ></v-list-item>
        <v-divider></v-divider>
        <v-list-item
          :to="{ name: 'UserSettings' }"
          prepend-icon="mdi-cog"
          title="Настройки"
        ></v-list-item>
        <v-list-item
          @click="handleLogout"
          prepend-icon="mdi-logout"
          title="Выход"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-container fluid class="pa-0">
        <router-view />
      </v-container>
    </v-main>

    <v-footer app class="justify-center" color="grey-lighten-4">
      <span class="text-caption text-grey-darken-2">
        {{ new Date().getFullYear() }} — Parks laboratory work
      </span>
    </v-footer>
  </v-app>
</template>

<script setup>
import { ref } from "vue";
import { useAuthStore } from "@/store/auth";
import { useRouter } from "vue-router";

const drawer = ref(false);
const auth = useAuthStore();
const router = useRouter();

const handleLogout = async () => {
  try {
    await auth.logout();
    router.push("/login");
  } catch (error) {
    console.error("Ошибка при выходе:", error);
  }
};
</script>

<style>
body {
  margin: 0;
  padding: 0;
}

.v-application {
  font-family: "Roboto", sans-serif;
}

.text-decoration-none {
  text-decoration: none;
}
</style>
