<template>
  <v-container class="fill-height" fluid>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="login-card" elevation="8">
          <v-card-title class="text-center pt-6 pb-4">
            <h2 class="text-h5 font-weight-bold">Вход в систему</h2>
          </v-card-title>
          
          <v-card-text class="pt-2">
            <v-form @submit.prevent="handleLogin">
              <v-text-field
                v-model="form.username"
                label="Логин"
                variant="outlined"
                :disabled="isLoading"
                required
                prepend-inner-icon="mdi-account"
                class="mb-4"
                :rules="[v => !!v || 'Введите логин']"
              ></v-text-field>
              
              <v-text-field
                v-model="form.password"
                label="Пароль"
                variant="outlined"
                :type="showPassword ? 'text' : 'password'"
                :disabled="isLoading"
                required
                prepend-inner-icon="mdi-lock"
                :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append-inner="showPassword = !showPassword"
                class="mb-2"
                :rules="[v => !!v || 'Введите пароль']"
              ></v-text-field>
              
              <v-alert
                v-if="error"
                type="error"
                variant="tonal"
                density="compact"
                class="mb-4"
                :text="getErrorMessage()"
              ></v-alert>
              
              <v-btn
                type="submit"
                color="primary"
                size="large"
                block
                :loading="isLoading"
                :disabled="isLoading"
                class="mt-2"
              >
                <template v-if="isLoading">Вход...</template>
                <template v-else>Войти</template>
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const form = reactive({
  username: '',
  password: ''
})

const showPassword = ref(false)
const error = ref(null)

const isLoading = computed(() => authStore.isLoading)

const getErrorMessage = () => {
  if (!error.value) return ''
  
  if (typeof error.value === 'object') {
    if (error.value.non_field_errors) {
      return error.value.non_field_errors[0]
    }
    return 'Неверные данные для входа'
  }
  
  return error.value
}

const handleLogin = async () => {
  error.value = null
  
  const result = await authStore.login({
    username: form.username,
    password: form.password
  })
  
  if (!result.success) {
    error.value = result.error
  }
}
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  border-radius: 16px;
  overflow: hidden;
}

.v-card-title h2 {
  color: #1976D2;
}
</style>