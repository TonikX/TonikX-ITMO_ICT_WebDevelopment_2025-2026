<template>
  <div class="readers-page">
    <div class="readers-container">
      <h2 class="page-title">Список читателей</h2>
      <div class="filter-section">
        <div class="filter-row">
          <div class="filter-item">
            <label>ФИО</label>
            <input
              v-model="filters.fullName"
              type="text"
              placeholder="Фамилия / Имя / Отчество"
              class="filter-input"
            />
          </div>
          <div class="filter-item">
            <label>Номер билета</label>
            <input
              v-model="filters.cardNumber"
              type="text"
              placeholder="Номер карты"
              class="filter-input"
            />
          </div>
          <div class="filter-item">
            <label>Телефон</label>
            <input
              v-model="filters.phone"
              type="text"
              placeholder="Телефон"
              class="filter-input"
            />
          </div>
          <div class="filter-item">
            <label>Образование</label>
            <select v-model="filters.education" class="filter-input">
              <option value="">Все</option>
              <option value="se">Среднее</option>
              <option value="he">Высшее</option>
              <option value="ad">Учёная степень</option>
            </select>
          </div>
          <div class="filter-item button-item">
            <AppButton @click="resetFilters" variant="secondary" class="reset-btn">
              Сбросить
            </AppButton>
          </div>
        </div>
      </div>

      <div v-if="filteredReaders.length" class="table-wrapper">
        <table class="readers-table">
          <thead>
            <tr>
              <th>ФИО</th>
              <th>Номер билета</th>
              <th>Дата рождения</th>
              <th>Телефон</th>
              <th>Образование</th>
              <th>Зал</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="reader in filteredReaders"
              :key="reader.id"
              @click="selectReader(reader.id)"
              :class="{ selected: selectedReaderId === reader.id }"
            >
              <td class="fio-cell">{{ reader.fullName }}</td>
              <td class="card-cell">{{ reader.reader_card_number }}</td>
              <td class="birth-cell">{{ formatDate(reader.birth_date) }}</td>
              <td class="phone-cell">{{ reader.phone_number }}</td>
              <td class="education-cell">{{ formatEducation(reader.education) }}</td>
              <td class="hall-cell">{{ reader.hall_name || '—' }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <p v-else class="empty-message">
        {{ readers.length ? 'Читатели не найдены' : 'Список читателей пуст' }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import authAPI from '@/api/api.js';
import AppButton from '@/components/UI/AppButton.vue';

const readers = ref([]);
const selectedReaderId = ref(null);
const filters = ref({
  fullName: '',
  cardNumber: '',
  phone: '',
  education: ''
});

const loadReaders = async () => {
  try {
    const response = await authAPI.getReaders();
    const rawReaders = response.data.Readers || response.data;
    readers.value = rawReaders.map(reader => ({
      id: reader.reader_id,
      fullName: `${reader.last_name} ${reader.first_name} ${reader.patronymic || ''}`.trim(),
      last_name: reader.last_name,
      first_name: reader.first_name,
      patronymic: reader.patronymic,
      reader_card_number: reader.reader_card_number,
      birth_date: reader.birth_date,
      passport_number: reader.passport_number,
      phone_number: reader.phone_number,
      education: reader.education,
      academic_degree: reader.academic_degree,
      address: reader.address,
      hall_id: reader.hall,
      hall_name: reader.hall_name
    }));
  } catch (error) {
    console.error('Ошибка загрузки читателей:', error);
    if (error.response?.status === 401) {
      window.location.href = '/login';
    }
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '—';
  return new Date(dateString).toLocaleDateString('ru-RU');
};

const formatEducation = (code) => {
  const map = {
    'se': 'Среднее',
    'he': 'Высшее',
    'ad': 'Уч. степень'
  };
  return map[code] || code;
};

const selectReader = (id) => {
  selectedReaderId.value = selectedReaderId.value === id ? null : id;
};

const resetFilters = () => {
  filters.value = {
    fullName: '',
    cardNumber: '',
    phone: '',
    education: ''
  };
};

const filteredReaders = computed(() => {
  return readers.value.filter(reader => {
    const f = filters.value;
    const nameMatch = !f.fullName ||
      reader.fullName.toLowerCase().includes(f.fullName.toLowerCase());
    const cardMatch = !f.cardNumber ||
      reader.reader_card_number.toLowerCase().includes(f.cardNumber.toLowerCase());
    const phoneMatch = !f.phone ||
      reader.phone_number.includes(f.phone);
    const eduMatch = !f.education || reader.education === f.education;
    return nameMatch && cardMatch && phoneMatch && eduMatch;
  });
});

defineExpose({
  loadReaders,
  selectedReaderId,
  readers,
  filteredReaders,
  resetFilters
});

onMounted(loadReaders);
</script>

<style scoped>
.readers-page {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  padding: 40px 20px;
  box-sizing: border-box;
}

.readers-container {
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

.filter-item.button-item {
  width: 140px;
}

.reset-btn {
  width: 100%;
  height: 38px;
  font-size: 0.9rem;
  margin: 0;
}

.readers-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.readers-table thead tr {
  background: #f7fafc;
  border-bottom: 2px solid #e2e8f0;
}

.readers-table th {
  padding: 16px 12px;
  text-align: left;
  font-weight: 600;
  color: #2d3748;
  white-space: nowrap;
}

.readers-table td {
  padding: 14px 12px;
  border-bottom: 1px solid #edf2f7;
  transition: background 0.15s;
}

.readers-table tbody tr:nth-child(even) {
  background-color: #fafafa;
}

.readers-table tbody tr:hover {
  background-color: #f0f5ff;
  cursor: pointer;
}

.readers-table tbody tr.selected {
  background-color: #e6f7ff;
  border-left: 4px solid #1890ff;
  box-shadow: inset 0 0 0 1px #1890ff;
}

.fio-cell {
  font-weight: 600;
  color: #1a202c;
}

.card-cell,
.birth-cell,
.phone-cell,
.education-cell,
.hall-cell {
  color: #4a5568;
}
</style>