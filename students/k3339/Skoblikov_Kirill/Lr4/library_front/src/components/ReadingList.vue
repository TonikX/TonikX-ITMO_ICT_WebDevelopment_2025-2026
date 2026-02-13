<template>
  <div class="readings-page">
    <div class="readings-container">
      <h2 class="page-title">Журнал выдачи книг</h2>
      <div class="filter-section">
        <div class="filter-row">
          <div class="filter-item">
            <label>Дата выдачи с</label>
            <input v-model="filters.dateFrom" type="date" class="filter-input" />
          </div>
          <div class="filter-item">
            <label>Дата выдачи по</label>
            <input v-model="filters.dateTo" type="date" class="filter-input" />
          </div>
          <div class="filter-item checkbox-item">
            <label class="checkbox-label">
              <input v-model="filters.onlyActive" type="checkbox" />
              Только невозвращённые
            </label>
          </div>
          <div class="filter-item button-item">
            <AppButton @click="resetFilters" variant="secondary" class="reset-btn">
              Сбросить
            </AppButton>
          </div>
        </div>
      </div>

      <div v-if="filteredReadings.length" class="table-wrapper">
        <table class="readings-table">
          <thead>
            <tr>
              <th>Книга</th>
              <th>Автор</th>
              <th>Читатель</th>
              <th>Дата выдачи</th>
              <th>Дата возврата</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="reading in filteredReadings"
              :key="reading.reading_id"
              @click="selectReading(reading.reading_id)"
              :class="{ selected: selectedReadingId === reading.reading_id }"
            >
              <td class="book-cell">{{ reading.book_name }}</td>
              <td class="author-cell">{{ reading.book_authors }}</td>
              <td class="reader-cell">{{ reading.reader_full_name }}</td>
              <td class="date-cell">{{ formatDate(reading.issued_date) }}</td>
              <td class="date-cell">{{ formatDate(reading.returned_date) || '—' }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <p v-else class="empty-message">
        {{ readings.length ? 'Записи не найдены' : 'Журнал пуст' }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import authAPI from '@/api/api.js';
import AppButton from '@/components/UI/AppButton.vue';

const readings = ref([]);
const selectedReadingId = ref(null);
const readersMap = ref({});

const filters = ref({
  dateFrom: '',
  dateTo: '',
  onlyActive: false
});

// Загрузка читателей (для отображения ФИО)
const loadReaders = async () => {
  try {
    const response = await authAPI.getReaders();
    let rawReaders = [];
    if (Array.isArray(response.data)) rawReaders = response.data;
    else if (response.data.Readers) rawReaders = response.data.Readers;
    else if (response.data.results) rawReaders = response.data.results;
    const map = {};
    rawReaders.forEach(reader => {
      const id = reader.reader_id || reader.id;
      const fullName = [reader.last_name, reader.first_name, reader.patronymic]
        .filter(Boolean)
        .join(' ') || '—';
      map[id] = fullName;
    });
    readersMap.value = map;
  } catch (error) {
    console.error('Ошибка загрузки читателей:', error);
  }
};

const loadReadings = async () => {
  try {
    await loadReaders();
    const response = await authAPI.getReadings();
    let rawReadings = [];
    if (Array.isArray(response.data)) rawReadings = response.data;
    else if (response.data.Readings) rawReadings = response.data.Readings;
    else if (response.data.results) rawReadings = response.data.results;
    readings.value = rawReadings.map(reading => ({
      reading_id: reading.reading_id || reading.id,
      book_id: reading.book,
      book_name: reading.book_name || '—',
      book_authors: reading.book_authors || '—',
      reader_id: reading.reader,
      reader_full_name: readersMap.value[reading.reader] || '—',
      issued_date: reading.issued_date,
      returned_date: reading.returned_date
    }));
  } catch (error) {
    console.error('Ошибка загрузки выдач:', error);
    if (error.response?.status === 401) window.location.href = '/login';
  }
};

const formatDate = (dateString) => {
  if (!dateString) return null;
  return new Date(dateString).toLocaleDateString('ru-RU');
};

const selectReading = (id) => {
  selectedReadingId.value = selectedReadingId.value === id ? null : id;
};

const resetFilters = () => {
  filters.value = {
    dateFrom: '',
    dateTo: '',
    onlyActive: false
  };
};

const filteredReadings = computed(() => {
  let result = readings.value.filter(reading => {
    const f = filters.value;
    if (f.dateFrom && reading.issued_date < f.dateFrom) return false;
    if (f.dateTo && reading.issued_date > f.dateTo) return false;
    if (f.onlyActive && reading.returned_date) return false;
    return true;
  });
  return result.sort((a, b) => new Date(b.issued_date) - new Date(a.issued_date));
});

defineExpose({
  loadReadings,
  selectedReadingId,
  readings,
  filteredReadings,
  resetFilters
});

onMounted(loadReadings);
</script>

<style scoped>
.readings-page {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  padding: 40px 20px;
  box-sizing: border-box;
}

.readings-container {
  width: 100%;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  padding: 40px 30px;
  transition: all 0.3s ease;
}

.filter-row {
  gap: 30px;
}

.filter-item {
  flex: 1 1 180px;
}

.filter-item.checkbox-item {
  flex: 0 1 auto;
  justify-content: flex-end;
  margin-bottom: 2px;
}

.filter-item.button-item {
  width: 140px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  text-transform: none !important;
  font-size: 0.9rem !important;
  font-weight: normal !important;
  white-space: nowrap;
}

.reset-btn {
  width: 100%;
  height: 38px;
  font-size: 0.9rem;
  margin: 0;
}

.readings-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.readings-table thead tr {
  background: #f7fafc;
  border-bottom: 2px solid #e2e8f0;
}

.readings-table th {
  padding: 16px 12px;
  text-align: left;
  font-weight: 600;
  color: #2d3748;
  white-space: nowrap;
}

.readings-table td {
  padding: 14px 12px;
  border-bottom: 1px solid #edf2f7;
  transition: background 0.15s;
}

.readings-table tbody tr:nth-child(even) {
  background-color: #fafafa;
}

.readings-table tbody tr:hover {
  background-color: #f0f5ff;
  cursor: pointer;
}

.readings-table tbody tr.selected {
  background-color: #e6f7ff;
  border-left: 4px solid #1890ff;
  box-shadow: inset 0 0 0 1px #1890ff;
}

.book-cell {
  font-weight: 600;
  color: #1a202c;
}

.author-cell,
.reader-cell {
  color: #4a5568;
}

.date-cell {
  color: #718096;
  font-feature-settings: "tnum";
  white-space: nowrap;
}
</style>