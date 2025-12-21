<template>
  <div class="login-page">
    <v-container fluid class="fill-height">
      <v-row justify="center" align="center">
        <v-col cols="12" sm="8" md="6" lg="4">
          <v-card class="pa-6" elevation="8">
            <v-card-title class="text-h5 mb-4 d-flex align-center justify-center">
              <v-icon icon="mdi-login" class="mr-2"></v-icon>
              Вход в систему
            </v-card-title>

            <v-card-text>
              <v-form @submit.prevent="login">
                <v-text-field
                  v-model="username"
                  label="Имя пользователя"
                  prepend-inner-icon="mdi-account"
                  variant="outlined"
                  :disabled="loading"
                  required
                  class="mb-4"
                ></v-text-field>

                <v-text-field
                  v-model="password"
                  label="Пароль"
                  prepend-inner-icon="mdi-lock"
                  variant="outlined"
                  :type="showPassword ? 'text' : 'password'"
                  :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                  @click:append-inner="showPassword = !showPassword"
                  :disabled="loading"
                  required
                  class="mb-4"
                ></v-text-field>

                <v-alert
                  v-if="error"
                  type="error"
                  variant="tonal"
                  class="mb-4"
                >
                  {{ error }}
                </v-alert>

                <v-btn
                  type="submit"
                  color="primary"
                  size="large"
                  block
                  :loading="loading"
                  :disabled="loading"
                  class="mt-2 mb-4"
                >
                  <template v-slot:loader>
                    <v-progress-circular indeterminate></v-progress-circular>
                  </template>
                  Войти
                </v-btn>
              </v-form>

              <v-divider class="my-4"></v-divider>

            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/api/axios'

export default {
  setup() {
    const username = ref('')
    const password = ref('')
    const showPassword = ref(false)
    const loading = ref(false)
    const error = ref('')
    const router = useRouter()

    const login = async () => {
      loading.value = true
      error.value = ''

      try {
        const response = await apiClient.post('token/', {
          username: username.value,
          password: password.value
        })

        localStorage.setItem('access_token', response.data.access)
        localStorage.setItem('refresh_token', response.data.refresh)

        router.push('/')
      } catch (err) {
        console.error('Login error:', err)
        if (err.response?.status === 401) {
          error.value = 'Неверное имя пользователя или пароль'
        } else if (err.code === 'ERR_NETWORK') {
          error.value = 'Сервер недоступен. Проверьте подключение.'
        } else {
          error.value = 'Произошла ошибка при входе'
        }
      } finally {
        loading.value = false
      }
    }

    return {
      username,
      password,
      showPassword,
      loading,
      error,
      login
    }
  }
}
</script>

<style scoped>
.login-page {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.fill-height {
  height: 100%;
}

.v-card {
  border-radius: 12px;
}

.text-h5 {
  font-weight: 600;
}

/* Убираем лишние отступы */
.v-container {
  padding: 0 !important;
}

.v-row {
  margin: 0 !important;
}
</style>
