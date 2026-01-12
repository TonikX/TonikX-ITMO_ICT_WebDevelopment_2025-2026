<template>
  <v-container class="sales-summary">
    <!-- Заголовок -->
    <v-card elevation="2" class="pa-4 mb-4">
      <div class="d-flex align-center justify-space-between">
        <h1 class="text-h5 text-primary">Анализ продаж</h1>
      </div>
    </v-card>

    <!-- Сообщения об ошибках -->
    <v-row v-if="error">
      <v-col cols="12">
        <v-alert
          type="error"
          variant="tonal"
          closable
          @click:close="clearError"
          class="mb-6"
        >
          {{ error }}
        </v-alert>
      </v-col>
    </v-row>

    <!-- Управление фильтрами -->
    <v-card class="mb-6">
      <v-card-title class="bg-primary text-white">
        <v-icon icon="mdi-filter" class="mr-2"></v-icon>
        Фильтры анализа
      </v-card-title>
      <v-card-item>       
        <v-card-text>
          <v-row class="filters-row">
            <!-- Выбор таблицы -->
            <v-col cols="12" lg="6" md="12" class="select-col">
              <v-select
                v-model="selectedTable"
                :items="availableTables"
                item-title="name"
                item-value="key"
                label="Группировать по"
                placeholder="Выберите таблицу"
                variant="outlined"
                clearable
                @update:model-value="handleTableChange"
                :loading="loading"
                :item-props="tableItemProps"
                density="comfortable"
              >
                <template v-slot:prepend>
                  <v-icon icon="mdi-table"></v-icon>
                </template>
              </v-select>
            </v-col>

            <!-- Фильтры по времени (всегда вместе в одной строке) -->
            <v-col cols="12" lg="6" md="12" class="time-filters-col">
              <div class="time-filters-wrapper">
                <v-text-field
                  v-model="startTimeLocal"
                  type="datetime-local"
                  label="Начало периода"
                  variant="outlined"
                  density="comfortable"
                  @update:model-value="handleTimeChange"
                  clearable
                  class="time-input start-time"
                >
                  <template v-slot:prepend>
                    <v-icon icon="mdi-calendar-start"></v-icon>
                  </template>
                </v-text-field>
                
                <v-text-field
                  v-model="endTimeLocal"
                  type="datetime-local"
                  label="Конец периода"
                  variant="outlined"
                  density="comfortable"
                  @update:model-value="handleTimeChange"
                  clearable
                  class="time-input end-time"
                >
                  <template v-slot:prepend>
                    <v-icon icon="mdi-calendar-end"></v-icon>
                  </template>
                </v-text-field>
              </div>
            </v-col>
          </v-row>

          <!-- Действия фильтров -->
          <v-row class="mt-2">
            <v-col cols="12" class="d-flex justify-space-between align-center">
              <div>
                <v-btn
                  @click="resetFilters"
                  color="secondary"
                  variant="outlined"
                  :disabled="!hasActiveFilters"
                  prepend-icon="mdi-filter-remove"
                  size="small"
                >
                  Сбросить фильтр
                </v-btn>
                
                <v-chip
                  v-if="hiddenColumns.length > 0"
                  class="ml-4"
                  color="warning"
                  variant="outlined"
                  size="small"
                >
                  <v-icon icon="mdi-eye-off" size="small" class="mr-1"></v-icon>
                  Скрыто колонок: {{ hiddenColumns.length }}
                </v-chip>
              </div>
              
              <div v-if="selectedTable" class="text-caption text-medium-emphasis">
                <v-icon icon="mdi-information" size="small" class="mr-1"></v-icon>
                Данные для: {{ selectedTableName }}
              </div>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card-item>
    </v-card>

    <!-- Таблица с данными -->
    <v-card>
      <v-card-title class="bg-secondary text-white">
        <v-icon icon="mdi-table" class="mr-2"></v-icon>
        Результаты анализа
      </v-card-title>
      <v-card-text>
        <!-- Загрузка -->
        <div v-if="loading" class="text-center py-8">
          <v-progress-circular
            indeterminate
            color="primary"
            size="64"
            class="mb-4"
          ></v-progress-circular>
          <div class="text-h6 text-medium-emphasis">Загрузка данных...</div>
        </div>

        <!-- Нет выбранной таблицы -->
        <div v-else-if="!selectedTable" class="text-center py-12">
          <v-icon icon="mdi-table-question" size="64" class="mb-4 text-medium-emphasis"></v-icon>
          <div class="text-h6 text-medium-emphasis mb-2">Выберите таблицу для группировки данных</div>
          <div class="text-caption">Выберите таблицу из выпадающего списка выше</div>
        </div>

        <!-- Нет данных -->
        <div v-else-if="tableData.length === 0" class="text-center py-12">
          <v-icon icon="mdi-database-off" size="64" class="mb-4 text-medium-emphasis"></v-icon>
          <div class="text-h6 text-medium-emphasis mb-2">Нет данных для отображения</div>
          <div class="text-caption">Попробуйте изменить параметры фильтров</div>
        </div>

        <!-- Таблица с данными -->
        <div v-else class="table-container">
          <v-table class="fuel-table" hover density="comfortable">
            <thead>
              <tr>
                <th 
                  v-for="column in visibleColumns" 
                  :key="column.key"
                  class="text-left"
                  @contextmenu.prevent="openContextMenu($event, column.key)"
                >
                  <div class="d-flex align-center">
                    {{ column.label }}
                    <v-icon v-if="hiddenColumns.includes(column.key)" 
                            icon="mdi-eye-off" 
                            size="small" 
                            class="ml-1 text-warning"
                            title="Колонка скрыта"></v-icon>
                  </div>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, rowIndex) in tableData" :key="rowIndex">
                <td v-for="column in visibleColumns" :key="column.key">
                  {{ formatCellValue(row[column.key]) }}
                </td>
              </tr>
            </tbody>
          </v-table>
        </div>
      </v-card-text>
      
      <!-- Информация о таблице -->
      <v-card-actions v-if="tableData.length > 0" class="px-4 py-3 bg-grey-lighten-4">
        <div class="d-flex justify-space-between align-center w-100">
          <div class="text-caption text-medium-emphasis">
            <v-icon icon="mdi-information" size="small" class="mr-1"></v-icon>
            Показано записей: {{ tableData.length }}
          </div>
          <div class="text-caption text-medium-emphasis">
            <v-icon icon="mdi-table-column" size="small" class="mr-1"></v-icon>
            Колонок: {{ visibleColumns.length }} из {{ analyticsStore.columns.length }}
            <v-tooltip v-if="hiddenColumns.length > 0" location="top">
              <template v-slot:activator="{ props }">
                <v-chip v-bind="props" size="x-small" variant="outlined" color="warning" class="ml-2">
                  -{{ hiddenColumns.length }}
                </v-chip>
              </template>
              <span>Скрытые колонки: {{ hiddenColumns.join(', ') }}</span>
            </v-tooltip>
          </div>
        </div>
      </v-card-actions>
    </v-card>

    <!-- Контекстное меню -->
    <TableContextMenu
      :visible="contextMenu.visible"
      :position="contextMenu.position"
      :column-key="contextMenu.columnKey"
      :can-hide="canHideColumn(contextMenu.columnKey)"
      @hide="handleHideColumn"
    />
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAnalyticsStore } from '../stores/analytics'
import TableContextMenu from '../components/TableContextMenu.vue'

const route = useRoute()
const router = useRouter()
const analyticsStore = useAnalyticsStore()

// Локальные состояния для времени
const startTimeLocal = ref('')
const endTimeLocal = ref('')

// Контекстное меню
const contextMenu = ref({
  visible: false,
  position: { x: 0, y: 0 },
  columnKey: ''
})

// Флаг для предотвращения рекурсивных вызовов
const updatingFromUrl = ref(false)

// Вычисляемые свойства из хранилища
const availableTables = computed(() => analyticsStore.availableTables)
const selectedTable = computed({
  get: () => analyticsStore.selectedTable,
  set: (value) => analyticsStore.setSelectedTable(value)
})
const tableData = computed(() => analyticsStore.tableData)
const visibleColumns = computed(() => analyticsStore.visibleColumns)
const hiddenColumns = computed(() => analyticsStore.hiddenColumns)
const loading = computed(() => analyticsStore.loading)
const error = computed(() => analyticsStore.error)

// Название выбранной таблицы
const selectedTableName = computed(() => {
  if (!selectedTable.value) return ''
  const table = availableTables.value.find(t => t.key === selectedTable.value)
  return table ? table.name : selectedTable.value
})

// Свойства для элементов таблицы
const tableItemProps = (item) => ({
  title: item.name,
  subtitle: item.description,
  prependIcon: 'mdi-table'
})

// Вычисляемые свойства для проверок
const hasActiveFilters = computed(() => {
  return analyticsStore.startTime || 
         analyticsStore.endTime || 
         analyticsStore.hiddenColumns.length > 0
})

// Методы
const handleTableChange = () => {
  if (selectedTable.value) {
    updateUrl()
    loadSalesSummary()
  }
}

const handleTimeChange = () => {
  if (startTimeLocal.value) {
    const date = new Date(startTimeLocal.value)
    analyticsStore.setStartTime(date.toISOString())
  } else {
    analyticsStore.setStartTime('')
  }
  
  if (endTimeLocal.value) {
    const date = new Date(endTimeLocal.value)
    analyticsStore.setEndTime(date.toISOString())
  } else {
    analyticsStore.setEndTime('')
  }
  
  if (selectedTable.value) {
    updateUrl()
    loadSalesSummary()
  }
}

const resetFilters = () => {
  analyticsStore.resetFilters()
  startTimeLocal.value = ''
  endTimeLocal.value = ''
  
  if (selectedTable.value) {
    updateUrl()
    loadSalesSummary()
  }
}

const openContextMenu = (event, columnKey) => {
  if (!canHideColumn(columnKey)) {
    return
  }
  
  contextMenu.value = {
    visible: true,
    position: { x: event.clientX, y: event.clientY },
    columnKey
  }
  
  const closeMenu = () => {
    contextMenu.value.visible = false
    document.removeEventListener('click', closeMenu)
  }
  
  setTimeout(() => {
    document.addEventListener('click', closeMenu)
  }, 0)
}

const handleHideColumn = (columnKey) => {
  analyticsStore.addHiddenColumn(columnKey)
  contextMenu.value.visible = false
  
  if (selectedTable.value) {
    updateUrl()
    loadSalesSummary()
  }
}

const canHideColumn = (columnKey) => {
  return analyticsStore.hideableColumns.some(col => col.key === columnKey)
}

const formatCellValue = (value) => {
  if (value === null || value === undefined) {
    return '-'
  }
  
  if (typeof value === 'number' || !isNaN(Number(value))) {
    const num = Number(value)
    if (num % 1 !== 0) {
      return num.toFixed(2)
    }
  }
  
  return value
}

const updateUrl = () => {
  const params = {}
  
  if (analyticsStore.startTime) {
    params.start_time = analyticsStore.startTime
  }
  
  if (analyticsStore.endTime) {
    params.end_time = analyticsStore.endTime
  }
  
  if (analyticsStore.hiddenColumns.length > 0) {
    params.hidden_columns = analyticsStore.hiddenColumns.join(',')
  }
  
  router.push({
    name: 'SalesSummary',
    params: { modelName: analyticsStore.selectedTable || '' },
    query: params
  })
}

const loadSalesSummary = () => {
  analyticsStore.loadSalesSummary()
}

const clearError = () => {
  analyticsStore.clearError()
}

// Восстановление состояния из URL при загрузке
const restoreFromUrl = () => {
  updatingFromUrl.value = true
  
  const { modelName } = route.params
  const { start_time, end_time, hidden_columns } = route.query
  
  if (modelName) {
    selectedTable.value = modelName
  }
  
  if (start_time) {
    analyticsStore.setStartTime(start_time)
    const date = new Date(start_time)
    startTimeLocal.value = date.toISOString().slice(0, 16)
  } else {
    analyticsStore.setStartTime('')
    startTimeLocal.value = ''
  }
  
  if (end_time) {
    analyticsStore.setEndTime(end_time)
    const date = new Date(end_time)
    endTimeLocal.value = date.toISOString().slice(0, 16)
  } else {
    analyticsStore.setEndTime('')
    endTimeLocal.value = ''
  }
  
  if (hidden_columns) {
    const columns = hidden_columns.split(',').map(col => col.trim()).filter(col => col)
    analyticsStore.setHiddenColumns(columns)
  } else {
    analyticsStore.setHiddenColumns([])
  }
  
  updatingFromUrl.value = false
}

// Загрузка данных при монтировании
onMounted(async () => {
  await analyticsStore.loadAvailableTables()
  restoreFromUrl()
  
  // Если в URL есть модель, загружаем данные
  if (route.params.modelName) {
    loadSalesSummary()
  }
})

// Следим за изменениями URL для поддержки кнопок назад/вперед
watch(
  () => route.fullPath,
  () => {
    if (updatingFromUrl.value) return
    
    restoreFromUrl()
    if (route.params.modelName) {
      loadSalesSummary()
    }
  }
)

// Следим за скрытыми колонками, чтобы закрыть контекстное меню
watch(hiddenColumns, () => {
  if (contextMenu.value.visible) {
    contextMenu.value.visible = false
  }
})

// Следим за selectedTable для обновления данных
watch(selectedTable, (newValue) => {
  if (newValue && !updatingFromUrl.value) {
    loadSalesSummary()
  }
})
</script>

<style scoped>
.sales-summary {
  max-width: 100%;
  margin: 0 auto;
  padding: 12px;
}

.table-container {
  overflow-x: auto;
  border-radius: 8px;
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}

/* Стили для фильтров */
.filters-row {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.select-col {
  flex: 1 1 auto;
  min-width: 300px;
}

.time-filters-col {
  flex: 2 1 auto;
  min-width: 300px;
}

.time-filters-wrapper {
  display: flex;
  gap: 16px;
  flex-wrap: nowrap;
  min-width: 0;
}

.time-input {
  flex: 1 1 auto;
  min-width: 280px;
}

/* Принудительная ширина для input[type="datetime-local"] */
.time-input :deep(input[type="datetime-local"]) {
  min-width: 220px !important;
}

.text-h5 {
  font-size: 1.4rem !important;
}

/* Стили для карточек */
.v-card-title.bg-primary {
  background: linear-gradient(135deg, var(--v-theme-primary), var(--v-theme-primary-darken-1));
  padding: 12px 16px;
  font-size: 1rem;
}

.v-card-title.bg-secondary {
  background: linear-gradient(135deg, var(--v-theme-secondary), var(--v-theme-secondary-darken-1));
  padding: 12px 16px;
  font-size: 1rem;
}

/* Адаптивность */
@media (max-width: 1264px) {
  .filters-row {
    flex-direction: column;
  }
  
  .select-col,
  .time-filters-col {
    min-width: 100%;
  }
  
  .time-filters-wrapper {
    flex-wrap: wrap;
  }
  
  .time-input {
    min-width: calc(50% - 8px);
  }
}

@media (max-width: 768px) {
  .sales-summary {
    padding: 12px;
  }
  
  .time-filters-wrapper {
    flex-direction: column;
    gap: 12px;
  }
  
  .time-input {
    min-width: 100%;
  }
  
  .time-input :deep(input[type="datetime-local"]) {
    min-width: calc(100vw - 100px) !important;
  }
}

@media (max-width: 480px) {
  .time-input :deep(input[type="datetime-local"]) {
    min-width: calc(100vw - 80px) !important;
  }
}
</style>