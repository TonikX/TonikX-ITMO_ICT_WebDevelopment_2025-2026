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
      <p class="mt-4">Загрузка компании...</p>
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

    <!-- Контент компании -->
    <div v-else-if="company">
      <!-- Заголовок компании -->
      <CompanyHeader
          :company="company"
          :is-company-owner="isCompanyOwner"
      />

      <!-- Табы с услугами и отзывами -->
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-tabs v-model="activeTab" color="primary">
              <v-tab value="services">
                <v-icon start icon="mdi-tools"></v-icon>
                Услуги
                <v-badge
                    v-if="company.services?.length"
                    :content="company.services.length"
                    color="primary"
                    inline
                    class="ml-2"
                ></v-badge>
              </v-tab>
              <v-tab value="reviews">
                <v-icon start icon="mdi-star"></v-icon>
                Отзывы
                <v-badge
                    v-if="company.reviews?.length"
                    :content="company.reviews.length"
                    color="primary"
                    inline
                    class="ml-2"
                ></v-badge>
              </v-tab>
            </v-tabs>

            <v-window v-model="activeTab">
              <!-- Вкладка услуг -->
              <v-window-item value="services">
                <v-card-text>
                  <CompanyServices
                      :services="services"
                      :is-loading="isLoading"
                      :is-authenticated="authStore.isAuthenticated"
                      :is-company-owner="isCompanyOwner"
                      :favorites="favorites"
                      :favorites-loading="favoritesLoading"
                      :service-loading="serviceLoading"
                      :no-services-message="'У этой компании пока нет услуг.'"
                      :show-add-button="isCompanyOwner"
                      :add-button-text="'Добавить первую услугу'"
                      @create-request="createRequest"
                      @add-to-favorites="addToFavorites"
                      @remove-from-favorites="removeFromFavorites"
                      @edit-service="editService"
                      @delete-service="initiateDeleteService"
                      @add-service="addService"
                  />
                </v-card-text>
              </v-window-item>

              <!-- Вкладка отзывов -->
              <v-window-item value="reviews">
                <v-card-text>
                  <CompanyReviews
                      :company="company"
                      :reviews="reviews"
                      :isLoading="isLoading"
                      :onReviewSubmitted="loadCompany"
                  />
                </v-card-text>
              </v-window-item>
            </v-window>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- Компания не найдена -->
    <div v-else class="text-center py-10">
      <v-alert type="error">
        Компания не найдена.
      </v-alert>
      <v-btn to="/companies" class="mt-4">
        Вернуться к списку компаний
      </v-btn>
    </div>

    <!-- Диалог создания заявки -->
    <ServiceRequestDialog
        :dialog="requestDialog"
        @update:dialog="requestDialog = $event"
        :selected-service="selectedService"
        :request-form="requestFormData"
        :loading="requestLoading"
        :error="requestError"
        @close="closeRequestDialog"
        @submit-request="submitRequest"
        @error-cleared="requestError = null"
    />

    <!-- Диалог добавления/редактирования услуги -->
    <ServiceFormDialog
        :dialog="serviceDialog"
        @update:dialog="serviceDialog = $event"
        :editing-service="editingService"
        :service-form-data="serviceFormData"
        :loading="serviceLoading"
        :error="serviceError"
        @close="closeServiceDialog"
        @submit-service="saveService"
        @error-cleared="serviceError = null"
    />

    <!-- Диалог подтверждения удаления услуги -->
    <DeleteConfirmationDialog
        :dialog="deleteServiceDialog"
        @update:dialog="deleteServiceDialog = $event"
        :loading="serviceLoading"
        title="Подтвердите удаление"
        :message="`Вы уверены, что хотите удалить эту услугу? <br><strong>Это действие нельзя отменить.</strong>`"
        @close="deleteServiceDialog = false"
        @confirm="confirmDeleteService"
    />
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/api'

// Компоненты
import CompanyHeader from '@/components/companies/CompanyHeader.vue'
import CompanyServices from '@/components/companies/CompanyServices.vue'
import CompanyReviews from '@/components/reviews/CompanyReviews.vue'
import ServiceRequestDialog from '@/components/companies/ServiceRequestDialog.vue'
import ServiceFormDialog from '@/components/companies/ServiceFormDialog.vue'
import DeleteConfirmationDialog from '@/components/ui/DeleteConfirmationDialog.vue'
import SuccessNotification from '@/components/ui/SuccessNotification.vue'

const route = useRoute()
const authStore = useAuthStore()

// Состояния
const isLoading = ref(false)
const error = ref(null)
const company = ref(null)
const activeTab = ref('services')

// Избранное
const favorites = ref([])
const favoritesLoading = ref(false)

// Заявки
const requestDialog = ref(false)
const selectedService = ref(null)
const requestFormData = reactive({
  description: ''
})
const requestLoading = ref(false)
const requestError = ref(null)

// Услуги (для владельца)
const serviceDialog = ref(false)
const editingService = ref(null)
const serviceFormData = reactive({
  name: '',
  description: '',
  price: ''
})
const serviceLoading = ref(false)
const serviceError = ref(null)
const deleteServiceDialog = ref(false)
const serviceToDeleteId = ref(null)

// Уведомления
const successSnackbar = reactive({
  show: false,
  text: '',
  color: 'success',
  icon: 'mdi-check-circle'
})

// Computed свойства
const services = computed(() => {
  return company.value?.services || []
})

const reviews = computed(() => {
  return company.value?.reviews || []
})

const isCompanyOwner = computed(() => {
  if (!authStore.user || !company.value) return false
  return authStore.user.id === company.value.user?.id
})

// Вспомогательные функции
const showSuccessMessage = (message, type = 'success') => {
  successSnackbar.text = message
  successSnackbar.color = type
  successSnackbar.icon = type === 'success' ? 'mdi-check-circle' : 'mdi-alert-circle'
  successSnackbar.show = true
}

// Основные методы
const loadCompany = async () => {
  isLoading.value = true
  error.value = null

  try {
    const companyId = route.params.id
    const response = await apiClient.get(`companies/${companyId}/`)
    company.value = response.data

    // Загружаем избранное если пользователь авторизован
    if (authStore.isAuthenticated) {
      await loadFavorites()
    }
  } catch (err) {
    console.error('Error loading company:', err)
    error.value = err.response?.data?.detail || 'Ошибка загрузки компании'
  } finally {
    isLoading.value = false
  }
}

const loadFavorites = async () => {
  favoritesLoading.value = true
  try {
    const response = await apiClient.get('favorites/my/')
    favorites.value = response.data
  } catch (error) {
    console.error('Error loading favorites:', error)
  } finally {
    favoritesLoading.value = false
  }
}

const addToFavorites = async (service) => {
  favoritesLoading.value = true
  try {
    await apiClient.post('favorites/', { service_id: service.id })
    await loadFavorites()
    showSuccessMessage('Услуга добавлена в избранное!')
  } catch (error) {
    console.error('Error adding to favorites:', error)
    showSuccessMessage('Ошибка добавления в избранное', 'error')
  } finally {
    favoritesLoading.value = false
  }
}

const removeFromFavorites = async (serviceId) => {
  favoritesLoading.value = true
  try {
    const favorite = favorites.value.find(fav => fav.service_info?.id === serviceId)
    if (favorite) {
      await apiClient.delete(`favorites/${favorite.id}/`)
      await loadFavorites()
      showSuccessMessage('Услуга удалена из избранного!')
    }
  } catch (error) {
    console.error('Error removing from favorites:', error)
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
  requestFormData.description = ''
  requestError.value = null
  requestDialog.value = true
}

const closeRequestDialog = () => {
  requestDialog.value = false
  setTimeout(() => {
    requestFormData.description = ''
    requestError.value = null
    selectedService.value = null
  }, 300)
}

const submitRequest = async (formData) => {
  if (!selectedService.value) {
    requestError.value = 'Не выбрана услуга'
    return
  }

  requestLoading.value = true
  requestError.value = null

  try {
    const response = await apiClient.post('requests/', {
      service_id: selectedService.value.id,
      description: formData.description
    })

    console.log('Request created:', response.data)
    requestDialog.value = false

    showSuccessMessage('Заявка успешно отправлена! Вы можете отслеживать её статус в разделе "Мои заявки".')

    // Сбрасываем данные
    selectedService.value = null
    requestFormData.description = ''
  } catch (err) {
    console.error('Error creating request:', err)

    if (err.response?.status === 401) {
      requestError.value = 'Необходимо авторизоваться'
    } else if (err.response?.data?.detail) {
      requestError.value = err.response.data.detail
    } else if (err.response?.data) {
      // Обработка ошибок валидации
      const errors = err.response.data
      if (typeof errors === 'object') {
        const errorMessages = []
        for (const [field, messages] of Object.entries(errors)) {
          if (Array.isArray(messages)) {
            errorMessages.push(...messages.map(msg => `${field}: ${msg}`))
          } else {
            errorMessages.push(`${field}: ${messages}`)
          }
        }
        requestError.value = errorMessages.join(', ')
      } else {
        requestError.value = 'Ошибка создания заявки'
      }
    } else {
      requestError.value = 'Ошибка соединения с сервером'
    }

    showSuccessMessage('Ошибка создания заявки', 'error')
  } finally {
    requestLoading.value = false
  }
}

// Методы для управления услугами (для владельца)
const addService = () => {
  editingService.value = null
  Object.assign(serviceFormData, {
    name: '',
    description: '',
    price: ''
  })
  serviceError.value = null
  serviceDialog.value = true
}

const editService = (service) => {
  editingService.value = service
  Object.assign(serviceFormData, {
    name: service.name,
    description: service.description || '',
    price: service.price
  })
  serviceError.value = null
  serviceDialog.value = true
}

const closeServiceDialog = () => {
  serviceDialog.value = false
  setTimeout(() => {
    Object.assign(serviceFormData, {
      name: '',
      description: '',
      price: ''
    })
    editingService.value = null
    serviceError.value = null
  }, 300)
}

const saveService = async (formData) => {
  serviceLoading.value = true
  serviceError.value = null

  try {
    // Валидация формы
    if (!formData.name.trim()) {
      throw new Error('Название услуги обязательно')
    }
    if (!formData.price || parseFloat(formData.price) <= 0) {
      throw new Error('Цена должна быть положительным числом')
    }

    if (editingService.value) {
      // Редактирование существующей услуги
      const response = await apiClient.put(`services/${editingService.value.id}/`, {
        name: formData.name,
        description: formData.description,
        price: parseFloat(formData.price)
      })
      console.log('Service updated:', response.data)
      showSuccessMessage('Услуга успешно обновлена!')
    } else {
      // Создание новой услуги
      const response = await apiClient.post('services/', {
        name: formData.name,
        description: formData.description,
        price: parseFloat(formData.price)
      })
      console.log('Service created:', response.data)
      showSuccessMessage('Услуга успешно создана!')
    }

    serviceDialog.value = false
    await loadCompany()
  } catch (err) {
    console.error('Error saving service:', err)
    serviceError.value = err.message || err.response?.data?.detail || 'Ошибка сохранения услуги'
    showSuccessMessage('Ошибка сохранения услуги', 'error')
  } finally {
    serviceLoading.value = false
  }
}

const initiateDeleteService = (serviceId) => {
  serviceToDeleteId.value = serviceId
  deleteServiceDialog.value = true
}

const confirmDeleteService = async () => {
  if (!serviceToDeleteId.value) return

  serviceLoading.value = true

  try {
    await apiClient.delete(`services/${serviceToDeleteId.value}/`)

    showSuccessMessage('Услуга успешно удалена!')
    deleteServiceDialog.value = false
    serviceToDeleteId.value = null

    await loadCompany()
  } catch (err) {
    console.error('Error deleting service:', err)
    showSuccessMessage('Ошибка удаления услуги', 'error')
  } finally {
    serviceLoading.value = false
  }
}

// Наблюдатели
watch(() => route.params.id, () => {
  loadCompany()
})

onMounted(() => {
  loadCompany()
})
</script>

<style scoped>
.h-100 {
  height: 100%;
}

.v-card {
  transition: transform 0.2s;
}

.v-card:hover {
  transform: translateY(-2px);
}

.no-logo-detail {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
  color: #9e9e9e;
}

/* Адаптивные стили */
@media (max-width: 600px) {
  .v-card {
    margin-bottom: 16px;
  }

  .company-image-container {
    height: 150px;
  }
}
</style>