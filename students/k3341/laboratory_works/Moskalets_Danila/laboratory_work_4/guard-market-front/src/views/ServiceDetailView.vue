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
      <p class="mt-4">Загрузка услуги...</p>
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

    <!-- Контент услуги -->
    <div v-else-if="service">
      <!-- Хлебные крошки -->
      <v-breadcrumbs :items="breadcrumbs" class="mb-4">
        <template v-slot:divider>
          <v-icon icon="mdi-chevron-right"></v-icon>
        </template>
      </v-breadcrumbs>

      <v-row class="mb-6">
        <v-col cols="12">
          <v-card class="pa-6">
            <v-row>
              <v-col cols="12" md="8">
                <!-- Заголовок и кнопки действий -->
                <div class="d-flex align-center mb-4">
                  <h1 class="text-h4">{{ service.name }}</h1>
                  <v-spacer></v-spacer>
                  <v-btn
                      v-if="authStore.isAuthenticated"
                      @click="toggleFavorite"
                      :color="isServiceInFavorites ? 'pink' : 'grey-lighten-1'"
                      :variant="isServiceInFavorites ? 'flat' : 'outlined'"
                      :loading="favoritesLoading"
                      class="mr-2"
                  >
                    <v-icon start>
                      {{ isServiceInFavorites ? 'mdi-heart' : 'mdi-heart-outline' }}
                    </v-icon>
                    {{ isServiceInFavorites ? 'В избранном' : 'В избранное' }}
                  </v-btn>
                </div>

                <!-- Описание -->
                <div class="mb-6">
                  <v-card outlined>
                    <v-card-title class="text-h6">
                      <v-icon start icon="mdi-text-box-outline"></v-icon>
                      Описание услуги
                    </v-card-title>
                    <v-card-text>
                      <p class="text-body-1" v-if="service.description">
                        {{ service.description }}
                      </p>
                      <v-alert v-else type="info">
                        Описание услуги отсутствует
                      </v-alert>
                    </v-card-text>
                  </v-card>
                </div>

                <!-- Детали услуги -->
                <v-row>
                  <!-- Категории -->
                  <v-col cols="12" md="6">
                    <v-card outlined>
                      <v-card-title class="text-h6">
                        <v-icon start icon="mdi-tag-multiple"></v-icon>
                        Категории
                      </v-card-title>
                      <v-card-text>
                        <div v-if="service.categories?.length">
                          <v-chip
                              v-for="category in service.categories"
                              :key="category.id"
                              color="primary"
                              variant="outlined"
                              class="mr-2 mb-2"
                          >
                            {{ category.name }}
                          </v-chip>
                        </div>
                        <v-alert v-else type="info" density="compact">
                          Категории не указаны
                        </v-alert>
                      </v-card-text>
                    </v-card>
                  </v-col>

                  <!-- Дополнительная информация -->
                  <v-col cols="12" md="6">
                    <v-card outlined>
                      <v-card-title class="text-h6">
                        <v-icon start icon="mdi-information"></v-icon>
                        Информация
                      </v-card-title>
                      <v-card-text>
                        <div class="mb-2">
                          <strong>ID услуги:</strong> {{ service.id }}
                        </div>
                        <div v-if="service.created_at" class="mb-2">
                          <strong>Добавлена:</strong> {{ formatDate(service.created_at) }}
                        </div>
                        <div v-if="service.updated_at" class="mb-2">
                          <strong>Обновлена:</strong> {{ formatDate(service.updated_at) }}
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
              </v-col>

              <!-- Боковая панель с ценой и компанией -->
              <v-col cols="12" md="4">
                <!-- Карточка с ценой -->
                <v-card class="mb-4 price-card" :class="{ 'has-discount': hasActiveDiscount }">
                  <v-card-title class="text-h5">
                    <v-icon start icon="mdi-cash"></v-icon>
                    Стоимость
                  </v-card-title>
                  <v-card-text class="text-center">
                    <div v-if="hasActiveDiscount" class="mb-2">
                      <v-chip color="red" text-color="white" size="large">
                        <v-icon start icon="mdi-sale"></v-icon>
                        Скидка -{{ service.current_discount.discount_percent }}%
                      </v-chip>
                    </div>

                    <div class="mb-2">
                      <div class="text-h3 font-weight-bold primary--text">
                        {{ getDisplayPrice }} ₽
                      </div>
                      <div
                          v-if="hasActiveDiscount"
                          class="text-h6 text-decoration-line-through text-grey"
                      >
                        {{ service.price }} ₽
                      </div>
                    </div>

                    <div v-if="hasActiveDiscount" class="text-caption text-red mt-2">
                      <v-icon small icon="mdi-clock-outline" class="mr-1"></v-icon>
                      Скидка действует до {{ formatDiscountEndDate }}
                    </div>

                    <v-divider class="my-4"></v-divider>

                    <v-btn
                        v-if="authStore.isAuthenticated"
                        color="primary"
                        size="large"
                        block
                        @click="createRequest"
                        :loading="requestLoading"
                    >
                      <v-icon start icon="mdi-message-text"></v-icon>
                      Оставить заявку
                    </v-btn>
                    <v-btn
                        v-else
                        to="/login"
                        color="primary"
                        size="large"
                        block
                        variant="outlined"
                    >
                      <v-icon start icon="mdi-login"></v-icon>
                      Войдите, чтобы оставить заявку
                    </v-btn>
                  </v-card-text>
                </v-card>

                <!-- Карточка компании -->
                <v-card>
                  <v-card-title class="text-h6">
                    <v-icon start icon="mdi-office-building"></v-icon>
                    Компания
                  </v-card-title>
                  <v-card-text class="text-center">
                    <v-avatar size="80" class="mb-3">
                      <v-img
                          v-if="companyLogo"
                          :src="companyLogo"
                          cover
                      >
                        <template v-slot:placeholder>
                          <v-icon size="40" color="grey-lighten-1">mdi-office-building</v-icon>
                        </template>
                      </v-img>
                      <v-icon v-else size="40" color="grey-lighten-1">mdi-office-building</v-icon>
                    </v-avatar>

                    <div class="text-h6 mb-2">{{ companyName }}</div>

                    <div v-if="companyWebsite" class="mb-3">
                      <v-icon small icon="mdi-web" class="mr-1"></v-icon>
                      <a :href="companyWebsite" target="_blank" class="text-body-2">
                        {{ formatWebsite(companyWebsite) }}
                      </a>
                    </div>

                    <v-btn
                        :to="`/companies/${companyId}`"
                        color="primary"
                        variant="outlined"
                        block
                        class="mt-2"
                    >
                      <v-icon start icon="mdi-arrow-right"></v-icon>
                      Перейти к компании
                    </v-btn>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- Услуга не найдена -->
    <div v-else class="text-center py-10">
      <v-alert type="error">
        Услуга не найдена.
      </v-alert>
      <v-btn to="/services" class="mt-4">
        Вернуться к списку услуг
      </v-btn>
    </div>

    <!-- Диалог создания заявки -->
    <ServiceRequestDialog
        :dialog="requestDialog"
        @update:dialog="requestDialog = $event"
        :selected-service="service"
        :request-form="requestForm"
        :loading="requestDialogLoading"
        :error="requestDialogError"
        @close="requestDialog = false"
        @submit-request="submitRequest"
        @error-cleared="requestDialogError = null"
    />
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useFavoritesStore } from '@/stores/favorites'
import apiClient from '@/api'
import ServiceRequestDialog from '@/components/companies/ServiceRequestDialog.vue'
import SuccessNotification from '@/components/ui/SuccessNotification.vue'

const route = useRoute()
const authStore = useAuthStore()
const favoritesStore = useFavoritesStore()

// Состояния
const isLoading = ref(false)
const error = ref(null)
const service = ref(null)

// Избранное
const favoritesLoading = ref(false)

// Заявки
const requestDialog = ref(false)
const requestForm = reactive({
  description: ''
})
const requestLoading = ref(false)
const requestDialogLoading = ref(false)
const requestDialogError = ref(null)

// Уведомления
const successSnackbar = reactive({
  show: false,
  text: '',
  color: 'success',
  icon: 'mdi-check-circle'
})

// Computed свойства
const breadcrumbs = computed(() => {
  const items = [
    { title: 'Главная', to: '/' },
    { title: 'Услуги', to: '/services' }
  ]

  if (service.value) {
    items.push({ title: service.value.name, disabled: true })
  }

  return items
})

const companyName = computed(() => {
  if (!service.value) return ''
  return service.value.security_company?.name || 'Неизвестная компания'
})

const companyId = computed(() => {
  if (!service.value) return null
  return service.value.security_company?.id
})

const companyLogo = computed(() => {
  if (!service.value) return null
  return service.value.security_company?.logo
})

const companyWebsite = computed(() => {
  if (!service.value) return null
  return service.value.security_company?.website
})

const isServiceInFavorites = computed(() => {
  if (!service.value?.id) return false
  return favoritesStore.isServiceInFavorites(service.value.id)
})

const hasActiveDiscount = computed(() => {
  if (!service.value?.current_discount) return false

  // Проверяем статус скидки
  if (service.value.current_discount.status === 'ended') {
    return false
  }

  // Проверяем даты скидки
  try {
    const now = new Date()
    const startDate = new Date(service.value.current_discount.start_date)
    const endDate = new Date(service.value.current_discount.end_date)

    return now >= startDate && now <= endDate
  } catch (e) {
    console.error('Error parsing discount dates:', e)
    return false
  }
})

const getDisplayPrice = computed(() => {
  if (!service.value) return '0'
  if (hasActiveDiscount.value) {
    return service.value.current_price
  }
  return service.value.price
})

const formatDiscountEndDate = computed(() => {
  if (!service.value?.current_discount?.end_date) return ''
  try {
    const date = new Date(service.value.current_discount.end_date)
    return date.toLocaleDateString('ru-RU', {
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    })
  } catch (e) {
    return service.value.current_discount.end_date
  }
})

// Вспомогательные функции
const showSuccessMessage = (message, type = 'success') => {
  successSnackbar.text = message
  successSnackbar.color = type
  successSnackbar.icon = type === 'success' ? 'mdi-check-circle' : 'mdi-alert-circle'
  successSnackbar.show = true
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (e) {
    return dateString
  }
}

const formatWebsite = (website) => {
  if (!website) return ''
  // Убираем протокол для отображения
  return website.replace(/^https?:\/\//, '').replace(/\/$/, '')
}

// Основные методы
const loadService = async () => {
  isLoading.value = true
  error.value = null

  try {
    const serviceId = route.params.id
    const response = await apiClient.get(`services/${serviceId}/`)
    service.value = response.data

    // Загружаем избранное если пользователь авторизован
    if (authStore.isAuthenticated) {
      await favoritesStore.fetchFavorites()
    }
  } catch (err) {
    console.error('Error loading service:', err)
    error.value = err.response?.data?.detail || 'Ошибка загрузки услуги'
  } finally {
    isLoading.value = false
  }
}

const toggleFavorite = async () => {
  if (!authStore.isAuthenticated) {
    window.location.href = '/login'
    return
  }

  favoritesLoading.value = true

  try {
    if (isServiceInFavorites.value) {
      // Удаляем из избранного
      const favoriteId = favoritesStore.getFavoriteIdByServiceId(service.value.id)
      if (favoriteId) {
        await favoritesStore.removeFromFavorites(favoriteId)
        showSuccessMessage('Услуга удалена из избранного!')
      }
    } else {
      // Добавляем в избранное
      await favoritesStore.addToFavorites(service.value.id)
      showSuccessMessage('Услуга добавлена в избранное!')
    }
  } catch (err) {
    console.error('Error toggling favorite:', err)
    showSuccessMessage('Ошибка при работе с избранным', 'error')
  } finally {
    favoritesLoading.value = false
  }
}

const createRequest = () => {
  if (!authStore.isAuthenticated) {
    window.location.href = '/login'
    return
  }

  requestForm.description = ''
  requestDialogError.value = null
  requestDialog.value = true
}

const submitRequest = async (formData) => {
  requestDialogLoading.value = true
  requestDialogError.value = null

  try {
    await apiClient.post('requests/', {
      service_id: service.value.id,
      description: formData.description
    })

    requestDialog.value = false
    showSuccessMessage('Заявка успешно отправлена! Вы можете отслеживать её статус в разделе "Мои заявки".')
    requestForm.description = ''
  } catch (err) {
    console.error('Error creating request:', err)
    requestDialogError.value = err.response?.data?.detail || 'Ошибка создания заявки'
    showSuccessMessage('Ошибка создания заявки', 'error')
  } finally {
    requestDialogLoading.value = false
  }
}

// Наблюдатели
watch(() => route.params.id, () => {
  loadService()
})

onMounted(() => {
  loadService()
})
</script>

<style scoped>
.price-card {
  transition: all 0.3s ease;
}

.price-card.has-discount {
  border-left: 4px solid #F44336;
  background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
}

.v-card {
  transition: transform 0.2s;
}

.v-card:hover {
  transform: translateY(-2px);
}

/* Стили для ссылок */
a {
  text-decoration: none;
  color: #1976D2;
}

a:hover {
  text-decoration: underline;
}

/* Адаптивные стили */
@media (max-width: 600px) {
  .v-card {
    margin-bottom: 16px;
  }

  .text-h4 {
    font-size: 1.5rem;
  }

  .text-h3 {
    font-size: 2rem;
  }
}
</style>