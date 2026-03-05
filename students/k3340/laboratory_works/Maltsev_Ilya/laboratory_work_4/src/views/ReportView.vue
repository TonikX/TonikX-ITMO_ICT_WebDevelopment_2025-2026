<script setup>
import axios from 'axios';
import { onMounted, ref } from 'vue';

const isLoading = ref(false);
const isError = ref(false);
const reportData = ref([]);

async function fetchReport() {
  isLoading.value = true;
  isError.value = false;

  await axios.get('insurance/report')
      .then(response => {
        reportData.value = response.data;
      })
      .catch(error => {
        console.error('Error fetching report:', error);
        isError.value = true;
      })
      .finally(() => {
        isLoading.value = false;
      });
}

onMounted(fetchReport);
</script>

<template>
  <div class="report-container">
    <h1>Отчёт</h1>

    <div v-if="isLoading">Загрузка...</div>
    <div v-if="isError" class="error">Возникла ошибка при загрузке отчёта</div>

    <table v-if="reportData.length" class="report-table">
      <thead>
      <tr>
        <th>ФИО</th>
        <th>Активные индивидуальные контракты</th>
        <th>Активные коллективные контракты</th>
        <th>Сумма по индивидуальным контрактам</th>
        <th>Сумма по коллективным контрактам</th>
        <th>Общая сумма</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="agent in reportData" :key="agent.id">
        <td>{{ agent.second_name }} {{ agent.first_name }}</td>
        <td>{{ agent.active_individual_contracts }}</td>
        <td>{{ agent.active_collective_contracts }}</td>
        <td>{{ agent.total_individual_sum }} руб.</td>
        <td>{{ agent.total_collective_sum }} руб.</td>
        <td>{{ agent.company_total_sum }} руб.</td>
      </tr>
      </tbody>
    </table>
    <p v-else>Нет данных для отображения</p>
  </div>
</template>

<style scoped>
.report-container {
  padding: 20px;
  text-align: center;
}

h1 {
  font-size: 24px;
  margin-bottom: 20px;
}

.report-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.report-table th, .report-table td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}

.report-table th {
  background-color: #f4f4f4;
}

.error {
  color: red;
  font-weight: bold;
}
</style>
