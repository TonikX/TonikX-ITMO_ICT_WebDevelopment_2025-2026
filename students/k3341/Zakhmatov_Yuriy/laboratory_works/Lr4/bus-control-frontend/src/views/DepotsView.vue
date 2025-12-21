<template>
  <div>
    <!-- Заголовок и кнопки -->
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card color="purple-darken-3" dark>
          <v-card-title class="text-h4">
            <v-icon icon="mdi-garage" size="large" class="mr-3"></v-icon>
            Автобусные депо
          </v-card-title>
          <v-card-subtitle class="text-h6">
            Управление местами стоянки автобусов
          </v-card-subtitle>
          <v-card-actions>
            <v-btn color="white" variant="outlined" @click="openCreateDialog">
              <v-icon icon="mdi-plus-circle" class="mr-2"></v-icon>
              Добавить депо
            </v-btn>
            <v-btn color="white" variant="text" @click="fetchDepots">
              <v-icon icon="mdi-refresh" class="mr-2"></v-icon>
              Обновить
            </v-btn>
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              label="Поиск депо..."
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              density="compact"
              clearable
              hide-details
              style="max-width: 300px;"
              class="bg-white rounded"
            ></v-text-field>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Карточки депо -->
    <v-row>
      <v-col
        v-for="depot in filteredDepots"
        :key="depot.id"
        cols="12" md="6" lg="4"
      >
        <v-card elevation="3" class="h-100">
          <v-card-title class="text-h6 d-flex justify-space-between align-center">
            <div class="d-flex align-center">
              <v-icon icon="mdi-garage" class="mr-2"></v-icon>
              {{ depot.name }}
            </div>
            <v-chip :color="getDepotStatusColor(depot)" size="small">
              {{ getDepotStatus(depot) }}
            </v-chip>
          </v-card-title>
          <v-card-subtitle>
            {{ depot.address }}
          </v-card-subtitle>
          <v-card-text>
            <!-- Контакты -->
            <v-list density="compact" class="mb-3">
              <v-list-item v-if="depot.phone">
                <template v-slot:prepend>
                  <v-icon icon="mdi-phone"></v-icon>
                </template>
                <v-list-item-title>{{ depot.phone }}</v-list-item-title>
              </v-list-item>

              <v-list-item v-if="depot.email">
                <template v-slot:prepend>
                  <v-icon icon="mdi-email"></v-icon>
                </template>
                <v-list-item-title>{{ depot.email }}</v-list-item-title>
              </v-list-item>
            </v-list>

            <!-- Статистика -->
            <div class="mb-3">
              <div class="d-flex justify-space-between mb-1">
                <span class="text-caption">Статистика депо</span>
                <span class="text-caption font-weight-bold">
                  {{ depot.current_occupancy || 0 }}/{{ depot.capacity || 0 }}
                </span>
              </div>
              <v-progress-linear
                :model-value="calculateOccupancyPercentage(depot)"
                :color="getOccupancyColor(depot)"
                height="10"
                rounded
              ></v-progress-linear>

              <div class="d-flex justify-space-between mt-1">
                <div>
                  <span class="text-caption text-medium-emphasis mr-2">
                    {{ calculateOccupancyPercentage(depot).toFixed(1) }}%
                  </span>
                  <v-chip
                    v-if="depot.active_buses !== undefined"
                    size="x-small"
                    color="green"
                  >
                    {{ depot.active_buses }} акт.
                  </v-chip>
                </div>
                <span class="text-caption text-medium-emphasis">
                  Свободно: {{ depot.free_spaces || 0 }}
                </span>
              </div>

              <!-- Неактивные автобусы -->
              <div v-if="depot.inactive_buses !== undefined && depot.inactive_buses > 0"
                   class="mt-1 text-caption text-red">
                Неактивных: {{ depot.inactive_buses }}
              </div>
            </div>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              icon="mdi-eye"
              size="small"
              color="info"
              variant="text"
              @click="viewDepot(depot)"
              title="Просмотр"
            ></v-btn>
            <v-btn
              icon="mdi-pencil"
              size="small"
              color="warning"
              variant="text"
              @click="editDepot(depot)"
              title="Редактировать"
            ></v-btn>
            <v-btn
              icon="mdi-delete"
              size="small"
              color="error"
              variant="text"
              @click="deleteDepot(depot)"
              title="Удалить"
              :disabled="depot.current_occupancy > 0"
            ></v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Диалог создания/редактирования -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title class="text-h5">
          <v-icon :icon="editMode ? 'mdi-pencil' : 'mdi-plus-circle'" class="mr-2"></v-icon>
          {{ editMode ? 'Редактирование депо' : 'Новое депо' }}
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="localForm.name"
                  label="Название депо*"
                  required
                  variant="outlined"
                  :rules="[v => !!v || 'Название обязательно']"
                  hint="Пример: Третий, Первый, Центральное"
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-text-field
                  v-model="localForm.address"
                  label="Адрес*"
                  required
                  variant="outlined"
                  :rules="[v => !!v || 'Адрес обязателен']"
                  hint="Полный адрес с городом, улицей, домом"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model.number="localForm.capacity"
                  label="Вместимость (автобусов)*"
                  type="number"
                  required
                  variant="outlined"
                  :rules="[
                    v => !!v || 'Вместимость обязательна',
                    v => v > 0 || 'Вместимость должна быть больше 0',
                    v => v <= 100 || 'Вместимость не может превышать 100'
                  ]"
                  hint="Максимальное количество автобусов"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="localForm.phone"
                  label="Телефон"
                  variant="outlined"
                  hint="Формат: +7(XXX)XXX-XX-XX"
                  counter="20"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="localForm.email"
                  label="Email"
                  type="email"
                  variant="outlined"
                  :rules="[v => !v || /.+@.+\..+/.test(v) || 'Email должен быть валидным']"
                  hint="example@mail.com"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="closeDialog">
            Отмена
          </v-btn>
          <v-btn color="primary" variant="flat" @click="saveDepot" :loading="saving">
            Сохранить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог подтверждения удаления -->
    <v-dialog v-model="deleteDialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">Подтверждение удаления</v-card-title>
        <v-card-text>
          <template v-if="depotToDelete?.current_occupancy > 0">
            <v-alert type="warning" variant="tonal" class="mb-4">
              В этом депо находятся {{ depotToDelete?.current_occupancy }} автобусов!
            </v-alert>
            <p>
              Вы не можете удалить депо <strong>{{ depotToDelete?.name }}</strong>,
              так как в нем находятся автобусы.
            </p>
            <p class="text-error">
              Сначала переместите все автобусы в другие депо.
            </p>
          </template>
          <template v-else>
            <p>
              Вы уверены, что хотите удалить депо
              <strong>{{ depotToDelete?.name }}</strong>?
            </p>
            <p class="text-error">
              Это действие нельзя отменить!
            </p>
          </template>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="deleteDialog = false">
            Отмена
          </v-btn>
          <v-btn
            v-if="!depotToDelete?.current_occupancy || depotToDelete.current_occupancy === 0"
            color="error"
            variant="flat"
            @click="confirmDelete"
            :loading="deleting"
          >
            Удалить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог просмотра -->
    <v-dialog v-model="viewDialog" max-width="700px">
      <v-card v-if="viewingDepot">
        <v-card-title class="text-h5">
          <v-icon icon="mdi-garage" class="mr-2"></v-icon>
          Депо "{{ viewingDepot.name }}"
        </v-card-title>

        <v-card-text>
          <v-row class="mb-4">
            <v-col cols="12" class="text-center">
              <v-avatar :color="getDepotStatusColor(viewingDepot)" size="120">
                <v-icon icon="mdi-garage" size="x-large" color="white"></v-icon>
              </v-avatar>
              <h2 class="mt-4">{{ viewingDepot.name }}</h2>
              <v-chip color="grey" variant="outlined" class="mt-2">
                ID: {{ viewingDepot.id }}
              </v-chip>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <v-row>
            <v-col cols="12" md="6">
              <v-list density="compact">
                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-map-marker"></v-icon>
                  </template>
                  <v-list-item-title>Адрес</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ viewingDepot.address }}
                  </v-list-item-subtitle>
                </v-list-item>

                <v-list-item v-if="viewingDepot.phone">
                  <template v-slot:prepend>
                    <v-icon icon="mdi-phone"></v-icon>
                  </template>
                  <v-list-item-title>Телефон</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ viewingDepot.phone }}
                  </v-list-item-subtitle>
                </v-list-item>

                <v-list-item v-if="viewingDepot.email">
                  <template v-slot:prepend>
                    <v-icon icon="mdi-email"></v-icon>
                  </template>
                  <v-list-item-title>Email</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ viewingDepot.email }}
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-col>

            <v-col cols="12" md="6">
              <v-list density="compact">
                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-bus-multiple"></v-icon>
                  </template>
                  <v-list-item-title>Вместимость</v-list-item-title>
                  <v-list-item-subtitle>
                    <v-chip :color="getOccupancyColor(viewingDepot)" size="small">
                      {{ viewingDepot.current_occupancy || 0 }}/{{ viewingDepot.capacity || 0 }}
                    </v-chip>
                  </v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-parking"></v-icon>
                  </template>
                  <v-list-item-title>Свободных мест</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ viewingDepot.free_spaces || 0 }}
                  </v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-chart-pie"></v-icon>
                  </template>
                  <v-list-item-title>Загруженность</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ calculateOccupancyPercentage(viewingDepot).toFixed(1) }}%
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-col>
          </v-row>

          <!-- Детальная статистика -->
          <v-row v-if="viewingDepot.active_buses !== undefined">
            <v-col cols="12">
              <v-divider class="my-4"></v-divider>
              <v-card variant="tonal" color="purple">
                <v-card-title class="text-h6">
                  <v-icon icon="mdi-chart-box" class="mr-2"></v-icon>
                  Статистика депо
                </v-card-title>
                <v-card-text>
                  <v-row>
                    <v-col cols="12" sm="4" class="text-center">
                      <div class="text-h4 text-green">{{ viewingDepot.active_buses }}</div>
                      <div class="text-subtitle-2">Активных автобусов</div>
                    </v-col>
                    <v-col cols="12" sm="4" class="text-center">
                      <div class="text-h4 text-red">{{ viewingDepot.inactive_buses || 0 }}</div>
                      <div class="text-subtitle-2">Неактивных автобусов</div>
                    </v-col>
                    <v-col cols="12" sm="4" class="text-center">
                      <div class="text-h4 text-blue">{{ viewingDepot.free_spaces || 0 }}</div>
                      <div class="text-subtitle-2">Свободных мест</div>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="text" @click="viewDialog = false">
            Закрыть
          </v-btn>
          <v-btn color="warning" variant="text" @click="editDepot(viewingDepot)">
            Редактировать
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Уведомления -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="3000">
      {{ snackbar.message }}
      <template v-slot:actions>
        <v-btn icon="mdi-close" @click="snackbar.show = false"></v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
  import {ref, computed, onMounted, reactive} from 'vue'
  import apiClient from '@/api/axios'

  export default {
  setup() {
  // Состояние
  const depots = ref([])
  const loading = ref(false)
  const saving = ref(false)
  const deleting = ref(false)
  const dialog = ref(false)
  const deleteDialog = ref(false)
  const viewDialog = ref(false)
  const editMode = ref(false)
  const search = ref('')

  // Локальная форма
  const localForm = reactive({
  id: null,
  name: '',
  address: '',
  capacity: 20,
  phone: '',
  email: ''
})

  // Для удаления и просмотра
  const depotToDelete = ref(null)
  const viewingDepot = ref(null)

  // Уведомления
  const snackbar = reactive({
  show: false,
  message: '',
  color: 'success'
})

  // Вспомогательные функции
  const calculateOccupancyPercentage = (depot) => {
  if (!depot || !depot.capacity || depot.capacity === 0) return 0
  const occupancy = depot.current_occupancy || 0
  return (occupancy / depot.capacity) * 100
}

  const calculateFreeSpaces = (depot) => {
  if (!depot || !depot.capacity) return 0
  const occupancy = depot.current_occupancy || 0
  return Math.max(0, depot.capacity - occupancy)
}

  const getOccupancyColor = (depot) => {
  const percentage = calculateOccupancyPercentage(depot)
  if (percentage < 50) return 'green'
  if (percentage < 80) return 'orange'
  return 'red'
}

  const getDepotStatusColor = (depot) => {
  const percentage = calculateOccupancyPercentage(depot)
  if (percentage === 0) return 'grey'
  if (percentage < 50) return 'green'
  if (percentage < 80) return 'blue'
  if (percentage < 95) return 'orange'
  return 'red'
}

  const getDepotStatus = (depot) => {
  const percentage = calculateOccupancyPercentage(depot)
  if (percentage === 0) return 'Пустое'
  if (percentage < 50) return 'Мало загружено'
  if (percentage < 80) return 'Средняя загрузка'
  if (percentage < 95) return 'Почти заполнено'
  return 'Переполнено'
}

  // Вычисляемые свойства
  const filteredDepots = computed(() => {
  if (!search.value.trim()) return depots.value

  const searchLower = search.value.toLowerCase().trim()
  return depots.value.filter(depot =>
  depot.name?.toLowerCase().includes(searchLower) ||
  depot.address?.toLowerCase().includes(searchLower) ||
  depot.phone?.toLowerCase().includes(searchLower) ||
  depot.email?.toLowerCase().includes(searchLower)
  )
})

  const fetchDepotStatistics = async (depotId) => {
  try {
  const response = await apiClient.get(`depots/${depotId}/statistics/`)
  console.log(`📊 Статистика для депо ${depotId}:`, response.data)
  const stats = response.data

  return {
  capacity: stats.capacity,
  current_occupancy: stats.current_occupancy,
  free_spaces: stats.free_spaces,
  active_buses: stats.active_buses,
  inactive_buses: stats.inactive_buses
}
} catch (error) {
  console.warn(`Не удалось загрузить статистику для депо ${depotId}:`, error)
  return null
}
}

  // API функции
  const fetchDepots = async () => {
  loading.value = true
  try {
  // GET запрос за всеми депо
  const response = await apiClient.get('depots/')
  const depotList = response.data || []

  console.log(' Получены депо с сервера:', depotList)

  const depotsWithStats = await Promise.all(
  depotList.map(async (depot) => {
  try {
  // Загружаем статистику для каждого депо
  const stats = await fetchDepotStatistics(depot.id)

  return {
  ...depot,  // Базовые данные (id, name, address, phone, email)
  capacity: stats?.capacity || depot.capacity || 0,
  current_occupancy: stats?.current_occupancy || 0,
  free_spaces: stats?.free_spaces || calculateFreeSpaces({
  capacity: depot.capacity,
  current_occupancy: 0
}),
  active_buses: stats?.active_buses || 0,
  inactive_buses: stats?.inactive_buses || 0
}
} catch (error) {
  console.warn(`Ошибка при обработке депо ${depot.id}:`, error)
  // Возвращаем депо без статистики
}
})
  )

  depots.value = depotsWithStats
  console.log('Депо с статистикой:', depots.value)
} catch (error) {
    console.error('Ошибка загрузки списка депо:', error)

  } finally {
  loading.value = false
}
}

  // CRUD операции
  const openCreateDialog = () => {
  editMode.value = false
  resetForm()
  dialog.value = true
}

  const editDepot = (depot) => {
  editMode.value = true
  Object.assign(localForm, {
  id: depot.id,
  name: depot.name || '',
  address: depot.address || '',
  capacity: depot.capacity || 20,
  phone: depot.phone || '',
  email: depot.email || ''
})
  dialog.value = true
}

  const viewDepot = (depot) => {
  viewingDepot.value = {...depot}
  viewDialog.value = true
}

  const saveDepot = async () => {
  // Валидация
  if (!localForm.name.trim()) {
  showSnackbar('Введите название депо', 'error')
  return
}
  if (!localForm.address.trim()) {
  showSnackbar('Введите адрес депо', 'error')
  return
}
  if (!localForm.capacity || localForm.capacity <= 0 || localForm.capacity > 100) {
  showSnackbar('Введите корректную вместимость (1-100)', 'error')
  return
}

  saving.value = true
  try {
  // 🔴 ВАЖНО: Проверьте, какой формат данных ожидает бэкенд
  const depotData = {
  name: localForm.name.trim(),
  address: localForm.address.trim(),
  capacity: Number(localForm.capacity),
  phone: localForm.phone.trim() || null,  // null может быть проблемой, попробуйте ''
  email: localForm.email.trim() || null    // null может быть проблемой, попробуйте ''
}

  console.log('📤 Отправляемые данные (JSON):', JSON.stringify(depotData))

  if (editMode.value) {
  // Обновление существующего депо
  await apiClient.put(`depots/${localForm.id}/`, depotData)
  showSnackbar('Депо успешно обновлено', 'success')
} else {
  // Создание нового депо
  console.log('🚀 Отправка POST запроса на /depots/')

  // 🔴 ДЕБАГ: Проверим, что именно отправляется
  console.log('Тип данных:', typeof depotData)
  console.log('Capacity тип:', typeof depotData.capacity)

  try {
  const response = await apiClient.post('depots/', depotData)
  console.log('✅ Успешный ответ:', response.data)
  showSnackbar('Депо успешно создано', 'success')
} catch (postError) {
  console.error('❌ Ошибка 400 Bad Request:')

  // 🔴 ВАЖНО: Выводим полные детали ошибки
  if (postError.response?.data) {
  console.error('Полный ответ сервера:')
  console.dir(postError.response.data, {depth: null})

  // Если это Django REST Framework ошибки валидации
  if (typeof postError.response.data === 'object') {
  console.error('Ошибки по полям:')
  for (const [field, errors] of Object.entries(postError.response.data)) {
  console.error(`  ${field}:`, errors)
}
}
}

  throw postError
}
}

  // Обновляем список депо
  await fetchDepots()

  // Закрываем диалог
  closeDialog()
} catch (error) {
  console.error('💥 Итоговая ошибка сохранения:', error)

  let errorMessage = 'Ошибка сохранения'

  // 🔴 ИСПРАВЛЕНО: Парсим ошибки Django REST Framework
  if (error.response?.data) {
  const data = error.response.data

  if (typeof data === 'string') {
  errorMessage = data
}
  else if (data.detail) {
  errorMessage = data.detail
}
  else if (typeof data === 'object') {
  // Обрабатываем ошибки валидации полей
  const fieldErrors = []

  for (const [field, errors] of Object.entries(data)) {
  if (Array.isArray(errors)) {
  fieldErrors.push(`${field}: ${errors.join(', ')}`)
} else if (typeof errors === 'string') {
  fieldErrors.push(`${field}: ${errors}`)
}
}

  if (fieldErrors.length > 0) {
  errorMessage = fieldErrors.join('; ')
} else {
  errorMessage = JSON.stringify(data)
}
}
}

  showSnackbar(errorMessage, 'error')
} finally {
  saving.value = false
}
}

  const deleteDepot = (depot) => {
  depotToDelete.value = depot
  deleteDialog.value = true
}

  const confirmDelete = async () => {
  if (!depotToDelete.value) return

  deleting.value = true
  try {
  await apiClient.delete(`depots/${depotToDelete.value.id}/`)
  showSnackbar('Депо успешно удалено', 'success')
  await fetchDepots()
} catch (error) {
  console.error('Ошибка удаления:', error)
  const errorMessage = error.response?.data?.detail || 'Ошибка удаления'
  showSnackbar(errorMessage, 'error')
} finally {
  deleting.value = false
  deleteDialog.value = false
  depotToDelete.value = null
}
}

  const closeDialog = () => {
  dialog.value = false
  resetForm()
}

  const resetForm = () => {
  Object.assign(localForm, {
  id: null,
  name: '',
  address: '',
  capacity: 20,
  phone: '',
  email: ''
})
  editMode.value = false
}

  const showSnackbar = (message, color = 'success') => {
  snackbar.message = message
  snackbar.color = color
  snackbar.show = true
}

  // Инициализация
  onMounted(() => {
  console.log('🚀 Компонент DepotsView инициализирован')
  fetchDepots()
})

  return {
  // Состояние
  depots,
  loading,
  saving,
  deleting,
  dialog,
  deleteDialog,
  viewDialog,
  editMode,
  search,
  localForm,
  depotToDelete,
  viewingDepot,
  snackbar,

  // Данные
  filteredDepots,

  // Методы
  fetchDepots,
  openCreateDialog,
  editDepot,
  viewDepot,
  saveDepot,
  deleteDepot,
  confirmDelete,
  closeDialog,

  // Вспомогательные методы
  calculateOccupancyPercentage,
  calculateFreeSpaces,
  getOccupancyColor,
  getDepotStatusColor,
  getDepotStatus,
  showSnackbar
}
}
}
</script>

<style scoped>
.h-100 {
  height: 100%;
}

.text-success {
  color: #4CAF50;
}

.text-error {
  color: #F44336;
}

.text-green {
  color: #4CAF50;
}

.text-red {
  color: #F44336;
}

.text-blue {
  color: #2196F3;
}

.text-purple {
  color: #9C27B0;
}

/* Анимации */
.v-card {
  transition: transform 0.3s ease;
}

.v-card:hover {
  transform: translateY(-5px);
}

/* Стили для прогресс-бара */
.v-progress-linear {
  border-radius: 5px;
}

/* Стили для чипов */
.v-chip {
  transition: all 0.2s;
}

.v-chip:hover {
  transform: scale(1.05);
}
</style>
