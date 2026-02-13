<template>
  <div class="on-loan-view">
    <h1>Книги на руках</h1>

    <!-- Доступ только админам -->
    <div v-if="!isAdmin" class="not-admin">
      <p>Эта страница доступна только администраторам.</p>
    </div>

    <div v-else>
      <!-- Кнопка обновления -->
      <div class="controls">
        <v-btn
          color="primary"
          @click="loadData"
          :loading="loading"
          prepend-icon="mdi-refresh"
        >
          {{ loading ? 'Загрузка...' : 'Обновить список' }}
        </v-btn>
      </div>

      <!-- Состояния загрузки/ошибки -->
      <div v-if="loading" class="loading">Загрузка данных...</div>
      <div v-else-if="error" class="error">{{ error }}</div>

      <div v-else>
        <!-- ===== ВСЕ АКТИВНЫЕ ВЫДАЧИ ===== -->
        <div class="section">
          <h2>📋 Все активные выдачи ({{ allLoans.length }})</h2>

          <v-data-table
            v-if="allLoans.length"
            :headers="allHeaders"
            :items="allLoans"
            class="elevation-1"
            density="comfortable"
          >
            <!-- Статус с цветным бейджем -->
            <template v-slot:item.status="{ item }">
              <v-chip
                :color="item.days_overdue > 0 ? 'warning' : 'success'"
                size="small"
              >
                {{ item.days_overdue > 0 ? 'Просрочена' : 'В сроке' }}
              </v-chip>
            </template>

            <!-- Формат дат -->
            <template v-slot:item.issued_at="{ item }">
              {{ formatDate(item.issued_at) }}
            </template>
            <template v-slot:item.due_date="{ item }">
              {{ formatDate(item.due_date) }}
            </template>
          </v-data-table>

          <div v-else class="no-data">
            <v-icon size="48" color="grey-lighten-1">mdi-book-off</v-icon>
            <p class="text-grey mt-2">Нет активных выдач</p>
          </div>
        </div>

        <v-divider class="my-6"></v-divider>

        <!-- ===== ПРОСРОЧЕННЫЕ КНИГИ ===== -->
        <div class="section">
          <h2>⚠️ Просроченные книги ({{ overdueLoans.length }})</h2>

          <v-data-table
            v-if="overdueLoans.length"
            :headers="overdueHeaders"
            :items="overdueLoans"
            class="elevation-1"
            density="comfortable"
          >
            <template v-slot:item.issued_at="{ item }">
              {{ formatDate(item.issued_at) }}
            </template>
            <template v-slot:item.due_date="{ item }">
              {{ formatDate(item.due_date) }}
            </template>
            <template v-slot:item.days_overdue="{ item }">
              <span class="overdue">{{ item.days_overdue }}</span>
            </template>
          </v-data-table>

          <div v-else class="no-data">
            <v-icon size="48" color="grey-lighten-1">mdi-check-circle</v-icon>
            <p class="text-grey mt-2">Нет просроченных книг</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import apiClient from '../api/client'

// ===== STORE =====
const auth = useAuthStore()
const isAdmin = computed(() => auth.isAdmin)

// ===== STATE =====
const allLoans = ref([])
const overdueLoans = ref([])
const loading = ref(false)
const error = ref(null)

// ===== HEADERS =====
const allHeaders = [
  { title: 'ID', key: 'loan_id', width: '70px' },
  { title: 'Читатель', key: 'reader_name' },
  { title: 'Билет', key: 'reader_card' },
  { title: 'Книга', key: 'book_title' },
  { title: 'Дата выдачи', key: 'issued_at' },
  { title: 'Срок возврата', key: 'due_date' },
  { title: 'Дней', key: 'days_on_loan', width: '80px' },
  { title: 'Статус', key: 'status', sortable: false }
]

const overdueHeaders = [
  { title: 'ID', key: 'loan_id', width: '70px' },
  { title: 'Читатель', key: 'reader_name' },
  { title: 'Билет', key: 'reader_card' },
  { title: 'Книга', key: 'book_title' },
  { title: 'Дата выдачи', key: 'issued_at' },
  { title: 'Срок возврата', key: 'due_date' },
  { title: 'Дней просрочки', key: 'days_overdue', width: '120px' }
]

// ===== METHODS =====
const formatDate = (dateString) => {
  if (!dateString) return '—'
  return new Date(dateString).toLocaleDateString('ru-RU')
}

// Загрузка всех активных выдач
const loadAllLoans = async () => {
  const response = await apiClient.get('loans/active/')
  allLoans.value = response.data
}

// Загрузка просроченных выдач
const loadOverdueLoans = async () => {
  const response = await apiClient.get('loans/overdue/')
  overdueLoans.value = response.data?.overdue_readers || []
}

// Общая загрузка
const loadData = async () => {
  if (!isAdmin.value) return

  loading.value = true
  error.value = null

  try {
    await Promise.all([loadAllLoans(), loadOverdueLoans()])
  } catch (err) {
    console.error('Ошибка:', err)
    error.value = 'Не удалось загрузить данные'
  } finally {
    loading.value = false
  }
}

// ===== LIFECYCLE =====
onMounted(() => {
  if (isAdmin.value) loadData()
})
</script>

<style scoped>
.on-loan-view {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.not-admin {
  text-align: center;
  padding: 40px;
  background: #f8f9fa;
  border-radius: 8px;
  color: #6c757d;
}

.controls {
  margin-bottom: 20px;
  display: flex;
  justify-content: flex-end;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #6c757d;
}

.error {
  padding: 15px;
  background: #f8d7da;
  color: #721c24;
  border-radius: 4px;
  margin-bottom: 20px;
}

.section {
  margin-bottom: 40px;
}

.section h2 {
  margin-bottom: 20px;
  color: #343a40;
}

.no-data {
  text-align: center;
  padding: 40px;
  background: #f8f9fa;
  border-radius: 8px;
}

.overdue {
  color: #dc3545;
  font-weight: 600;
}

/* Vuetify overrides */
:deep(.v-data-table) {
  border-radius: 8px;
}

:deep(.v-data-table thead th) {
  background-color: #343a40 !important;
  color: white !important;
  font-weight: 500;
}

:deep(.v-chip) {
  font-weight: 500;
}
</style>