<template>
  <v-container class="mt-10" max-width="500">
    <v-card>
      <v-card-title class="justify-center">
        👤 {{ username }}
      </v-card-title>

      <v-card-subtitle class="text-center">
        Профиль пользователя
      </v-card-subtitle>

      <v-divider class="my-3"></v-divider>

      <v-card-text>
        <v-text-field
          v-model="currentPassword"
          label="Старый пароль"
          type="password"
          outlined
          dense
        ></v-text-field>

        <v-text-field
          v-model="newPassword"
          label="Новый пароль"
          type="password"
          outlined
          dense
        ></v-text-field>

        <v-btn
          color="#00850d"
          block
          class="mt-3"
          @click="changePassword"
        >
          Сменить пароль
        </v-btn>
        <v-btn
          color="#1B5E20"
          block
          class="mt-3"
          @click="logout"
        >
          Выйти из аккаунта
        </v-btn>

        <div
          v-if="success"
          class="mt-3 text-center"
          style="color:green"
        >
          {{ success }}
        </div>

        <div
          v-if="error"
          class="mt-3 text-center"
          style="color:red"
        >
          {{ error }}
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'
import { useRouter } from 'vue-router'

const router = useRouter()

const username = ref('')
const currentPassword = ref('')
const newPassword = ref('')
const success = ref('')
const error = ref('')

onMounted(async () => {
  try {
    const res = await api.get('auth/users/me/')
    username.value = res.data.username || res.data.email
  } catch {
    localStorage.removeItem('token')
    router.push('/login')
  }
})

const logout = async () => {
  try {
    await api.post('auth/token/logout/')
  } catch (e) {
    console.warn('Ошибка logout на сервере', e)
  } finally {
    localStorage.removeItem('token')
    router.push('/login')
  }
}

const changePassword = async () => {
  success.value = ''
  error.value = ''

  if (!currentPassword.value || !newPassword.value) {
    error.value = 'Заполните оба поля'
    return
  }

  try {
    await api.post('auth/users/set_password/', {
      current_password: currentPassword.value,
      new_password: newPassword.value
    })
    success.value = 'Пароль успешно изменён'
    currentPassword.value = ''
    newPassword.value = ''
  } catch {
    error.value = 'Ошибка смены пароля'
  }
}
</script>
