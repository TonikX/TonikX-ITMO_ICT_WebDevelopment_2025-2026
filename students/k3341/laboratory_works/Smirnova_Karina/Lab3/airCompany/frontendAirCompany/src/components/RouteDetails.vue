<template>
  <div class="route-details">
    <div class="content-wrapper">
      <h1>Маршрут №{{ routeId }}</h1>

      <div class="route-info-card">
        <h2>Информация о маршруте</h2>
        <p><strong>Пункт вылета:</strong> {{ route.departure_point }}</p>
        <p><strong>Пункт назначения:</strong> {{ route. destination_point }}</p>
        <p><strong>Расстояние:</strong> {{ route. distance }} км</p>
        <p v-if="route. landing_points"><strong>Пункты посадки:</strong> {{ route.landing_points }}</p>
        <p v-if="route.transit_landings"><strong>Транзитные посадки:</strong> {{ route. transit_landings }}</p>
      </div>

      <h2>Связанные рейсы</h2>
      <div v-if="route.flights && route.flights.length > 0" class="flights-container">
        <div class="flight-card" v-for="flight in route.flights" :key="flight.id">
          <h3>Рейс №{{ flight.flight_number }}</h3>
          <p><strong>Пункт вылета:</strong> {{ flight.departure_point }}</p>
          <p><strong>Пункт прилета:</strong> {{ flight. arrival_point }}</p>
          <p><strong>Дата вылета:</strong> {{ flight.departure_datetime }}</p>
          <p><strong>Дата прилета:</strong> {{ flight.arrival_datetime }}</p>
          <p><strong>Транзитный:</strong> {{ flight.is_transit ? 'Да' : 'Нет' }}</p>
          <p><strong>Количество проданных билетов:</strong> {{ flight.sold_tickets }}</p>
          <p><strong>Самолет:</strong> {{ flight.plane.number }}</p>
          <router-link :to="`/flight/${flight.id}`" class="button button-primary button-full">
            Открыть информацию о рейсе
          </router-link>
        </div>
      </div>
      <p v-else class="no-data">Рейсы не найдены. </p>
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
      this.route = response.data;
    } catch (err) {
      this.error = 'Ошибка загрузки маршрута.';
      console.error(err);
    }
  },
};
</script>

<style scoped>
.route-details {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 20px 0;
}

.content-wrapper {
  max-width:  1400px;
  margin: 0 auto;
  padding: 0 30px;
}

.content-wrapper h1 {
  color: #333;
  margin-bottom: 20px;
}

.content-wrapper h2 {
  color: #333;
  margin-top:  30px;
  margin-bottom: 20px;
}

.route-info-card {
  background-color: white;
  border:  1px solid #e0e0e0;
  padding:  20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.route-info-card h2 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
  font-size: 20px;
}

.route-info-card p {
  margin: 8px 0;
  color: #555;
  line-height: 1.5;
}

.flights-container {
  display: grid;
  grid-template-columns:  repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.flight-card {
  background-color: white;
  border: 1px solid #e0e0e0;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  transition: box-shadow 0.3s ease;
}

.flight-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.flight-card h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
  font-size: 18px;
}

.flight-card p {
  margin:  8px 0;
  color: #555;
  line-height: 1.5;
}

.button {
  display: inline-block;
  padding: 10px 20px;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  border: none;
  cursor:  pointer;
  font-size:  14px;
  text-align: center;
  transition:  background-color 0.3s ease;
  white-space:  nowrap;
  font-weight: 500;
}

.button.button-primary {
  background-color: #007BFF;
}

.button.button-primary:hover {
  background-color: #0056b3;
}

.button-full {
  width: 100%;
  margin-top: 15px;
}

.no-data {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  color: #666;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .flights-container {
    grid-template-columns: 1fr;
  }
}
</style>