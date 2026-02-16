<template>
  <div class="on-loan-view">
    <h1>Книги на руках</h1>

    <div v-if="!isAdmin" class="not-admin">
      <p>Доступно только администраторам</p>
    </div>

    <div v-else>
      <div class="controls">
        <v-btn color="primary" @click="loadData" :loading="loading" prepend-icon="mdi-refresh">
          {{ loading ? 'Загрузка...' : 'Обновить' }}
        </v-btn>
      </div>

      <div v-if="loading" class="loading">Загрузка...</div>
      <div v-else-if="error" class="error">{{ error }}</div>

      <div v-else>
        <!-- Активные выдачи -->
        <div class="section">
          <h2>📋 Активные выдачи ({{ allLoans.length }})</h2>
          <v-data-table v-if="allLoans.length" :headers="allHeaders" :items="allLoans" density="compact">
            <template v-slot:item.status="{ item }">
              <v-chip :color="item.days_overdue > 0 ? 'warning' : 'success'" size="x-small">
                {{ item.days_overdue > 0 ? 'Просрочена' : 'В сроке' }}
              </v-chip>
            </template>
            <template v-slot:item.issued_at="{ item }">{{ formatDate(item.issued_at) }}</template>
            <template v-slot:item.due_date="{ item }">{{ formatDate(item.due_date) }}</template>
          </v-data-table>
          <div v-else class="no-data">Нет активных выдач</div>
        </div>

        <v-divider class="my-4" />

        <!-- Просроченные -->
        <div class="section">
          <h2>⚠️ Просроченные ({{ overdueLoans.length }})</h2>
          <v-data-table v-if="overdueLoans.length" :headers="overdueHeaders" :items="overdueLoans" density="compact">
            <template v-slot:item.issued_at="{ item }">{{ formatDate(item.issued_at) }}</template>
            <template v-slot:item.due_date="{ item }">{{ formatDate(item.due_date) }}</template>
            <template v-slot:item.days_overdue="{ item }">
              <span class="overdue">{{ item.days_overdue }}</span>
            </template>
          </v-data-table>
          <div v-else class="no-data">Нет просроченных</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import apiClient from '../../api/client'

const auth = useAuthStore()
const isAdmin = computed(() => auth.isAdmin)

const allLoans = ref([])
const overdueLoans = ref([])
const loading = ref(false)
const error = ref(null)

const allHeaders = [
  { title: 'ID', key: 'loan_id', width: '70px' },
  { title: 'Читатель', key: 'reader_name' },
  { title: 'Билет', key: 'reader_card' },
  { title: 'Книга', key: 'book_title' },
  { title: 'Выдана', key: 'issued_at' },
  { title: 'Срок', key: 'due_date' },
  { title: 'Дней', key: 'days_on_loan', width: '70px' },
  { title: 'Статус', key: 'status' }
]

const overdueHeaders = [
  { title: 'ID', key: 'loan_id', width: '70px' },
  { title: 'Читатель', key: 'reader_name' },
  { title: 'Билет', key: 'reader_card' },
  { title: 'Книга', key: 'book_title' },
  { title: 'Выдана', key: 'issued_at' },
  { title: 'Срок', key: 'due_date' },
  { title: 'Просрочка', key: 'days_overdue', width: '100px' }
]

const formatDate = d => d ? new Date(d).toLocaleDateString('ru-RU') : '—'

const loadAllLoans = async () => {
  const res = await apiClient.get('loans/active/')
  allLoans.value = res.data
}

const loadOverdueLoans = async () => {
  const res = await apiClient.get('loans/overdue/')
  overdueLoans.value = res.data?.overdue_readers || []
}

const loadData = async () => {
  if (!isAdmin.value) return
  loading.value = true; error.value = null
  try {
    await Promise.all([loadAllLoans(), loadOverdueLoans()])
  } catch (err) {
    error.value = 'Ошибка загрузки'
  } finally { loading.value = false }
}

onMounted(() => { if (isAdmin.value) loadData() })
</script>

<style scoped>
.on-loan-view { max-width: 1400px; margin: 0 auto; padding: 20px; }
.not-admin { text-align: center; padding: 40px; background: #f8f9fa; border-radius: 8px; color: #6c757d; }
.controls { margin-bottom: 20px; display: flex; justify-content: flex-end; }
.loading, .no-data { text-align: center; padding: 40px; color: #6c757d; background: #f8f9fa; border-radius: 8px; }
.error { padding: 15px; background: #f8d7da; color: #721c24; border-radius: 4px; margin-bottom: 20px; }
.section { margin-bottom: 40px; }
.section h2 { margin-bottom: 20px; color: #343a40; }
.overdue { color: #dc3545; font-weight: 600; }
:deep(.v-data-table thead th) { background-color: #343a40 !important; color: white !important; }
:deep(.v-data-table) { border-radius: 8px; }
</style>