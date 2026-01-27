<template>
  <v-container class="fill-height" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12" :loading="loading">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title class="text-h5">
              <v-icon class="mr-2">mdi-account-plus</v-icon>
              Регистрация
            </v-toolbar-title>
          </v-toolbar>

          <v-card-text class="pa-6">
            <div class="text-center mb-6">
              <h2 class="text-h4 mb-2">Создание аккаунта</h2>
              <p class="text-body-1 text-grey">Заполните данные для регистрации</p>
            </div>

            <v-form ref="form" v-model="valid" @submit.prevent="register">
              <v-text-field
                v-model="userData.username"
                label="Имя пользователя"
                :rules="[rules.required, rules.minLength(3)]"
                prepend-icon="mdi-account"
                variant="outlined"
                class="mb-4"
                required
                :disabled="loading"
              />

              <v-text-field
                v-model="userData.email"
                label="Email"
                :rules="[rules.required, rules.email]"
                prepend-icon="mdi-email"
                variant="outlined"
                class="mb-4"
                required
                :disabled="loading"
              />

              <v-text-field
                v-model="userData.first_name"
                label="Имя"
                :rules="[rules.required]"
                prepend-icon="mdi-account-details"
                variant="outlined"
                class="mb-4"
                required
                :disabled="loading"
              />

              <v-text-field
                v-model="userData.last_name"
                label="Фамилия"
                :rules="[rules.required]"
                prepend-icon="mdi-account-details"
                variant="outlined"
                class="mb-4"
                required
                :disabled="loading"
              />

              <v-text-field
                v-model="userData.password"
                label="Пароль"
                :type="showPassword ? 'text' : 'password'"
                :rules="[rules.required, rules.minLength(6)]"
                prepend-icon="mdi-lock"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="showPassword = !showPassword"
                variant="outlined"
                class="mb-4"
                required
                :disabled="loading"
              />

              <v-text-field
                v-model="confirmPassword"
                label="Подтверждение пароля"
                :type="showPassword ? 'text' : 'password'"
                :rules="[rules.required, passwordMatch]"
                prepend-icon="mdi-lock-check"
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

              <v-alert
                v-if="success"
                type="success"
                density="compact"
                class="mb-4"
              >
                Регистрация успешна! Вы будете перенаправлены на страницу входа.
              </v-alert>

              <v-btn
                type="submit"
                color="primary"
                block
                size="large"
                :loading="loading"
                :disabled="!valid || loading || success"
                class="mt-4"
              >
                <v-icon left>mdi-account-plus</v-icon>
                Зарегистрироваться
              </v-btn>
            </v-form>
          </v-card-text>

          <v-divider />

          <v-card-actions class="pa-4">
            <v-btn color="grey" variant="text" to="/" :disabled="loading">
              <v-icon left>mdi-arrow-left</v-icon>
              На главную
            </v-btn>
            <v-spacer />
            <span class="text-body-2 mr-2">Уже есть аккаунт?</span>
            <v-btn color="secondary" variant="text" to="/login" :disabled="loading">
              Войти
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'Register',
  data() {
    return {
      valid: false,
      loading: false,
      showPassword: false,
      error: null,
      success: false,
      confirmPassword: '',
      userData: {
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        password: '',
        re_password: ''
      },
      rules: {
        required: value => !!value || 'Обязательное поле',
        minLength: min => value => (value && value.length >= min) || `Минимум ${min} символов`,
        email: value => {
          const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
          return pattern.test(value) || 'Некорректный email'
        }
      }
    }
  },
  computed: {
    passwordMatch() {
      return () => this.userData.password === this.confirmPassword || 'Пароли не совпадают'
    }
  },
  methods: {
    ...mapActions('auth', ['register']),

    notify(type, message) {
      if (this.$toast && typeof this.$toast[type] === 'function') {
        this.$toast[type](message)
      }
    },

    async register() {
      if (!this.$refs.form.validate()) return

      this.loading = true
      this.error = null

      try {
        this.userData.re_password = this.confirmPassword
        const result = await this.$store.dispatch('auth/register', this.userData)

        if (result.success) {
          this.success = true
          this.notify('success', 'Регистрация успешна!')

          // Перенаправляем через 3 секунды
          setTimeout(() => {
            this.$router.push('/login')
          }, 3000)
        } else {
          this.error = result.error?.username?.[0] ||
                      result.error?.email?.[0] ||
                      'Ошибка регистрации'
          this.notify('error', 'Ошибка регистрации')
        }
      } catch (err) {
        this.error = 'Ошибка подключения к серверу'
        this.notify('error', 'Сервер не отвечает')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
}
</style>