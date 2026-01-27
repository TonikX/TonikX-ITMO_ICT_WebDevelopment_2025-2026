<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card>
          <v-card-title class="text-h5 text-center">Вход в систему</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleLogin">
              <v-text-field
                v-model="form.username"
                label="Имя пользователя или Email"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                :error-messages="errors.username"
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
                Войти
              </v-btn>
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
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const form = reactive({
      username: '',
      password: ''
    })
    
    const errors = reactive({})
    const errorMessage = ref('')
    const loading = ref(false)

    const handleLogin = async () => {
      errors.username = ''
      errors.password = ''
      errorMessage.value = ''
      loading.value = true

      const result = await authStore.login(form)

      if (result.success) {
        router.push('/')
      } else {
        if (result.error) {
          if (result.error.username) {
            errors.username = result.error.username
          }
          if (result.error.password) {
            errors.password = result.error.password
          }
          if (result.error.non_field_errors) {
            errorMessage.value = result.error.non_field_errors.join(', ')
          } else {
            errorMessage.value = 'Неверное имя пользователя или пароль'
          }
        }
      }
      
      loading.value = false
    }

    return {
      form,
      errors,
      errorMessage,
      loading,
      handleLogin
    }
  }
}
</script>
