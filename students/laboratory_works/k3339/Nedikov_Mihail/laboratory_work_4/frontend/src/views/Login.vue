<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Вход в систему</v-toolbar-title>
            <v-spacer></v-spacer>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="login" ref="form" v-model="valid">
              <v-text-field
                  v-model="username"
                  label="Логин"
                  name="login"
                  prepend-icon="mdi-account"
                  type="text"
                  :rules="[v => !!v || 'Обязательное поле']"
                  required
              ></v-text-field>

              <v-text-field
                  v-model="password"
                  label="Пароль"
                  name="password"
                  prepend-icon="mdi-lock"
                  type="password"
                  :rules="[v => !!v || 'Обязательное поле']"
                  required
              ></v-text-field>

              <v-alert v-if="error" type="error" dense>
                {{ errorMessage }}
              </v-alert>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="login" :loading="loading">Войти</v-btn>
            <v-btn text to="/register">Регистрация</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      valid: false,
      loading: false,
      error: false,
      errorMessage: ''
    }
  },
  methods: {
    ...mapActions('auth', ['login']),

    async login() {
      if (!this.$refs.form.validate()) return

      this.loading = true
      this.error = false

      try {
        // Правильный вызов - передаем credentials как второй аргумент
        const result = await this.$store.dispatch('auth/login', {
          username: this.username,
          password: this.password
        })

        console.log('Результат авторизации:', result)

        if (result && result.success) {
          this.$router.push('/')
        } else {
          this.error = true
          this.errorMessage = result?.error?.detail || 'Неверный логин или пароль'
        }
      } catch (error) {
        console.error('Ошибка при вызове login action:', error)
        this.error = true
        this.errorMessage = 'Произошла ошибка при авторизации'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>