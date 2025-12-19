<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="headline">
            Добро пожаловать в систему лизинга авто
          </v-card-title>
          <v-card-text>
            <p v-if="user">
              Вы вошли как: <strong>{{ user.username }}</strong>
              <br>
              Должность: {{ user.position || 'Не указана' }}
              <br>
              Email: {{ user.email || 'Не указан' }}
            </p>
            <p v-else>
              Пожалуйста, войдите в систему для доступа к функционалу
            </p>

            <v-divider class="my-4"></v-divider>

            <h3>Доступные разделы:</h3>
            <v-row class="mt-3">
              <v-col cols="12" md="6" v-if="isAdmin">
                <v-card class="pa-3" to="/admin" hover>
                  <v-icon large color="primary" class="mr-3">mdi-shield-account</v-icon>
                  <span class="title">Административная панель</span>
                  <p class="mt-2">Управление автомобилями, клиентами, заявками</p>
                </v-card>
              </v-col>

              <v-col cols="12" md="6">
                <v-card class="pa-3" to="/cars" hover>
                  <v-icon large color="primary" class="mr-3">mdi-car</v-icon>
                  <span class="title">Каталог автомобилей</span>
                  <p class="mt-2">Просмотр доступных автомобилей для аренды</p>
                </v-card>
              </v-col>

              <v-col cols="12" md="6">
                <v-card class="pa-3" to="/profile" hover>
                  <v-icon large color="primary" class="mr-3">mdi-account</v-icon>
                  <span class="title">Мой профиль</span>
                  <p class="mt-2">Просмотр и редактирование личных данных</p>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Home',
  computed: {
    ...mapGetters('auth', ['user', 'isAdmin', 'isAuthenticated'])
  },
  created() {
    // Загружаем данные пользователя если ещё не загружены
    if (this.isAuthenticated && !this.user) {
      this.$store.dispatch('auth/fetchUser')
    }
  }
}
</script>