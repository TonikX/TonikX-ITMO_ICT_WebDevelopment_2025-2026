<template>
  <div class="route-details">
    <h1>Маршрут №{{ routeId }}</h1>
    <p><strong>Пункт вылета:</strong> {{ route.departure_point }}</p>
    <p><strong>Пункт назначения:</strong> {{ route.destination_point }}</p>
    <p><strong>Расстояние:</strong> {{ route.distance }} км</p>
    <p v-if="route.landing_points"><strong>Пункты посадки:</strong> {{ route.landing_points }}</p>
    <p v-if="route.transit_landings"><strong>Транзитные посадки:</strong> {{ route.transit_landings }}</p>

    <h2>Связанные рейсы</h2>
    <div class="flight-card" v-for="flight in route.flights" :key="flight.id">
      <p><strong>Номер рейса:</strong> {{ flight.flight_number }}</p>
      <p><strong>Дата вылета:</strong> {{ flight.departure_datetime }}</p>
      <p><strong>Дата прилета:</strong> {{ flight.arrival_datetime }}</p>
      <p><strong>Самолет:</strong> {{ flight.plane.number }}</p>
      <router-link :to="`/flight/${flight.id}`" class="button">Открыть информацию о рейсе</router-link>
    </div>
  </div>
</template>

<script>
import axiosInstance from '../api/index.js';

export default {
  name: 'RouteDetails',
  props: ['id'],
  data() {
    return {
      routeId: this.id,
      route: {},
      error: null,
    };
  },
  async created() {
    try {
      const response = await axiosInstance.get(`/api/routes/${this.routeId}/`);
      this.route = response.data; // Информация о маршруте и связанных рейсах
    } catch (err) {
      this.error = 'Ошибка загрузки маршрута.';
      console.error(err);
    }
  },
};
</script>

<style>
.route-details {
  margin: 20px;
}

.flight-card {
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
  background-color: #f9f9f9;
}

.button {
  display: inline-block;
  padding: 10px 15px;
  color: white;
  background-color: #007BFF;
  text-decoration: none;
  border-radius: 5px;
}
</style>