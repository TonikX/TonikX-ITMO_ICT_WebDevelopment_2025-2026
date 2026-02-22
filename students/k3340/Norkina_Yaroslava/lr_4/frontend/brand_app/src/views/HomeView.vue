<template>
  <v-container class="my-12">
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 text-center mb-4">Главная страница</h1>

        <div class="text-center mb-8">
          <!-- Для всех пользователей -->
          <v-btn
              to="/services"
              color="primary"
              class="mr-4"
          >
            Услуги
          </v-btn>

          <!-- Только для НЕ авторизованных -->
          <v-btn
              v-if="!isAuthenticated"
              to="/register"
              variant="outlined"
              color="primary"
          >
            Регистрация
          </v-btn>

          <!-- Только для авторизованных -->
          <v-btn
              v-if="isAuthenticated"
              to="/profile"
              color="secondary"
              class="mr-4"
          >
            Личный кабинет
          </v-btn>

          <v-btn
              v-if="isAuthenticated"
              to="/orders"
              color="primary"
              class="mr-4"
          >
            <v-icon start>mdi-clipboard-text</v-icon>
            Мои заявки
          </v-btn>

          <!-- для админов -->
          <v-btn
              v-if="isAdmin"
              to="/admin/services"
              color="error"
          >
            <v-icon start>mdi-shield-account</v-icon>
            Админ: Услуги
          </v-btn>

          <v-btn
              v-if="isAdmin"
              to="/admin/orders"
              color="error"
              class="mr-4"
          >
            <v-icon start>mdi-clipboard-list</v-icon>
            Админ: Заявки
          </v-btn>

          <v-btn
              v-if="isAdmin"
              to="/admin/reviews"
              color="error"
          >
            <v-icon start>mdi-star</v-icon>
            Админ: Отзывы
          </v-btn>
        </div>

        <!-- Информация о пользователе -->
        <div v-if="isAuthenticated" class="text-center">
          <p>Добро пожаловать, {{ userName }}</p>
          <p>Логин: {{ userData.username }}</p>
          <p>Email: {{ userData.email }}</p>
          <p>Роль: {{ userData.role }}</p>
          <p v-if="isAdmin" class="text-error font-weight-bold">Вы администратор</p>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'HomeView',

  computed: {
    ...mapGetters(['isAuthenticated', 'isAdmin', 'userName', 'userData'])
  }
}
</script>