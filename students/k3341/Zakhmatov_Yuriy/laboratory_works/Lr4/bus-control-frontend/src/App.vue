<template>
  <v-app>
    <!-- App Bar (верхняя панель) -->
    <v-app-bar color="primary" prominent>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>

      <v-toolbar-title>
        <v-icon icon="mdi-bus" class="mr-2"></v-icon>
        Управление автобусным парком
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn @click="logout" v-if="isAuthenticated" prepend-icon="mdi-logout">
        Выйти
      </v-btn>
    </v-app-bar>

    <!-- Боковая навигация -->
    <v-navigation-drawer v-model="drawer" temporary>
      <v-list>
        <v-list-item
          v-for="item in menuItems"
          :key="item.title"
          :to="item.to"
          :prepend-icon="item.icon"
          :title="item.title"
          @click="item.click"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Основное содержимое -->
    <v-main>
      <v-container fluid class="pa-6">
        <router-view></router-view>
      </v-container>
    </v-main>

    <!-- Футер -->
    <v-footer app color="primary" class="text-center d-flex flex-column">
      <div class="text-white">
        {{ new Date().getFullYear() }} — <strong>Автобусный парк</strong>
      </div>
    </v-footer>
  </v-app>
</template>

<script>
import { computed, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'

export default {
  setup() {
    const router = useRouter()
    const route = useRoute()
    const drawer = ref(false)

    const isAuthenticated = computed(() => {
      return !!localStorage.getItem('access_token')
    })

    const menuItems = computed(() => {
      const items = [
        { title: 'Главная', icon: 'mdi-home', to: '/' },
        { title: 'Водители', icon: 'mdi-account-group', to: '/drivers' },
        { title: 'Автобусы', icon: 'mdi-bus', to: '/buses' },
        { title: 'Маршруты', icon: 'mdi-map-marker-path', to: '/routes' },
        { title: 'Смены', icon: 'mdi-calendar-clock', to: '/workshifts' },
        { title: 'Отчеты', icon: 'mdi-chart-bar', to: '/reports' },
        { title: 'Классы водителей', icon: 'mdi-license', to: '/driver-classes'},
        { title: 'Типы автобусов', icon: 'mdi-bus-double-decker', to: '/bus-types'},
        { title: 'Депо', icon: 'mdi-garage', to: '/depots'}
      ]

      if (!isAuthenticated.value) {
        items.push(
          { title: 'Вход', icon: 'mdi-login', to: '/login' },
        )
      }

      return items
    })

    const logout = () => {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      router.push('/login')
    }

    return {
      drawer,
      isAuthenticated,
      menuItems,
      logout
    }
  }
}
</script>

<style>
/* Глобальные стили */
.v-application {
  font-family: 'Roboto', sans-serif;
}

/* Кастомные цвета для темы */
:root {
  --primary-color: #1976D2;
  --secondary-color: #424242;
  --accent-color: #82B1FF;
  --error-color: #FF5252;
  --info-color: #2196F3;
  --success-color: #4CAF50;
  --warning-color: #FFC107;
}

.v-toolbar-title {
  font-weight: 500;
  font-size: 1.25rem;
}
</style>
