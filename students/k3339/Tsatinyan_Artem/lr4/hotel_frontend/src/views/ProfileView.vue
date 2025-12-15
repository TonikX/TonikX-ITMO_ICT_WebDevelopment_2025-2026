<template>
  <div>
    <h1>Профиль</h1>

    <v-alert
      v-if="!loaded && !error"
      type="info"
      class="mb-4"
    >
      Загружаем данные пользователя...
    </v-alert>

    <v-alert
      v-if="error"
      type="error"
      class="mb-4"
    >
      {{ error }}
    </v-alert>

    <v-form
      v-if="loaded"
      @submit.prevent="onSave"
      style="max-width: 400px;"
    >
      <v-text-field v-model="username" label="Логин" disabled />
      <v-text-field v-model="email" label="Email" />
      <v-btn :loading="saving" type="submit" color="primary">Сохранить</v-btn>
    </v-form>

    <p v-if="success" class="mt-4" style="color: green;">Данные обновлены</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/api'

const username = ref('')
const email = ref('')
const loaded = ref(false)
const error = ref('')
const saving = ref(false)
const success = ref(false)

onMounted(async () => {
  try {
    const { data } = await api.get('/auth/users/me/')
    username.value = data.username
    email.value = data.email || ''
    loaded.value = true
  } catch (e) {
    error.value = 'Не удалось загрузить профиль. Возможно, вы не авторизованы.'
  }
})

const onSave = async () => {
  saving.value = true
  success.value = false
  error.value = ''
  try {
    await api.patch('/auth/users/me/', {
      email: email.value,
    })
    success.value = true
  } catch (e) {
    error.value = 'Ошибка при сохранении профиля'
  } finally {
    saving.value = false
  }
}
</script>
