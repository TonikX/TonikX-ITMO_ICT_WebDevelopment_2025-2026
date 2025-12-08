<template>
  <div class="page">
    <h1>Флот авиакомпаний</h1>

    <p v-if="loading">Загружаем данные по самолётам...</p>
    <p v-if="error" class="error">{{ error }}</p>

    <v-table v-if="planes.length && !loading">
      <thead>
        <tr>
          <th>ID</th>
          <th>Бортовой номер</th>
          <th>Компания (id)</th>
          <th>Тип самолёта (id)</th>
          <th>Статус</th>
          <th>Налёт (часов)</th>
          <th>Последнее ТО</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="plane in planes" :key="plane.id">
          <td>{{ plane.id }}</td>
          <td>{{ plane.reg_number }}</td>
          <td>{{ plane.company }}</td>
          <td>{{ plane.plane_type }}</td>
          <td>
            <span
              :class="[
                'status-tag',
                plane.status === 'maintenance'
                  ? 'status-maintenance'
                  : plane.status === 'active'
                  ? 'status-active'
                  : 'status-other',
              ]"
            >
              {{ statusLabel(plane.status) }}
            </span>
          </td>
          <td>{{ plane.flight_hours }}</td>
          <td>{{ formatDateTime(plane.last_technical_service) }}</td>
        </tr>
      </tbody>
    </v-table>

    <p v-else-if="!loading && !error">
      Самолёты не найдены.
    </p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../api/api";

const loading = ref(false);
const error = ref("");
const planes = ref([]);

const loadPlanes = async () => {
  loading.value = true;
  error.value = "";
  try {
    const resp = await api.get("/api/planes/");
    planes.value = resp.data || [];
  } catch (e) {
    console.error(e);
    error.value = "Ошибка при загрузке списка самолётов.";
  } finally {
    loading.value = false;
  }
};

const statusLabel = (status) => {
  if (status === "maintenance") return "В ремонте";
  if (status === "active") return "В строю";
  if (status === "retired") return "Списан";
  return status;
};

const formatDateTime = (isoString) => {
  if (!isoString) return "";
  return new Date(isoString).toLocaleString();
};

onMounted(loadPlanes);
</script>

<style scoped>
.error {
  color: #d32f2f;
  margin-top: 8px;
}

.status-tag {
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
}

.status-maintenance {
  background-color: #ffebee;
  color: #c62828;
}

.status-active {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.status-other {
  background-color: #eceff1;
  color: #455a64;
}
</style>