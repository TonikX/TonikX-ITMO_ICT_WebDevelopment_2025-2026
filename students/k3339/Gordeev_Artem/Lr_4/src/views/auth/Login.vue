<template>
  <v-card class="mx-auto pa-12 pb-8" elevation="8" max-width="448" rounded="lg">
    <div class="text-subtitle-1 text-medium-emphasis">Аккаунт</div>
    <div class="text-h4 font-weight-bold mb-4">Вход</div>

    <v-form @submit.prevent="handleLogin" v-model="isValid">
      <div class="text-subtitle-1 text-medium-emphasis">Имя пользователя</div>
      <v-text-field
        v-model="form.username"
        density="compact"
        placeholder="Имя пользователя"
        prepend-inner-icon="mdi-account"
        variant="outlined"
        :rules="[rules.required]"
      ></v-text-field>

      <div class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
        Пароль
      </div>
      <v-text-field
        v-model="form.password"
        :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
        :type="visible ? 'text' : 'password'"
        density="compact"
        placeholder="Введите пароль"
        prepend-inner-icon="mdi-lock-outline"
        variant="outlined"
        @click:append-inner="visible = !visible"
        :rules="[rules.required]"
      ></v-text-field>



      <v-btn
        block
        class="mb-8"
        color="blue"
        size="large"
        variant="tonal"
        type="submit"
        :loading="loading"
        :disabled="!isValid"
      >
        Войти
      </v-btn>

      <v-card-text class="text-center">
        <router-link class="text-blue text-decoration-none" to="/register">
          Зарегистрироваться <v-icon icon="mdi-chevron-right"></v-icon>
        </router-link>
      </v-card-text>
    </v-form>
  </v-card>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useAlertStore } from '@/stores/alert'

const router = useRouter()
const authStore = useAuthStore()
const alertStore = useAlertStore()

const visible = ref(false)
const isValid = ref(false)
const loading = ref(false)

const form = reactive({
  username: '',
  password: ''
})

const rules = {
  required: value => !!value || 'Required.',
}

const handleLogin = async () => {
  if (!isValid.value) return
  
  loading.value = true
  
  try {
    await authStore.login(form)
    router.push('/dashboard')
  } catch (err) {
    console.error(err)
    alertStore.showError(err)
  } finally {
    loading.value = false
  }
}
</script>
