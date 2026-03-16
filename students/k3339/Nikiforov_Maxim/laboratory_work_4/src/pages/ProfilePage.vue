<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const username = ref('')
const newPassword = ref('')
const reNewPassword = ref('')
const currentPassword = ref('')
const message = ref('')
const error = ref('')
const loading = ref(false)

onMounted(() => {
  if (auth.user) username.value = auth.user.username
})

async function onSubmit() {
  error.value = ''
  message.value = ''
  const payload: { username?: string; current_password?: string; new_password?: string; re_new_password?: string } = {}
  if (username.value && username.value !== auth.user?.username) payload.username = username.value
  if (newPassword.value) {
    if (!currentPassword.value) {
      error.value = 'Введите текущий пароль для смены пароля'
      return
    }
    if (newPassword.value !== reNewPassword.value) {
      error.value = 'Новый пароль и повтор не совпадают'
      return
    }
    if (newPassword.value.length < 8) {
      error.value = 'Новый пароль не менее 8 символов'
      return
    }
    payload.current_password = currentPassword.value
    payload.new_password = newPassword.value
    payload.re_new_password = reNewPassword.value
  }
  if (Object.keys(payload).length === 0) {
    message.value = 'Нет изменений'
    return
  }
  loading.value = true
  try {
    await auth.updateProfile(payload)
    message.value = 'Данные сохранены'
    newPassword.value = ''
    reNewPassword.value = ''
    currentPassword.value = ''
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e)
    error.value = msg
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <v-card>
    <v-card-title>Учётные данные</v-card-title>
    <v-card-text>
      <v-form @submit.prevent="onSubmit">
        <v-text-field
          v-model="username"
          label="Имя пользователя"
          type="text"
        />
        <v-text-field
          v-model="currentPassword"
          label="Текущий пароль (для смены пароля)"
          type="password"
          autocomplete="current-password"
        />
        <v-text-field
          v-model="newPassword"
          label="Новый пароль"
          type="password"
          autocomplete="new-password"
        />
        <v-text-field
          v-model="reNewPassword"
          label="Повтор нового пароля"
          type="password"
          autocomplete="new-password"
        />
        <v-alert v-if="error" type="error" density="compact" class="mt-2">
          {{ error }}
        </v-alert>
        <v-alert v-if="message" type="success" density="compact" class="mt-2">
          {{ message }}
        </v-alert>
        <v-btn type="submit" color="primary" class="mt-4" :loading="loading">
          Сохранить
        </v-btn>
      </v-form>
    </v-card-text>
  </v-card>
</template>
