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

    <!-- Заголовок -->
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card class="pa-6">
          <v-card-title class="text-h4 mb-2">
            <v-icon large color="primary" class="mr-3">mdi-tools</v-icon>
            Услуги охранных компаний
          </v-card-title>
          <v-card-subtitle class="text-body-1">
            Найдите подходящую охранную услугу для ваших нужд
          </v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>

    <!-- Панель поиска и фильтров -->
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                    v-model="search"
                    label="Поиск услуг"
                    placeholder="Введите название или описание услуги..."
                    prepend-inner-icon="mdi-magnify"
                    clearable
                    @update:model-value="debouncedSearch"
                    density="comfortable"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="3">
                <v-select
                    v-model="sortBy"
                    :items="sortOptions"
                    label="Сортировать по"
                    density="comfortable"
                    @update:model-value="applyFilters"
                ></v-select>
              </v-col>

              <v-col cols="12" md="3">
                <v-select
                    v-model="categoryFilter"
                    :items="categoryOptions"
                    item-title="name"
                    item-value="id"
                    label="Категория"
                    clearable
                    density="comfortable"
                    placeholder="Все категории"
                    @update:model-value="applyFilters"
                ></v-select>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Состояние загрузки -->
    <v-row v-if="isLoading">
      <v-col cols="12" class="text-center">
        <v-progress-circular
            indeterminate
            color="primary"
            size="64"
        ></v-progress-circular>
        <p class="mt-4">Загрузка услуг...</p>
      </v-col>
    </v-row>

    <!-- Ошибка -->
    <v-row v-else-if="error">
      <v-col cols="12">
        <v-alert type="error" @click:close="error = null" closable>
          {{ error }}
        </v-alert>
      </v-col>
    </v-row>

    <!-- Список услуг -->
    <v-row v-else>
      <v-col
          v-for="service in paginatedServices"
          :key="service.id"
          cols="12"
          md="6"
          lg="4"
      >
        <v-card class="h-100 service-card">
          <!-- Заголовок с категориями -->
          <v-card-title class="text-h6 pb-2">
            {{ service.name }}
          </v-card-title>

          <v-card-subtitle class="pb-2">
            <div class="d-flex align-center mb-1">
              <v-chip
                  color="primary"
                  variant="outlined"
                  size="small"
                  :to="`/companies/${service.security_company.id}`"
                  class="mr-2"
              >
                <v-icon start icon="mdi-office-building"></v-icon>
                {{ service.security_company.name }}
              </v-chip>

              <v-chip
                  v-if="hasActiveDiscount(service)"
                  color="red"
                  text-color="white"
                  size="small"
              >
                <v-icon start icon="mdi-sale"></v-icon>
                -{{ service.current_discount.discount_percent }}%
              </v-chip>
            </div>

            <!-- Категории -->
            <div v-if="service.categories?.length" class="mt-1">
              <v-chip
                  v-for="category in service.categories.slice(0, 2)"
                  :key="category.id"
                  size="x-small"
                  variant="outlined"
                  class="mr-1 mb-1"
              >
                {{ category.name }}
              </v-chip>
              <v-chip
                  v-if="service.categories.length > 2"
                  size="x-small"
                  variant="outlined"
                  color="grey"
              >
                +{{ service.categories.length - 2 }}
              </v-chip>
            </div>
          </v-card-subtitle>

          <v-card-text>
            <!-- Описание -->
            <p class="text-body-2 mb-4 line-clamp-3">
              {{ service.description || 'Нет описания' }}
            </p>

            <!-- Цена -->
            <div class="mb-4">
              <div class="text-h5 font-weight-bold primary--text">
                {{ getDisplayPrice(service) }} ₽
              </div>
              <div
                  v-if="hasActiveDiscount(service)"
                  class="text-body-2 text-decoration-line-through text-grey"
              >
                {{ service.price }} ₽
              </div>
              <div v-if="hasActiveDiscount(service)" class="text-caption text-red mt-1">
                <v-icon x-small icon="mdi-clock-outline" class="mr-1"></v-icon>
                Скидка действует до {{ formatDiscountEndDate(service.current_discount.end_date) }}
              </div>
            </div>

            <!-- Кнопки действий -->
            <div class="d-flex flex-wrap gap-2">
              <v-btn
                  :to="`/services/${service.id}`"
                  color="primary"
                  variant="outlined"
                  size="small"
              >
                <v-icon start icon="mdi-information"></v-icon>
                Подробнее
              </v-btn>

              <v-btn
                  v-if="authStore.isAuthenticated"
                  color="secondary"
                  @click="createRequest(service)"
                  size="small"
              >
                <v-icon start icon="mdi-message-text"></v-icon>
                Заявка
              </v-btn>

              <v-btn
                  v-else
                  to="/login"
                  color="secondary"
                  variant="outlined"
                  size="small"
              >
                <v-icon start icon="mdi-login"></v-icon>
                Войдите
              </v-btn>

              <v-spacer></v-spacer>

              <!-- Кнопка избранного -->
              <v-btn
                  v-if="authStore.isAuthenticated"
                  @click="toggleFavorite(service)"
                  icon
                  size="small"
                  :color="isServiceInFavorites(service.id) ? 'pink' : 'grey-lighten-1'"
                  :variant="isServiceInFavorites(service.id) ? 'flat' : 'text'"
                  :loading="favoritesLoading && loadingServiceId === service.id"
                  :disabled="favoritesLoading"
              >
                <v-icon>
                  {{ isServiceInFavorites(service.id) ? 'mdi-heart' : 'mdi-heart-outline' }}
                </v-icon>
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Сообщение если услуг нет -->
      <v-col v-if="filteredServices.length === 0" cols="12">
        <v-alert type="info">
          Услуги не найдены. Попробуйте изменить параметры поиска.
          <div class="mt-2">
            <v-btn @click="resetFilters" color="primary" size="small">
              Сбросить фильтры
            </v-btn>
          </div>
        </v-alert>
      </v-col>
    </v-row>

    <!-- Пагинация -->
    <v-row v-if="totalPages > 1">
      <v-col cols="12" class="text-center">
        <v-pagination
            v-model="currentPage"
            :length="totalPages"
            :total-visible="7"
            @update:model-value="changePage"
        ></v-pagination>
      </v-col>
    </v-row>

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
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useFavoritesStore } from '@/stores/favorites'
import apiClient from '@/api'
import ServiceRequestDialog from '@/components/companies/ServiceRequestDialog.vue'
import SuccessNotification from '@/components/ui/SuccessNotification.vue'

const authStore = useAuthStore()
const favoritesStore = useFavoritesStore()

// Состояния
const isLoading = ref(false)
const error = ref(null)
const allServices = ref([]) // Все загруженные услуги
const categories = ref([])
const search = ref('')
const sortBy = ref('-created_at')
const categoryFilter = ref(null)
const currentPage = ref(1)
const totalPages = ref(1)
const searchTimeout = ref(null)

// Заявки
const requestDialog = ref(false)
const selectedService = ref(null)
const requestForm = reactive({
  description: ''
})
const requestLoading = ref(false)
const requestError = ref(null)

// Избранное
const favoritesLoading = ref(false)
const loadingServiceId = ref(null)

// Уведомления
const successSnackbar = reactive({
  show: false,
  text: '',
  color: 'success',
  icon: 'mdi-check-circle'
})

// Опции сортировки
const sortOptions = [
  { title: 'По дате (новые)', value: '-created_at' },
  { title: 'По дате (старые)', value: 'created_at' },
  { title: 'По названию (А-Я)', value: 'name' },
  { title: 'По названию (Я-А)', value: '-name' },
  { title: 'По цене (дешевые)', value: 'current_price' },
  { title: 'По цене (дорогие)', value: '-current_price' }
]

// Computed свойства
const categoryOptions = computed(() => {
  return [
    { id: null, name: 'Все категории' },
    ...categories.value
  ]
})

// Отфильтрованные услуги (на клиенте)
const filteredServices = computed(() => {
  let result = [...allServices.value]

  // Поиск по названию и описанию
  if (search.value) {
    const searchTerm = search.value.toLowerCase()
    result = result.filter(service =>
        service.name.toLowerCase().includes(searchTerm) ||
        service.description?.toLowerCase().includes(searchTerm)
    )
  }

  // Фильтрация по категории
  if (categoryFilter.value) {
    result = result.filter(service =>
        service.categories?.some(category => category.id === categoryFilter.value)
    )
  }

  // Сортировка
  if (sortBy.value === 'name') {
    result.sort((a, b) => a.name.localeCompare(b.name))
  } else if (sortBy.value === '-name') {
    result.sort((a, b) => b.name.localeCompare(a.name))
  } else if (sortBy.value === 'current_price') {
    result.sort((a, b) => parseFloat(a.current_price) - parseFloat(b.current_price))
  } else if (sortBy.value === '-current_price') {
    result.sort((a, b) => parseFloat(b.current_price) - parseFloat(a.current_price))
  } else if (sortBy.value === 'created_at') {
    result.sort((a, b) => new Date(a.created_at || 0) - new Date(b.created_at || 0))
  } else if (sortBy.value === '-created_at') {
    result.sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0))
  }

  return result
})

// Пагинированные услуги
const paginatedServices = computed(() => {
  const startIndex = (currentPage.value - 1) * 12
  return filteredServices.value.slice(startIndex, startIndex + 12)
})

// Обновляем totalPages при изменении фильтров
watch(filteredServices, () => {
  totalPages.value = Math.max(1, Math.ceil(filteredServices.value.length / 12))
  // Если текущая страница больше общего количества страниц, переходим на первую
  if (currentPage.value > totalPages.value) {
    currentPage.value = 1
  }
})

// Вспомогательные функции
const showSuccessMessage = (message, type = 'success') => {
  successSnackbar.text = message
  successSnackbar.color = type
  successSnackbar.icon = type === 'success' ? 'mdi-check-circle' : 'mdi-alert-circle'
  successSnackbar.show = true
}

// Проверка активной скидки
const hasActiveDiscount = (service) => {
  if (!service.current_discount) return false

  // Проверяем статус скидки
  if (service.current_discount.status === 'ended') {
    return false
  }

  // Проверяем даты скидки
  try {
    const now = new Date()
    const startDate = new Date(service.current_discount.start_date)
    const endDate = new Date(service.current_discount.end_date)

    return now >= startDate && now <= endDate
  } catch (e) {
    console.error('Error parsing discount dates:', e)
    return false
  }
}

// Получение отображаемой цены
const getDisplayPrice = (service) => {
  if (hasActiveDiscount(service)) {
    return service.current_price
  }
  return service.price
}

// Форматирование даты окончания скидки
const formatDiscountEndDate = (dateString) => {
  if (!dateString) return ''
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('ru-RU', {
      day: 'numeric',
      month: 'long'
    })
  } catch (e) {
    return dateString
  }
}

// Проверка нахождения в избранном
const isServiceInFavorites = (serviceId) => {
  // Используем computed свойство для реактивности
  return favoritesStore.isServiceInFavorites(serviceId)
}

// Основные методы
const fetchServices = async () => {
  isLoading.value = true
  error.value = null

  try {
    // Загружаем все услуги без пагинации для клиентской фильтрации
    const params = {
      page_size: 100 // Загружаем достаточно много для фильтрации
    }

    const response = await apiClient.get('services/', { params })

    if (Array.isArray(response.data)) {
      allServices.value = response.data
    } else if (response.data.results) {
      allServices.value = response.data.results
    } else {
      allServices.value = response.data
    }
  } catch (err) {
    console.error('Error loading services:', err)
    error.value = err.response?.data?.detail || 'Ошибка загрузки услуг'
  } finally {
    isLoading.value = false
  }
}

const fetchCategories = async () => {
  try {
    const response = await apiClient.get('categories/')
    categories.value = response.data
  } catch (err) {
    console.error('Error loading categories:', err)
  }
}

const debouncedSearch = () => {
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value)
  }
  searchTimeout.value = setTimeout(() => {
    currentPage.value = 1
  }, 500)
}

const applyFilters = () => {
  currentPage.value = 1
}

const changePage = (page) => {
  currentPage.value = page
  // Прокрутка к верху страницы
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const resetFilters = () => {
  search.value = ''
  sortBy.value = '-created_at'
  categoryFilter.value = null
  currentPage.value = 1
}

const toggleFavorite = async (service) => {
  if (!authStore.isAuthenticated) {
    window.location.href = '/login'
    return
  }

  loadingServiceId.value = service.id
  favoritesLoading.value = true

  try {
    if (isServiceInFavorites(service.id)) {
      // Удаляем из избранного
      const favoriteId = favoritesStore.getFavoriteIdByServiceId(service.id)
      if (favoriteId) {
        await favoritesStore.removeFromFavorites(favoriteId)
        showSuccessMessage('Услуга удалена из избранного!')
      } else {
        // Если не нашли favoriteId, перезагружаем список избранного
        await favoritesStore.fetchFavorites()
      }
    } else {
      // Добавляем в избранное
      await favoritesStore.addToFavorites(service.id)
      showSuccessMessage('Услуга добавлена в избранное!')
    }
  } catch (err) {
    console.error('Error toggling favorite:', err)
    showSuccessMessage('Ошибка при работе с избранным', 'error')
  } finally {
    favoritesLoading.value = false
    loadingServiceId.value = null
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

// Инициализация
onMounted(async () => {
  await fetchServices()
  await fetchCategories()

  if (authStore.isAuthenticated) {
    await favoritesStore.fetchFavorites()
  }
})
</script>

<style scoped>
.h-100 {
  height: 100%;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.v-card {
  transition: transform 0.2s;
}

.service-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1) !important;
}

.gap-2 {
  gap: 8px;
}

/* Стили для карточек со скидкой */
.service-card:has(.v-chip--red) {
  border-top: 4px solid #F44336;
}

/* Адаптивные стили */
@media (max-width: 600px) {
  .v-card {
    margin-bottom: 16px;
  }

  .gap-2 {
    gap: 4px;
  }
}
</style>