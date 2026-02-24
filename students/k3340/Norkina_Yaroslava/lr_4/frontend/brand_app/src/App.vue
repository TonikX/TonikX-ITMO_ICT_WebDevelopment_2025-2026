<template>
  <v-app>
    <!-- Шапка -->
    <v-app-bar color="background">
      <v-container>
        <v-row align="center">
          <!-- Логотип -->
          <v-col cols="auto">
            <router-link to="/" class="text-decoration-none">
              <v-toolbar-title class="text-h6 font-weight-bold">
                Лабораторная 4
              </v-toolbar-title>
            </router-link>
          </v-col>

          <!-- Навигация -->
          <v-col cols="auto" class="ml-6">
            <v-btn to="/" variant="text" color="primary" size="small">Главная</v-btn>

            <!-- КНОПКА УСЛУГ В ЗАВИСИМОСТИ ОТ РОЛИ -->
            <v-btn
                :to="isAdmin ? '/admin/services' : '/services'"
                variant="text"
                color="primary"
                size="small"
            >
              <span v-if="isAdmin">Админ: Услуги</span>
              <span v-else>Услуги</span>
            </v-btn>
          </v-col>

          <v-spacer></v-spacer>

          <!-- Кнопки входа/выхода -->
          <v-col cols="auto">
            <div v-if="!isAuthenticated">
              <v-btn to="/login" variant="outlined" color="primary" size="small" class="mr-2">Войти</v-btn>
              <v-btn to="/register" color="primary" size="small">Регистрация</v-btn>
            </div>

            <!-- Для авторизованных -->
            <div v-else class="d-flex align-center">
              <v-menu location="bottom">
                <template v-slot:activator="{ props }">
                  <v-btn v-bind="props" variant="text" color="primary" size="small">
                    <!-- Аватар -->
                    <v-avatar size="32" color="primary" class="mr-2">
                      <span class="text-white text-caption">{{ userInitials }}</span>
                    </v-avatar>

                    <!-- Имя + (Админ) -->
                    <span class="mr-1">{{ userName }}</span>
                    <span v-if="isAdmin" class="text-error font-weight-bold">(Админ)</span>

                    <v-icon end size="small">mdi-chevron-down</v-icon>
                  </v-btn>
                </template>
                <v-list>
                  <v-list-item to="/profile">
                    <v-list-item-title>Профиль</v-list-item-title>
                  </v-list-item>

                  <!-- Разделитель -->
                  <v-divider></v-divider>

                  <v-list-item @click="logout">
                    <v-list-item-title>Выйти</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-app-bar>

    <!-- Основное содержимое -->
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'App',

  computed: {
    ...mapGetters(['isAuthenticated', 'isAdmin', 'userName']),

    userInitials() {
      if (!this.userName) return '?'
      return this.userName.charAt(0).toUpperCase()
    }
  },

  methods: {
    ...mapActions(['logout'])
  }
}
</script>