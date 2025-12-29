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
            <v-icon large color="primary" class="mr-3">mdi-format-list-bulleted</v-icon>
            Мои заявки
          </v-card-title>
          <v-card-subtitle class="text-body-1">
            Управляйте вашими заявками на услуги охранных компаний
          </v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>

    <!-- Статистика и быстрые фильтры -->
    <v-row class="mb-4">
      <v-col cols="12">
        <v-card>
          <v-card-text class="pa-4">
            <div class="d-flex align-center flex-wrap gap-3 mb-4">
              <!-- Быстрые фильтры по статусу -->
              <v-btn
                  @click="applyQuickFilter('')"
                  :variant="statusFilter === '' ? 'flat' : 'outlined'"
                  color="primary"
                  size="small"
              >
                Все ({{ requestsStats.total }})
              </v-btn>
              <v-btn
                  @click="applyQuickFilter('pending')"
                  :variant="statusFilter === 'pending' ? 'flat' : 'outlined'"
                  color="warning"
                  size="small"
              >
                <v-icon start icon="mdi-clock"></v-icon>
                Ожидание ({{ requestsStats.pending }})
              </v-btn>
              <v-btn
                  @click="applyQuickFilter('confirmed')"
                  :variant="statusFilter === 'confirmed' ? 'flat' : 'outlined'"
                  color="info"
                  size="small"
              >
                <v-icon start icon="mdi-check"></v-icon>
                Подтверждено ({{ requestsStats.confirmed }})
              </v-btn>
              <v-btn
                  @click="applyQuickFilter('in_progress')"
                  :variant="statusFilter === 'in_progress' ? 'flat' : 'outlined'"
                  color="primary"
                  size="small"
              >
                <v-icon start icon="mdi-progress-clock"></v-icon>
                В работе ({{ requestsStats.in_progress }})
              </v-btn>
              <v-btn
                  @click="applyQuickFilter('completed')"
                  :variant="statusFilter === 'completed' ? 'flat' : 'outlined'"
                  color="success"
                  size="small"
              >
                <v-icon start icon="mdi-check-all"></v-icon>
                Завершено ({{ requestsStats.completed }})
              </v-btn>
              <v-btn
                  @click="applyQuickFilter('cancelled')"
                  :variant="statusFilter === 'cancelled' ? 'flat' : 'outlined'"
                  color="error"
                  size="small"
              >
                <v-icon start icon="mdi-close"></v-icon>
                Отменено ({{ requestsStats.cancelled }})
              </v-btn>
            </div>

            <!-- Поиск -->
            <div class="d-flex align-center">
              <v-text-field
                  v-model="search"
                  label="Поиск заявок"
                  placeholder="Поиск по услуге, описанию, компании..."
                  prepend-inner-icon="mdi-magnify"
                  clearable
                  @update:model-value="debouncedSearch"
                  density="compact"
                  class="mr-4"
                  style="max-width: 400px;"
              ></v-text-field>

              <v-spacer></v-spacer>

              <v-btn
                  @click="loadRequests"
                  variant="outlined"
                  size="small"
                  :loading="requestsStore.isLoading"
                  class="mr-2"
              >
                <v-icon start icon="mdi-refresh"></v-icon>
                Обновить
              </v-btn>

              <v-btn
                  @click="resetFilters"
                  variant="outlined"
                  size="small"
                  color="secondary"
              >
                <v-icon start icon="mdi-filter-remove"></v-icon>
                Сбросить
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Таблица заявок -->
    <v-row>
      <v-col cols="12">
        <v-card>
          <!-- Состояние загрузки -->
          <div v-if="requestsStore.isLoading" class="text-center py-10">
            <v-progress-circular
                indeterminate
                color="primary"
                size="64"
            ></v-progress-circular>
            <p class="mt-4">Загрузка заявок...</p>
          </div>

          <!-- Ошибка -->
          <v-alert
              v-else-if="requestsStore.error"
              type="error"
              class="ma-4"
              @click:close="requestsStore.error = null"
              closable
          >
            {{ requestsStore.error }}
          </v-alert>

          <!-- Таблица -->
          <v-data-table
              v-else
              :headers="headers"
              :items="filteredRequests"
              :loading="requestsStore.isLoading"
              density="comfortable"
              hover
              :items-per-page="-1"
              hide-default-footer
          >
            <!-- Кастомный заголовок для статуса -->
            <template v-slot:header.status="{ column }">
              <v-chip
                  :color="getStatusColor(column.value)"
                  size="small"
                  variant="outlined"
              >
                {{ column.title }}
              </v-chip>
            </template>

            <!-- Статус -->
            <template v-slot:item.status="{ item }">
              <v-chip
                  :color="getStatusColor(item.status)"
                  size="small"
                  :text="getStatusTranslation(item.status)"
                  class="font-weight-medium"
              ></v-chip>
            </template>

            <!-- Услуга -->
            <template v-slot:item.service="{ item }">
              <div class="d-flex align-center">
                <v-avatar size="36" color="primary" class="mr-2">
                  <v-icon icon="mdi-tools" color="white" size="20"></v-icon>
                </v-avatar>
                <div>
                  <div class="font-weight-medium text-body-2">{{ item.service_info?.name }}</div>
                  <div class="text-caption text-grey">{{ item.service_info?.company?.name }}</div>
                </div>
              </div>
            </template>

            <!-- Описание -->
            <template v-slot:item.description="{ item }">
              <div class="line-clamp-2 text-body-2">
                {{ item.description || 'Нет описания' }}
              </div>
            </template>

            <!-- Комментарий -->
            <template v-slot:item.admin_comment="{ item }">
              <div v-if="item.admin_comment" class="line-clamp-2 text-body-2 text-blue">
                {{ item.admin_comment }}
              </div>
              <div v-else class="text-caption text-grey">
                Нет комментария
              </div>
            </template>

            <!-- Даты -->
            <template v-slot:item.created_at="{ item }">
              <div class="text-body-2">
                {{ formatTableDate(item.created_at) }}
              </div>
            </template>

            <template v-slot:item.updated_at="{ item }">
              <div class="text-body-2">
                {{ formatTableDate(item.updated_at) }}
              </div>
            </template>

            <!-- Действия -->
            <template v-slot:item.actions="{ item }">
              <div class="d-flex gap-1">
                <!-- Кнопка деталей -->
                <v-btn
                    @click="viewRequestDetails(item)"
                    icon
                    size="small"
                    variant="text"
                    color="info"
                    title="Подробнее"
                >
                  <v-icon>mdi-information</v-icon>
                </v-btn>

                <!-- Кнопка редактирования (только для pending) -->
                <v-btn
                    v-if="item.status === 'pending'"
                    @click="openEditDialog(item)"
                    icon
                    size="small"
                    variant="text"
                    color="primary"
                    title="Изменить описание"
                >
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>

                <!-- Кнопка удаления -->
                <v-btn
                    @click="initiateDeleteRequest(item)"
                    icon
                    size="small"
                    variant="text"
                    color="error"
                    title="Удалить"
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </div>
            </template>

            <!-- Сообщение если нет данных -->
            <template v-slot:no-data>
              <div class="text-center py-10">
                <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-file-document-outline</v-icon>
                <p class="text-h6 mb-2">Заявки не найдены</p>
                <p class="text-body-1 mb-4">
                  {{ requests.length === 0 ? 'У вас пока нет заявок.' : 'Попробуйте изменить параметры поиска.' }}
                </p>
                <v-btn
                    v-if="requests.length === 0"
                    to="/services"
                    color="primary"
                    size="large"
                >
                  <v-icon start icon="mdi-magnify"></v-icon>
                  Найти услуги
                </v-btn>
                <v-btn
                    v-else
                    @click="resetFilters"
                    color="primary"
                    size="large"
                >
                  <v-icon start icon="mdi-filter-remove"></v-icon>
                  Сбросить фильтры
                </v-btn>
              </div>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <!-- Диалог редактирования описания -->
    <v-dialog v-model="editDialog.show" max-width="500">
      <v-card>
        <v-card-title class="d-flex align-center">
          <v-icon icon="mdi-pencil" color="primary" class="mr-2"></v-icon>
          Изменение описания заявки
        </v-card-title>
        <v-card-text>
          <div class="mb-4">
            <div class="text-body-2 text-grey mb-1">Услуга:</div>
            <div class="text-h6">{{ editDialog.serviceName }}</div>
            <div class="text-body-2">{{ editDialog.companyName }}</div>
          </div>

          <v-divider class="my-4"></v-divider>

          <v-form @submit.prevent="updateRequestDescription">
            <v-textarea
                v-model="editDialog.description"
                label="Описание заявки"
                :rules="[rules.required]"
                rows="3"
                placeholder="Опишите подробно, что вам нужно..."
                class="mb-4"
                :disabled="editDialog.loading"
            ></v-textarea>

            <div class="d-flex justify-end">
              <v-btn
                  @click="editDialog.show = false"
                  class="mr-2"
                  :disabled="editDialog.loading"
              >
                Отмена
              </v-btn>
              <v-btn
                  type="submit"
                  color="primary"
                  :loading="editDialog.loading"
              >
                Сохранить изменения
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
        title="Подтвердите удаление"
        :message="`Вы уверены, что хотите удалить заявку на услугу <strong>${deleteDialog.serviceName}</strong>? <br>Это действие нельзя отменить.`"
        @close="deleteDialog.show = false"
        @confirm="confirmDeleteRequest"
    />

    <!-- Диалог просмотра деталей заявки -->
    <v-dialog v-model="detailsDialog.show" max-width="600">
      <v-card v-if="detailsDialog.request">
        <v-card-title class="d-flex align-center">
          <v-icon icon="mdi-information" color="primary" class="mr-2"></v-icon>
          Детали заявки
          <v-spacer></v-spacer>
          <v-chip
              :color="getStatusColor(detailsDialog.request.status)"
              size="small"
              class="font-weight-medium"
          >
            {{ getStatusTranslation(detailsDialog.request.status) }}
          </v-chip>
        </v-card-title>

        <v-card-text>
          <v-table density="comfortable">
            <tbody>
            <tr>
              <th class="text-right" style="width: 30%;">ID заявки:</th>
              <td>{{ detailsDialog.request.id }}</td>
            </tr>
            <tr>
              <th class="text-right">Услуга:</th>
              <td>
                <div>{{ detailsDialog.request.service_info?.name }}</div>
                <div class="text-caption text-grey">
                  {{ detailsDialog.request.service_info?.company?.name }}
                </div>
                <v-btn
                    v-if="detailsDialog.request.service_info?.company?.id"
                    :to="`/companies/${detailsDialog.request.service_info.company.id}`"
                    variant="text"
                    size="x-small"
                    color="primary"
                    class="mt-1"
                >
                  <v-icon start icon="mdi-arrow-right" size="x-small"></v-icon>
                  Перейти к компании
                </v-btn>
              </td>
            </tr>
            <tr>
              <th class="text-right">Описание:</th>
              <td>{{ detailsDialog.request.description || 'Нет описания' }}</td>
            </tr>
            <tr>
              <th class="text-right">Комментарий компании:</th>
              <td>
                  <span v-if="detailsDialog.request.admin_comment" class="text-blue">
                    {{ detailsDialog.request.admin_comment }}
                  </span>
                <span v-else class="text-grey">
                    Комментарий отсутствует
                  </span>
              </td>
            </tr>
            <tr>
              <th class="text-right">Дата создания:</th>
              <td>{{ formatFullDate(detailsDialog.request.created_at) }}</td>
            </tr>
            <tr>
              <th class="text-right">Дата обновления:</th>
              <td>{{ formatFullDate(detailsDialog.request.updated_at) }}</td>
            </tr>
            <tr v-if="detailsDialog.request.user_info">
              <th class="text-right">Пользователь:</th>
              <td>
                <div>{{ detailsDialog.request.user_info.name }}</div>
                <div class="text-caption text-grey">{{ detailsDialog.request.user_info.email }}</div>
              </td>
            </tr>
            </tbody>
          </v-table>
        </v-card-text>

        <v-card-actions class="justify-end">
          <v-btn @click="detailsDialog.show = false" color="primary">
            Закрыть
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRequestsStore } from '@/stores/requests'
import DeleteConfirmationDialog from '@/components/ui/DeleteConfirmationDialog.vue'
import SuccessNotification from '@/components/ui/SuccessNotification.vue'

const authStore = useAuthStore()
const requestsStore = useRequestsStore()

// Состояния
const search = ref('')
const statusFilter = ref('')
const searchTimeout = ref(null)

// Диалоги
const editDialog = reactive({
  show: false,
  requestId: null,
  serviceName: '',
  companyName: '',
  description: '',
  loading: false
})

const deleteDialog = reactive({
  show: false,
  requestId: null,
  serviceName: '',
  loading: false
})

const detailsDialog = reactive({
  show: false,
  request: null
})

// Уведомления
const successSnackbar = reactive({
  show: false,
  text: '',
  color: 'success',
  icon: 'mdi-check-circle'
})

// Заголовки таблицы
const headers = [
  { title: 'ID', key: 'id', width: '80px' },
  { title: 'Статус', key: 'status', width: '120px' },
  { title: 'Услуга', key: 'service', width: '250px' },
  { title: 'Описание', key: 'description' },
  { title: 'Комментарий', key: 'admin_comment' },
  { title: 'Дата создания', key: 'created_at', width: '140px' },
  { title: 'Дата обновления', key: 'updated_at', width: '140px' },
  { title: 'Действия', key: 'actions', width: '120px', sortable: false }
]

// Правила валидации
const rules = {
  required: value => !!value?.trim() || 'Обязательное поле'
}

// Computed свойства
const requests = computed(() => {
  return requestsStore.myRequests
})

const filteredRequests = computed(() => {
  return requestsStore.filteredMyRequestsTable(statusFilter.value, search.value)
})

const requestsStats = computed(() => {
  return requestsStore.myRequestsStats
})

// Вспомогательные функции
const showSuccessMessage = (message, type = 'success') => {
  successSnackbar.text = message
  successSnackbar.color = type
  successSnackbar.icon = type === 'success' ? 'mdi-check-circle' : 'mdi-alert-circle'
  successSnackbar.show = true
}

const getStatusTranslation = (status) => {
  return requestsStore.statusTranslation[status] || status
}

const getStatusColor = (status) => {
  return requestsStore.statusColors[status] || 'grey'
}

const formatTableDate = (dateString) => {
  if (!dateString) return ''
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('ru-RU', {
      day: '2-digit',
      month: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (e) {
    return dateString
  }
}

const formatFullDate = (dateString) => {
  if (!dateString) return ''
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    })
  } catch (e) {
    return dateString
  }
}

// Основные методы
const loadRequests = async () => {
  try {
    // Загружаем все заявки без пагинации
    await requestsStore.fetchMyRequests()
  } catch (error) {
    console.error('Error loading requests:', error)
  }
}

const debouncedSearch = () => {
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value)
  }
  searchTimeout.value = setTimeout(() => {
    // Поиск выполняется через computed свойство filteredRequests
  }, 300)
}

const applyQuickFilter = (status) => {
  statusFilter.value = status
}

const resetFilters = () => {
  search.value = ''
  statusFilter.value = ''
}

const openEditDialog = (request) => {
  console.log('Opening edit dialog for request:', request)
  editDialog.requestId = request.id
  editDialog.serviceName = request.service_info?.name || 'Неизвестная услуга'
  editDialog.companyName = request.service_info?.company?.name || 'Неизвестная компания'
  editDialog.description = request.description || ''
  editDialog.loading = false
  editDialog.show = true
}

const updateRequestDescription = async () => {
  if (!editDialog.requestId || !editDialog.description.trim()) {
    console.error('Missing request ID or description')
    return
  }

  editDialog.loading = true

  try {
    console.log('Updating request:', editDialog.requestId, 'with description:', editDialog.description)

    await requestsStore.updateRequest(editDialog.requestId, {
      description: editDialog.description.trim()
    })

    // После обновления перезагружаем данные для гарантии
    await loadRequests()

    editDialog.show = false
    showSuccessMessage('Описание заявки успешно обновлено!')
  } catch (error) {
    console.error('Error updating request:', error)
    showSuccessMessage('Ошибка обновления заявки', 'error')
  } finally {
    editDialog.loading = false
  }
}

const initiateDeleteRequest = (request) => {
  console.log('Initiating delete for request:', request)
  deleteDialog.requestId = request.id
  deleteDialog.serviceName = request.service_info?.name || 'эту услугу'
  deleteDialog.loading = false
  deleteDialog.show = true
}

const confirmDeleteRequest = async () => {
  if (!deleteDialog.requestId) {
    console.error('Missing request ID for deletion')
    return
  }

  console.log('Confirming delete for request ID:', deleteDialog.requestId)
  deleteDialog.loading = true

  try {
    await requestsStore.deleteRequest(deleteDialog.requestId)

    deleteDialog.show = false
    showSuccessMessage('Заявка успешно удалена!')
  } catch (error) {
    console.error('Error deleting request:', error)
    showSuccessMessage('Ошибка удаления заявки', 'error')
  } finally {
    deleteDialog.loading = false
    deleteDialog.requestId = null
  }
}

const viewRequestDetails = (request) => {
  detailsDialog.request = request
  detailsDialog.show = true
}

// Инициализация
onMounted(() => {
  if (authStore.isAuthenticated) {
    loadRequests()
  }
})
</script>

<style scoped>
.gap-1 {
  gap: 4px;
}

.gap-3 {
  gap: 12px;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Стили для таблицы */
:deep(.v-data-table) {
  border-radius: 8px;
}

:deep(.v-data-table__tr:hover) {
  background-color: rgba(25, 118, 210, 0.04) !important;
}

/* Стили для чипов статуса */
:deep(.v-chip) {
  min-width: 100px;
  justify-content: center;
}

/* Адаптивные стили */
@media (max-width: 960px) {
  :deep(.v-data-table) {
    font-size: 0.875rem;
  }

  .gap-3 {
    gap: 8px;
  }
}

@media (max-width: 600px) {
  :deep(.v-data-table-header) th {
    padding: 8px !important;
    font-size: 0.75rem;
  }

  :deep(.v-data-table-row) td {
    padding: 8px !important;
    font-size: 0.75rem;
  }
}
</style>