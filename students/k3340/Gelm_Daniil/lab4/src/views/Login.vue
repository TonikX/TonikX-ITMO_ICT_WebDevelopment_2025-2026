<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card>
          <v-card-title>Вход</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleLogin">
              <v-text-field
                v-model="username"
                label="Имя пользователя"
                required
              ></v-text-field>
              <v-text-field
                v-model="password"
                label="Пароль"
                type="password"
                required
              ></v-text-field>
              <v-alert v-if="error" type="error" class="mt-2">{{ error }}</v-alert>
              <v-btn type="submit" color="primary" block class="mt-4">Войти</v-btn>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text to="/register">Нет аккаунта? Зарегистрироваться</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { ref } from 'vue'
import { useAuth } from '../composables/useAuth'

export default {
  name: 'Login',
  setup() {
    const { login } = useAuth()
    const username = ref('')
    const password = ref('')
    const error = ref('')

    const handleLogin = async () => {
      error.value = ''
      const result = await login(username.value, password.value)
      if (!result.success) {
        const err = result.error
        if (err?.non_field_errors) {
          error.value = Array.isArray(err.non_field_errors) ? err.non_field_errors[0] : err.non_field_errors
        } else {
          error.value = 'Ошибка входа'
        }
      }
    }

    return { username, password, error, handleLogin }
  }
}
</script>

