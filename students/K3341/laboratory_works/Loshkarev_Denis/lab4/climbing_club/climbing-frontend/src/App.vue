<template>
  <v-app class="app-root">
    <v-app-bar color="white" elevation="1" density="comfortable" class="pr-2">
      <div class="brand">
        <div class="brand-logo">АльпКлуб</div>
      </div>

      <v-divider vertical class="mx-3" />

      <v-btn
        v-if="isAuthed"
        variant="text"
        class="text-none"
        :to="{ name: 'dashboard' }"
      >
        Дашборд
      </v-btn>

      <v-spacer />

      <template v-if="isAuthed">
        <div class="nav-block">
          <v-btn variant="text" class="text-none" :to="{ name: 'mountains' }">Вершины</v-btn>
          <v-btn variant="text" class="text-none" :to="{ name: 'routes' }">Маршруты</v-btn>
          <v-btn variant="text" class="text-none" :to="{ name: 'clubs' }">Клубы</v-btn>
          <v-btn variant="text" class="text-none" :to="{ name: 'alpinists' }">Альпинисты</v-btn>
          <v-btn variant="text" class="text-none" :to="{ name: 'climbs' }">Восхождения</v-btn>
          <v-btn variant="text" class="text-none" :to="{ name: 'reports' }">Отчёты</v-btn>
        </div>

        <v-divider vertical class="mx-3" />

        <div class="auth-block">
          <div class="d-flex align-center ga-1 text-body-2 text-grey-darken-2 px-2">
            <v-icon icon="mdi-account-circle-outline" size="18" />
            <span>{{ auth.username }}</span>
          </div>

          <v-btn
            variant="text"
            class="text-none"
            :to="{ name: 'change-password' }"
          >
            Сменить пароль
          </v-btn>

          <v-btn
            variant="outlined"
            color="grey-darken-2"
            class="text-none"
            @click="onLogout"
          >
            Выйти
          </v-btn>
        </div>
      </template>

      <template v-else>
        <v-btn
          variant="outlined"
          color="grey-darken-2"
          class="text-none"
          :to="{ name: 'login' }"
        >
          Войти
        </v-btn>
      </template>
    </v-app-bar>

    <v-main class="app-main">
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const router = useRouter()
const auth = useAuthStore()

const isAuthed = computed(() => !!auth.token)

function onLogout() {
  auth.logout()
  router.push({ name: 'login' })
}
</script>