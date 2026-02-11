<template>
  <div class="reports-view">
    <h1>Отчёты библиотеки</h1>

    <div v-if="!isAdmin" class="not-admin">
      <p>Эта страница доступна только администраторам.</p>
    </div>

    <div v-else>
      <div class="controls">
        <button @click="loadReports" :disabled="loading" class="refresh-btn">
          {{ loading ? 'Загрузка...' : 'Обновить отчёты' }}
        </button>
      </div>

      <div v-if="loading" class="loading">Загрузка отчётов...</div>
      <div v-else-if="error" class="error">{{ error }}</div>

      <div v-else class="reports">
        <!-- Статистика по образованию -->
        <div class="report-card">
          <h2>Распределение читателей по образованию</h2>

          <div v-if="educationStats.length === 0" class="no-data">
            <p>Нет данных о читателях</p>
          </div>

          <div v-else class="stats-grid">
            <div v-for="stat in educationStats" :key="stat.education" class="stat-item">
              <div class="stat-label">{{ stat.education }}</div>
              <div class="stat-bar">
                <div
                  class="stat-bar-fill"
                  :style="{ width: stat.percentage + '%' }"
                ></div>
              </div>
              <div class="stat-numbers">
                <span class="count">{{ stat.count }} чел.</span>
                <span class="percentage">{{ stat.percentage.toFixed(1) }}%</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Молодые читатели -->
        <div class="report-card">
          <h2>Читатели младше 20 лет</h2>

          <div v-if="youngReaders.length === 0" class="no-data">
            <p>Нет читателей младше 20 лет</p>
          </div>

          <div v-else class="young-readers">
            <div class="summary">
              <p class="total">Всего: <strong>{{ youngReaders.length }}</strong> читателей</p>
            </div>

            <div class="readers-list">
              <div v-for="reader in youngReaders" :key="reader.reader_id" class="reader-item">
                <div class="reader-name">{{ reader.full_name }}</div>
                <div class="reader-info">
                  <span>Билет: {{ reader.library_card_id }}</span>
                  <span>Возраст: {{ calculateAge(reader.birth_date) }} лет</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Редкие книги -->
        <div class="report-card">
          <h2>Читатели с редкими книгами (≤2 экз.)</h2>

          <div v-if="rareBooksReaders.length === 0" class="no-data">
            <p>Нет читателей с редкими книгами</p>
          </div>

          <div v-else class="rare-books">
            <table>
              <thead>
                <tr>
                  <th>Читатель</th>
                  <th>Книга</th>
                  <th>Экземпляров</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in rareBooksReaders" :key="item.reader_id + '-' + item.book_id">
                  <td>{{ item.reader_name }}</td>
                  <td>{{ item.book_title }}</td>
                  <td class="rare">{{ item.copy_count }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Месячный отчёт -->
        <div class="report-card">
          <h2>Отчёт за месяц</h2>

          <div v-if="!monthlyReport" class="no-data">
            <p>Нет данных за месяц</p>
          </div>

          <div v-else class="monthly-report">
            <div class="monthly-summary">
              <h3>Итоги за месяц:</h3>
              <div class="summary-stats">
                <div class="summary-item">
                  <span class="label">Всего книг:</span>
                  <span class="value">{{ monthlyReport.total?.books || 0 }}</span>
                </div>
                <div class="summary-item">
                  <span class="label">Всего читателей:</span>
                  <span class="value">{{ monthlyReport.total?.readers || 0 }}</span>
                </div>
                <div class="summary-item">
                  <span class="label">Новых читателей:</span>
                  <span class="value">{{ monthlyReport.total?.new_readers || 0 }}</span>
                </div>
              </div>
            </div>

            <div v-if="monthlyReport.halls && monthlyReport.halls.length > 0" class="halls-stats">
              <h3>Новые читатели по залам:</h3>
              <div class="halls-list">
                <div v-for="hall in monthlyReport.halls" :key="hall.name" class="hall-item">
                  <span class="hall-name">{{ hall.name }}</span>
                  <span class="hall-count">{{ hall.new_readers }} чел.</span>
                </div>
              </div>
            </div>
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

const educationStats = ref([])
const youngReaders = ref([])
const rareBooksReaders = ref([])
const monthlyReport = ref(null)
const loading = ref(false)
const error = ref(null)

const calculateAge = (birthDate) => {
  const today = new Date()
  const birth = new Date(birthDate)
  let age = today.getFullYear() - birth.getFullYear()
  const monthDiff = today.getMonth() - birth.getMonth()

  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    age--
  }

  return age
}

const loadReports = async () => {
  if (!isAdmin.value) return

  loading.value = true
  error.value = null

  try {
    // Загружаем все отчёты параллельно
    const [eduRes, youngRes, rareRes, monthlyRes] = await Promise.all([
      apiClient.get('stats/education/'),
      apiClient.get('readers/young/'),
      apiClient.get('readers/rare-books/'),
      apiClient.get('reports/monthly/')  // Добавляем месячный отчёт
    ])

    educationStats.value = eduRes.data.stats || []
    youngReaders.value = youngRes.data.readers || []
    rareBooksReaders.value = rareRes.data.readers_with_rare_books || []
    monthlyReport.value = monthlyRes.data

  } catch (err) {
    console.error('Ошибка загрузки отчётов:', err)
    // Если какой-то эндпоинт не работает, продолжаем с остальными
    error.value = 'Некоторые отчёты не загружены'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (isAdmin.value) {
    loadReports()
  }
})
</script>

<style scoped>
.reports-view {
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

.reports {
  display: grid;
  gap: 30px;
}

.report-card {
  padding: 30px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  border: 1px solid #e9ecef;
}

.report-card h2 {
  margin-top: 0;
  margin-bottom: 25px;
  color: #495057;
  border-bottom: 2px solid #dee2e6;
  padding-bottom: 10px;
}

.no-data {
  text-align: center;
  padding: 30px;
  color: #6c757d;
  background: #f8f9fa;
  border-radius: 6px;
}

.stats-grid {
  display: grid;
  gap: 20px;
}

.stat-item {
  display: grid;
  grid-template-columns: 150px 1fr auto;
  gap: 20px;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #f1f3f4;
}

.stat-item:last-child {
  border-bottom: none;
}

.stat-label {
  font-weight: 500;
  color: #495057;
}

.stat-bar {
  height: 20px;
  background: #e9ecef;
  border-radius: 10px;
  overflow: hidden;
}

.stat-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #007bff, #17a2b8);
  border-radius: 10px;
  transition: width 0.5s ease;
}

.stat-numbers {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  min-width: 100px;
}

.count {
  font-weight: 500;
  color: #212529;
}

.percentage {
  font-size: 14px;
  color: #6c757d;
}

.young-readers .summary {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #dee2e6;
}

.total {
  font-size: 18px;
  color: #495057;
}

.total strong {
  color: #007bff;
  font-size: 24px;
}

.readers-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.reader-item {
  padding: 15px;
  background: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #e9ecef;
}

.reader-name {
  font-weight: 500;
  color: #212529;
  margin-bottom: 8px;
}

.reader-info {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: #6c757d;
}

.rare-books table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.rare-books thead {
  background: #343a40;
  color: white;
}

.rare-books th, .rare-books td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #dee2e6;
}

.rare-books tbody tr:hover {
  background-color: #f8f9fa;
}

.rare-books .rare {
  color: #dc3545;
  font-weight: bold;
}

/* Стили для месячного отчёта */
.monthly-summary {
  margin-bottom: 25px;
  padding-bottom: 20px;
  border-bottom: 1px solid #dee2e6;
}

.monthly-summary h3 {
  color: #495057;
  margin-bottom: 15px;
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.summary-item {
  padding: 15px;
  background: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #e9ecef;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.summary-item .label {
  font-weight: 500;
  color: #495057;
}

.summary-item .value {
  font-size: 24px;
  font-weight: bold;
  color: #28a745;
}

.halls-stats h3 {
  color: #495057;
  margin-bottom: 15px;
}

.halls-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 10px;
}

.hall-item {
  padding: 12px 15px;
  background: #e8f4fd;
  border-radius: 6px;
  border: 1px solid #b3d7ff;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.hall-name {
  font-weight: 500;
  color: #0056b3;
}

.hall-count {
  font-weight: bold;
  color: #28a745;
}

@media (max-width: 768px) {
  .stat-item {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .readers-list {
    grid-template-columns: 1fr;
  }

  .reader-info {
    flex-direction: column;
    gap: 5px;
  }

  .summary-stats {
    grid-template-columns: 1fr;
  }

  .halls-list {
    grid-template-columns: 1fr;
  }
}
</style>