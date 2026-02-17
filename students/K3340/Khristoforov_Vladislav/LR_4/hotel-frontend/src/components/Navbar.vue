<script setup>
/**
 * Navbar.vue - Верхняя навигационная панель.
 * Отвечает за навигацию по сайту и отображение кнопок в зависимости от статуса авторизации.
 */
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
// Реактивная переменная для отслеживания статуса входа
const isAuthenticated = ref(false)

// При загрузке проверяем наличие токена авторизации в localStorage
onMounted(() => {
  isAuthenticated.value = !!localStorage.getItem('auth_token')
})

// Функция выхода из системы
function logout() {
  localStorage.removeItem('auth_token') // Удаляем токен
  isAuthenticated.value = false
  router.push('/login') // Перенаправляем на страницу входа

  // Перезагружаем страницу, чтобы сбросить все состояния (простой способ очистки)
  setTimeout(() => window.location.reload(), 10)
}
</script>

<template>
  <v-app-bar color="indigo-darken-3" elevation="2">
    <!-- Логотип / Иконка слева -->
    <template v-slot:prepend>
      <v-icon icon="mdi-office-building-cog" class="ml-2"></v-icon>
    </template>

    <!-- Заголовок (кликабельный) -->
    <v-app-bar-title class="font-weight-bold cursor-pointer" @click="router.push('/')">
      Hotel Admin
    </v-app-bar-title>

    <template v-slot:append>
      <!-- Меню для авторизованных пользователей -->
      <div v-if="isAuthenticated" class="d-none d-md-flex">
        <!-- Ссылка на Главную -->
        <v-btn to="/" variant="text" prepend-icon="mdi-view-dashboard">Главная</v-btn>

        <!-- Выпадающее меню "Данные" для справочников и списков -->
        <v-menu open-on-hover>
          <template v-slot:activator="{ props }">
            <v-btn v-bind="props" variant="text" append-icon="mdi-chevron-down">Справочники</v-btn>
          </template>

          <v-list>
            <v-list-item to="/rooms" prepend-icon="mdi-door">
              <v-list-item-title>Номера</v-list-item-title>
            </v-list-item>
            <v-list-item to="/guests" prepend-icon="mdi-account-group">
              <v-list-item-title>Гости</v-list-item-title>
            </v-list-item>
            <v-list-item to="/employees" prepend-icon="mdi-badge-account">
              <v-list-item-title>Сотрудники</v-list-item-title>
            </v-list-item>
            <v-list-item to="/schedules" prepend-icon="mdi-calendar-clock">
              <v-list-item-title>Графики уборки</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>

        <!-- Основные оперативные кнопки -->
        <v-btn to="/bookings" variant="text" prepend-icon="mdi-book-open-page-variant">Заселение</v-btn>
        <v-btn to="/reports" variant="text" prepend-icon="mdi-chart-bar">Отчеты</v-btn>

        <!-- Разделитель -->
        <v-divider vertical class="mx-3 my-auto" style="height: 20px"></v-divider>

        <!-- Профиль и Выход -->
        <v-btn to="/profile" variant="text" prepend-icon="mdi-account-circle">Профиль</v-btn>
        <v-btn @click="logout" color="red-lighten-4" variant="text" prepend-icon="mdi-logout">
          Выйти
        </v-btn>
      </div>

      <!-- Меню для гостей (неавторизованных) -->
      <div v-else>
        <v-btn to="/login" variant="outlined" class="mr-2">Вход</v-btn>
        <v-btn to="/register" variant="text">Регистрация</v-btn>
      </div>
    </template>
  </v-app-bar>
</template>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}
</style>