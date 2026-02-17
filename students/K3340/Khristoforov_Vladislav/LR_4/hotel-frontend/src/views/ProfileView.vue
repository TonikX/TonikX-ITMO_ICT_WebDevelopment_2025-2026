<script setup>
/**
 * ProfileView.vue - Страница настроек профиля текущего пользователя.
 * Позволяет просматривать и редактировать данные (логин, email) администратора.
 */
import { ref, onMounted } from 'vue'
import api from '../services/api'

// Состояние профиля пользователя
const user = ref({
  id: null,
  username: '',
  email: '',
})

const loading = ref(false)
const message = ref({ text: '', type: '' }) // Для уведомлений об успехе или ошибке

// Валидация
const formRef = ref(null)
const valid = ref(false)
const rules = {
  required: v => !!v || 'Обязательное поле',
  email: v => /.+@.+\..+/.test(v) || 'Введите корректный Email'
}

/**
 * Загрузка данных профиля из Django (Djoser me endpoint).
 */
async function fetchProfile() {
  loading.value = true
  try {
    const response = await api.get('/auth/users/me/')
    user.value = response.data
  } catch (e) {
    console.error('Ошибка загрузки профиля:', e)
    message.value = { text: 'Не удалось загрузить данные профиля', type: 'error' }
  } finally {
    loading.value = false
  }
}

/**
 * Обновление данных профиля.
 * Используется метод PATCH для частичного изменения данных.
 */
async function updateProfile() {
  const { valid: isFormValid } = await formRef.value.validate()
  if (!isFormValid) return

  loading.value = true
  message.value = { text: '', type: '' }

  try {
    // Отправляем изменения на сервер
    await api.patch('/auth/users/me/', {
      email: user.value.email,
      username: user.value.username,
    })
    message.value = { text: 'Данные успешно обновлены!', type: 'success' }
  } catch (e) {
    console.error('Ошибка обновления профиля:', e)
    const serverError = e.response?.data?.username ? 'Это имя пользователя уже занято' : 'Ошибка при обновлении данных'
    message.value = { text: serverError, type: 'error' }
  } finally {
    loading.value = false
  }
}

// Загружаем данные при открытии страницы
onMounted(fetchProfile)
</script>

<template>
  <!-- Контейнер с отступом сверху -->
  <v-container class="mt-10 d-flex justify-center">
    <v-card width="600" elevation="4" class="rounded-lg">

      <!-- Заголовок карточки -->
      <v-card-title class="text-h5 pa-4 bg-indigo-darken-3 text-white d-flex align-center">
        <v-icon icon="mdi-account-cog" class="mr-3"></v-icon>
        Настройки профиля
      </v-card-title>

      <v-card-text class="pa-6">
        <v-form ref="formRef" v-model="valid" @submit.prevent="updateProfile">

          <v-row dense>
            <!-- ID пользователя (только для чтения) -->
            <v-col cols="12">
              <v-text-field :model-value="user.id" label="Системный ID" variant="outlined" density="compact" prefix="#"
                readonly disabled></v-text-field>
            </v-col>

            <!-- Логин -->
            <v-col cols="12">
              <v-text-field v-model="user.username" label="Логин (Username)" variant="outlined"
                prepend-inner-icon="mdi-account" :rules="[rules.required]"></v-text-field>
            </v-col>

            <!-- Email -->
            <v-col cols="12">
              <v-text-field v-model="user.email" label="Email" variant="outlined" prepend-inner-icon="mdi-email"
                :rules="[rules.required, rules.email]"></v-text-field>
            </v-col>
          </v-row>

          <!-- Блок уведомлений -->
          <v-alert v-if="message.text" :type="message.type" class="mb-4" variant="tonal" density="compact">
            {{ message.text }}
          </v-alert>

          <!-- Кнопка сохранения -->
          <div class="d-flex justify-end mt-4">
            <v-btn type="submit" color="indigo-darken-2" :loading="loading" prepend-icon="mdi-check" variant="flat">
              Сохранить изменения
            </v-btn>
          </div>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<style scoped>
/* Стили для страницы профиля */
</style>