<!-- components/Auth/LoginForm.vue -->
<template>
  <v-form @submit.prevent="handleLogin" class="mt-4">
    <v-text-field
      v-model="form.username"
      label="Username"
      type="username"
      required
      variant="outlined"
      prepend-inner-icon="mdi-account"
      :rules="[rules.required]"
      class="mb-4"
    ></v-text-field>

    <v-text-field
      v-model="form.password"
      label="Пароль"
      type="password"
      required
      variant="outlined"
      prepend-inner-icon="mdi-lock"
      :rules="[rules.required]"
      class="mb-2"
    ></v-text-field>

    <div class="d-flex justify-end mb-6">
      <v-btn
        variant="text"
        color="primary"
        size="small"
      >
        Забыли пароль?
      </v-btn>
    </div>

    <v-btn
      type="submit"
      color="primary"
      size="large"
      block
      :loading="loading"
      class="mb-4"
    >
      <v-icon start icon="mdi-login"></v-icon>
      Войти в систему
    </v-btn>

    <v-alert
      v-if="error"
      type="error"
      variant="tonal"
      density="compact"
      class="mt-4"
    >
      {{ error }}
    </v-alert>
  </v-form>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const form = ref({
  username: '',
  password: ''
})

const loading = ref(false)
const error = ref('')

const rules = {
  required: value => !!value || 'Обязательное поле',
}

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const userData = {
      username: form.value.username,
      password: form.value.password,
    }
    //console.log(userData);
    await authStore.login(userData)
    router.push('/')
  } catch (err) {
    console.log(err);
    error.value = 'Неверный username или пароль'
  } finally {
    loading.value = false
  }
}
</script>