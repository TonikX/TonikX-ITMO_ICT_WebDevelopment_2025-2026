<script setup>
import axios from 'axios';
import { onMounted, ref } from 'vue';

const isLoading = ref(false);
const isError = ref(false);
const reportData = ref(null);

async function fetchReport() {
  isLoading.value = true;
  isError.value = false;

  await axios.get('manufactory/reports').then(response => {
    reportData.value = response.data;
  }).catch(error => {
    console.error('Error fetching report:', error);
    isError.value = true;
  }).finally(() => {
    isLoading.value = false;
  });
}

onMounted(fetchReport);
</script>

<template>
  <div class="date-range-report">
    <h1>Отчёт за последний месяц</h1>

    <div v-if="isLoading">Загрузка...</div>
    <div v-if="isError" class="error">Возникла ошибка при загрузке отчёта</div>

    <div v-if="reportData && reportData.last_month_data && reportData.last_month_data.length > 0">
      <div v-for="data in reportData.last_month_data" :key="data.workshop" class="report-item">
        <v-card class="mt-3">
          <v-card-title>{{ data.workshop }}</v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <p><strong>Порода:</strong> {{ data.breed_name }}</p>
            <p><strong>Количество куриц:</strong> {{ data.chicken_count }}</p>
            <p><strong>Всего яиц:</strong> {{ data.total_eggs }}</p>
            <p><strong>Средняя продуктивность:</strong> {{ data.avg_performance }}</p>
          </v-card-text>
        </v-card>
      </div>
    </div>
  </div>
</template>


<style scoped>
.date-range-report {
  max-width: 600px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}

.date-selectors label {
  display: block;
  margin-bottom: 5px;
}

.date-selectors input {
  margin-bottom: 10px;
  width: 100%;
  padding: 5px;
}

button {
  padding: 10px 20px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.error {
  color: red;
  font-weight: bold;
}

.report-item {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
}

.report-item h3 {
  margin-top: 0;
}
</style>
