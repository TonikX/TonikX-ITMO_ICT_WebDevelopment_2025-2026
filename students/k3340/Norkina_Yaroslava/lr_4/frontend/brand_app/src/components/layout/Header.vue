<template>
  <v-app-bar :elevation="2" color="background">
    <v-container>
      <v-row align="center" no-gutters>
        <!-- Логотип -->
        <v-col cols="auto">
          <router-link to="/" class="text-decoration-none">
            <v-toolbar-title class="text-h5 font-weight-bold">
              <span class="text-primary">Brand</span>
              <span class="text-secondary">Pro</span>
            </v-toolbar-title>
          </router-link>
        </v-col>

        <!-- Навигация -->
        <v-col cols="auto" class="ml-6">
          <v-tabs v-model="tab" color="primary">
            <v-tab to="/" value="home">Главная</v-tab>
            <v-tab to="/services" value="services">Услуги</v-tab>
            <v-tab v-if="authStore.isAuthenticated" value="dashboard">Личный кабинет</v-tab>
          </v-tabs>
        </v-col>

        <v-spacer></v-spacer>

        <!-- Правая часть -->
        <v-col cols="auto">
          <v-btn-group v-if="!authStore.isAuthenticated">
            <v-btn to="/login" variant="outlined" color="primary">
              <v-icon start icon="mdi-login"></v-icon>
              Войти
            </v-btn>
            <v-btn to="/register" color="primary">
              <v-icon start icon="mdi-account-plus"></v-icon>
              Регистрация
            </v-btn>
          </v-btn-group>

          <!-- Для авторизованных -->
          <div v-else class="d-flex align-center">
            <v-menu location="bottom">
              <template v-slot:activator="{ props }">
                <v-btn v-bind="props" variant="text" color="primary" class="ml-2">
                  <v-avatar size="36" color="primary" class="mr-2">
                    <span class="text-white">{{ userInitials }}</span>
                  </v-avatar>
                  <v-chip v-if="isAdmin" size="x-small" color="secondary" class="mr-1">
                    Админ
                  </v-chip>

                  {{ authStore.userName }}

                  <v-icon end icon="mdi-chevron-down"></v-icon>
                </v-btn>
              </template>
              <v-list>
                <v-list-item to="/profile" prepend-icon="mdi-account">
                  <v-list-item-title>Профиль</v-list-item-title>
                </v-list-item>
                <v-list-item to="/orders" prepend-icon="mdi-clipboard-list">
                  <v-list-item-title>Мои заявки</v-list-item-title>
                </v-list-item>
                <v-divider></v-divider>
                <v-list-item
                    @click="logout"
                    prepend-icon="mdi-logout"
                    color="error"
                >
                  <v-list-item-title>Выйти</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </v-app-bar>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useAuthStore } from '../../store/modules/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()
const tab = ref(null)

// Получаем инициалы для аватара
const userInitials = computed(() => {
  if (!authStore.user) return '?'
  const name = authStore.user.first_name || authStore.user.email
  return name.charAt(0).toUpperCase()
})

const logout = async () => {
  await authStore.logout()
  router.push('/')
}
</script>