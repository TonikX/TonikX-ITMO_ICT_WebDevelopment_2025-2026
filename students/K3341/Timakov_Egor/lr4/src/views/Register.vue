<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card>
          <v-card-title class="text-h5 text-center">Регистрация</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleRegister">
              <v-text-field
                v-model="form.username"
                label="Имя пользователя"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                :error-messages="errors.username"
                required
              ></v-text-field>

              <v-text-field
                v-model="form.email"
                label="Email"
                type="email"
                prepend-inner-icon="mdi-email"
                variant="outlined"
                :error-messages="errors.email"
                required
              ></v-text-field>

              <v-text-field
                v-model="form.password"
                label="Пароль"
                type="password"
                prepend-inner-icon="mdi-lock"
                variant="outlined"
                :error-messages="errors.password"
                required
              ></v-text-field>

              <v-text-field
                v-model="form.re_password"
                label="Подтверждение пароля"
                type="password"
                prepend-inner-icon="mdi-lock-check"
                variant="outlined"
                :error-messages="errors.re_password"
                required
              ></v-text-field>

              <v-alert v-if="errorMessage" type="error" class="mb-4">
                {{ errorMessage }}
              </v-alert>

              <v-btn
                type="submit"
                color="primary"
                block
                size="large"
                :loading="loading"
              >
                Зарегистрироваться
              </v-btn>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text to="/login">Уже есть аккаунт? Войти</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Register',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const form = reactive({
      username: '',
      email: '',
      password: '',
      re_password: ''
    })
    
    const errors = reactive({})
    const errorMessage = ref('')
    const loading = ref(false)

    const handleRegister = async () => {
      // Очистка ошибок
      Object.keys(errors).forEach(key => errors[key] = '')
      errorMessage.value = ''
      loading.value = true

      const result = await authStore.register(form)

      if (result.success) {
        router.push('/')
      } else {
        if (result.error) {
          Object.keys(result.error).forEach(key => {
            if (Array.isArray(result.error[key])) {
              errors[key] = result.error[key].join(', ')
            } else {
              errors[key] = result.error[key]
            }
          })
          errorMessage.value = 'Ошибка регистрации. Проверьте введённые данные.'
        }
      }
      
      loading.value = false
    }

    return {
      form,
      errors,
      errorMessage,
      loading,
      handleRegister
    }
  }
}
</script>
