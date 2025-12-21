<script setup>
import { useAuthStore } from './stores/auth'
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()

const isAuthed = computed(() => auth.isAuthenticated)
const userName = computed(() => auth.user?.username || 'Гость')

const logout = async () => {
  await auth.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <v-app>
    <v-app-bar flat color="primary" density="comfortable">
      <v-app-bar-title class="font-weight-bold text-white">LR4 · Vue + DRF</v-app-bar-title>
      <v-spacer />
      <v-btn variant="text" color="white" :to="{ name: 'dashboard' }">Дашборд</v-btn>
      <v-menu location="bottom" open-on-hover v-if="isAuthed">
        <template #activator="{ props }">
          <v-btn variant="text" color="white" v-bind="props">Справочники</v-btn>
        </template>
        <v-list>
          <v-list-item :to="{ name: 'subjects' }">Предметы</v-list-item>
          <v-list-item :to="{ name: 'classrooms' }">Кабинеты</v-list-item>
          <v-list-item :to="{ name: 'classes' }">Классы</v-list-item>
          <v-list-item :to="{ name: 'teachers' }">Учителя</v-list-item>
          <v-list-item :to="{ name: 'students' }">Ученики</v-list-item>
        </v-list>
      </v-menu>
      <v-menu location="bottom" open-on-hover v-if="isAuthed">
        <template #activator="{ props }">
          <v-btn variant="text" color="white" v-bind="props">Учебный процесс</v-btn>
        </template>
        <v-list>
          <v-list-item :to="{ name: 'schedule' }">Расписание</v-list-item>
          <v-list-item :to="{ name: 'grades' }">Оценки</v-list-item>
        </v-list>
      </v-menu>
      <v-btn variant="text" color="white" :to="{ name: 'profile' }" v-if="isAuthed">Профиль</v-btn>
      <v-btn variant="text" color="white" :to="{ name: 'login' }" v-if="!isAuthed">Войти</v-btn>
      <v-btn variant="text" color="white" :to="{ name: 'register' }" v-if="!isAuthed">Регистрация</v-btn>
      <v-menu v-if="isAuthed" location="bottom end">
        <template #activator="{ props }">
          <v-btn variant="tonal" color="white" v-bind="props" class="ml-2">{{ userName }}</v-btn>
        </template>
        <v-list>
          <v-list-item @click="logout">
            <v-list-item-title>Выйти</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-main>
      <v-container class="py-6" fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>
