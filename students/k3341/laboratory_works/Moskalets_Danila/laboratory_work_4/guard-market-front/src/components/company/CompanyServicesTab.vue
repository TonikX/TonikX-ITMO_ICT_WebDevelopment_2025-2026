<template>
  <div>
    <!-- Уведомление об успехе -->
    <SuccessNotification
        :show="successSnackbar.show"
        :text="successSnackbar.text"
        :color="successSnackbar.color"
        @close="successSnackbar.show = false"
    />

    <!-- Заголовок и кнопка добавления -->
    <div class="d-flex justify-space-between align-center mb-4">
      <h3 class="text-h5">Услуги компании</h3>
      <v-btn
          color="primary"
          @click="openAddDialog"
          :loading="loading"
      >
        <v-icon start icon="mdi-plus"></v-icon>
        Добавить услугу
      </v-btn>
    </div>

    <!-- Состояние загрузки -->
    <div v-if="loading && services.length === 0" class="text-center py-10">
      <v-progress-circular indeterminate></v-progress-circular>
      <p class="mt-4">Загрузка услуг...</p>
    </div>

    <!-- Список услуг -->
    <v-row v-else-if="services.length > 0">
      <v-col
          v-for="service in services"
          :key="service.id"
          cols="12"
          md="6"
          lg="4"
      >
        <v-card class="h-100">
          <v-card-title class="text-h6">
            {{ service.name }}
          </v-card-title>

          <v-card-subtitle>
            <v-chip
                v-if="service.current_discount"
                color="red"
                text-color="white"
                size="small"
                class="mr-2"
            >
              -{{ service.current_discount.discount_percent }}%
            </v-chip>
            <span class="text-body-2">ID: {{ service.id }}</span>
          </v-card-subtitle>

          <v-card-text>
            <p class="text-body-2 mb-4 line-clamp-3">
              {{ service.description || 'Нет описания' }}
            </p>

            <div class="mb-4">
              <div class="d-flex align-center mb-1">
                <div class="text-h5 font-weight-bold">
                  {{ service.current_price || service.price }} ₽
                </div>
                <div
                    v-if="service.current_price && service.current_price !== service.price"
                    class="text-body-2 text-decoration-line-through text-grey ml-2"
                >
                  {{ service.price }} ₽
                </div>
              </div>
              <div v-if="service.current_discount" class="text-caption text-red">
                Скидка действует до: {{ formatDate(service.current_discount.end_date) }}
              </div>
            </div>

            <!-- Категории -->
            <div v-if="service.categories?.length" class="mb-4">
              <div class="text-caption text-grey mb-1">Категории:</div>
              <div class="d-flex flex-wrap gap-1">
                <v-chip
                    v-for="category in getServiceCategories(service)"
                    :key="category.id"
                    size="small"
                    variant="outlined"
                >
                  {{ category.name }}
                </v-chip>
              </div>
            </div>
          </v-card-text>

          <v-card-actions>
            <v-btn
                @click="openEditDialog(service)"
                variant="text"
                size="small"
                color="primary"
                :loading="serviceLoading === service.id"
            >
              <v-icon start icon="mdi-pencil"></v-icon>
              Редактировать
            </v-btn>

            <v-btn
                @click="openDiscountDialog(service)"
                variant="text"
                size="small"
                color="orange"
                :loading="serviceLoading === service.id"
            >
              <v-icon start icon="mdi-sale"></v-icon>
              Скидка
            </v-btn>

            <v-spacer></v-spacer>

            <v-btn
                @click="openDeleteDialog(service)"
                variant="text"
                size="small"
                color="error"
                :loading="serviceLoading === service.id"
            >
              <v-icon start icon="mdi-delete"></v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Сообщение если нет услуг -->
    <div v-else class="text-center py-10">
      <v-alert type="info">
        У вашей компании пока нет услуг. Добавьте первую услугу!
      </v-alert>
    </div>

    <!-- Диалог добавления/редактирования услуги -->
    <v-dialog v-model="serviceDialog.show" max-width="600">
      <v-card>
        <v-card-title>
          {{ serviceDialog.editing ? 'Редактировать услугу' : 'Добавить услугу' }}
        </v-card-title>
        <v-card-text>
          <v-form @submit.prevent="saveService" ref="serviceForm">
            <v-text-field
                v-model="serviceDialog.form.name"
                label="Название услуги"
                :rules="[rules.required, rules.maxLength(100)]"
                class="mb-3"
                :disabled="serviceDialog.loading"
            ></v-text-field>

            <v-textarea
                v-model="serviceDialog.form.description"
                label="Описание услуги"
                :rules="[rules.maxLength(500)]"
                rows="3"
                class="mb-3"
                :disabled="serviceDialog.loading"
            ></v-textarea>

            <v-text-field
                v-model="serviceDialog.form.price"
                label="Цена (руб.)"
                type="number"
                :rules="[rules.required, rules.price]"
                class="mb-3"
                :disabled="serviceDialog.loading"
            ></v-text-field>

            <!-- Выбор категорий -->
            <v-combobox
                v-model="serviceDialog.form.selectedCategories"
                :items="availableCategories"
                item-title="name"
                item-value="id"
                label="Категории"
                multiple
                chips
                closable-chips
                :disabled="serviceDialog.loading"
                class="mb-3"
                clearable
                return-object
            >
              <template v-slot:selection="{ item }">
                <v-chip
                    size="small"
                    variant="outlined"
                    closable
                    @click:close="removeCategory(item.value.id)"
                >
                  {{ item.title }}
                </v-chip>
              </template>
            </v-combobox>

            <v-alert v-if="serviceError" type="error" class="mb-4" @click:close="serviceError = null" closable>
              {{ serviceError }}
            </v-alert>

            <div class="d-flex justify-end">
              <v-btn
                  @click="serviceDialog.show = false"
                  class="mr-2"
                  :disabled="serviceDialog.loading"
              >
                Отмена
              </v-btn>
              <v-btn
                  type="submit"
                  color="primary"
                  :loading="serviceDialog.loading"
              >
                {{ serviceDialog.editing ? 'Сохранить' : 'Добавить' }}
              </v-btn>
            </div>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Диалог скидки -->
    <v-dialog v-model="discountDialog.show" max-width="500">
      <v-card>
        <v-card-title>
          {{ discountDialog.editing ? 'Редактировать скидку' : 'Добавить скидку' }}
          <v-chip color="primary" variant="outlined" size="small" class="ml-2">
            {{ discountDialog.serviceName }}
          </v-chip>
        </v-card-title>
        <v-card-text>
          <v-form @submit.prevent="saveDiscount" ref="discountForm">
            <v-text-field
                v-model="discountDialog.form.discount_percent"
                label="Процент скидки"
                type="number"
                :rules="[rules.required, rules.discountPercent]"
                suffix="%"
                class="mb-3"
                :disabled="discountDialog.loading"
                hint="Введите от 1 до 100"
                persistent-hint
            ></v-text-field>

            <v-text-field
                v-model="discountDialog.form.start_date"
                label="Дата начала"
                type="datetime-local"
                :rules="[rules.required]"
                class="mb-3"
                :disabled="discountDialog.loading"
            ></v-text-field>

            <v-text-field
                v-model="discountDialog.form.end_date"
                label="Дата окончания"
                type="datetime-local"
                :rules="[rules.required]"
                class="mb-3"
                :disabled="discountDialog.loading"
            ></v-text-field>

            <v-alert v-if="discountError" type="error" class="mb-4" @click:close="discountError = null" closable>
              {{ discountError }}
            </v-alert>

            <div class="d-flex justify-end">
              <v-btn
                  @click="discountDialog.show = false"
                  class="mr-2"
                  :disabled="discountDialog.loading"
              >
                Отмена
              </v-btn>
              <v-btn
                  type="submit"
                  color="primary"
                  :loading="discountDialog.loading"
              >
                {{ discountDialog.editing ? 'Сохранить' : 'Добавить' }}
              </v-btn>
            </div>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Диалог подтверждения удаления -->
    <DeleteConfirmationDialog
        :dialog="deleteDialog.show"
        @update:dialog="deleteDialog.show = $event"
        :loading="deleteDialog.loading"
        title="Удаление услуги"
        :message="`Вы уверены, что хотите удалить услугу <strong>${deleteDialog.serviceName}</strong>? <br>Это действие нельзя отменить.`"
        @close="deleteDialog.show = false"
        @confirm="confirmDeleteService"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import apiClient from '@/api'
import { checkDiscountOverlap } from '@/utils/dates'
import SuccessNotification from '@/components/ui/SuccessNotification.vue'
import DeleteConfirmationDialog from '@/components/ui/DeleteConfirmationDialog.vue'

const props = defineProps({
  company: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['service-added', 'service-updated', 'service-deleted', 'service-discount-added'])

// Состояния
const loading = ref(false)
const serviceLoading = ref(null)
const serviceError = ref(null)
const discountError = ref(null)
const allCategories = ref([])
const existingDiscounts = ref([])

// Компоненты компании
const services = computed(() => {
  return props.company.services || []
})

// Диалоги
const serviceDialog = reactive({
  show: false,
  editing: false,
  loading: false,
  serviceId: null,
  form: {
    name: '',
    description: '',
    price: '',
    selectedCategories: [] // Храним объекты категорий
  }
})

const discountDialog = reactive({
  show: false,
  editing: false,
  loading: false,
  serviceId: null,
  serviceName: '',
  form: {
    discount_percent: '',
    start_date: '',
    end_date: ''
  }
})

const deleteDialog = reactive({
  show: false,
  loading: false,
  serviceId: null,
  serviceName: ''
})

// Уведомления
const successSnackbar = reactive({
  show: false,
  text: '',
  color: 'success'
})

// Правила валидации
const rules = {
  required: value => !!value || 'Обязательное поле',
  maxLength: (max) => value => !value || value.length <= max || `Максимум ${max} символов`,
  price: value => {
    const num = parseFloat(value)
    return (num > 0 && !isNaN(num)) || 'Цена должна быть больше 0'
  },
  discountPercent: value => {
    const num = parseFloat(value)
    return (num > 0 && num <= 100 && !isNaN(num)) || 'Процент скидки должен быть от 1 до 100'
  }
}

// Вспомогательные функции
const showSuccessMessage = (message, type = 'success') => {
  successSnackbar.text = message
  successSnackbar.color = type
  successSnackbar.show = true
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU')
}

// Получение категорий для услуги
const getServiceCategories = (service) => {
  if (!service.categories || !service.categories.length) return []

  // Преобразуем ID категорий в объекты
  return service.categories.map(catId => {
    if (typeof catId === 'object' && catId.id) {
      return catId // Уже объект
    }
    // Ищем категорию по ID
    return allCategories.value.find(c => c.id === catId) || { id: catId, name: `Категория ${catId}` }
  }).filter(Boolean)
}

// Доступные категории для выбора
const availableCategories = computed(() => {
  return allCategories.value
})

// Загрузка данных
const loadCategories = async () => {
  try {
    const response = await apiClient.get('categories/')
    allCategories.value = response.data
  } catch (err) {
    console.error('Error loading categories:', err)
  }
}

const loadDiscounts = async () => {
  try {
    const response = await apiClient.get('discounts/')
    existingDiscounts.value = response.data
  } catch (err) {
    console.error('Error loading discounts:', err)
  }
}

const removeCategory = (categoryId) => {
  const index = serviceDialog.form.selectedCategories.findIndex(c => c.id === categoryId)
  if (index !== -1) {
    serviceDialog.form.selectedCategories.splice(index, 1)
  }
}

// Диалоги услуг
const openAddDialog = async () => {
  await loadCategories()
  serviceDialog.show = true
  serviceDialog.editing = false
  serviceDialog.serviceId = null
  serviceDialog.form = { name: '', description: '', price: '', selectedCategories: [] }
  serviceError.value = null
}

const openEditDialog = async (service) => {
  await loadCategories()
  serviceDialog.show = true
  serviceDialog.editing = true
  serviceDialog.serviceId = service.id

  // Получаем категории для редактирования
  const serviceCategories = getServiceCategories(service)

  serviceDialog.form = {
    name: service.name,
    description: service.description || '',
    price: service.price,
    selectedCategories: serviceCategories
  }
  serviceError.value = null
}

const openDiscountDialog = async (service) => {
  await loadDiscounts() // Загружаем существующие скидки

  discountDialog.show = true
  discountDialog.editing = false
  discountDialog.serviceId = service.id
  discountDialog.serviceName = service.name
  discountDialog.form = {
    discount_percent: '',
    start_date: '',
    end_date: ''
  }

  // Устанавливаем текущую дату как начальную
  const now = new Date()
  discountDialog.form.start_date = now.toISOString().slice(0, 16)

  // Устанавливаем дату окончания на неделю вперед
  const weekLater = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000)
  discountDialog.form.end_date = weekLater.toISOString().slice(0, 16)

  discountError.value = null
}

const openDeleteDialog = (service) => {
  deleteDialog.serviceId = service.id
  deleteDialog.serviceName = service.name
  deleteDialog.loading = false
  deleteDialog.show = true
}

// CRUD операции услуг
const saveService = async () => {
  serviceDialog.loading = true
  serviceError.value = null

  try {
    // Преобразуем выбранные категории в массив ID
    const categoryIds = serviceDialog.form.selectedCategories.map(cat => cat.id)

    const serviceData = {
      name: serviceDialog.form.name.trim(),
      description: serviceDialog.form.description.trim(),
      price: serviceDialog.form.price,
      category_ids: categoryIds
    }

    console.log('Saving service data:', serviceData)

    if (serviceDialog.editing) {
      await apiClient.put(`services/${serviceDialog.serviceId}/`, serviceData)
      showSuccessMessage('Услуга успешно обновлена!')
    } else {
      await apiClient.post('services/', serviceData)
      showSuccessMessage('Услуга успешно добавлена!')
    }

    serviceDialog.show = false
    emit(serviceDialog.editing ? 'service-updated' : 'service-added')
  } catch (err) {
    console.error('Error saving service:', err)
    serviceError.value = err.response?.data?.detail || 'Ошибка сохранения услуги'
  } finally {
    serviceDialog.loading = false
  }
}

const saveDiscount = async () => {
  discountDialog.loading = true
  discountError.value = null

  try {
    const discountData = {
      service: discountDialog.serviceId,
      discount_percent: discountDialog.form.discount_percent,
      start_date: new Date(discountDialog.form.start_date).toISOString(),
      end_date: new Date(discountDialog.form.end_date).toISOString()
    }

    // Проверяем пересечение скидок
    const overlapCheck = checkDiscountOverlap(
        discountData,
        existingDiscounts.value,
        discountDialog.serviceId
    )

    if (overlapCheck.hasOverlap) {
      discountError.value = overlapCheck.message
      return
    }

    await apiClient.post('discounts/', discountData)

    discountDialog.show = false
    showSuccessMessage('Скидка успешно добавлена!')

    // Обновляем данные компании после добавления скидки
    emit('service-discount-added')
    // Также эмитим обновление для перезагрузки списка услуг
    emit('service-updated')
  } catch (err) {
    console.error('Error saving discount:', err)
    discountError.value = err.response?.data?.detail || 'Ошибка сохранения скидки'
  } finally {
    discountDialog.loading = false
  }
}

const confirmDeleteService = async () => {
  deleteDialog.loading = true

  try {
    await apiClient.delete(`services/${deleteDialog.serviceId}/`)

    deleteDialog.show = false
    showSuccessMessage('Услуга успешно удалена!')
    emit('service-deleted')
  } catch (err) {
    console.error('Error deleting service:', err)
    showSuccessMessage('Ошибка удаления услуги', 'error')
  } finally {
    deleteDialog.loading = false
  }
}

onMounted(() => {
  loadCategories()
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

.v-card:hover {
  transform: translateY(-2px);
}

.gap-1 {
  gap: 4px;
}
</style>