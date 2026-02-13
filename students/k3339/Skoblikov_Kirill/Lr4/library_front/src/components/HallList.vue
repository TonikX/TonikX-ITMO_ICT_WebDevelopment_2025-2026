<template>
  <div class="halls-page">
    <div class="halls-container">
      <h2 class="page-title">Список залов</h2>
      <div class="filter-section">
        <div class="filter-row">
          <div class="filter-item">
            <label>Номер зала</label>
            <input
              v-model="filters.hall_number"
              type="text"
              placeholder="Номер"
              class="filter-input"
            />
          </div>
          <div class="filter-item">
            <label>Название</label>
            <input
              v-model="filters.hall_name"
              type="text"
              placeholder="Название"
              class="filter-input"
            />
          </div>
          <div class="filter-item">
            <label>Вместимость</label>
            <input
              v-model="filters.capacity"
              type="text"
              placeholder="Вместимость"
              class="filter-input"
            />
          </div>
          <div class="filter-item button-item">
            <AppButton @click="resetFilters" variant="secondary" class="reset-btn">
              Сбросить
            </AppButton>
          </div>
        </div>
      </div>

      <div v-if="filteredHalls.length" class="table-wrapper">
        <table class="halls-table">
          <thead>
            <tr>
              <th>Номер зала</th>
              <th>Название</th>
              <th>Вместимость</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="hall in filteredHalls"
              :key="hall.hall_number"
              @click="selectHall(hall.hall_number)"
              :class="{ selected: selectedHallNumber === hall.hall_number }"
            >
              <td class="number-cell">{{ hall.hall_number }}</td>
              <td class="name-cell">{{ hall.hall_name }}</td>
              <td class="capacity-cell">{{ hall.capacity }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <p v-else class="empty-message">
        {{ halls.length ? 'Залы не найдены' : 'Список залов пуст' }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import authAPI from '@/api/api.js';
import AppButton from '@/components/UI/AppButton.vue';

const halls = ref([]);
const selectedHallNumber = ref(null);
const filters = ref({
  hall_number: '',
  hall_name: '',
  capacity: ''
});

const loadHalls = async () => {
  try {
    const response = await authAPI.getHalls();
    const rawHalls = response.data.Halls || response.data;
    halls.value = rawHalls.map(hall => ({
      hall_number: hall.hall_number,
      hall_name: hall.hall_name,
      capacity: hall.capacity
    }));
  } catch (error) {
    console.error('Ошибка загрузки залов:', error);
    if (error.response?.status === 401) {
      window.location.href = '/login';
    }
  }
};

const selectHall = (number) => {
  selectedHallNumber.value = selectedHallNumber.value === number ? null : number;
};

const resetFilters = () => {
  filters.value = {
    hall_number: '',
    hall_name: '',
    capacity: ''
  };
};

const filteredHalls = computed(() => {
  return halls.value.filter(hall => {
    const f = filters.value;
    const numberMatch = !f.hall_number ||
      String(hall.hall_number).toLowerCase().includes(f.hall_number.toLowerCase());
    const nameMatch = !f.hall_name ||
      hall.hall_name.toLowerCase().includes(f.hall_name.toLowerCase());
    const capacityMatch = !f.capacity ||
      String(hall.capacity).toLowerCase().includes(f.capacity.toLowerCase());
    return numberMatch && nameMatch && capacityMatch;
  });
});

defineExpose({
  loadHalls,
  selectedHallNumber,
  halls,
  filteredHalls,
  resetFilters
});

onMounted(loadHalls);
</script>

<style scoped>
.halls-page {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  padding: 40px 20px;
  box-sizing: border-box;
}

.halls-container {
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
  gap: 4px;
}

.filter-item.button-item {
  flex: 0 0 auto;
  width: 140px;
  margin-left: auto;
}

.filter-item label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #4a5568;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  white-space: nowrap;
}

.reset-btn {
  width: 100%;
  height: 38px;
  font-size: 0.9rem;
  margin: 0;
}

.halls-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.halls-table thead tr {
  background: #f7fafc;
  border-bottom: 2px solid #e2e8f0;
}

.halls-table th {
  padding: 16px 12px;
  text-align: left;
  font-weight: 600;
  color: #2d3748;
  white-space: nowrap;
}

.halls-table td {
  padding: 14px 12px;
  border-bottom: 1px solid #edf2f7;
  transition: background 0.15s;
}

.halls-table tbody tr:nth-child(even) {
  background-color: #fafafa;
}

.halls-table tbody tr:hover {
  background-color: #f0f5ff;
  cursor: pointer;
}

.halls-table tbody tr.selected {
  background-color: #e6f7ff;
  border-left: 4px solid #1890ff;
  box-shadow: inset 0 0 0 1px #1890ff;
}

.number-cell {
  font-weight: 600;
  color: #1a202c;
}

.name-cell {
  color: #4a5568;
}

.capacity-cell {
  color: #4a5568;
}
</style>