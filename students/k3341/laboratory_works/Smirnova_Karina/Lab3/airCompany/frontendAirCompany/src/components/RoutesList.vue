<template>
  <div class="routes-list">
    <h1>Список маршрутов</h1>
    <div class="route-card" v-for="route in routes" :key="route.id">
      <h2>Маршрут №{{ route.id }}</h2>
      <p><strong>Пункт вылета:</strong> {{ route.departure_point }}</p>
      <p><strong>Пункт назначения:</strong> {{ route.destination_point }}</p>
      <p><strong>Расстояние:</strong> {{ route.distance }} км</p>
      <p v-if="route.landing_points"><strong>Пункты посадки:</strong> {{ route.landing_points }}</p>
      <p v-if="route.transit_landings"><strong>Транзитные посадки:</strong> {{ route.transit_landings }}</p>
      <router-link :to="`/route/${route.id}`" class="button">Открыть связанные рейсы</router-link>
    </div>
  </div>
</template>

<script>
import axiosInstance from '../api/index.js';

export default {
  name: 'RoutesList',
  data() {
    return {
      routes: [],
      error: null,
    };
  },
  async created() {
    try {
      const response = await axiosInstance.get('/api/routes/');
      this.routes = response.data; // Список маршрутов
    } catch (err) {
      this.error = 'Ошибка загрузки маршрутов.';
      console.error(err);
    }
  },
};
</script>

<style>
.routes-list {
  margin: 20px;
  font-family: Arial, sans-serif;
}

.route-card {
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
  background-color: white;
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