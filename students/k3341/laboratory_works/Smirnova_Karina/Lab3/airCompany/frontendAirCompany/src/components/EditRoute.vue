<template>
  <div class="edit-route">
    <div class="content-wrapper">
      <h1>Редактировать маршрут</h1>

      <div class="form-container">
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label for="departure_point">Пункт вылета:</label>
            <input type="text" id="departure_point" v-model="route.departure_point" required />
          </div>

          <div class="form-group">
            <label for="destination_point">Пункт назначения:</label>
            <input type="text" id="destination_point" v-model="route.destination_point" required />
          </div>

          <div class="form-group">
            <label for="distance">Расстояние (км):</label>
            <input type="number" id="distance" v-model="route.distance" required />
          </div>

          <div class="form-group">
            <label for="landing_points">Пункты посадки:</label>
            <textarea id="landing_points" v-model="route.landing_points" rows="3"></textarea>
          </div>

          <div class="form-group">
            <label for="transit_landings">Транзитные посадки:</label>
            <textarea id="transit_landings" v-model="route.transit_landings" rows="3"></textarea>
          </div>

          <div class="button-group">
            <button type="submit" class="button button-primary">Сохранить</button>
            <button type="button" @click="$router.push('/routes')" class="button button-secondary">Отмена</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from '../api/index.js';

export default {
  name: 'EditRoute',
  data() {
    return {
      route:  {
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
  methods:  {
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

<style scoped>
.edit-route {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 20px 0;
}

.content-wrapper {
  max-width:  800px;
  margin: 0 auto;
  padding: 0 30px;
}

.content-wrapper h1 {
  color: #333;
  margin-bottom: 30px;
  font-size: 28px;
}

.form-container {
  background-color: white;
  border:  1px solid #e0e0e0;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight:  500;
  color: #333;
  font-size: 14px;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px 15px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
  transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #007BFF;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.button {
  display: inline-block;
  padding: 12px 24px;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  text-align:  center;
  transition: background-color 0.3s ease;
  font-weight: 500;
}

.button.button-primary {
  background-color: #007BFF;
}

.button.button-primary:hover {
  background-color: #0056b3;
}

.button.button-secondary {
  background-color: #6c757d;
}

.button.button-secondary:hover {
  background-color: #5a6268;
}

.button-group {
  display:  flex;
  gap: 10px;
  margin-top:  30px;
}

.button-group.button {
  flex: 1;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .form-container {
    padding: 20px;
  }

  .button-group {
    flex-direction: column;
  }

  .button-group.button {
    width: 100%;
  }
}
</style>