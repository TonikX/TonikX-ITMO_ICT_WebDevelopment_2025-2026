<template>
  <div class="on-loan-view">
    <h1>Книги на руках</h1>

    <div v-if="!isAdmin" class="not-admin">
      <p>Эта страница доступна только администраторам.</p>
    </div>

    <div v-else>
      <div class="controls">
        <button @click="loadData" :disabled="loading" class="refresh-btn">
          {{ loading ? 'Загрузка...' : 'Обновить список' }}
        </button>
      </div>

      <div v-if="loading" class="loading">Загрузка данных...</div>
      <div v-else-if="error" class="error">{{ error }}</div>

      <div v-else>
        <!-- ===== ВСЕ АКТИВНЫЕ ВЫДАЧИ ===== -->
        <div class="section">
          <h2>📋 Все активные выдачи ({{ allLoans.length }})</h2>
          <div v-if="allLoans.length === 0" class="no-data">
            <p>Нет активных выдач.</p>
          </div>
          <div v-else class="loans-table">
            <table>
              <thead>
                <tr>
                  <th>ID выдачи</th>
                  <th>Читатель</th>
                  <th>Билет</th>
                  <th>Книга</th>
                  <th>Дата выдачи</th>
                  <th>Срок возврата</th>
                  <th>Дней на руках</th>
                  <th>Статус</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="loan in allLoans" :key="loan.loan_id">
                  <td>{{ loan.loan_id }}</td>
                  <td>{{ loan.reader_name }}</td>
                  <td>{{ loan.reader_card }}</td>
                  <td>{{ loan.book_title }}</td>
                  <td>{{ formatDate(loan.issued_at) }}</td>
                  <td>{{ formatDate(loan.due_date) }}</td>
                  <td>{{ loan.days_on_loan }}</td>
                  <td>
                    <span :class="['status-badge', loan.days_overdue > 0 ? 'status-overdue' : 'status-active']">
                      {{ loan.days_overdue > 0 ? 'Просрочена' : 'В сроке' }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <v-divider class="my-6"></v-divider>

        <!-- ===== ПРОСРОЧЕННЫЕ ВЫДАЧИ (БОЛЕЕ 30 ДНЕЙ) ===== -->
        <div class="section">
          <h2>⚠️ Просроченные выдачи (более 30 дней) ({{ overdueLoans.length }})</h2>
          <div v-if="overdueLoans.length === 0" class="no-data">
            <p>Нет просроченных выдач.</p>
          </div>
          <div v-else class="loans-table">
            <table>
              <thead>
                <tr>
                  <th>ID выдачи</th>
                  <th>Читатель</th>
                  <th>Билет</th>
                  <th>Книга</th>
                  <th>Дата выдачи</th>
                  <th>Дней просрочки</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="loan in overdueLoans" :key="loan.loan_id">
                  <td>{{ loan.loan_id }}</td>
                  <td>{{ loan.reader_name }}</td>
                  <td>{{ loan.reader_card }}</td>
                  <td>{{ loan.book_title }}</td>
                  <td>{{ formatDate(loan.issued_at) }}</td>
                  <td class="overdue">{{ loan.days_overdue }}</td>
                </tr>
              </tbody>
            </table>
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

const auth = useAuthStore()
const isAdmin = computed(() => auth.isAdmin)

const allLoans = ref([])
const overdueLoans = ref([])
const loading = ref(false)
const error = ref(null)

const formatDate = (dateString) => {
  if (!dateString) return 'Не указано'
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU')
}

// Загрузка ВСЕХ активных выдач (используем готовый эндпоинт!)
const loadAllLoans = async () => {
  try {
    const response = await apiClient.get('loans/active/')
    allLoans.value = response.data
    console.log('Все активные выдачи:', allLoans.value)
  } catch (err) {
    console.error('Ошибка загрузки всех выдач:', err)
    allLoans.value = []
    throw err
  }
}

// Загрузка просроченных выдач (более 30 дней)
const loadOverdueLoans = async () => {
  try {
    const response = await apiClient.get('loans/overdue/')

    if (response.data && response.data.overdue_readers) {
      // Преобразуем формат из overdue в единый формат
      overdueLoans.value = response.data.overdue_readers.map(loan => ({
        loan_id: loan.loan_id || loan.copy_book_id,
        reader_name: loan.reader_name,
        reader_card: loan.reader_card || 'Не указан',
        book_title: loan.book_title,
        issued_at: loan.issued_at,
        days_overdue: loan.days_overdue
      }))

      // Фильтруем только те, у которых > 30 дней
      overdueLoans.value = overdueLoans.value.filter(
        loan => loan.days_overdue > 30
      )
    } else {
      overdueLoans.value = []
    }

    console.log('Просроченные (>30 дней):', overdueLoans.value)
  } catch (err) {
    console.error('Ошибка загрузки просроченных выдач:', err)
    overdueLoans.value = []
  }
}

// Общая загрузка данных
const loadData = async () => {
  if (!isAdmin.value) return

  loading.value = true
  error.value = null

  try {
    await Promise.all([
      loadAllLoans(),
      loadOverdueLoans()
    ])
  } catch (err) {
    console.error('Ошибка загрузки:', err)
    error.value = 'Не удалось загрузить данные'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (isAdmin.value) {
    loadData()
  }
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

.refresh-btn {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.refresh-btn:hover:not(:disabled) { background: #0069d9; }
.refresh-btn:disabled { background: #6c757d; cursor: not-allowed; }

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
  border: 1px solid #f5c6cb;
}

.section {
  margin-bottom: 40px;
}

.section h2 {
  margin-bottom: 20px;
  color: #343a40;
  font-size: 1.5rem;
}

.no-data {
  text-align: center;
  padding: 40px;
  color: #6c757d;
  background: #f8f9fa;
  border-radius: 8px;
}

.loans-table {
  overflow-x: auto;
  margin-top: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

thead {
  background: #343a40;
  color: white;
}

th, td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #dee2e6;
}

tbody tr:hover { background-color: #f8f9fa; }

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.status-active {
  background: #d4edda;
  color: #155724;
}

.status-overdue {
  background: #fff3cd;
  color: #856404;
}

.overdue {
  color: #dc3545;
  font-weight: bold;
}

@media (max-width: 768px) {
  .loans-table { font-size: 14px; }
  th, td { padding: 8px 10px; }
}
</style>