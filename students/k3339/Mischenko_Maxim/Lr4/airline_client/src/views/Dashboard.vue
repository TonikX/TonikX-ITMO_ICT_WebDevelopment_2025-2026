<template>
  <v-container>
    <h1 class="mb-4">Панель администратора</h1>

    <v-tabs v-model="tab" bg-color="primary">
      <v-tab value="one">Самолеты в ремонте</v-tab>
      <v-tab value="two">Анализ маршрутов</v-tab>
      <v-tab value="three">Поиск мест</v-tab>
    </v-tabs>

    <v-card-text>
      <v-window v-model="tab">

        <!-- 1 Самолеты в ремонте (GET planes/in_repair/) -->
        <v-window-item value="one">
          <v-btn @click="loadRepairPlanes" class="mb-2">Обновить список</v-btn>
          <v-table v-if="repairPlanes.length">
            <thead>
              <tr>
                <th>ID</th>
                <th>Модель (Mark)</th>
                <th>Компания</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="plane in repairPlanes" :key="plane.id">
                <td>{{ plane.id }}</td>
                <td>{{ plane.mark }}</td>
                <td>{{ plane.company }}</td>
              </tr>
            </tbody>
          </v-table>
          <v-alert v-else type="info">Нет самолетов в ремонте или данные не загружены</v-alert>
        </v-window-item>

        <!-- 2 Выборка маршрутов (POST routes/pick/) -->
        <v-window-item value="two">
          <v-card variant="outlined" class="pa-4 mb-4">
            <p>Найти рейсы с заполненностью МЕНЬШЕ, чем:</p>
            <v-slider
              v-model="occupancyThreshold"
              min="0"
              max="1"
              step="0.1"
              thumb-label
              label="Коэффициент (0.0 - 1.0)"
            ></v-slider>
            <v-btn color="primary" @click="pickRoutes">Найти рейсы</v-btn>
          </v-card>

          <v-list v-if="pickedFlights.length">
            <v-list-item v-for="flight in pickedFlights" :key="flight.id">
              <v-list-item-title>Рейс #{{ flight.id }}</v-list-item-title>
              <v-list-item-subtitle>
                {{ flight.departure_airport }} -> {{ flight.destination_airport }}
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-window-item>

        <!-- 3 Доступные места (GET flights/<id>/available_seats/) -->
        <v-window-item value="three">
          <v-text-field v-model="flightIdSearch" label="Введите ID рейса" type="number"></v-text-field>
          <v-btn @click="checkSeats" color="secondary">Показать места</v-btn>
          
          <div v-if="availableSeats.length" class="mt-4">
            <v-chip v-for="seat in availableSeats" :key="seat" class="ma-1" color="green">
              {{ seat }}
            </v-chip>
          </div>
        </v-window-item>

      </v-window>
    </v-card-text>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api';

const tab = ref(null);

const repairPlanes = ref([]);
const loadRepairPlanes = async () => {
  try {
    const res = await api.get('/air/planes/in_repair/');
    repairPlanes.value = res.data.planes;
  } catch (e) {
    console.error(e);
  }
};

const occupancyThreshold = ref(0.5);
const pickedFlights = ref([]);
const pickRoutes = async () => {
  try {
    const res = await api.post('/air/routes/pick/', {
      filled_less_than: occupancyThreshold.value
    });
    pickedFlights.value = res.data.flights;
  } catch (e) {
    console.error(e);
    alert('Ошибка загрузки маршрутов');
  }
};

const flightIdSearch = ref('');
const availableSeats = ref([]);
const checkSeats = async () => {
  if (!flightIdSearch.value) return;
  try {
    const res = await api.get(`/air/flights/${flightIdSearch.value}/available_seats/`);
    availableSeats.value = res.data.available_seats;
  } catch (e) {
    alert('Рейс не найден или ошибка сервера');
    availableSeats.value = [];
  }
};

onMounted(() => {
  loadRepairPlanes();
});
</script>
