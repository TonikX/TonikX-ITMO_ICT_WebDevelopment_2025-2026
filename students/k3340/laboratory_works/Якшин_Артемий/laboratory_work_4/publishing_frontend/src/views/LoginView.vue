<template>
  <div class="login-page">
    <div class="login-background"></div>
    <v-container fluid class="fill-height">
      <v-row justify="center" align="center">
        <v-col cols="12" sm="8" md="5" lg="4" xl="3">
          <v-card class="login-card pa-6" elevation="12">
            <div class="text-center mb-6">
              <v-avatar size="80" color="primary" class="mb-4">
                <v-icon size="48" color="secondary">mdi-book-open-variant</v-icon>
              </v-avatar>
              <h1 class="login-title">Издательский дом</h1>
              <p class="text-medium-emphasis">Войдите в систему</p>
            </div>

            <v-form ref="form" v-model="valid" @submit.prevent="handleLogin">
              <v-text-field
                v-model="credentials.username"
                label="Имя пользователя"
                prepend-inner-icon="mdi-account"
                :rules="[rules.required]"
                :disabled="loading"
                class="mb-2"
              ></v-text-field>

              <v-text-field
                v-model="credentials.password"
                label="Пароль"
                prepend-inner-icon="mdi-lock"
                :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                :type="showPassword ? 'text' : 'password'"
                :rules="[rules.required]"
                :disabled="loading"
                @click:append-inner="showPassword = !showPassword"
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

              <v-btn
                type="submit"
                color="primary"
                size="large"
                block
                :loading="loading"
                :disabled="!valid"
                class="mb-4"
              >
                <v-icon left>mdi-login</v-icon>
                Войти
              </v-btn>

              <v-divider class="my-4"></v-divider>

              <p class="text-center text-body-2 text-medium-emphasis">
                Нет аккаунта?
                <router-link :to="{ name: 'register' }" class="text-primary font-weight-medium">
                  Зарегистрироваться
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
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const form = ref(null)
const valid = ref(false)
const loading = ref(false)
const showPassword = ref(false)
const error = ref(null)

const credentials = reactive({
  username: '',
  password: ''
})

const rules = {
  required: (v) => !!v || 'Обязательное поле'
}

const handleLogin = async () => {
  const { valid: isValid } = await form.value.validate()
  if (!isValid) return

  loading.value = true
  error.value = null

  const result = await authStore.login(credentials)

  if (result.success) {
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  } else {
    error.value = result.error
  }

  loading.value = false
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-background {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #2D3E50 0%, #1A252F 50%, #2D3E50 100%);
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
}

.login-background::before {
  content: '';
  position: absolute;
  inset: 0;
  background: 
    radial-gradient(circle at 20% 30%, rgba(201, 169, 89, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(201, 169, 89, 0.1) 0%, transparent 50%);
}

.login-background::after {
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

.login-card {
  position: relative;
  background: rgba(255, 255, 255, 0.98) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(201, 169, 89, 0.3) !important;
}

.login-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2rem;
  font-weight: 600;
  color: #2D3E50;
  letter-spacing: 0.02em;
}
</style>

