<template>
  <div class="flight-list">
    <h1>Список рейсов</h1>
    <div class="flight-card" v-for="flight in flights" :key="flight.id">
      <h2>Рейс №{{ flight.flight_number }}</h2>
      <p><strong>Номер маршрута:</strong> {{ flight.route.id }}</p>
      <p><strong>Пункт вылета:</strong> {{ flight.route.departure_point }}</p>
      <p><strong>Пункт назначения:</strong> {{ flight.route.destination_point }}</p>
      <p><strong>Дата вылета:</strong> {{ flight.departure_datetime }}</p>
      <p><strong>Дата прилета:</strong> {{ flight.arrival_datetime }}</p>
      <p><strong>Количество проданных билетов:</strong> {{ flight.sold_tickets }}</p>
      <p><strong>Номер самолета:</strong> {{ flight.plane.number }}</p>
      <p v-if="flight.crew.length > 0"><strong>Номер команды:</strong>
        <span v-for="crew in flight.crew" :key="crew.id">{{ crew.id }}{{ flight.crew.indexOf(crew) < flight.crew.length - 1 ? ',' : '' }}</span>
      </p>
      <router-link :to="`/flight/${flight.id}`" class="button">Открыть информацию о рейсе</router-link>
    </div>
    <p v-if="flights.length === 0">Нет доступных рейсов</p>
  </div>
</template>

<script>
import { getFlights } from '../api/index.js';

export default {
  name: 'FlightList',
  data() {
    return {
      flights: [],
      error: null,
    };
  },
  async created() {
    try {
      const response = await getFlights();
      this.flights = response.data; // Предполагается, что API возвращает массив рейсов с вложенными данными
    } catch (err) {
      this.error = 'Ошибка загрузки данных рейсов.';
      console.error(err);
    }
  },
};
</script>

<style>
.flight-list {
  margin: 20px;
  font-family: Arial, sans-serif;
}

.flight-card {
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
  background-color: #f9f9f9;
  border-radius: 5px;
}

.flight-card h2 {
  font-size: 20px;
  margin-bottom: 10px;
}

.flight-card p {
  margin: 5px 0;
}

.button {
  display: inline-block;
  padding: 10px 15px;
  color: white;
  background-color: #007BFF;
  text-decoration: none;
  border-radius: 5px;
  margin-top: 10px;
}
</style>