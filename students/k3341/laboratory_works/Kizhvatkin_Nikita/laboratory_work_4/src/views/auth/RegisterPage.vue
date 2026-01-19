<template>
  <v-card>
    <v-card-title class="text-h6">Регистрация</v-card-title>
    <v-card-text>
      <v-alert v-if="error" type="error" variant="tonal" class="mb-4">
        {{ error }}
      </v-alert>
      <v-form @submit.prevent="onSubmit" ref="formRef">
        <div class="d-flex flex-wrap" style="gap: 12px">
          <v-text-field
            v-model="form.username"
            label="Логин"
            variant="outlined"
            density="compact"
            :rules="[req]"
            style="flex:1 0 280px"
          />
          <v-text-field
            v-model="form.email"
            label="Email"
            variant="outlined"
            density="compact"
            style="flex:1 0 280px"
          />
          <v-text-field
            v-model="form.first_name"
            label="Имя"
            variant="outlined"
            density="compact"
            style="flex:1 0 280px"
          />
          <v-text-field
            v-model="form.last_name"
            label="Фамилия"
            variant="outlined"
            density="compact"
            style="flex:1 0 280px"
          />
          <v-text-field
            v-model="form.password"
            label="Пароль"
            type="password"
            variant="outlined"
            density="compact"
            :rules="[req]"
            style="flex:1 0 280px"
          />
          <v-text-field
            v-model="form.re_password"
            label="Повторите пароль"
            type="password"
            variant="outlined"
            density="compact"
            :rules="[req, samePassword]"
            style="flex:1 0 280px"
          />
        </div>
        <v-btn class="mt-3" color="primary" block type="submit" :loading="loading">
          Зарегистрироваться
        </v-btn>
      </v-form>
      <div class="mt-4 text-body-2">
        Уже есть аккаунт?
        <router-link :to="{ name: 'login' }">Войти</router-link>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const auth = useAuthStore()
auth.hydrate()

const form = reactive({
  username: '',
  email: '',
  password: '',
  re_password: '',
  first_name: '',
  last_name: '',
})

const loading = ref(false)
const error = ref('')
const formRef = ref(null)

const req = (v) => !!v || 'Обязательное поле'
const samePassword = (v) => v === form.password || 'Пароли не совпадают'

async function onSubmit() {
  const res = await formRef.value?.validate?.()
  if (res && !res.valid) return

  loading.value = true
  error.value = ''

  try {
    await auth.register({ ...form })
    await auth.login({ username: form.username, password: form.password })
    router.push('/companies')
  } catch (e) {
    const data = e?.response?.data
    if (data && typeof data === 'object') {
      const parts = []
      for (const [k, v] of Object.entries(data)) {
        parts.push(`${k}: ${Array.isArray(v) ? v.join(', ') : String(v)}`)
      }
      error.value = parts.join(' | ')
    } else {
      error.value = e?.message || 'Не удалось зарегистрироваться'
    }
  } finally {
    loading.value = false
  }
}
</script>
