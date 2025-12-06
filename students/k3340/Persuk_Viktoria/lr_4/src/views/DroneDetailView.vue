<template>
  <div>
    <v-btn
      prepend-icon="mdi-arrow-left"
      variant="text"
      @click="$router.push('/drones')"
      class="mb-4"
    >
      Назад к списку
    </v-btn>

    <v-card v-if="loading">
      <v-card-text>
        <v-progress-circular
          indeterminate
          color="primary"
          class="d-block mx-auto"
        ></v-progress-circular>
      </v-card-text>
    </v-card>

    <div v-else-if="drone">
      <!-- Информация о дроне -->
      <v-card class="mb-4">
        <v-card-title class="d-flex justify-space-between align-center">
          <div>
            <h2 class="text-h4">{{ drone.manufacturer }} {{ drone.model }}</h2>
            <div class="text-body-2 text-grey">{{ drone.serial_number }}</div>
          </div>
          <div>
            <v-btn
              color="primary"
              prepend-icon="mdi-pencil"
              @click="editDrone"
              class="mr-2"
            >
              Редактировать
            </v-btn>
            <v-btn
              color="error"
              prepend-icon="mdi-delete"
              @click="confirmDelete"
            >
              Удалить
            </v-btn>
          </div>
        </v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="12" md="6">
              <v-chip
                :color="getStatusColor(drone.status)"
                class="mb-2"
              >
                {{ getStatusLabel(drone.status) }}
              </v-chip>
              <v-chip
                :color="getCategoryColor(drone.category)"
                class="ml-2"
              >
                {{ getCategoryLabel(drone.category) }}
              </v-chip>
              <div class="mt-4">
                <div><strong>Камера:</strong> {{ drone.has_camera ? 'Да' : 'Нет' }}</div>
                <div v-if="drone.weight"><strong>Вес:</strong> {{ drone.weight }} кг</div>
                <div v-if="drone.max_speed"><strong>Максимальная скорость:</strong> {{ drone.max_speed }} км/ч</div>
                <div v-if="drone.max_flight_distance"><strong>Максимальная дистанция:</strong> {{ drone.max_flight_distance }} км</div>
                <div v-if="drone.length || drone.width || drone.height">
                  <strong>Размеры:</strong>
                  {{ drone.length ? `${drone.length}×` : '' }}
                  {{ drone.width ? `${drone.width}×` : '' }}
                  {{ drone.height ? `${drone.height}` : '' }} см
                </div>
                <div v-if="drone.registration_date">
                  <strong>Дата регистрации:</strong>
                  {{ formatDate(drone.registration_date) }}
                </div>
              </div>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Вкладки -->
      <v-tabs v-model="tab" color="primary" class="mb-4">
        <v-tab value="flights">Полёты ({{ drone.flights?.length || 0 }})</v-tab>
        <v-tab value="documents">Документы ({{ drone.documents?.length || 0 }})</v-tab>
      </v-tabs>

      <v-window v-model="tab">
        <!-- Вкладка полётов -->
        <v-window-item value="flights">
          <v-card>
            <v-card-title class="d-flex justify-space-between align-center">
              <span>Полёты</span>
              <v-btn
                color="primary"
                prepend-icon="mdi-plus"
                @click="showFlightDialog = true"
              >
                Добавить полёт
              </v-btn>
            </v-card-title>
            <v-card-text>
              <v-list v-if="drone.flights && drone.flights.length > 0">
                <v-list-item
                  v-for="flight in drone.flights"
                  :key="flight.id"
                  prepend-icon="mdi-airplane"
                  @click="$router.push(`/flights/${flight.id}`)"
                >
                  <v-list-item-title>
                    Полёт #{{ flight.id }} - {{ formatDateTime(flight.start_datetime) }}
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    {{ flight.location }} | Дистанция: {{ flight.distance }} км | Батарея: {{ flight.battery_usage }}%
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
              <div v-else class="text-center text-h6 pa-4">
                Полёты не найдены
              </div>
            </v-card-text>
          </v-card>
        </v-window-item>

        <!-- Вкладка документов -->
        <v-window-item value="documents">
          <v-card>
            <v-card-title class="d-flex justify-space-between align-center">
              <span>Документы</span>
              <v-btn
                color="primary"
                prepend-icon="mdi-plus"
                @click="showDocumentDialog = true"
              >
                Добавить документ
              </v-btn>
            </v-card-title>
            <v-card-text>
              <v-list v-if="drone.documents && drone.documents.length > 0">
                <v-list-item
                  v-for="document in drone.documents"
                  :key="document.id"
                  :prepend-icon="mdi-file-document"
                >
                  <v-list-item-title>
                    {{ getDocumentTypeLabel(document.document_type) }}
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    {{ formatDateTime(document.uploaded_at) }}
                  </v-list-item-subtitle>
                  <template v-slot:append>
                    <v-btn
                      icon
                      variant="text"
                      :href="document.url"
                      target="_blank"
                    >
                      <v-icon>mdi-open-in-new</v-icon>
                    </v-btn>
                    <v-btn
                      icon
                      variant="text"
                      color="error"
                      @click="deleteDocument(document.id)"
                    >
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </template>
                </v-list-item>
              </v-list>
              <div v-else class="text-center text-h6 pa-4">
                Документы не найдены
              </div>
            </v-card-text>
          </v-card>
        </v-window-item>
      </v-window>

      <!-- Диалог создания полёта -->
      <FlightDialog
        v-model="showFlightDialog"
        :drone-id="parseInt($route.params.id)"
        @saved="loadDrone"
      />

      <!-- Диалог создания документа -->
      <DocumentDialog
        v-model="showDocumentDialog"
        :drone-id="parseInt($route.params.id)"
        @saved="loadDrone"
      />

      <!-- Диалог редактирования дрона -->
      <DroneEditDialog
        v-model="showEditDialog"
        :drone="drone"
        @saved="loadDrone"
      />

      <!-- Диалог подтверждения удаления -->
      <v-dialog v-model="showDeleteDialog" max-width="400">
        <v-card>
          <v-card-title>Подтверждение удаления</v-card-title>
          <v-card-text>
            Вы уверены, что хотите удалить дрон {{ drone.manufacturer }} {{ drone.model }}?
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn variant="text" @click="showDeleteDialog = false">Отмена</v-btn>
            <v-btn color="error" @click="deleteDrone">Удалить</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import * as dronesAPI from '@/api/drones'
import * as documentsAPI from '@/api/documents'
import FlightDialog from '@/components/FlightDialog.vue'
import DocumentDialog from '@/components/DocumentDialog.vue'
import DroneEditDialog from '@/components/DroneEditDialog.vue'

const route = useRoute()
const router = useRouter()
const showSnackbar = inject('showSnackbar')

const loading = ref(false)
const drone = ref(null)
const tab = ref('flights')
const showFlightDialog = ref(false)
const showDocumentDialog = ref(false)
const showEditDialog = ref(false)
const showDeleteDialog = ref(false)

const categoryOptions = [
  { title: 'Любительский', value: 'hobby' },
  { title: 'Коммерческий', value: 'commercial' },
  { title: 'Профессиональный', value: 'pro' },
]

const statusOptions = [
  { title: 'Активен', value: 'active' },
  { title: 'Требуется проверка', value: 'pending' },
  { title: 'Архивирован', value: 'archived' },
]

const documentTypeOptions = [
  { title: 'Сертификат соответствия', value: 'certificate' },
  { title: 'Страховой полис', value: 'insurance' },
  { title: 'Фото дрона', value: 'photo' },
  { title: 'Лицензия/разрешение', value: 'license' },
  { title: 'Прочее', value: 'other' },
]

const getStatusLabel = (status) => {
  const option = statusOptions.find(opt => opt.value === status)
  return option ? option.title : status
}

const getStatusColor = (status) => {
  const colors = { active: 'success', pending: 'warning', archived: 'grey' }
  return colors[status] || 'grey'
}

const getCategoryLabel = (category) => {
  const option = categoryOptions.find(opt => opt.value === category)
  return option ? option.title : category
}

const getCategoryColor = (category) => {
  const colors = { hobby: 'info', commercial: 'primary', pro: 'purple' }
  return colors[category] || 'grey'
}

const getDocumentTypeLabel = (type) => {
  const option = documentTypeOptions.find(opt => opt.value === type)
  return option ? option.title : type
}

const formatDate = (dateString) => {
  if (!dateString) return 'Не указано'
  return new Date(dateString).toLocaleDateString('ru-RU')
}

const formatDateTime = (dateString) => {
  if (!dateString) return 'Не указано'
  return new Date(dateString).toLocaleString('ru-RU')
}

const loadDrone = async () => {
  loading.value = true
  try {
    drone.value = await dronesAPI.getDrone(route.params.id)
  } catch (error) {
    showSnackbar('Ошибка загрузки дрона', 'error')
    router.push('/drones')
  } finally {
    loading.value = false
  }
}

const editDrone = () => {
  showEditDialog.value = true
}

const confirmDelete = () => {
  showDeleteDialog.value = true
}

const deleteDrone = async () => {
  try {
    await dronesAPI.deleteDrone(route.params.id)
    showSnackbar('Дрон успешно удалён', 'success')
    router.push('/drones')
  } catch (error) {
    showSnackbar('Ошибка удаления дрона', 'error')
  }
}

const deleteDocument = async (documentId) => {
  try {
    await documentsAPI.deleteDocument(documentId)
    showSnackbar('Документ успешно удалён', 'success')
    loadDrone()
  } catch (error) {
    showSnackbar('Ошибка удаления документа', 'error')
  }
}

onMounted(() => {
  loadDrone()
})
</script>
