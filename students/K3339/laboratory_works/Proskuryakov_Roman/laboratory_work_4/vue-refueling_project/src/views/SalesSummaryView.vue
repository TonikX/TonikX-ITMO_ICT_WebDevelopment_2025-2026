<template>
  <div class="sales-summary">
    <h1>Анализ продаж</h1>
    
    <!-- Сообщения об ошибках -->
    <div v-if="error" class="alert alert-error">
      {{ error }}
      <button @click="clearError" class="close-btn">×</button>
    </div>
    
    <!-- Управление фильтрами -->
    <div class="filters-section">
      <div class="filter-group">
        <label for="table-select">Группировать по:</label>
        <select 
          id="table-select" 
          v-model="selectedTable"
          @change="handleTableChange"
          class="table-select"
        >
          <option value="" disabled>Выберите таблицу</option>
          <option 
            v-for="table in availableTables" 
            :key="table.key"
            :value="table.key"
            :title="table.description"
          >
            {{ table.name }}
          </option>
        </select>
      </div>
      
      <div class="time-filters">
        <div class="filter-group">
          <label for="start-time">Начало периода:</label>
          <input
            id="start-time"
            v-model="startTimeLocal"
            type="datetime-local"
            @change="handleTimeChange"
          />
        </div>
        
        <div class="filter-group">
          <label for="end-time">Конец периода:</label>
          <input
            id="end-time"
            v-model="endTimeLocal"
            type="datetime-local"
            @change="handleTimeChange"
          />
        </div>
      </div>
      
      <div class="filter-actions">
        <button 
          @click="resetFilters" 
          class="reset-btn"
          :disabled="!hasActiveFilters"
        >
          Сбросить фильтр
        </button>
        
        <div v-if="hiddenColumns.length > 0" class="hidden-columns-info">
          <span>Скрытые колонки: {{ hiddenColumns.length }}</span>
        </div>
      </div>
    </div>
    
    <!-- Таблица с данными -->
    <div class="table-section">
      <div v-if="loading" class="loading">
        Загрузка данных...
      </div>
      
      <div v-else-if="!selectedTable" class="no-table-selected">
        Выберите таблицу для группировки данных
      </div>
      
      <div v-else-if="tableData.length === 0" class="no-data">
        Нет данных для отображения
      </div>
      
      <div v-else class="table-container">
        <table class="summary-table">
          <thead>
            <tr>
              <th 
                v-for="column in visibleColumns" 
                :key="column.key"
                @contextmenu.prevent="openContextMenu($event, column.key)"
              >
                {{ column.label }}
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
        </table>
      </div>
    </div>
    
    <!-- Контекстное меню -->
    <TableContextMenu
      :visible="contextMenu.visible"
      :position="contextMenu.position"
      :column-key="contextMenu.columnKey"
      :can-hide="canHideColumn(contextMenu.columnKey)"
      @hide="handleHideColumn"
    />
  </div>
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
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem;
}

.alert {
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 4px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.alert-error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: inherit;
}

.filters-section {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.filter-group {
  margin-bottom: 1rem;
}

.filter-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: #333;
}

.table-select {
  width: 100%;
  max-width: 400px;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.time-filters {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

.time-filters input[type="datetime-local"] {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.filter-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
}

.reset-btn {
  padding: 0.5rem 1rem;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.reset-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.reset-btn:not(:disabled):hover {
  background-color: #5a6268;
}

.hidden-columns-info {
  font-size: 0.9rem;
  color: #666;
}

.table-section {
  margin-top: 2rem;
}

.loading, .no-table-selected, .no-data {
  padding: 3rem;
  text-align: center;
  background-color: #f8f9fa;
  border-radius: 8px;
  color: #666;
  font-size: 1.1rem;
}

.table-container {
  overflow-x: auto;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.summary-table {
  width: 100%;
  border-collapse: collapse;
}

.summary-table th {
  background-color: #f8f9fa;
  padding: 1rem;
  text-align: left;
  font-weight: bold;
  border-bottom: 2px solid #dee2e6;
  cursor: pointer;
  position: relative;
  user-select: none;
}

.summary-table th:hover {
  background-color: #e9ecef;
}

.summary-table td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #dee2e6;
}

.summary-table tr:last-child td {
  border-bottom: none;
}

.summary-table tr:hover {
  background-color: #f8f9fa;
}

/* Адаптивность */
@media (max-width: 768px) {
  .time-filters {
    grid-template-columns: 1fr;
  }
  
  .filter-actions {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}
</style>