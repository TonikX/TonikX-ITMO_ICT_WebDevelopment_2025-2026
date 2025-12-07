<template>
  <v-app>
    <v-navigation-drawer
      v-model="drawer"
      :permanent="$vuetify.display.mdAndUp"
      :temporary="$vuetify.display.smAndDown"
    >
      <v-list v-if="isAuthenticated">
        <v-list-item>
          <v-list-item-title class="text-h6">ЖК Коннект</v-list-item-title>
          <v-list-item-subtitle>{{ userName }}</v-list-item-subtitle>
        </v-list-item>
        <v-divider></v-divider>

        <!-- Общие пункты меню -->
        <v-list-item to="/" prepend-icon="mdi-home">
          <v-list-item-title>Главная</v-list-item-title>
        </v-list-item>
        <v-list-item to="/profile" prepend-icon="mdi-account">
          <v-list-item-title>Профиль</v-list-item-title>
        </v-list-item>

        <v-divider></v-divider>

        <!-- Меню для жильца -->
        <template v-if="userRole === 'resident'">
          <v-list-item to="/service-requests/my" prepend-icon="mdi-clipboard-list">
            <v-list-item-title>Мои заявки</v-list-item-title>
          </v-list-item>
          <v-list-item to="/service-requests/new" prepend-icon="mdi-plus-circle">
            <v-list-item-title>Подать заявку</v-list-item-title>
          </v-list-item>
          <v-list-item to="/meter-readings" prepend-icon="mdi-counter">
            <v-list-item-title>Показания счетчиков</v-list-item-title>
          </v-list-item>
          <v-list-item to="/meter-readings/new" prepend-icon="mdi-plus">
            <v-list-item-title>Подать показания</v-list-item-title>
          </v-list-item>
          <v-list-item to="/apartments" prepend-icon="mdi-home">
            <v-list-item-title>Мои квартиры</v-list-item-title>
          </v-list-item>
        </template>

        <!-- Меню для мастера -->
        <template v-if="userRole === 'master'">
          <v-list-item to="/service-requests/assigned" prepend-icon="mdi-clipboard-check">
            <v-list-item-title>Назначенные заявки</v-list-item-title>
          </v-list-item>
          <v-list-item to="/service-requests" prepend-icon="mdi-clipboard-list">
            <v-list-item-title>Все заявки</v-list-item-title>
          </v-list-item>
        </template>

        <!-- Меню для диспетчера -->
        <template v-if="userRole === 'dispatcher'">
          <v-list-group value="buildings">
            <template v-slot:activator="{ props }">
              <v-list-item v-bind="props" prepend-icon="mdi-office-building">
                <v-list-item-title>Дома</v-list-item-title>
              </v-list-item>
            </template>
            <v-list-item to="/buildings" prepend-icon="mdi-format-list-bulleted">
              <v-list-item-title>Список домов</v-list-item-title>
            </v-list-item>
            <v-list-item to="/buildings/new" prepend-icon="mdi-plus">
              <v-list-item-title>Создать дом</v-list-item-title>
            </v-list-item>
            <v-list-item to="/buildings/statistics" prepend-icon="mdi-chart-bar">
              <v-list-item-title>Статистика</v-list-item-title>
            </v-list-item>
          </v-list-group>

          <v-list-group value="apartments">
            <template v-slot:activator="{ props }">
              <v-list-item v-bind="props" prepend-icon="mdi-home">
                <v-list-item-title>Квартиры</v-list-item-title>
              </v-list-item>
            </template>
            <v-list-item to="/apartments" prepend-icon="mdi-format-list-bulleted">
              <v-list-item-title>Список квартир</v-list-item-title>
            </v-list-item>
            <v-list-item to="/apartments/new" prepend-icon="mdi-plus">
              <v-list-item-title>Создать квартиру</v-list-item-title>
            </v-list-item>
          </v-list-group>

          <v-list-group value="requests">
            <template v-slot:activator="{ props }">
              <v-list-item v-bind="props" prepend-icon="mdi-clipboard-list">
                <v-list-item-title>Заявки</v-list-item-title>
              </v-list-item>
            </template>
            <v-list-item to="/service-requests" prepend-icon="mdi-format-list-bulleted">
              <v-list-item-title>Все заявки</v-list-item-title>
            </v-list-item>
            <v-list-item to="/service-requests/statistics" prepend-icon="mdi-chart-bar">
              <v-list-item-title>Статистика</v-list-item-title>
            </v-list-item>
          </v-list-group>

          <v-list-group value="readings">
            <template v-slot:activator="{ props }">
              <v-list-item v-bind="props" prepend-icon="mdi-counter">
                <v-list-item-title>Показания</v-list-item-title>
              </v-list-item>
            </template>
            <v-list-item to="/meter-readings" prepend-icon="mdi-format-list-bulleted">
              <v-list-item-title>Все показания</v-list-item-title>
            </v-list-item>
            <v-list-item to="/meter-readings/statistics" prepend-icon="mdi-chart-bar">
              <v-list-item-title>Статистика</v-list-item-title>
            </v-list-item>
          </v-list-group>
        </template>
      </v-list>

      <v-list v-else>
        <v-list-item>
          <v-list-item-title class="text-h6">ЖК Коннект</v-list-item-title>
        </v-list-item>
        <v-divider></v-divider>
        <v-list-item to="/login" prepend-icon="mdi-login">
          <v-list-item-title>Вход</v-list-item-title>
        </v-list-item>
        <v-list-item to="/register" prepend-icon="mdi-account-plus">
          <v-list-item-title>Регистрация</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar color="primary" dark>
      <v-app-bar-nav-icon
        v-if="$vuetify.display.smAndDown"
        @click="drawer = !drawer"
      ></v-app-bar-nav-icon>
      <v-app-bar-title>ЖК Коннект</v-app-bar-title>
      <v-spacer></v-spacer>
      <v-chip v-if="isAuthenticated" color="white" variant="flat" class="mr-4">
        {{ roleDisplay }}
      </v-chip>
      <v-menu v-if="isAuthenticated" location="bottom">
        <template v-slot:activator="{ props }">
          <v-btn icon="mdi-account" v-bind="props" variant="text"></v-btn>
        </template>
        <v-list>
          <v-list-item to="/profile">Профиль</v-list-item>
          <v-list-item @click="logout">Выход</v-list-item>
        </v-list>
      </v-menu>
      <v-btn v-if="!isAuthenticated" to="/login" variant="text">Вход</v-btn>
      <v-btn v-if="!isAuthenticated" to="/register" variant="text">Регистрация</v-btn>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import { useAuthStore } from '@/stores/auth'
import { getRoleLabel } from '@/utils/roleUtils'

export default {
  name: 'App',
  data() {
    return {
      drawer: null,
    }
  },
  computed: {
    isAuthenticated() {
      return useAuthStore().isAuthenticated
    },
    userRole() {
      return useAuthStore().userRole
    },
    userName() {
      return useAuthStore().userName
    },
    roleDisplay() {
      return getRoleLabel(this.userRole)
    },
  },
  methods: {
    logout() {
      useAuthStore().logout()
      this.$router.push('/login')
    },
  },
}
</script>
