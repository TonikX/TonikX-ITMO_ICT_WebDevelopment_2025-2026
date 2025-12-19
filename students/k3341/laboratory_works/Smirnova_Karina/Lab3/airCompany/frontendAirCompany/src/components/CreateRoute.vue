<template>
  <div class="create-form">
    <h1>Создать Маршрут</h1>

    <div v-if="!isAuthenticated" class="warning">
      <p>Вы должны <router-link to="/login">войти</router-link>, чтобы создать маршрут.</p>
    </div><br/>

    <form @submit.prevent="submitForm">
      <label for="departure-point">Пункт вылета:</label>
      <input type="text" id="departure-point" v-model="route.departure_point" placeholder="Введите пункт вылета" required />

      <label for="destination-point">Пункт назначения:</label>
      <input type="text" id="destination-point" v-model="route.destination_point" placeholder="Введите пункт назначения" required />

      <label for="distance">Расстояние:</label>
      <input type="number" id="distance" v-model="route.distance" placeholder="Введите расстояние" required />

      <label for="landing-points">Пункты посадки:</label>
      <textarea id="landing-points" v-model="route.landing_points" placeholder="Введите пункты посадки (через запятую)"></textarea>

      <label for="transit-landings">Транзитные посадки:</label>
      <textarea id="transit-landings" v-model="route.transit_landings" placeholder="Введите транзитные посадки (через запятую)"></textarea>

      <button type="submit">Создать</button>
    </form>
  </div>
</template>

<script>
import { createRoute } from '../api/index.js';
export default {
  name: 'CreateRoute',
  data() {
    return {
      route: {
        departure_point: '',
        destination_point: '',
        distance: null,
        landing_points: '',
        transit_landings: '',
      },
    };
  },
  computed: {
    isAuthenticated() {
      return !!this.$store.state.auth.token;
    },
  },
  methods: {
    async submitForm() {
      try {
        const response = await createRoute(this.route);
        alert('Маршрут успешно создан.')
        console.log('Результат:', response.data);
        this.resetForm();
        this.$router.push('/routes');
      } catch(err){
        if (err.response && err.response.status === 401) {
          alert('Ошибка:  требуется авторизация.');
        } else if (err.response && err.response.status === 403) {
          alert('Ошибка: доступ запрещён.');
        } else {
          alert('Ошибка создания маршрута.');
        }
        console.error(err);

      }
    },
    resetForm() {
      this.route = {
        departure_point: '',
        destination_point: '',
        distance: null,
        landing_points: '',
        transit_landings: '',
      };
    }
  },
};
</script>

<style>
.create-form {
  margin: 20px;
  font-family: Arial, sans-serif;
}

h1 {
  font-size: 24px;
  margin-bottom: 20px;
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

button {
  padding: 10px 15px;
  font-size: 16px;
  color: white;
  background-color: #007BFF;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>