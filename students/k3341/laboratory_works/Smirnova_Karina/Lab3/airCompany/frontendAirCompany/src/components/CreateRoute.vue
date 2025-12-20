<template>
  <div class="create-route">
    <div class="content-wrapper">
      <h1>Создать маршрут</h1>

      <div v-if="! isAuthenticated" class="warning">
        <p>Вы должны <router-link to="/login">войти</router-link>, чтобы создать маршрут.</p>
      </div>

      <div class="form-container">
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label for="departure-point">Пункт вылета:</label>
            <input type="text" id="departure-point" v-model="route.departure_point" placeholder="Введите пункт вылета" required />
          </div>

          <div class="form-group">
            <label for="destination-point">Пункт назначения:</label>
            <input type="text" id="destination-point" v-model="route.destination_point" placeholder="Введите пункт назначения" required />
          </div>

          <div class="form-group">
            <label for="distance">Расстояние (км):</label>
            <input type="number" id="distance" v-model="route.distance" placeholder="Введите расстояние" required />
          </div>

          <div class="form-group">
            <label for="landing-points">Пункты посадки:</label>
            <textarea id="landing-points" v-model="route.landing_points" placeholder="Введите пункты посадки (через запятую)" rows="3"></textarea>
          </div>

          <div class="form-group">
            <label for="transit-landings">Транзитные посадки:</label>
            <textarea id="transit-landings" v-model="route.transit_landings" placeholder="Введите транзитные посадки (через запятую)" rows="3"></textarea>
          </div>

          <div class="button-group">
            <button type="submit" class="button button-primary">Создать</button>
            <button type="button" @click="$router.push('/routes')" class="button button-secondary">Отмена</button>
          </div>
        </form>
      </div>
    </div>
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
        distance:  null,
        landing_points:  '',
        transit_landings:  '',
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
        console.error('Ошибка создания маршрута:', err);

        if (err.response && err. response.status === 401) {
          alert('Ошибка:  требуется авторизация.');
        } else if (err.response && err.response.status === 403) {
          alert('Ошибка: доступ запрещён.');
        } else if (err.response && err.response.data) {
          alert(`Ошибка создания маршрута: ${JSON.stringify(err.response.data)}`);
        } else {
          alert('Ошибка создания маршрута.');
        }

        console.error(err);
      }
    },
    resetForm() {
      this.route = {
        departure_point:  '',
        destination_point: '',
        distance: null,
        landing_points: '',
        transit_landings: '',
      };
    }
  },
};
</script>

<style scoped>
.create-route {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 20px 0;
}

.content-wrapper {
  max-width:  800px;
  margin:  0 auto;
  padding: 0 30px;
}

.content-wrapper h1 {
  color: #333;
  margin-bottom: 30px;
  font-size: 28px;
}

.warning {
  background-color: #fff3cd;
  border: 1px solid #ffc107;
  border-radius: 8px;
  padding: 15px 20px;
  margin-bottom: 20px;
  color: #856404;
}

.warning p {
  margin: 0;
  font-size:  14px;
}

.warning a {
  color: #007BFF;
  text-decoration: none;
  font-weight: 500;
}

.warning a:hover {
  text-decoration: underline;
}

.form-container {
  background-color: white;
  border: 1px solid #e0e0e0;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom:  20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
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
  text-align: center;
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
  display: flex;
  gap: 10px;
  margin-top: 30px;
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