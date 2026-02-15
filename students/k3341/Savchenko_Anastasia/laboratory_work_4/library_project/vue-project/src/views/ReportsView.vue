<template>
  <div class="reports-view">
    <h1>Отчёты библиотеки</h1>

    <!-- Доступ только админам -->
    <div v-if="!isAdmin" class="not-admin">
      <p>Доступно только администраторам</p>
    </div>

    <div v-else>
      <!-- Кнопка обновления -->
      <div class="controls">
        <v-btn color="primary" @click="loadReports" :loading="loading" prepend-icon="mdi-refresh">
          {{ loading ? 'Загрузка...' : 'Обновить' }}
        </v-btn>
      </div>

      <div v-if="loading" class="loading">Загрузка...</div>
      <div v-else-if="error" class="error">{{ error }}</div>

      <div v-else class="reports">
        <!-- Статистика по образованию -->
        <v-card class="report-card">
          <v-card-title class="text-h6">
            <v-icon left color="primary" class="mr-2">mdi-chart-pie</v-icon>
            Распределение читателей по образованию
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <div v-if="!eduStats.length" class="no-data">Нет данных</div>
            <div v-else v-for="s in eduStats" :key="s.education" class="stat-item">
              <div class="stat-label">{{ s.education }}</div>
              <div class="stat-bar-wrapper">
                <div class="stat-bar">
                  <div class="stat-bar-fill" :style="{ width: s.percentage + '%' }"></div>
                </div>
              </div>
              <div class="stat-numbers">
                <span class="count">{{ s.count }} чел.</span>
                <span class="percentage">{{ s.percentage.toFixed(1) }}%</span>
              </div>
            </div>
          </v-card-text>
        </v-card>

        <!-- Читатели младше 20 лет -->
        <v-card class="report-card">
          <v-card-title class="text-h6">
            <v-icon left color="primary" class="mr-2">mdi-account-child</v-icon>
            Читатели младше 20 лет
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <div v-if="!young.length" class="no-data">Нет читателей младше 20 лет</div>
            <div v-else>
              <div class="summary">
                <p class="total">Всего: <strong>{{ young.length }}</strong> читателей</p>
              </div>
              <div class="readers-grid">
                <div v-for="r in young" :key="r.reader_id" class="reader-card">
                  <div class="reader-name">{{ r.full_name }}</div>
                  <div class="reader-details">
                    <span><v-icon size="small">mdi-card-account-details</v-icon> {{ r.library_card_id }}</span>
                    <span><v-icon size="small">mdi-calendar</v-icon> {{ age(r.birth_date) }} лет</span>
                  </div>
                </div>
              </div>
            </div>
          </v-card-text>
        </v-card>

        <!-- Редкие книги -->
        <v-card class="report-card">
          <v-card-title class="text-h6">
            <v-icon left color="primary" class="mr-2">mdi-book-alert</v-icon>
            Читатели с редкими книгами (≤2 экз.)
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <div v-if="!rare.length" class="no-data">Нет читателей с редкими книгами</div>
            <v-table v-else class="rare-table">
              <thead>
                <tr>
                  <th>Читатель</th>
                  <th>Книга</th>
                  <th class="text-center">Экз.</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, i) in rare" :key="i">
                  <td>{{ item.reader_name }}</td>
                  <td>{{ item.book_title }}</td>
                  <td class="text-center"><span class="rare-badge">{{ item.copy_count }}</span></td>
                </tr>
              </tbody>
            </v-table>
          </v-card-text>
        </v-card>

        <!-- Месячный отчёт -->
        <v-card class="report-card">
          <v-card-title class="text-h6">
            <v-icon left color="primary" class="mr-2">mdi-calendar-month</v-icon>
            Отчёт за месяц
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <div v-if="!monthly" class="no-data">Нет данных за месяц</div>
            <div v-else>
              <div class="monthly-summary">
                <div class="summary-item">
                  <div class="summary-label">Всего книг</div>
                  <div class="summary-value">{{ monthly.total?.books || 0 }}</div>
                </div>
                <div class="summary-item">
                  <div class="summary-label">Всего читателей</div>
                  <div class="summary-value">{{ monthly.total?.readers || 0 }}</div>
                </div>
                <div class="summary-item">
                  <div class="summary-label">Новых читателей</div>
                  <div class="summary-value">{{ monthly.total?.new_readers || 0 }}</div>
                </div>
              </div>

              <div v-if="monthly.halls?.length" class="halls-section">
                <h4 class="text-subtitle-2 mb-2">Новые читатели по залам:</h4>
                <div class="halls-grid">
                  <div v-for="h in monthly.halls" :key="h.name" class="hall-card">
                    <span class="hall-name">{{ h.name }}</span>
                    <span class="hall-count">{{ h.new_readers }} чел.</span>
                  </div>
                </div>
              </div>
            </div>
          </v-card-text>
        </v-card>
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

// Данные
const eduStats = ref([])
const young = ref([])
const rare = ref([])
const monthly = ref(null)
const loading = ref(false)
const error = ref(null)

// Вычисление возраста
const age = (birth) => {
  const b = new Date(birth)
  const today = new Date()
  let a = today.getFullYear() - b.getFullYear()
  const m = today.getMonth() - b.getMonth()
  if (m < 0 || (m === 0 && today.getDate() < b.getDate())) a--
  return a
}

// Загрузка всех отчётов
const loadReports = async () => {
  if (!isAdmin.value) return
  loading.value = true; error.value = null
  try {
    const [e, y, r, m] = await Promise.all([
      apiClient.get('stats/education/'),
      apiClient.get('readers/young/'),
      apiClient.get('readers/rare-books/'),
      apiClient.get('reports/monthly/')
    ])
    eduStats.value = e.data.stats || []
    young.value = y.data.readers || []
    rare.value = r.data.readers_with_rare_books || []
    monthly.value = m.data
  } catch (err) {
    error.value = 'Ошибка загрузки'
  } finally { loading.value = false }
}

onMounted(() => { if (isAdmin.value) loadReports() })
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

.reports {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.report-card {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
}

.report-card :deep(.v-card-title) {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  padding: 16px 20px;
}

/* Статистика по образованию */
.stat-item {
  display: grid;
  grid-template-columns: 150px 1fr 120px;
  gap: 20px;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f1f3f4;
}
.stat-item:last-child { border-bottom: none; }
.stat-label { font-weight: 500; color: #495057; }
.stat-bar-wrapper { width: 100%; }
.stat-bar { height: 20px; background: #e9ecef; border-radius: 10px; overflow: hidden; }
.stat-bar-fill { height: 100%; background: linear-gradient(90deg, #007bff, #17a2b8); border-radius: 10px; transition: width 0.5s; }
.stat-numbers { display: flex; flex-direction: column; align-items: flex-end; }
.count { font-weight: 500; color: #212529; }
.percentage { font-size: 14px; color: #6c757d; }

/* Молодые читатели */
.summary { margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #dee2e6; }
.total { font-size: 18px; color: #495057; }
.total strong { color: #007bff; font-size: 24px; }
.readers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px;
}
.reader-card {
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}
.reader-name { font-weight: 500; color: #212529; margin-bottom: 8px; }
.reader-details {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #6c757d;
}
.reader-details span { display: flex; align-items: center; gap: 4px; }

/* Редкие книги */
.rare-table {
  width: 100%;
  border-collapse: collapse;
}
.rare-table th {
  background: #343a40;
  color: white;
  padding: 12px 16px;
  font-weight: 500;
}
.rare-table td {
  padding: 12px 16px;
  border-bottom: 1px solid #dee2e6;
}
.rare-table tr:hover { background-color: #f8f9fa; }
.rare-badge {
  display: inline-block;
  padding: 4px 8px;
  background: #dc3545;
  color: white;
  border-radius: 4px;
  font-weight: bold;
  min-width: 30px;
}

/* Месячный отчёт */
.monthly-summary {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}
.summary-item {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  text-align: center;
}
.summary-label { font-weight: 500; color: #495057; margin-bottom: 8px; }
.summary-value { font-size: 32px; font-weight: bold; color: #28a745; }

.halls-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 10px;
}
.hall-card {
  padding: 12px 16px;
  background: #e8f4fd;
  border-radius: 6px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.hall-name { font-weight: 500; color: #0056b3; }
.hall-count { font-weight: bold; color: #28a745; }

.no-data {
  text-align: center;
  padding: 40px;
  color: #6c757d;
  background: #f8f9fa;
  border-radius: 6px;
}

@media (max-width: 768px) {
  .stat-item { grid-template-columns: 1fr; gap: 10px; }
  .readers-grid { grid-template-columns: 1fr; }
  .monthly-summary { grid-template-columns: 1fr; }
}
</style>