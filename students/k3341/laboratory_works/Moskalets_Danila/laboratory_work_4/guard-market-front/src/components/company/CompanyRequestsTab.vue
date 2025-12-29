<template>
  <div>
    <!-- Заголовок и статистика -->
    <div class="mb-6">
      <div class="d-flex justify-space-between align-center mb-4">
        <h3 class="text-h5">Заявки на услуги</h3>
        <v-btn
            @click="loadRequests"
            variant="outlined"
            size="small"
            :loading="loading"
        >
          <v-icon start icon="mdi-refresh"></v-icon>
          Обновить
        </v-btn>
      </div>

      <!-- Статистика заявок -->
      <v-row class="mb-4">
        <v-col cols="6" sm="3">
          <v-card color="warning" variant="flat" class="text-center pa-3">
            <div class="text-h4 font-weight-bold">{{ stats.pending }}</div>
            <div class="text-caption">Ожидание</div>
          </v-card>
        </v-col>
        <v-col cols="6" sm="3">
          <v-card color="info" variant="flat" class="text-center pa-3">
            <div class="text-h4 font-weight-bold">{{ stats.confirmed }}</div>
            <div class="text-caption">Подтверждено</div>
          </v-card>
        </v-col>
        <v-col cols="6" sm="3">
          <v-card color="primary" variant="flat" class="text-center pa-3">
            <div class="text-h4 font-weight-bold">{{ stats.in_progress }}</div>
            <div class="text-caption">В работе</div>
          </v-card>
        </v-col>
        <v-col cols="6" sm="3">
          <v-card color="success" variant="flat" class="text-center pa-3">
            <div class="text-h4 font-weight-bold">{{ stats.completed }}</div>
            <div class="text-caption">Завершено</div>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- Состояние загрузки -->
    <div v-if="loading && requests.length === 0" class="text-center py-10">
      <v-progress-circular indeterminate></v-progress-circular>
      <p class="mt-4">Загрузка заявок...</p>
    </div>

    <!-- Список заявок -->
    <div v-else-if="requests.length > 0">
      <v-card
          v-for="request in filteredRequests"
          :key="request.id"
          class="mb-4"
      >
        <v-card-title class="d-flex align-center">
          <v-chip
              :color="getStatusColor(request.status)"
              size="small"
              class="mr-2"
          >
            {{ getStatusTranslation(request.status) }}
          </v-chip>
          <span class="text-h6 ml-2">{{ request.service_info.name }}</span>
          <v-spacer></v-spacer>
          <div class="text-caption text-grey">
            {{ formatDate(request.created_at) }}
          </div>
        </v-card-title>

        <v-card-subtitle class="pb-0">
          <div class="d-flex align-center">
            <v-icon icon="mdi-account" size="small" class="mr-1"></v-icon>
            <span>{{ request.user_info.name }}</span>
            <span class="text-grey ml-2">({{ request.user_info.email }})</span>
          </div>
        </v-card-subtitle>

        <v-card-text>
          <div class="mb-3">
            <strong class="text-body-2">Описание заявки:</strong>
            <p class="text-body-1 mt-1">{{ request.description }}</p>
          </div>

          <div v-if="request.admin_comment" class="mb-3">
            <strong class="text-body-2">Ваш комментарий:</strong>
            <p class="text-body-1 mt-1 text-blue">{{ request.admin_comment }}</p>
          </div>

          <div class="d-flex justify-space-between text-caption text-grey">
            <div>ID: {{ request.id }}</div>
            <div v-if="request.updated_at !== request.created_at">
              Обновлено: {{ formatDate(request.updated_at) }}
            </div>
          </div>
        </v-card-text>

        <v-card-actions>
          <v-btn
              @click="openStatusDialog(request)"
              variant="text"
              size="small"
              color="primary"
              :loading="requestLoading === request.id"
          >
            <v-icon start icon="mdi-cog"></v-icon>
            Изменить статус
          </v-btn>

          <v-btn
              @click="openCommentDialog(request)"
              variant="text"
              size="small"
              color="secondary"
              :loading="requestLoading === request.id"
          >
            <v-icon start icon="mdi-comment"></v-icon>
            Комментарий
          </v-btn>
        </v-card-actions>
      </v-card>
    </div>

    <!-- Сообщение если нет заявок -->
    <div v-else class="text-center py-10">
      <v-alert type="info">
        На услуги вашей компании пока нет заявок.
      </v-alert>
    </div>

    <!-- Фильтры -->
    <v-card v-if="requests.length > 0" class="mt-4">
      <v-card-text>
        <div class="d-flex align-center">
          <v-chip-group v-model="statusFilter" mandatory>
            <v-chip filter value="all">
              Все ({{ requests.length }})
            </v-chip>
            <v-chip filter value="pending" color="warning">
              Ожидание ({{ stats.pending }})
            </v-chip>
            <v-chip filter value="confirmed" color="info">
              Подтверждено ({{ stats.confirmed }})
            </v-chip>
            <v-chip filter value="in_progress" color="primary">
              В работе ({{ stats.in_progress }})
            </v-chip>
            <v-chip filter value="completed" color="success">
              Завершено ({{ stats.completed }})
            </v-chip>
            <v-chip filter value="cancelled" color="error">
              Отменено ({{ stats.cancelled }})
            </v-chip>
          </v-chip-group>

          <v-spacer></v-spacer>

          <v-text-field
              v-model="search"
              label="Поиск заявок"
              placeholder="Поиск по пользователю или услуге..."
              prepend-inner-icon="mdi-magnify"
              clearable
              density="compact"
              style="max-width: 300px;"
          ></v-text-field>
        </div>
      </v-card-text>
    </v-card>

    <!-- Диалог изменения статуса -->
    <v-dialog v-model="statusDialog.show" max-width="400">
      <v-card>
        <v-card-title>Изменение статуса заявки</v-card-title>
        <v-card-text>
          <div class="mb-4">
            <div class="text-body-2 text-grey mb-1">Услуга:</div>
            <div class="text-h6">{{ statusDialog.serviceName }}</div>
            <div class="text-body-2">{{ statusDialog.userName }}</div>
          </div>

          <v-select
              v-model="statusDialog.newStatus"
              :items="availableStatuses"
              label="Новый статус"
              :rules="[rules.required]"
              class="mb-4"
              :disabled="statusDialog.loading"
          ></v-select>

          <div class="d-flex justify-end">
            <v-btn
                @click="statusDialog.show = false"
                class="mr-2"
                :disabled="statusDialog.loading"
            >
              Отмена
            </v-btn>
            <v-btn
                @click="updateRequestStatus"
                color="primary"
                :loading="statusDialog.loading"
            >
              Сохранить
            </v-btn>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Диалог добавления комментария -->
    <v-dialog v-model="commentDialog.show" max-width="500">
      <v-card>
        <v-card-title>Добавить комментарий к заявке</v-card-title>
        <v-card-text>
          <div class="mb-4">
            <div class="text-body-2 text-grey mb-1">Услуга:</div>
            <div class="text-h6">{{ commentDialog.serviceName }}</div>
            <div class="text-body-2">{{ commentDialog.userName }}</div>
          </div>

          <v-textarea
              v-model="commentDialog.comment"
              label="Комментарий для пользователя"
              :rules="[rules.maxLength(500)]"
              rows="3"
              placeholder="Введите комментарий, который увидит пользователь..."
              class="mb-4"
              :disabled="commentDialog.loading"
          ></v-textarea>

          <div class="d-flex justify-end">
            <v-btn
                @click="commentDialog.show = false"
                class="mr-2"
                :disabled="commentDialog.loading"
            >
              Отмена
            </v-btn>
            <v-btn
                @click="updateRequestComment"
                color="primary"
                :loading="commentDialog.loading"
            >
              Сохранить комментарий
            </v-btn>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import apiClient from '@/api'

const props = defineProps({
  company: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['request-updated'])

// Состояния
const loading = ref(false)
const requestLoading = ref(null)
const statusFilter = ref('all')
const search = ref('')

// Заявки
const requests = computed(() => {
  return props.company.service_requests || []
})

// Фильтрованные заявки
const filteredRequests = computed(() => {
  let filtered = [...requests.value]

  // Фильтрация по статусу
  if (statusFilter.value !== 'all') {
    filtered = filtered.filter(request => request.status === statusFilter.value)
  }

  // Поиск
  if (search.value) {
    const term = search.value.toLowerCase()
    filtered = filtered.filter(request =>
        request.user_info.name.toLowerCase().includes(term) ||
        request.user_info.email.toLowerCase().includes(term) ||
        request.service_info.name.toLowerCase().includes(term) ||
        request.description.toLowerCase().includes(term)
    )
  }

  return filtered
})

// Статистика
const stats = computed(() => {
  const stats = {
    pending: 0,
    confirmed: 0,
    in_progress: 0,
    completed: 0,
    cancelled: 0,
    total: requests.value.length
  }

  requests.value.forEach(request => {
    if (request.status && stats.hasOwnProperty(request.status)) {
      stats[request.status]++
    }
  })

  return stats
})

// Диалоги
const statusDialog = reactive({
  show: false,
  loading: false,
  requestId: null,
  serviceName: '',
  userName: '',
  currentStatus: '',
  newStatus: ''
})

const commentDialog = reactive({
  show: false,
  loading: false,
  requestId: null,
  serviceName: '',
  userName: '',
  comment: ''
})

// Доступные статусы для перехода
const availableStatuses = computed(() => {
  if (!statusDialog.currentStatus) return []

  const statusMap = {
    pending: [
      { title: 'Подтверждено', value: 'confirmed' },
      { title: 'Отменено', value: 'cancelled' }
    ],
    confirmed: [
      { title: 'В работе', value: 'in_progress' },
      { title: 'Отменено', value: 'cancelled' }
    ],
    in_progress: [
      { title: 'Завершено', value: 'completed' },
      { title: 'Отменено', value: 'cancelled' }
    ],
    completed: [],
    cancelled: []
  }

  return statusMap[statusDialog.currentStatus] || []
})

// Правила валидации
const rules = {
  required: value => !!value || 'Обязательное поле',
  maxLength: (max) => value => !value || value.length <= max || `Максимум ${max} символов`
}

// Вспомогательные функции
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getStatusTranslation = (status) => {
  const translations = {
    pending: 'Ожидание',
    confirmed: 'Подтверждено',
    in_progress: 'В работе',
    completed: 'Завершено',
    cancelled: 'Отменено'
  }
  return translations[status] || status
}

const getStatusColor = (status) => {
  const colors = {
    pending: 'warning',
    confirmed: 'info',
    in_progress: 'primary',
    completed: 'success',
    cancelled: 'error'
  }
  return colors[status] || 'grey'
}

// Основные методы
const loadRequests = async () => {
  try {
    await emit('request-updated')
  } catch (error) {
    console.error('Error loading requests:', error)
  }
}

const openStatusDialog = (request) => {
  statusDialog.requestId = request.id
  statusDialog.serviceName = request.service_info.name
  statusDialog.userName = `${request.user_info.name} (${request.user_info.email})`
  statusDialog.currentStatus = request.status
  statusDialog.newStatus = ''
  statusDialog.loading = false
  statusDialog.show = true
}

const openCommentDialog = (request) => {
  commentDialog.requestId = request.id
  commentDialog.serviceName = request.service_info.name
  commentDialog.userName = `${request.user_info.name} (${request.user_info.email})`
  commentDialog.comment = request.admin_comment || ''
  commentDialog.loading = false
  commentDialog.show = true
}

const updateRequestStatus = async () => {
  if (!statusDialog.newStatus) return

  statusDialog.loading = true
  requestLoading.value = statusDialog.requestId

  try {
    await apiClient.patch(`requests/${statusDialog.requestId}/`, {
      status: statusDialog.newStatus
    })

    statusDialog.show = false
    await loadRequests()
  } catch (error) {
    console.error('Error updating request status:', error)
  } finally {
    statusDialog.loading = false
    requestLoading.value = null
  }
}

const updateRequestComment = async () => {
  commentDialog.loading = true
  requestLoading.value = commentDialog.requestId

  try {
    await apiClient.patch(`requests/${commentDialog.requestId}/`, {
      admin_comment: commentDialog.comment.trim() || null
    })

    commentDialog.show = false
    await loadRequests()
  } catch (error) {
    console.error('Error updating request comment:', error)
  } finally {
    commentDialog.loading = false
    requestLoading.value = null
  }
}

onMounted(() => {
  // Уже загружено через пропс
})
</script>