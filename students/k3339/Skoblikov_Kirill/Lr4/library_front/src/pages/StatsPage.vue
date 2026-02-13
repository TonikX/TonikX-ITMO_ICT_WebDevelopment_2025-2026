<template>
  <div class="statistics-page">
    <div class="statistics-container">
      <h2 class="page-title">Статистика библиотеки</h2>

      <div class="stats-grid">
        <div class="stat-card">
          <div class="card-header">
            <h3>Образование читателей</h3>
            <AppButton v-if="educationStats.length" @click="loadEducationStats" variant="icon" class="refresh-btn">
              🔄
            </AppButton>
          </div>
          <div v-if="educationLoading" class="loading">Загрузка...</div>
          <div v-else-if="educationError" class="error-message">{{ educationError }}</div>
          <div v-else-if="educationStats.length" class="stats-content">
            <table class="stats-table">
              <thead>
                <tr>
                  <th>Уровень образования</th>
                  <th>Количество</th>
                  <th>Процент</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in educationStats" :key="item.education_code">
                  <td>{{ item.education_type }}</td>
                  <td>{{ item.count }}</td>
                  <td>{{ item.percentage }}%</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="empty-state">Нет данных о читателях</div>
        </div>

        <div class="stat-card">
          <h3>Читатели младше 20 лет</h3>
          <div v-if="youngLoading" class="loading">Загрузка...</div>
          <div v-else-if="youngError" class="error-message">{{ youngError }}</div>
          <div v-else class="big-number">
            {{ youngCount }}
            <span class="big-number-label">читателей</span>
          </div>
        </div>

        <div class="stat-card">
          <div class="card-header">
            <h3>Читатели с долгами</h3>
            <AppButton v-if="badReaders.length" @click="loadBadReaders" variant="icon" class="refresh-btn">
              🔄
            </AppButton>
          </div>
          <div v-if="badLoading" class="loading">Загрузка...</div>
          <div v-else-if="badError" class="error-message">{{ badError }}</div>
          <div v-else-if="badReaders.length" class="stats-content">
            <div v-for="reader in badReaders" :key="reader.reader_id" class="reader-item">
              {{ reader.last_name }} {{ reader.first_name }} ({{ reader.reader_card_number }})
            </div>
          </div>
          <div v-else class="empty-state">Нет читателей с долгами</div>
        </div>

        <div class="stat-card">
          <div class="card-header">
            <h3>Читатели редких книг</h3>
            <AppButton v-if="rareReaders.length" @click="loadRareReaders" variant="icon" class="refresh-btn">
              🔄
            </AppButton>
          </div>
          <div v-if="rareLoading" class="loading">Загрузка...</div>
          <div v-else-if="rareError" class="error-message">{{ rareError }}</div>
          <div v-else-if="rareReaders.length" class="stats-content">
            <div v-for="reader in rareReaders" :key="reader.reader_id" class="reader-item">
              {{ reader.last_name }} {{ reader.first_name }} ({{ reader.reader_card_number }})
            </div>
          </div>
          <div v-else class="empty-state">Нет читателей редких книг</div>
        </div>
      </div>

      <div class="stat-card full-width">
        <div class="card-header">
          <h3>Книги на руках у читателя</h3>
          <div class="reader-selector">
            <select v-model="selectedReaderId" @change="loadReaderBooks" class="reader-select">
              <option value="">— Выберите читателя —</option>
              <option v-for="reader in allReaders" :key="reader.reader_id" :value="reader.reader_id">
                {{ reader.last_name }} {{ reader.first_name }} ({{ reader.reader_card_number }})
              </option>
            </select>
            <AppButton @click="loadReaderBooks" :disabled="!selectedReaderId" class="load-btn">
              Показать
            </AppButton>
          </div>
        </div>
        <div v-if="readerBooksLoading" class="loading">Загрузка книг...</div>
        <div v-else-if="readerBooksError" class="error-message">{{ readerBooksError }}</div>
        <div v-else-if="readerBooks.length" class="stats-content">
          <table class="books-table">
            <thead>
              <tr>
                <th>Название</th>
                <th>Автор</th>
                <th>Год</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="book in readerBooks" :key="book.book_id">
                <td>{{ book.book_name }}</td>
                <td>{{ book.authors }}</td>
                <td>{{ book.publication_year ? new Date(book.publication_year).getFullYear() : '—' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else-if="selectedReaderId" class="empty-state">
          У выбранного читателя нет книг на руках
        </div>
        <div v-else class="empty-state">Выберите читателя из списка</div>
      </div>

      <div class="stat-card full-width">
        <div class="card-header">
          <h3>Ежемесячный отчёт</h3>
          <div class="report-selector">
            <input type="number" v-model.number="reportYear" placeholder="Год" min="2000" max="2100" class="report-input" />
            <input type="number" v-model.number="reportMonth" placeholder="Месяц (1-12)" min="1" max="12" class="report-input" />
            <AppButton @click="loadMonthlyReport" :disabled="!reportYear || !reportMonth" class="load-btn">
              Сформировать
            </AppButton>
          </div>
        </div>
        <div v-if="reportLoading" class="loading">Загрузка отчёта...</div>
        <div v-else-if="reportError" class="error-message">{{ reportError }}</div>
        <div v-else-if="reportData" class="report-content">
          <h4>Период: {{ reportData.period }}</h4>

          <div class="report-section">
            <h5>Книги</h5>
            <div class="report-stats">
              <div class="stat-badge">Всего: {{ reportData.daily_statistics[0]?.books.total || 0 }}</div>
              <div v-for="hall in reportData.daily_statistics[0]?.books.per_hall || []" :key="hall.hall__hall_number" class="stat-badge">
                Зал {{ hall.hall__hall_name }}: {{ hall.count }}
              </div>
            </div>
          </div>

          <div class="report-section">
            <h5>Читатели</h5>
            <div class="report-stats">
              <div class="stat-badge">Всего: {{ reportData.daily_statistics[0]?.readers.total || 0 }}</div>
              <div v-for="hall in reportData.daily_statistics[0]?.readers.per_hall || []" :key="hall.hall__hall_number" class="stat-badge">
                Зал {{ hall.hall__hall_name }}: {{ hall.count }}
              </div>
            </div>
          </div>

          <div class="report-section">
            <h5>Регистрации</h5>
            <div class="report-stats">
              <div class="stat-badge">Всего: {{ reportData.registrations.total }}</div>
              <div v-for="hall in reportData.registrations.per_hall" :key="hall.hall__hall_number" class="stat-badge">
                Зал {{ hall.hall__hall_name }}: {{ hall.count }}
              </div>
            </div>
          </div>

          <details class="daily-details">
            <summary>Подневная статистика</summary>
            <table class="daily-table">
              <thead>
                <tr>
                  <th>Дата</th>
                  <th>Книги</th>
                  <th>Читатели</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="day in reportData.daily_statistics" :key="day.date">
                  <td>{{ formatDate(day.date) }}</td>
                  <td>{{ day.books.total }}</td>
                  <td>{{ day.readers.total }}</td>
                </tr>
              </tbody>
            </table>
          </details>
        </div>
        <div v-else class="empty-state">
          Укажите год и месяц для формирования отчёта
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import authAPI from '@/api/api.js';
import AppButton from '@/components/UI/AppButton.vue';

const educationStats = ref([]);
const educationLoading = ref(false);
const educationError = ref('');

const youngCount = ref(0);
const youngLoading = ref(false);
const youngError = ref('');

const badReaders = ref([]);
const badLoading = ref(false);
const badError = ref('');

const rareReaders = ref([]);
const rareLoading = ref(false);
const rareError = ref('');

const allReaders = ref([]);
const selectedReaderId = ref('');
const readerBooks = ref([]);
const readerBooksLoading = ref(false);
const readerBooksError = ref('');

const reportYear = ref(new Date().getFullYear());
const reportMonth = ref(new Date().getMonth() + 1);
const reportData = ref(null);
const reportLoading = ref(false);
const reportError = ref('');
const loadEducationStats = async () => {
  educationLoading.value = true;
  educationError.value = '';
  try {
    const response = await authAPI.getEducationStats();
    const stats = response.data.statistics || response.data;
    educationStats.value = stats.filter(s => s.education_code !== 'total');
  } catch (error) {
    console.error('Ошибка загрузки статистики образования:', error);
    if (error.response?.data?.detail) {
      educationError.value = error.response.data.detail;
    } else {
      educationError.value = 'Не удалось загрузить статистику';
    }
    educationStats.value = [];
  } finally {
    educationLoading.value = false;
  }
};

const loadYoungReaders = async () => {
  youngLoading.value = true;
  youngError.value = '';
  try {
    const response = await authAPI.getYoungReadersCount();
    const detail = response.data.detail;
    const match = detail.match(/\d+/);
    youngCount.value = match ? parseInt(match[0]) : 0;
  } catch (error) {
    console.error('Ошибка загрузки молодых читателей:', error);
    if (error.response?.status === 404) {
      youngCount.value = 0;
      youngError.value = '';
    } else {
      youngError.value = 'Не удалось загрузить данные';
    }
  } finally {
    youngLoading.value = false;
  }
};

const loadBadReaders = async () => {
  badLoading.value = true;
  badError.value = '';
  try {
    const response = await authAPI.getBadReaders();
    badReaders.value = Array.isArray(response.data) ? response.data : (response.data.results || []);
  } catch (error) {
    console.error('Ошибка загрузки должников:', error);
    if (error.response?.status === 404) {
      badReaders.value = [];
    } else {
      badError.value = 'Не удалось загрузить список';
    }
  } finally {
    badLoading.value = false;
  }
};

const loadRareReaders = async () => {
  rareLoading.value = true;
  rareError.value = '';
  try {
    const response = await authAPI.getRareBookReaders();
    rareReaders.value = Array.isArray(response.data) ? response.data : (response.data.results || []);
  } catch (error) {
    console.error('Ошибка загрузки читателей редких книг:', error);
    if (error.response?.status === 404) {
      rareReaders.value = [];
    } else {
      rareError.value = 'Не удалось загрузить список';
    }
  } finally {
    rareLoading.value = false;
  }
};

const loadAllReaders = async () => {
  try {
    const response = await authAPI.getReaders();
    const rawReaders = response.data.Readers || response.data.results || response.data;
    allReaders.value = Array.isArray(rawReaders) ? rawReaders : [];
  } catch (error) {
    console.error('Ошибка загрузки списка читателей:', error);
  }
};

const loadReaderBooks = async () => {
  if (!selectedReaderId.value) return;
  readerBooksLoading.value = true;
  readerBooksError.value = '';
  readerBooks.value = [];
  try {
    const response = await authAPI.getReaderBooks(selectedReaderId.value);
    readerBooks.value = Array.isArray(response.data) ? response.data : (response.data.results || []);
  } catch (error) {
    console.error('Ошибка загрузки книг читателя:', error);
    if (error.response?.status === 404) {
      readerBooks.value = [];
    } else {
      readerBooksError.value = 'Не удалось загрузить книги';
    }
  } finally {
    readerBooksLoading.value = false;
  }
};

const loadMonthlyReport = async () => {
  if (!reportYear.value || !reportMonth.value) return;
  reportLoading.value = true;
  reportError.value = '';
  reportData.value = null;
  try {
    const response = await authAPI.getMonthlyReport(reportYear.value, reportMonth.value);
    reportData.value = response.data;
  } catch (error) {
    console.error('Ошибка загрузки отчёта:', error);
    reportError.value = 'Не удалось загрузить отчёт';
  } finally {
    reportLoading.value = false;
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '—';
  const d = new Date(dateString);
  return d.toLocaleDateString('ru-RU');
};

onMounted(async () => {
  await Promise.all([
    loadEducationStats(),
    loadYoungReaders(),
    loadBadReaders(),
    loadRareReaders(),
    loadAllReaders()
  ]);
});
</script>

<style scoped>
.statistics-page {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  padding: 40px 20px;
  box-sizing: border-box;
}

.statistics-container {
  width: 100%;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  padding: 40px 30px;
  transition: all 0.3s ease;
}

.page-title {
  margin-top: 0;
  margin-bottom: 30px;
  font-size: 2rem;
  font-weight: 600;
  color: #2d3748;
  text-align: center;
  letter-spacing: -0.5px;
  border-bottom: 2px solid #e2e8f0;
  padding-bottom: 15px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 25px;
  margin-bottom: 25px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  display: flex;
  flex-direction: column;
  margin-bottom: 15px;
}

.stat-card.full-width {
  grid-column: 1 / -1;
}

.stat-card.full-width .books-table td {
  padding: 12px 20px;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.card-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #2d3748;
}

.refresh-btn {
  padding: 4px 8px;
  font-size: 1rem;
}

.big-number {
  font-size: 3rem;
  font-weight: 700;
  color: #7a66ea;
  display: flex;
  align-items: baseline;
  gap: 8px;
  justify-content: center;
  padding: 20px 0;
}

.big-number-label {
  font-size: 1.2rem;
  font-weight: 400;
  color: #4a5568;
}

.stats-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}

.stats-table th {
  text-align: left;
  padding: 8px 4px;
  color: #718096;
  font-weight: 600;
  border-bottom: 1px solid #e2e8f0;
}

.stats-table td {
  padding: 8px 4px;
  border-bottom: 1px solid #edf2f7;
}

.reader-item {
  padding: 8px 12px;
  border-bottom: 1px solid #edf2f7;
  color: #4a5568;
}

.reader-item:last-child {
  border-bottom: none;
}

.reader-selector {
  display: flex;
  gap: 10px;
  align-items: center;
}

.reader-select {
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.95rem;
  min-width: 250px;
}

.load-btn {
  white-space: nowrap;
}

.report-selector {
  display: flex;
  gap: 10px;
  align-items: center;
}

.report-input {
  width: 80px;
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.95rem;
}

.report-content {
  margin-top: 15px;
}

.report-section {
  margin-bottom: 20px;
}

.report-section h5 {
  margin: 0 0 10px 0;
  font-size: 1rem;
  color: #2d3748;
}

.report-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.stat-badge {
  background: #edf2f7;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
  color: #2d3748;
}

.daily-details {
  margin-top: 15px;
}

.daily-details summary {
  cursor: pointer;
  color: #7a66ea;
  font-weight: 500;
  margin-bottom: 10px;
}

.daily-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.daily-table th,
.daily-table td {
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid #edf2f7;
}

.loading {
  text-align: center;
  color: #718096;
  padding: 20px;
}

.error-message {
  background: #ffeaea;
  color: #d32f2f;
  padding: 12px 15px;
  border-radius: 8px;
  font-weight: 500;
}

.empty-state {
  text-align: center;
  color: #718096;
  padding: 20px;
  background: #f7fafc;
  border-radius: 8px;
}
</style>