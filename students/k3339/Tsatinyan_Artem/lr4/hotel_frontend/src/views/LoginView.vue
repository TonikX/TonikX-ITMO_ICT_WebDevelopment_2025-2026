<template>
  <v-container class="fill-height bg-deep-purple-lighten-5" fluid>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-5" rounded="lg">
          <div class="text-center pt-6 pb-2">
            <v-avatar color="primary" size="64">
              <v-icon size="40" color="white">mdi-office-building</v-icon>
            </v-avatar>
            <h2 class="text-h5 font-weight-bold mt-3 text-primary">Hotel Admin</h2>
            <div class="text-subtitle-2 text-grey">Вход в систему</div>
          </div>

          <v-card-text class="px-6 pb-6">
            <v-form @submit.prevent="onSubmit">
              <v-text-field
                v-model="username"
                label="Логин"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                density="comfortable"
                class="mb-2"
                required
              />
              <v-text-field
                v-model="password"
                label="Пароль"
                prepend-inner-icon="mdi-lock"
                type="password"
                variant="outlined"
                density="comfortable"
                required
              />

              <v-alert v-if="error" type="error" density="compact" variant="tonal" class="mb-4">
                {{ error }}
              </v-alert>

              <v-btn
                :loading="loading"
                type="submit"
                color="primary"
                block
                size="large"
                class="mt-2"
              >
                Войти
              </v-btn>
            </v-form>
          </v-card-text>

          <v-divider></v-divider>

          <div class="pa-4 text-center bg-grey-lighten-5">
            <span class="text-body-2 text-grey">Нет аккаунта?</span>
            <router-link to="/register" class="text-primary font-weight-bold ml-2 text-decoration-none">
              Регистрация
            </router-link>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/api'
import { setAuthToken } from '../auth'

const router = useRouter()
const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

onMounted(() => {
  setAuthToken(null)
})

const onSubmit = async () => {
  error.value = ''
  loading.value = true
  try {
    delete api.defaults.headers.common['Authorization']
    const { data } = await api.post('/auth/token/login/', {
      username: username.value,
      password: password.value,
    })
    setAuthToken(data.auth_token)
    router.push('/dashboard')
  } catch (e) {
    if (e.response && e.response.status === 400) {
      error.value = 'Неверный логин или пароль'
    } else {
      error.value = 'Ошибка сервера'
    }
  } finally {
    loading.value = false
  }
}
</script>
