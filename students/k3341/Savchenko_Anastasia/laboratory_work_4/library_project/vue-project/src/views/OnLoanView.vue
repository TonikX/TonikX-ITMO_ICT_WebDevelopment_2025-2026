<template>
  <div class="on-loan-view">
    <h1>Книги на руках</h1>

    <div v-if="!isAdmin" class="not-admin">
      <p>Эта страница доступна только администраторам.</p>
    </div>

    <div v-else>
      <div class="controls">
        <button @click="loadOverdueLoans" :disabled="loading" class="refresh-btn">
          {{ loading ? 'Загрузка...' : 'Обновить список' }}
        </button>
      </div>

      <div v-if="loading" class="loading">Загрузка данных...</div>
      <div v-else-if="error" class="error">{{ error }}</div>

      <div v-else>
        <h2>Просроченные выдачи (более 30 дней)</h2>

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
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import apiClient from '../api/client'

const auth = useAuthStore()
const isAdmin = computed(() => auth.isAdmin)

const overdueLoans = ref([])
const loading = ref(false)
const error = ref(null)

const formatDate = (dateString) => {
  if (!dateString) return 'Не указано'
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU')
}

const loadOverdueLoans = async () => {
  if (!isAdmin.value) return

  loading.value = true
  error.value = null

  try {
    // Используем эндпоинт из твоего API
    const response = await apiClient.get('loans/overdue/')
    overdueLoans.value = response.data.overdue_readers || []
  } catch (err) {
    console.error('Ошибка загрузки просроченных выдач:', err)
    error.value = 'Не удалось загрузить данные'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (isAdmin.value) {
    loadOverdueLoans()
  }
})
</script>

<style scoped>
.on-loan-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.not-admin {
  text-align: center;
  padding: 40px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
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

.refresh-btn:hover:not(:disabled) {
  background: #0069d9;
}

.refresh-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
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
  border: 1px solid #f5c6cb;
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

tbody tr:hover {
  background-color: #f8f9fa;
}

.overdue {
  color: #dc3545;
  font-weight: bold;
}

@media (max-width: 768px) {
  .loans-table {
    font-size: 14px;
  }

  th, td {
    padding: 8px 10px;
  }
}
</style>