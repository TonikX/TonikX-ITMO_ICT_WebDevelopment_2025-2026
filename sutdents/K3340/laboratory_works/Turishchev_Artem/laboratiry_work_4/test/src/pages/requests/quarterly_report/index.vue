<template>
  <v-container>
    <v-card class="pa-6">
      <v-card-title class="text-h5">Квартальный отчёт</v-card-title>
      
      <v-card-text>
        <v-form @submit.prevent="fetchReport">
          <v-select
            v-model="quarter"
            :items="quarters"
            label="Квартал"
            variant="outlined"
            required
          ></v-select>

          <v-btn
            type="submit"
            color="primary"
            :loading="loading"
          >
            Получить отчёт
          </v-btn>
        </v-form>

        <div v-if="report" class="mt-4">
          <v-card class="mb-4 pa-4" color="primary" variant="tonal">
            <v-card-title class="text-h4">{{ report.income }} ₽</v-card-title>
            <v-card-subtitle>Общий доход за квартал</v-card-subtitle>
          </v-card>

          <h3 class="mb-3">Отчёт по номерам:</h3>
          <v-table>
            <thead>
              <tr>
                <th>ID Номера</th>
                <th>Количество гостей</th>
                <th>Доход (₽)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="room in report.room_report" :key="room.room_id">
                <td>{{ room.room_id }}</td>
                <td>{{ room.guests }}</td>
                <td>{{ room.income }}</td>
              </tr>
            </tbody>
          </v-table>

          <h3 class="mt-6 mb-3">Отчёт по этажам:</h3>
          <v-table>
            <thead>
              <tr>
                <th>ID Этажа</th>
                <th>Количество номеров</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(count, floorId) in report.floor_report" :key="floorId">
                <td>{{ floorId }}</td>
                <td>{{ count }}</td>
              </tr>
            </tbody>
          </v-table>
        </div>

        <v-alert v-if="error" type="error" class="mt-4">
          {{ error }}
        </v-alert>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import api from '@/api';

const quarter = ref(null);
const quarters = [
  { value: 1, title: '1 квартал (январь-март)' },
  { value: 2, title: '2 квартал (апрель-июнь)' },
  { value: 3, title: '3 квартал (июль-сентябрь)' },
  { value: 4, title: '4 квартал (октябрь-декабрь)' }
];
const report = ref(null);
const loading = ref(false);
const error = ref(null);

const fetchReport = async () => {
  if (!quarter.value) return;
  
  loading.value = true;
  error.value = null;
  report.value = null;
  try {
    const res = await api.get('api/report/quarterly/', {
      params: { quarter: quarter.value }
    });
    report.value = res.data;
  } catch (err) {
    error.value = 'Не удалось получить отчёт';
    console.error(err);
  } finally {
    loading.value = false;
  }
};
</script>
