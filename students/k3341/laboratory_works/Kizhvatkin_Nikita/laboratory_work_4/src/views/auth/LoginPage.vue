<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-card style="width: 520px; max-width: 100%">
      <v-card-title class="text-h6">Вход</v-card-title>
      <v-card-text>
        <v-alert v-if="error" type="error" variant="tonal" class="mb-4">
          {{ error }}
        </v-alert>

        <v-form @submit.prevent="onSubmit" ref="formRef">
          <v-text-field v-model="username" label="Логин" variant="outlined" density="compact" :rules="[req]" />
          <v-text-field v-model="password" label="Пароль" type="password" variant="outlined" density="compact" :rules="[req]" />
          <v-btn class="mt-3" color="primary" block type="submit" :loading="loading">
            Войти
          </v-btn>
        </v-form>

        <div class="mt-4 text-body-2">
          Нет аккаунта?
          <router-link :to="{name:'register'}">Регистрация</router-link>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')
const formRef = ref(null)

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
auth.hydrate()

const req = (v) => !!v || 'Обязательное поле'

async function onSubmit() {
  const res = await formRef.value?.validate?.()
  if (res && !res.valid) return

  loading.value = true
  error.value = ''
  try {
    await auth.login({ username: username.value, password: password.value })
    const next = route.query.next || '/companies'
    router.push(String(next))
  } catch (e) {
    error.value = e?.message || 'Не удалось войти'
  } finally {
    loading.value = false
  }
}
</script>
