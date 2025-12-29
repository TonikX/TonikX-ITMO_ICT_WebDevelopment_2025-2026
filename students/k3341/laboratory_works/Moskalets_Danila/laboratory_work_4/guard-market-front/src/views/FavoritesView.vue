<template>
  <div>
    <!-- Уведомление об успехе -->
    <SuccessNotification
        :show="successSnackbar.show"
        :text="successSnackbar.text"
        :color="successSnackbar.color"
        :icon="successSnackbar.icon"
        @close="successSnackbar.show = false"
    />

    <!-- Загрузка -->
    <div v-if="isLoading" class="text-center py-10">
      <v-progress-circular
          indeterminate
          color="primary"
          size="64"
      ></v-progress-circular>
      <p class="mt-4">Загрузка избранного...</p>
    </div>

    <!-- Ошибка -->
    <v-alert
        v-else-if="error"
        type="error"
        class="mb-4"
        @click:close="error = null"
        closable
    >
      {{ error }}
    </v-alert>

    <!-- Список избранного -->
    <div v-else>
      <v-row class="mb-6">
        <v-col cols="12">
          <v-card class="pa-6">
            <v-card-title class="text-h4 mb-2">
              <v-icon large color="pink" class="mr-3">mdi-heart</v-icon>
              Избранные услуги
            </v-card-title>
            <v-card-subtitle class="text-body-1">
              Здесь собраны услуги, которые вы добавили в избранное
              <v-chip
                  v-if="favorites.length > 0"
                  color="primary"
                  size="small"
                  class="ml-2"
              >
                {{ favorites.length }} услуг
              </v-chip>
            </v-card-subtitle>
          </v-card>
        </v-col>
      </v-row>

      <v-row v-if="favorites.length > 0">
        <v-col
            v-for="favorite in favorites"
            :key="favorite.id"
            cols="12"
            md="6"
            lg="4"
        >
          <FavoriteServiceCard
              :favorite-id="favorite.id"
              :service="getServiceData(favorite)"
              :loading="favoritesLoading"
              @create-request="createRequest"
              @remove-from-favorites="removeFromFavorites"
          />
        </v-col>
      </v-row>

      <!-- Пустой список -->
      <div v-else class="text-center py-10">
        <v-alert type="info" class="mb-4">
          <template v-slot:prepend>
            <v-icon size="64" color="info">mdi-heart-outline</v-icon>
          </template>
          <div class="text-h6 mb-2">У вас пока нет избранных услуг</div>
          <p class="text-body-1">
            Добавляйте понравившиеся услуги в избранное, чтобы вернуться к ним позже
          </p>
          <div class="mt-4">
            <v-btn
                to="/services"
                color="primary"
                size="large"
                class="mr-2"
            >
              <v-icon start icon="mdi-magnify"></v-icon>
              Найти услуги
            </v-btn>
            <v-btn
                to="/companies"
                color="secondary"
                size="large"
                variant="outlined"
            >
              <v-icon start icon="mdi-office-building"></v-icon>
              Просмотреть компании
            </v-btn>
          </div>
        </v-alert>
      </div>
    </div>

    <!-- Диалог создания заявки -->
    <ServiceRequestDialog
        :dialog="requestDialog"
        @update:dialog="requestDialog = $event"
        :selected-service="selectedService"
        :request-form="requestForm"
        :loading="requestLoading"
        :error="requestError"
        @close="requestDialog = false"
        @submit-request="submitRequest"
        @error-cleared="requestError = null"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/api'

// Компоненты
import FavoriteServiceCard from '@/components/favorites/FavoriteServiceCard.vue'
import ServiceRequestDialog from '@/components/companies/ServiceRequestDialog.vue'
import SuccessNotification from '@/components/ui/SuccessNotification.vue'

const authStore = useAuthStore()

// Состояния
const isLoading = ref(false)
const error = ref(null)
const favorites = ref([])
const favoritesLoading = ref(false)

// Заявки
const requestDialog = ref(false)
const selectedService = ref(null)
const requestForm = reactive({
  description: ''
})
const requestLoading = ref(false)
const requestError = ref(null)

// Уведомления
const successSnackbar = reactive({
  show: false,
  text: '',
  color: 'success',
  icon: 'mdi-check-circle'
})

// Вспомогательные функции
const showSuccessMessage = (message, type = 'success') => {
  successSnackbar.text = message
  successSnackbar.color = type
  successSnackbar.icon = type === 'success' ? 'mdi-check-circle' : 'mdi-alert-circle'
  successSnackbar.show = true
}

// Нормализация данных услуги из избранного
const getServiceData = (favorite) => {
  // Проверяем разные форматы ответа API
  if (favorite.service_info) {
    // Формат из /favorites/my/
    const serviceData = {
      id: favorite.service_info.id,
      name: favorite.service_info.name,
      description: favorite.service_info.description,
      price: favorite.service_info.price,
      current_price: favorite.service_info.current_price,
      current_discount: favorite.service_info.current_discount,
      company: favorite.service_info.company
    }

    // Проверяем, активна ли скидка
    if (serviceData.current_discount) {
      const now = new Date()
      const startDate = serviceData.current_discount.start_date ?
          new Date(serviceData.current_discount.start_date) : null
      const endDate = serviceData.current_discount.end_date ?
          new Date(serviceData.current_discount.end_date) : null

      // Если скидка не активна, скрываем ее
      if ((startDate && startDate > now) || (endDate && endDate < now)) {
        serviceData.current_discount = null
      }
    }

    return serviceData
  } else {
    // Формат из /favorites/ (старый формат)
    return {
      id: favorite.service_id || 0,
      name: favorite.service_name || 'Неизвестная услуга',
      description: 'Описание недоступно',
      price: favorite.service_price,
      current_price: favorite.service_price,
      company: {
        id: favorite.company_id || 0,
        name: favorite.service_company || 'Неизвестная компания'
      }
    }
  }
}

// Основные методы
const loadFavorites = async () => {
  isLoading.value = true
  error.value = null

  try {
    // Пробуем сначала новый эндпоинт
    const response = await apiClient.get('favorites/my/')
    favorites.value = response.data
  } catch (err) {
    console.log('Trying /favorites/my/ failed, trying /favorites/')

    // Если новый эндпоинт не работает, пробуем старый
    try {
      const response = await apiClient.get('favorites/')
      favorites.value = response.data
    } catch (altError) {
      console.error('Error loading favorites:', altError)
      error.value = altError.response?.data?.detail || 'Ошибка загрузки избранного'
      throw altError
    }
  } finally {
    isLoading.value = false
  }
}

const removeFromFavorites = async (favoriteId) => {
  favoritesLoading.value = true
  try {
    await apiClient.delete(`favorites/${favoriteId}/`)
    await loadFavorites()
    showSuccessMessage('Услуга удалена из избранного!')
  } catch (err) {
    console.error('Error removing from favorites:', err)
    showSuccessMessage('Ошибка удаления из избранного', 'error')
  } finally {
    favoritesLoading.value = false
  }
}

const createRequest = (service) => {
  if (!authStore.isAuthenticated) {
    window.location.href = '/login'
    return
  }

  selectedService.value = service
  requestForm.description = ''
  requestError.value = null
  requestDialog.value = true
}

const submitRequest = async (formData) => {
  requestLoading.value = true
  requestError.value = null

  try {
    await apiClient.post('requests/', {
      service_id: selectedService.value.id,
      description: formData.description
    })

    requestDialog.value = false
    showSuccessMessage('Заявка успешно отправлена! Вы можете отслеживать её статус в разделе "Мои заявки".')
    requestForm.description = ''
  } catch (err) {
    console.error('Error creating request:', err)
    requestError.value = err.response?.data?.detail || 'Ошибка создания заявки'
    showSuccessMessage('Ошибка создания заявки', 'error')
  } finally {
    requestLoading.value = false
  }
}

onMounted(() => {
  if (authStore.isAuthenticated) {
    loadFavorites()
  } else {
    // Если не авторизован, перенаправляем на страницу входа
    window.location.href = '/login'
  }
})
</script>

<style scoped>
.v-card {
  transition: transform 0.2s;
}

.v-card:hover {
  transform: translateY(-2px);
}

/* Адаптивные стили */
@media (max-width: 600px) {
  .v-card {
    margin-bottom: 16px;
  }
}
</style>