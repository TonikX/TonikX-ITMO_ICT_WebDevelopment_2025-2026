<template>
  <div class="link-reader-view">
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="6">
          <v-card>
            <!-- Заголовок -->
            <v-card-title class="text-h5">
              <v-icon left color="primary">mdi-link</v-icon>
              Привязать читательский билет
            </v-card-title>

            <v-card-text>
              <v-form @submit.prevent="linkReader">
                <!-- Поле для номера билета -->
                <v-text-field v-model="card" label="Номер читательского билета" placeholder="Б-26-0001" required
                  variant="outlined" prepend-inner-icon="mdi-card-account-details" class="mb-3" />

                <!-- Поле для паспорта -->
                <v-text-field v-model="pass" label="Номер паспорта" placeholder="1234 567890" required
                  variant="outlined" prepend-inner-icon="mdi-passport" class="mb-3" />

                <!-- Сообщение об ошибке -->
                <v-alert v-if="error" type="error" class="mt-3" closable @click:close="error = ''">
                  {{ error }}
                </v-alert>

                <!-- Кнопка отправки -->
                <v-btn type="submit" color="primary" block size="large" :loading="loading">
                  Привязать билет
                </v-btn>
              </v-form>

              <v-divider class="my-4" />

              <!-- Подсказка -->
              <p class="text-caption text-grey">
                Введите данные из читательского билета.<br>
                Если билета нет — обратитесь к библиотекарю.
              </p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../api/client'

const router = useRouter()

// Состояние формы
const card = ref('')      // номер билета
const pass = ref('')      // паспорт
const loading = ref(false)
const error = ref('')

// Привязка читательского билета к аккаунту
const linkReader = async () => {
  // Валидация
  if (!card.value || !pass.value) {
    error.value = 'Заполните все поля'
    return
  }

  loading.value = true
  error.value = ''

  try {
    // Отправляем запрос на привязку
    await apiClient.post('user/link-reader/', {
      card_number: card.value,
      passport: pass.value
    })
    // Успех — переходим в профиль
    router.push('/profile')
  } catch (err) {
    console.error('Ошибка привязки:', err)
    // Обработка разных типов ошибок
    if (err.response?.status === 404) {
      error.value = 'Читатель с такими данными не найден'
    } else if (err.response?.data?.error) {
      error.value = err.response.data.error
    } else {
      error.value = 'Ошибка привязки. Попробуйте позже.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.link-reader-view {
  padding: 40px 20px;
  min-height: calc(100vh - 200px);
}
</style>