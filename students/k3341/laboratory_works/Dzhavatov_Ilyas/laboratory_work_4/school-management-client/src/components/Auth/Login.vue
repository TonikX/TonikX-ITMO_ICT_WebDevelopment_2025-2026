<template>
  <v-container class="fill-height" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12" :loading="loading">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title class="text-h5">
              <v-icon class="mr-2">mdi-school</v-icon>
              Школьная система управления
            </v-toolbar-title>
          </v-toolbar>

          <v-card-text class="pa-6">
            <div class="text-center mb-6">
              <h2 class="text-h4 mb-2">Вход в систему</h2>
              <p class="text-body-1 text-grey">Введите учетные данные</p>
            </div>

            <v-form ref="form" v-model="valid" @submit.prevent="login">
              <v-text-field
                v-model="credentials.username"
                label="Имя пользователя"
                :rules="[rules.required]"
                prepend-icon="mdi-account"
                variant="outlined"
                class="mb-4"
                required
                :disabled="loading"
              />

              <v-text-field
                v-model="credentials.password"
                label="Пароль"
                :type="showPassword ? 'text' : 'password'"
                :rules="[rules.required]"
                prepend-icon="mdi-lock"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="showPassword = !showPassword"
                variant="outlined"
                class="mb-2"
                required
                :disabled="loading"
              />

              <v-alert
                v-if="error"
                type="error"
                density="compact"
                class="mb-4"
              >
                {{ error }}
              </v-alert>

              <v-btn
                type="submit"
                color="primary"
                block
                size="large"
                :loading="loading"
                :disabled="!valid || loading"
                class="mt-4"
              >
                <v-icon left>mdi-login</v-icon>
                Войти
              </v-btn>
            </v-form>
          </v-card-text>

          <v-divider />

          <v-card-actions class="pa-4">
            <v-spacer />
            <span class="text-body-2 mr-2">Нет аккаунта?</span>
            <v-btn color="secondary" variant="text" to="/register" :disabled="loading">
              Зарегистрироваться
            </v-btn>
          </v-card-actions>
        </v-card>

        <div class="text-center mt-6">
          <v-chip color="grey-lighten-3" variant="flat">
            <v-icon small class="mr-1">mdi-information</v-icon>
            <span class="text-caption">Тестовые данные: admin / admin</span>
          </v-chip>
        </div>
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
      valid: false,
      loading: false,
      showPassword: false,
      error: null,
      credentials: {
        username: '',
        password: ''
      },
      rules: {
        required: value => !!value || 'Обязательное поле'
      }
    }
  },
  methods: {
    ...mapActions('auth', ['login']),

    async login() {
      if (!this.$refs.form.validate()) return

      this.loading = true
      this.error = null

      try {
        const result = await this.$store.dispatch('auth/login', this.credentials)

        if (result.success) {
          this.$toast.success('Вход выполнен успешно!')
          this.$router.push('/dashboard')
        } else {
          this.error = result.error?.non_field_errors?.[0] || 'Неверное имя пользователя или пароль'
          this.$toast.error('Ошибка входа')
        }
      } catch (err) {
        this.error = 'Ошибка подключения к серверу'
        this.$toast.error('Сервер не отвечает')
      } finally {
        this.loading = false
      }
    }
  },
  mounted() {
    // Автозаполнение для тестирования
    if (process.env.NODE_ENV === 'development') {
      this.credentials.username = 'admin'
      this.credentials.password = 'admin'
    }
  }
}
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
}
</style>