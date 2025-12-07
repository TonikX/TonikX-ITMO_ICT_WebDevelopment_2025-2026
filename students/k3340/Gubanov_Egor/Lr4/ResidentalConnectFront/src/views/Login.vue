<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark>
            <v-toolbar-title>Вход в систему</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="handleLogin">
              <v-text-field
                v-model="username"
                label="Имя пользователя"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                required
                :error-messages="errors.username"
              ></v-text-field>

              <v-text-field
                v-model="password"
                label="Пароль"
                prepend-inner-icon="mdi-lock"
                type="password"
                variant="outlined"
                required
                :error-messages="errors.password"
              ></v-text-field>

              <v-alert
                v-if="errorMessage"
                type="error"
                class="mb-4"
                closable
                @click:close="errorMessage = ''"
              >
                {{ errorMessage }}
              </v-alert>

              <v-btn
                type="submit"
                color="primary"
                block
                size="large"
                :loading="loading"
                class="mt-4"
              >
                Войти
              </v-btn>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text to="/register">
              Нет аккаунта? Зарегистрироваться
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      errors: {},
      errorMessage: '',
      loading: false,
    }
  },
  methods: {
    async handleLogin() {
      this.errors = {}
      this.errorMessage = ''
      this.loading = true

      if (!this.username) {
        this.errors.username = 'Введите имя пользователя'
        this.loading = false
        return
      }

      if (!this.password) {
        this.errors.password = 'Введите пароль'
        this.loading = false
        return
      }

      try {
        const authStore = useAuthStore()
        const result = await authStore.login(this.username, this.password)

        if (result.success) {
          const redirect = this.$route.query.redirect || '/'
          this.$router.push(redirect)
        } else {
          this.errorMessage = result.error || 'Ошибка входа'
        }
      } catch (error) {
        console.error('Login error:', error)
        this.errorMessage = 'Произошла ошибка при входе. Попробуйте еще раз.'
      } finally {
        this.loading = false
      }
    },
  },
}
</script>

