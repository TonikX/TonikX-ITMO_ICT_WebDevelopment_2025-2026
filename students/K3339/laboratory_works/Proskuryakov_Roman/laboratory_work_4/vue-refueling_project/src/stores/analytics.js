import { defineStore } from 'pinia'
import { analyticsApi } from '../api/analytics'

export const useAnalyticsStore = defineStore('analytics', {
  state: () => ({
    availableTables: [],
    selectedTable: null, // Изменяем с selectedTableKey на selectedTable
    startTime: '',
    endTime: '',
    hiddenColumns: [],
    tableData: [],
    columns: [],
    loading: false,
    error: null
  }),
  
  getters: {
    // Отфильтрованные колонки (кроме скрытых)
    visibleColumns: (state) => {
      if (state.columns.length === 0) return []
      
      // Определяем колонки, которые нельзя скрывать (последние 3)
      const nonHideableColumns = state.columns.slice(-3).map(col => col.key)
      
      // Фильтруем колонки, оставляя только видимые
      return state.columns.filter(column => 
        !state.hiddenColumns.includes(column.key) || 
        nonHideableColumns.includes(column.key)
      )
    },
    
    // Колонки, которые можно скрыть (все кроме последних 3)
    hideableColumns: (state) => {
      if (state.columns.length <= 3) return []
      return state.columns.slice(0, -3)
    },
    
    // Форматированные параметры для запроса
    queryParams: (state) => {
      const params = {}
      
      if (state.startTime) {
        params.start_time = state.startTime
      }
      
      if (state.endTime) {
        params.end_time = state.endTime
      }
      
      if (state.hiddenColumns.length > 0) {
        params.hidden_columns = state.hiddenColumns.join(',')
      }
      
      return params
    }
  },
  
  actions: {
    async loadAvailableTables() {
      this.loading = true
      this.error = null
      
      try {
        const response = await analyticsApi.getAvailableTables()
        this.availableTables = response.data
      } catch (error) {
        this.error = error.response?.data || error.message
        console.error('Ошибка загрузки таблиц:', error)
      } finally {
        this.loading = false
      }
    },
    
    async loadSalesSummary() {
      if (!this.selectedTable) {
        this.tableData = []
        this.columns = []
        return
      }
      
      this.loading = true
      this.error = null
      
      try {
        const response = await analyticsApi.getSalesSummary(
          this.selectedTable,
          this.queryParams
        )
        
        this.tableData = response.data
        
        // Извлекаем колонки из первого элемента данных
        if (response.data.length > 0) {
          const firstRow = response.data[0]
          this.columns = Object.keys(firstRow).map(key => ({
            key,
            label: this.formatColumnLabel(key)
          }))
        } else {
          this.columns = []
        }
        
      } catch (error) {
        this.error = error.response?.data || error.message
        console.error('Ошибка загрузки сводки:', error)
      } finally {
        this.loading = false
      }
    },
    
    setSelectedTable(table) {
      this.selectedTable = table
      this.hiddenColumns = [] // Сбрасываем скрытые колонки при смене таблицы
    },
    
    setStartTime(time) {
      this.startTime = time
    },
    
    setEndTime(time) {
      this.endTime = time
    },
    
    addHiddenColumn(columnKey) {
      // Проверяем, можно ли скрыть эту колонку
      const canHide = this.hideableColumns.some(col => col.key === columnKey)
      if (canHide && !this.hiddenColumns.includes(columnKey)) {
        this.hiddenColumns.push(columnKey)
      }
    },
    
    removeHiddenColumn(columnKey) {
      const index = this.hiddenColumns.indexOf(columnKey)
      if (index > -1) {
        this.hiddenColumns.splice(index, 1)
      }
    },
    
    resetFilters() {
      this.startTime = ''
      this.endTime = ''
      this.hiddenColumns = []
    },
    
    formatColumnLabel(key) {
      // Преобразуем snake_case в читаемый текст
      return key
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
    },
    
    clearError() {
      this.error = null
    }
  }
})