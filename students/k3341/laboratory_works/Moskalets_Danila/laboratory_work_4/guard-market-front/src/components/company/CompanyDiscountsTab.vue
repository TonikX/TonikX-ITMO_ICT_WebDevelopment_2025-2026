<template>
  <div>
    <!-- Заголовок -->
    <div class="d-flex justify-space-between align-center mb-6">
      <h3 class="text-h5">Скидки на услуги</h3>
      <v-btn
          color="primary"
          @click="openAddDialog"
          :loading="loading"
      >
        <v-icon start icon="mdi-plus"></v-icon>
        Добавить скидку
      </v-btn>
    </div>

    <!-- Состояние загрузки -->
    <div v-if="loading && discounts.length === 0" class="text-center py-10">
      <v-progress-circular indeterminate></v-progress-circular>
      <p class="mt-4">Загрузка скидок...</p>
    </div>

    <!-- Список скидок -->
    <div v-else-if="discounts.length > 0">
      <v-card
          v-for="discount in sortedDiscounts"
          :key="discount.id"
          class="mb-4"
          :class="getDiscountStatusClass(discount)"
      >
        <v-card-title class="d-flex align-center">
          <div class="flex-grow-1">
            <div class="text-h6">
              Скидка {{ discount.discount_percent }}% на услугу
              <v-chip size="small" color="primary" variant="outlined" class="ml-2">
                {{ getServiceName(discount.service) }}
              </v-chip>
            </div>
            <div class="text-caption text-grey">
              ID: {{ discount.id }}
            </div>
          </div>
          <v-chip :color="getDiscountStatusColor(discount)" size="small">
            {{ getDiscountStatus(discount) }}
          </v-chip>
        </v-card-title>

        <v-card-text>
          <v-row>
            <v-col cols="12" sm="6">
              <div class="mb-2">
                <strong class="text-body-2">Дата начала:</strong>
                <div class="text-body-1">{{ formatDateTime(discount.start_date) }}</div>
              </div>
            </v-col>
            <v-col cols="12" sm="6">
              <div class="mb-2">
                <strong class="text-body-2">Дата окончания:</strong>
                <div class="text-body-1">{{ formatDateTime(discount.end_date) }}</div>
              </div>
            </v-col>
          </v-row>

          <div v-if="getDaysRemaining(discount) > 0" class="mt-2">
            <v-progress-linear
                :model-value="getDiscountProgress(discount)"
                color="primary"
                height="8"
                rounded
            ></v-progress-linear>
            <div class="text-caption text-grey mt-1">
              {{ getDaysRemaining(discount) }} дней осталось
            </div>
          </div>
        </v-card-text>

        <v-card-actions>
          <v-btn
              @click="openEditDialog(discount)"
              variant="text"
              size="small"
              color="primary"
              :loading="discountLoading === discount.id"
          >
            <v-icon start icon="mdi-pencil"></v-icon>
            Редактировать
          </v-btn>

          <v-spacer></v-spacer>

          <v-btn
              @click="openDeleteDialog(discount)"
              variant="text"
              size="small"
              color="error"
              :loading="discountLoading === discount.id"
          >
            <v-icon start icon="mdi-delete"></v-icon>
            Удалить
          </v-btn>
        </v-card-actions>
      </v-card>
    </div>

    <!-- Сообщение если нет скидок -->
    <div v-else class="text-center py-10">
      <v-alert type="info">
        У вашей компании пока нет скидок на услуги.
      </v-alert>
    </div>

    <!-- Диалог добавления/редактирования скидки -->
    <v-dialog v-model="discountDialog.show" max-width="600">
      <v-card>
        <v-card-title>
          {{ discountDialog.editing ? 'Редактировать скидку' : 'Добавить скидку' }}
        </v-card-title>
        <v-card-text>
          <v-form @submit.prevent="saveDiscount" ref="discountForm">
            <!-- Выбор услуги -->
            <v-select
                v-model="discountDialog.form.service"
                :items="availableServices"
                item-title="name"
                item-value="id"
                label="Услуга"
                :rules="[rules.required]"
                class="mb-3"
                :disabled="discountDialog.loading || discountDialog.editing"
            ></v-select>

            <v-text-field
                v-model="discountDialog.form.discount_percent"
                label="Процент скидки"
                type="number"
                :rules="[rules.required, rules.discountPercent]"
                suffix="%"
                class="mb-3"
                :disabled="discountDialog.loading"
            ></v-text-field>

            <v-row>
              <v-col cols="12" sm="6">
                <v-text-field
                    v-model="discountDialog.form.start_date"
                    label="Дата начала"
                    type="datetime-local"
                    :rules="[rules.required]"
                    class="mb-3"
                    :disabled="discountDialog.loading"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                    v-model="discountDialog.form.end_date"
                    label="Дата окончания"
                    type="datetime-local"
                    :rules="[rules.required]"
                    class="mb-3"
                    :disabled="discountDialog.loading"
                ></v-text-field>
              </v-col>
            </v-row>

            <!-- Проверка дат -->
            <v-alert
                v-if="discountDialog.form.end_date && discountDialog.form.start_date"
                :type="getDateAlertType(discountDialog.form)"
                density="compact"
                class="mb-4"
            >
              {{ getDateAlertMessage(discountDialog.form) }}
            </v-alert>

            <v-alert v-if="error" type="error" class="mb-4" @click:close="error = null" closable>
              {{ error }}
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
        title="Удаление скидки"
        :message="`Вы уверены, что хотите удалить скидку <strong>${deleteDialog.discountPercent}%</strong> на услугу <strong>${deleteDialog.serviceName}</strong>?`"
        @close="deleteDialog.show = false"
        @confirm="confirmDeleteDiscount"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import apiClient from '@/api'
import { checkDiscountOverlap, formatDateTime } from '@/utils/dates'
import DeleteConfirmationDialog from '@/components/ui/DeleteConfirmationDialog.vue'

const props = defineProps({
  company: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['discount-added', 'discount-updated', 'discount-deleted'])

// Состояния
const loading = ref(false)
const discountLoading = ref(null)
const error = ref(null)
const discounts = ref([])

// Диалоги
const discountDialog = reactive({
  show: false,
  editing: false,
  loading: false,
  discountId: null,
  form: {
    service: '',
    discount_percent: '',
    start_date: '',
    end_date: ''
  }
})

const deleteDialog = reactive({
  show: false,
  loading: false,
  discountId: null,
  discountPercent: '',
  serviceName: ''
})

// Доступные услуги компании
const availableServices = computed(() => {
  if (!props.company.services) return []
  return props.company.services.map(service => ({
    id: service.id,
    name: `${service.name} (${service.price} ₽)`
  }))
})

// Правила валидации
const rules = {
  required: value => !!value || 'Обязательное поле',
  discountPercent: value => {
    const num = parseFloat(value)
    return (num > 0 && num <= 100 && !isNaN(num)) || 'Процент скидки должен быть от 1 до 100'
  }
}

// Вспомогательные функции
const getServiceName = (serviceId) => {
  const service = props.company.services?.find(s => s.id === serviceId)
  return service?.name || `Услуга #${serviceId}`
}

const getDiscountStatus = (discount) => {
  const now = new Date()
  const start = new Date(discount.start_date)
  const end = new Date(discount.end_date)

  if (now < start) return 'Ожидает начала'
  if (now > end) return 'Завершена'
  return 'Активна'
}

const getDiscountStatusColor = (discount) => {
  const status = getDiscountStatus(discount)
  switch (status) {
    case 'Активна': return 'success'
    case 'Ожидает начала': return 'warning'
    case 'Завершена': return 'grey'
    default: return 'grey'
  }
}

const getDiscountStatusClass = (discount) => {
  const status = getDiscountStatus(discount)
  switch (status) {
    case 'Активна': return 'border-left-success'
    case 'Ожидает начала': return 'border-left-warning'
    case 'Завершена': return 'border-left-grey'
    default: return ''
  }
}

const getDaysRemaining = (discount) => {
  const now = new Date()
  const end = new Date(discount.end_date)
  const diff = end - now
  return Math.max(0, Math.ceil(diff / (1000 * 60 * 60 * 24)))
}

const getDiscountProgress = (discount) => {
  const now = new Date()
  const start = new Date(discount.start_date)
  const end = new Date(discount.end_date)

  const total = end - start
  const passed = now - start

  return Math.min(100, Math.max(0, (passed / total) * 100))
}

const getDateAlertType = (form) => {
  if (!form.start_date || !form.end_date) return 'info'

  const start = new Date(form.start_date)
  const end = new Date(form.end_date)

  if (end < start) return 'error'
  if (start < new Date()) return 'warning'
  return 'info'
}

const getDateAlertMessage = (form) => {
  if (!form.start_date || !form.end_date) return ''

  const start = new Date(form.start_date)
  const end = new Date(form.end_date)

  if (end < start) return 'Дата окончания должна быть позже даты начала!'
  if (start < new Date()) return 'Скидка начнется в прошлом. Рекомендуется установить будущую дату.'

  const durationDays = Math.round((end - start) / (1000 * 60 * 60 * 24))
  return `Скидка будет действовать ${durationDays} дней`
}

// Основные методы
const loadDiscounts = async () => {
  loading.value = true
  try {
    const response = await apiClient.get('discounts/')
    discounts.value = response.data.filter(discount => {
      // Фильтруем скидки только для услуг нашей компании
      return props.company.services?.some(service => service.id === discount.service)
    })
  } catch (err) {
    console.error('Error loading discounts:', err)
    error.value = err.response?.data?.detail || 'Ошибка загрузки скидок'
  } finally {
    loading.value = false
  }
}

const openAddDialog = () => {
  discountDialog.show = true
  discountDialog.editing = false
  discountDialog.discountId = null
  discountDialog.form = {
    service: '',
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

  error.value = null
}

const openEditDialog = (discount) => {
  discountDialog.show = true
  discountDialog.editing = true
  discountDialog.discountId = discount.id
  discountDialog.form = {
    service: discount.service,
    discount_percent: discount.discount_percent,
    start_date: new Date(discount.start_date).toISOString().slice(0, 16),
    end_date: new Date(discount.end_date).toISOString().slice(0, 16)
  }
  error.value = null
}

const openDeleteDialog = (discount) => {
  deleteDialog.discountId = discount.id
  deleteDialog.discountPercent = discount.discount_percent
  deleteDialog.serviceName = getServiceName(discount.service)
  deleteDialog.loading = false
  deleteDialog.show = true
}

const saveDiscount = async () => {
  discountDialog.loading = true
  error.value = null

  try {
    const discountData = {
      service: discountDialog.form.service,
      discount_percent: discountDialog.form.discount_percent,
      start_date: new Date(discountDialog.form.start_date).toISOString(),
      end_date: new Date(discountDialog.form.end_date).toISOString()
    }

    // Проверяем пересечение скидок (если редактируем, исключаем текущую скидку)
    const discountsToCheck = discountDialog.editing
        ? discounts.value.filter(d => d.id !== discountDialog.discountId)
        : discounts.value

    const overlapCheck = checkDiscountOverlap(
        discountData,
        discountsToCheck,
        discountDialog.form.service
    )

    if (overlapCheck.hasOverlap) {
      error.value = overlapCheck.message
      return
    }

    if (discountDialog.editing) {
      await apiClient.put(`discounts/${discountDialog.discountId}/`, discountData)
      emit('discount-updated')
    } else {
      await apiClient.post('discounts/', discountData)
      emit('discount-added')
    }

    discountDialog.show = false
    await loadDiscounts()
  } catch (err) {
    console.error('Error saving discount:', err)
    error.value = err.response?.data?.detail || 'Ошибка сохранения скидки'
  } finally {
    discountDialog.loading = false
  }
}

const confirmDeleteDiscount = async () => {
  deleteDialog.loading = true
  discountLoading.value = deleteDialog.discountId

  try {
    await apiClient.delete(`discounts/${deleteDialog.discountId}/`)

    deleteDialog.show = false
    emit('discount-deleted')
    await loadDiscounts()
  } catch (err) {
    console.error('Error deleting discount:', err)
  } finally {
    deleteDialog.loading = false
    discountLoading.value = null
  }
}

// Сортированные скидки (сначала активные, потом ожидающие, потом завершенные)
const sortedDiscounts = computed(() => {
  return [...discounts.value].sort((a, b) => {
    const statusA = getDiscountStatus(a)
    const statusB = getDiscountStatus(b)

    const statusOrder = {
      'Активна': 1,
      'Ожидает начала': 2,
      'Завершена': 3
    }

    if (statusOrder[statusA] !== statusOrder[statusB]) {
      return statusOrder[statusA] - statusOrder[statusB]
    }

    // Сначала новые для одинакового статуса
    return new Date(b.start_date) - new Date(a.start_date)
  })
})

onMounted(() => {
  loadDiscounts()
})
</script>

<style scoped>
.border-left-success {
  border-left: 4px solid #4caf50;
}

.border-left-warning {
  border-left: 4px solid #ff9800;
}

.border-left-grey {
  border-left: 4px solid #9e9e9e;
}
</style>