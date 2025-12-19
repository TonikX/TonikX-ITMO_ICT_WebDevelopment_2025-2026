<template>
  <div class="edit-route">
    <h1>Редактировать Маршрут</h1>
    <form @submit.prevent="submitForm">
      <label for="departure_point">Пункт вылета:</label>
      <input type="text" id="departure_point" v-model="route.departure_point" required />

      <label for="destination_point">Пункт назначения:</label>
      <input type="text" id="destination_point" v-model="route.destination_point" required />

      <label for="distance">Расстояние:</label>
      <input type="number" id="distance" v-model="route.distance" required />

      <label for="landing_points">Пункты посадки:</label>
      <textarea id="landing_points" v-model="route.landing_points"></textarea>

      <label for="transit_landings">Транзитные посадки:</label>
      <textarea id="transit_landings" v-model="route.transit_landings"></textarea>

      <button type="submit" class="button">Сохранить</button>
    </form>
  </div>
</template>

<script>
import axiosInstance from '../api/index.js';

export default {
  name: 'EditRoute',
  data() {
    return {
      route: {
        departure_point: '',
        destination_point: '',
        distance: null,
        landing_points: '',
        transit_landings: '',
      },
      error: null,
    };
  },
  async created() {
    const routeId = this.$route.params.id;
    try {
      const response = await axiosInstance.get(`/api/routes/${routeId}/`);
      this.route = response.data;
    } catch (err) {
      this.error = 'Ошибка загрузки данных маршрута.';
      console.error(err);
    }
  },
  methods: {
    async submitForm() {
      const routeId = this.$route.params.id;
      try {
        await axiosInstance.put(`/api/routes/${routeId}/`, this.route);
        alert('Маршрут успешно обновлен.');
        this.$router.push('/routes');
      } catch (err) {
        alert('Ошибка сохранения маршрута.');
        console.error(err);
      }
    },
  },
};
</script>

<style>
.edit-route {
  margin: 20px;
  font-family: Arial, sans-serif;
}

form {
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 5px;
  font-weight: bold;
}

input,
textarea {
  margin-bottom: 10px;
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.button {
  padding: 10px 15px;
  color: white;
  background-color: #007BFF;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.button:hover {
  background-color: #0056b3;
}
</style>