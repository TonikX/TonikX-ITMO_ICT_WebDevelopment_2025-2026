<template>
  <v-app>
    <v-app-bar v-if="authStore.isAuthenticated" color="primary" prominent>
      <v-app-bar-title>
        <v-icon icon="mdi-school" class="mr-2"></v-icon>
        Система управления колледжем
      </v-app-bar-title>

      <template v-slot:append>
        <v-btn variant="text" @click="router.push('/')">
          <v-icon icon="mdi-home" class="mr-1"></v-icon>
          Главная
        </v-btn>
        <v-btn variant="text" @click="router.push('/groups')">
          <v-icon icon="mdi-account-group" class="mr-1"></v-icon>
          Группы
        </v-btn>
        <v-btn variant="text" @click="router.push('/students')">
          <v-icon icon="mdi-account-school" class="mr-1"></v-icon>
          Студенты
        </v-btn>
        <v-btn variant="text" @click="router.push('/teachers')">
          <v-icon icon="mdi-account-tie" class="mr-1"></v-icon>
          Преподаватели
        </v-btn>
        <v-btn variant="text" @click="router.push('/schedule')">
          <v-icon icon="mdi-calendar-clock" class="mr-1"></v-icon>
          Расписание
        </v-btn>
        <v-btn variant="text" @click="router.push('/grades')">
          <v-icon icon="mdi-chart-bar" class="mr-1"></v-icon>
          Оценки
        </v-btn>

        <v-menu>
          <template v-slot:activator="{ props }">
            <v-btn icon v-bind="props">
              <v-icon icon="mdi-account-circle"></v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item>
              <v-list-item-title>{{ authStore.user?.username }}</v-list-item-title>
            </v-list-item>
            <v-divider></v-divider>
            <v-list-item @click="handleLogout">
              <v-list-item-title>
                <v-icon icon="mdi-logout" class="mr-2"></v-icon>
                Выход
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </template>
    </v-app-bar>

    <v-main>
      <RouterView />
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterView, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

onMounted(async () => {
  await authStore.loadUser()
})

async function handleLogout() {
  await authStore.logout()
  router.push('/login')
}
</script>
