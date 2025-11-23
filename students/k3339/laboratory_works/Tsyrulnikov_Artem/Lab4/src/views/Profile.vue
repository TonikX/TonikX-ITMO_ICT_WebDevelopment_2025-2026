<template>
  <v-card max-width="500" class="mx-auto">
    <v-card-title>Профиль</v-card-title>
    <v-card-text>
      <v-form @submit.prevent="submit">
        <v-text-field v-model="form.username" label="Логин" disabled />
        <v-text-field v-model="form.first_name" label="Имя" />
        <v-text-field v-model="form.last_name" label="Фамилия" />
        <v-text-field v-model="form.email" label="Email" type="email" />
        <v-alert v-if="message" :type="messageType" class="mb-3">{{ message }}</v-alert>
        <v-btn type="submit" color="primary" :loading="loading">Сохранить</v-btn>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const form = reactive({ username: '', first_name: '', last_name: '', email: '' })
const loading = ref(false)
const message = ref('')
const messageType = ref('success')

onMounted(async () => {
  await auth.fetchUser()
  if (auth.user) Object.assign(form, auth.user)
})

const submit = async () => {
  loading.value = true
  message.value = ''
  try {
    await auth.updateUser({ first_name: form.first_name, last_name: form.last_name, email: form.email })
    message.value = 'Данные сохранены'
    messageType.value = 'success'
  } catch {
    message.value = 'Ошибка сохранения'
    messageType.value = 'error'
  }
  loading.value = false
}
</script>
