<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12" md="8" lg="6">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title class="text-h4">
              <v-icon class="mr-3">mdi-school</v-icon>
              Школьная система управления
            </v-toolbar-title>
          </v-toolbar>

          <v-card-text class="pa-8">
            <div class="text-center mb-6">
              <v-icon size="96" color="primary" class="mb-4">mdi-school</v-icon>
              <h1 class="text-h3 mb-4">Добро пожаловать!</h1>
              <p class="text-h6 text-grey mb-6">
                Система управления учебным процессом школы
              </p>
            </div>

            <v-row class="mb-6">
              <v-col cols="12" md="4" class="text-center">
                <v-icon size="48" color="success" class="mb-3">mdi-account-multiple</v-icon>
                <h3 class="text-h5 mb-2">Управление персоналом</h3>
                <p class="text-body-1 text-grey">Учителя и классные руководители</p>
              </v-col>

              <v-col cols="12" md="4" class="text-center">
                <v-icon size="48" color="info" class="mb-3">mdi-school</v-icon>
                <h3 class="text-h5 mb-2">Ученики и оценки</h3>
                <p class="text-body-1 text-grey">Учет успеваемости и посещаемости</p>
              </v-col>

              <v-col cols="12" md="4" class="text-center">
                <v-icon size="48" color="warning" class="mb-3">mdi-calendar</v-icon>
                <h3 class="text-h5 mb-2">Расписание</h3>
                <p class="text-body-1 text-grey">Составление и управление расписанием</p>
              </v-col>
            </v-row>

            <v-divider class="my-6" />

            <div class="text-center">
              <h2 class="text-h4 mb-4">Начните работу с системой</h2>

              <div class="d-flex justify-center gap-4 mt-6">
                <v-btn
                  color="primary"
                  size="x-large"
                  to="/login"
                  class="px-8"
                >
                  <v-icon left>mdi-login</v-icon>
                  Войти в систему
                </v-btn>

                <v-btn
                  color="success"
                  size="x-large"
                  to="/register"
                  variant="outlined"
                  class="px-8"
                >
                  <v-icon left>mdi-account-plus</v-icon>
                  Зарегистрироваться
                </v-btn>
              </div>

              <div class="mt-8">
                <v-chip color="grey-lighten-3" variant="flat" class="ma-1">
                  <v-icon left size="small">mdi-shield-check</v-icon>
                  Безопасность данных
                </v-chip>
                <v-chip color="grey-lighten-3" variant="flat" class="ma-1">
                  <v-icon left size="small">mdi-speedometer</v-icon>
                  Высокая производительность
                </v-chip>
                <v-chip color="grey-lighten-3" variant="flat" class="ma-1">
                  <v-icon left size="small">mdi-cellphone</v-icon>
                  Адаптивный дизайн
                </v-chip>
              </div>
            </div>
          </v-card-text>

          <v-card-actions class="pa-4 bg-grey-lighten-4">
            <v-spacer />
            <span class="text-caption text-grey">
              Лабораторная работа 4. Клиентская часть на Vue.js
            </span>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'Home',
  mounted() {
    // Проверяем, авторизован ли пользователь
    const token = localStorage.getItem('token')
    if (token) {
      this.$router.push('/dashboard')
    }
  }
}
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}
</style>