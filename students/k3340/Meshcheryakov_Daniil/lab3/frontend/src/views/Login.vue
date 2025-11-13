<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center" class="fill-height">
      <v-col cols="12" sm="10" md="6" lg="4">
        <v-card elevation="8" class="pa-2">
          <v-card-title class="text-h4 text-center pa-6 pb-4">
            <v-icon size="48" color="primary" class="mb-2 d-block w-100">mdi-book-open-variant</v-icon>
            <div class="w-100 mt-2">Система управления<br>читальным залом</div>
          </v-card-title>
          <v-divider class="mx-4"></v-divider>
          <v-card-text class="pa-6">
            <v-form @submit.prevent="handleLogin">
              <v-text-field
                v-model="username"
                label="Имя пользователя"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                density="comfortable"
                required
                :error-messages="errors.username"
                class="mb-3"
              ></v-text-field>
              <v-text-field
                v-model="password"
                label="Пароль"
                type="password"
                prepend-inner-icon="mdi-lock"
                variant="outlined"
                density="comfortable"
                required
                :error-messages="errors.password"
                class="mb-4"
              ></v-text-field>
              <v-alert
                v-if="successMessage"
                type="success"
                class="mb-4"
                variant="tonal"
                :icon="false"
              >
                <div class="d-flex align-center">
                  <v-icon color="success" class="mr-2">mdi-check-circle</v-icon>
                  <span>{{ successMessage }}</span>
                </div>
              </v-alert>
              <v-alert
                v-if="errorMessage"
                type="error"
                class="mb-4"
                variant="tonal"
              >
                {{ errorMessage }}
              </v-alert>
              <v-btn
                type="submit"
                color="primary"
                size="large"
                block
                :loading="loading"
                class="mb-4"
              >
                <v-icon start>mdi-login</v-icon>
                Войти
              </v-btn>
            </v-form>
            <v-divider class="my-4"></v-divider>
            <v-btn
              variant="outlined"
              color="primary"
              size="large"
              block
              class="register-btn"
              @click="showRegister = true"
            >
              <v-icon start>mdi-account-plus</v-icon>
              Регистрация
            </v-btn>
          </v-card-text>
        </v-card>

        <v-dialog v-model="showRegister" max-width="600">
          <v-card>
            <v-card-title class="text-h5 pa-4">
              <v-icon color="primary" class="mr-2">mdi-account-plus</v-icon>
              Регистрация нового пользователя
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="pa-6">
              <v-form @submit.prevent="handleRegister">
                <v-text-field
                  v-model="registerForm.username"
                  label="Имя пользователя"
                  prepend-inner-icon="mdi-account"
                  variant="outlined"
                  density="comfortable"
                  required
                  class="mb-3"
                ></v-text-field>
                <v-text-field
                  v-model="registerForm.email"
                  label="Email"
                  type="email"
                  prepend-inner-icon="mdi-email"
                  variant="outlined"
                  density="comfortable"
                  required
                  class="mb-3"
                ></v-text-field>
                <v-text-field
                  v-model="registerForm.password"
                  label="Пароль"
                  type="password"
                  prepend-inner-icon="mdi-lock"
                  variant="outlined"
                  density="comfortable"
                  required
                  class="mb-3"
                ></v-text-field>
                <v-text-field
                  v-model="registerForm.re_password"
                  label="Подтвердите пароль"
                  type="password"
                  prepend-inner-icon="mdi-lock-check"
                  variant="outlined"
                  density="comfortable"
                  required
                  class="mb-4"
                ></v-text-field>
                <v-alert
                  v-if="registerError"
                  type="error"
                  class="mb-4"
                  variant="tonal"
                >
                  {{ registerError }}
                </v-alert>
                <v-card-actions class="pa-0">
                  <v-spacer></v-spacer>
                  <v-btn
                    variant="outlined"
                    class="mr-2"
                    @click="showRegister = false"
                  >
                    Отмена
                  </v-btn>
                  <v-btn
                    type="submit"
                    color="primary"
                    :loading="registerLoading"
                  >
                    <v-icon start>mdi-check</v-icon>
                    Зарегистрироваться
                  </v-btn>
                </v-card-actions>
              </v-form>
            </v-card-text>
          </v-card>
        </v-dialog>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const errors = ref({})

const showRegister = ref(false)
const registerForm = ref({
  username: '',
  email: '',
  password: '',
  re_password: ''
})
const registerLoading = ref(false)
const registerError = ref('')

const handleLogin = async () => {
  loading.value = true
  errorMessage.value = ''
  successMessage.value = ''
  errors.value = {}

  const result = await authStore.login({
    username: username.value,
    password: password.value
  })

  if (result.success) {
    router.push('/dashboard')
  } else {
    errorMessage.value = result.error
  }

  loading.value = false
}

const handleRegister = async () => {
  registerLoading.value = true
  registerError.value = ''
  errorMessage.value = ''

  const result = await authStore.register(registerForm.value)

  if (result.success) {
    showRegister.value = false
    successMessage.value = 'Регистрация успешна! Теперь вы можете войти в систему.'
    registerForm.value = {
      username: '',
      email: '',
      password: '',
      re_password: ''
    }
    // Очищаем сообщение через 5 секунд
    setTimeout(() => {
      successMessage.value = ''
    }, 5000)
  } else {
    registerError.value = typeof result.error === 'string' ? result.error : JSON.stringify(result.error)
  }

  registerLoading.value = false
}
</script>

<style scoped>
.register-btn {
  border: 2px solid rgb(25, 118, 210);
  font-weight: 500;
}

.register-btn:hover {
  border-width: 2px;
  background-color: rgba(25, 118, 210, 0.08);
}
</style>

