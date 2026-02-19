<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Регистрация</v-toolbar-title>
            <v-spacer></v-spacer>
          </v-toolbar>
          <v-card-text>
            <v-form ref="form" v-model="valid" @submit.prevent="registerUser">
              <v-text-field
                  v-model="form.username"
                  label="Логин"
                  prepend-icon="mdi-account"
                  :rules="[v => !!v || 'Обязательное поле']"
                  required
                  variant="outlined"
                  class="mb-3"
              ></v-text-field>

              <v-text-field
                  v-model="form.email"
                  label="Email"
                  prepend-icon="mdi-email"
                  type="email"
                  :rules="[
                  v => !!v || 'Обязательное поле',
                  v => /.+@.+\..+/.test(v) || 'Некорректный email'
                ]"
                  required
                  variant="outlined"
                  class="mb-3"
              ></v-text-field>

              <v-text-field
                  v-model="form.password"
                  label="Пароль"
                  prepend-icon="mdi-lock"
                  type="password"
                  :rules="[
                  v => !!v || 'Обязательное поле',
                  v => (v && v.length >= 8) || 'Минимум 8 символов'
                ]"
                  required
                  variant="outlined"
                  class="mb-3"
              ></v-text-field>

              <v-text-field
                  v-model="form.first_name"
                  label="Имя"
                  prepend-icon="mdi-account-outline"
                  variant="outlined"
                  class="mb-3"
              ></v-text-field>

              <v-text-field
                  v-model="form.last_name"
                  label="Фамилия"
                  prepend-icon="mdi-account-outline"
                  variant="outlined"
                  class="mb-3"
              ></v-text-field>

              <v-text-field
                  v-model="form.phone"
                  label="Телефон"
                  prepend-icon="mdi-phone"
                  variant="outlined"
                  class="mb-3"
              ></v-text-field>

              <v-text-field
                  v-model="form.position"
                  label="Должность"
                  prepend-icon="mdi-briefcase"
                  variant="outlined"
                  class="mb-3"
              ></v-text-field>

              <v-alert v-if="error" type="error" dense class="mt-3">
                <div class="d-flex align-center">
                  <v-icon class="mr-2">mdi-alert-circle</v-icon>
                  {{ errorMessage }}
                </div>
              </v-alert>

              <v-alert v-if="success" type="success" dense class="mt-3">
                <div class="d-flex align-center">
                  <v-icon class="mr-2">mdi-check-circle</v-icon>
                  Регистрация успешна! Теперь вы можете войти.
                </div>
              </v-alert>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
                color="primary"
                @click="registerUser"
                :loading="loading"
                :disabled="!valid || success"
            >
              Зарегистрироваться
            </v-btn>
            <v-btn text to="/login">Уже есть аккаунт?</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Register',
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: '',
        first_name: '',
        last_name: '',
        phone: '',
        position: ''
      },
      valid: false,
      loading: false,
      error: false,
      success: false,
      errorMessage: ''
    }
  },
  methods: {
    async registerUser() {
      if (!this.$refs.form.validate()) return

      this.loading = true
      this.error = false
      this.success = false
      this.errorMessage = ''

      try {
        // Подготавливаем данные для отправки
        const payload = {
          username: this.form.username,
          email: this.form.email,
          password: this.form.password,
          first_name: this.form.first_name || '',
          last_name: this.form.last_name || '',
          phone: this.form.phone || '',
          position: this.form.position || ''
        }

        console.log('Регистрируем пользователя:', {...payload, password: '***'})

        // Отправляем POST запрос на регистрацию
        const response = await axios.post('http://localhost:8000/auth/users/', payload)

        this.success = true
        console.log('Регистрация успешна:', response.data)

        // Очищаем форму
        this.form = {
          username: '',
          email: '',
          password: '',
          first_name: '',
          last_name: '',
          phone: '',
          position: ''
        }

        this.$refs.form.resetValidation()

        // Через 3 секунды предлагаем перейти на страницу входа
        setTimeout(() => {
          this.$router.push('/login')
        }, 3000)

      } catch (error) {
        console.error('Ошибка регистрации:', error)
        this.error = true

        if (error.response?.status === 400) {
          // Ошибки валидации от Djoser
          if (error.response.data) {
            // Преобразуем ошибки в читаемый вид
            const errors = []

            for (const [field, messages] of Object.entries(error.response.data)) {
              const fieldNames = {
                'username': 'Логин',
                'email': 'Email',
                'password': 'Пароль',
                'first_name': 'Имя',
                'last_name': 'Фамилия',
                'phone': 'Телефон',
                'position': 'Должность'
              }

              const fieldName = fieldNames[field] || field
              const messageText = Array.isArray(messages) ? messages.join(', ') : messages
              errors.push(`${fieldName}: ${messageText}`)
            }

            this.errorMessage = errors.join('; ')
          } else {
            this.errorMessage = 'Ошибка валидации данных'
          }
        } else if (error.response?.data?.detail) {
          this.errorMessage = error.response.data.detail
        } else if (error.response?.status === 500) {
          this.errorMessage = 'Ошибка сервера. Попробуйте позже.'
        } else {
          this.errorMessage = 'Ошибка при регистрации'
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>