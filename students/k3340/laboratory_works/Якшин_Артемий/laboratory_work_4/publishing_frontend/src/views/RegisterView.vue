<template>
  <div class="register-page">
    <div class="register-background"></div>
    <v-container fluid class="fill-height">
      <v-row justify="center" align="center">
        <v-col cols="12" sm="8" md="6" lg="5" xl="4">
          <v-card class="register-card pa-6" elevation="12">
            <div class="text-center mb-6">
              <v-avatar size="80" color="primary" class="mb-4">
                <v-icon size="48" color="secondary">mdi-account-plus</v-icon>
              </v-avatar>
              <h1 class="register-title">Регистрация</h1>
              <p class="text-medium-emphasis">Создайте новый аккаунт</p>
            </div>

            <v-form ref="form" v-model="valid" @submit.prevent="handleRegister">
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="userData.username"
                    label="Имя пользователя"
                    prepend-inner-icon="mdi-account"
                    :rules="[rules.required, rules.username]"
                    :disabled="loading"
                    counter="150"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="userData.email"
                    label="Email"
                    type="email"
                    prepend-inner-icon="mdi-email"
                    :rules="[rules.required, rules.email]"
                    :disabled="loading"
                  ></v-text-field>
                </v-col>
              </v-row>

              <v-text-field
                v-model="userData.password"
                label="Пароль"
                prepend-inner-icon="mdi-lock"
                :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                :type="showPassword ? 'text' : 'password'"
                :rules="[rules.required, rules.minLength]"
                :disabled="loading"
                @click:append-inner="showPassword = !showPassword"
                hint="Минимум 8 символов"
                class="mb-2"
              ></v-text-field>

              <v-text-field
                v-model="userData.re_password"
                label="Подтвердите пароль"
                prepend-inner-icon="mdi-lock-check"
                :append-inner-icon="showConfirmPassword ? 'mdi-eye-off' : 'mdi-eye'"
                :type="showConfirmPassword ? 'text' : 'password'"
                :rules="[rules.required, rules.passwordMatch]"
                :disabled="loading"
                @click:append-inner="showConfirmPassword = !showConfirmPassword"
                class="mb-4"
              ></v-text-field>

              <v-alert
                v-if="error"
                type="error"
                variant="tonal"
                class="mb-4"
                closable
                @click:close="error = null"
              >
                {{ error }}
              </v-alert>

              <v-alert
                v-if="success"
                type="success"
                variant="tonal"
                class="mb-4"
              >
                Регистрация успешна! Теперь вы можете войти в систему.
              </v-alert>

              <v-btn
                type="submit"
                color="primary"
                size="large"
                block
                :loading="loading"
                :disabled="!valid || success"
                class="mb-4"
              >
                <v-icon left>mdi-account-plus</v-icon>
                Зарегистрироваться
              </v-btn>

              <v-divider class="my-4"></v-divider>

              <p class="text-center text-body-2 text-medium-emphasis">
                Уже есть аккаунт?
                <router-link :to="{ name: 'login' }" class="text-primary font-weight-medium">
                  Войти
                </router-link>
              </p>
            </v-form>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const form = ref(null)
const valid = ref(false)
const loading = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const error = ref(null)
const success = ref(false)

const userData = reactive({
  username: '',
  email: '',
  password: '',
  re_password: ''
})

const rules = {
  required: (v) => !!v || 'Обязательное поле',
  email: (v) => /.+@.+\..+/.test(v) || 'Введите корректный email',
  username: (v) => /^[\w.@+-]+$/.test(v) || 'Только буквы, цифры и @/./+/-/_',
  minLength: (v) => v.length >= 8 || 'Минимум 8 символов',
  passwordMatch: (v) => v === userData.password || 'Пароли не совпадают'
}

const handleRegister = async () => {
  const { valid: isValid } = await form.value.validate()
  if (!isValid) return

  loading.value = true
  error.value = null
  success.value = false

  const result = await authStore.register(userData)

  if (result.success) {
    success.value = true
    // Clear form
    userData.username = ''
    userData.email = ''
    userData.password = ''
    userData.re_password = ''
  } else {
    error.value = result.error
  }

  loading.value = false
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.register-background {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #2D3E50 0%, #1A252F 50%, #2D3E50 100%);
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
}

.register-background::before {
  content: '';
  position: absolute;
  inset: 0;
  background: 
    radial-gradient(circle at 80% 20%, rgba(201, 169, 89, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 20% 80%, rgba(201, 169, 89, 0.1) 0%, transparent 50%);
}

.register-background::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23C9A959' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  opacity: 0.5;
}

@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.register-card {
  position: relative;
  background: rgba(255, 255, 255, 0.98) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(201, 169, 89, 0.3) !important;
}

.register-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2rem;
  font-weight: 600;
  color: #2D3E50;
  letter-spacing: 0.02em;
}
</style>

