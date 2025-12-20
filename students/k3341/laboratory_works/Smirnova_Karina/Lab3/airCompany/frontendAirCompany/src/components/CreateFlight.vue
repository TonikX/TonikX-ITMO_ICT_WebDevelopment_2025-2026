<template>
  <div class="create-flight">
    <div class="content-wrapper">
      <h1>Создать рейс</h1>

      <div v-if="!isAuthenticated" class="warning">
        <p>Вы должны <router-link to="/login">войти</router-link>, чтобы создать рейс.</p>
      </div>

      <div class="form-container">
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label for="flight-number">Номер рейса:</label>
            <input type="number" id="flight-number" v-model="flight.flight_number" placeholder="Введите номер рейса" required />
          </div>

          <div class="form-group">
            <label for="departure-point">Пункт вылета: </label>
            <input type="text" id="departure-point" v-model="flight.departure_point" placeholder="Введите пункт вылета" required />
          </div>

          <div class="form-group">
            <label for="arrival-point">Пункт прилета:</label>
            <input type="text" id="arrival-point" v-model="flight.arrival_point" placeholder="Введите пункт прилета" required />
          </div>

          <div class="form-group">
            <label for="departure-datetime">Дата и время вылета:</label>
            <input type="datetime-local" id="departure-datetime" v-model="flight.departure_datetime" required />
          </div>

          <div class="form-group">
            <label for="arrival-datetime">Дата и время прилета:</label>
            <input type="datetime-local" id="arrival-datetime" v-model="flight.arrival_datetime" required />
          </div>

          <div class="form-group">
            <label for="sold-tickets">Количество проданных билетов:</label>
            <input type="number" id="sold-tickets" v-model="flight.sold_tickets" placeholder="Введите количество проданных билетов" required />
          </div>

          <div class="form-group">
            <label for="route">Маршрут:</label>
            <select id="route" v-model="flight.route" required>
              <option value="" disabled selected>Выберите маршрут</option>
              <option v-for="route in routes" :value="route.id" :key="route.id">
                {{ route.departure_point }} → {{ route.destination_point }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="plane">Самолет:</label>
            <select id="plane" v-model="flight.plane" required>
              <option value="" disabled selected>Выберите самолет</option>
              <option v-for="plane in planes" :value="plane.id" :key="plane.id">
                {{ plane.number }} — {{ plane.type }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="crew">Экипаж (можно выбрать несколько):</label>
            <select id="crew" multiple v-model="flight.crew" required class="multi-select">
              <option v-for="crew in crews" :value="crew.id" :key="crew.id">
                Команда №{{ crew.id }}
              </option>
            </select>
            <small class="form-hint">Удерживайте Ctrl (Cmd на Mac) для выбора нескольких команд</small>
          </div>

          <div class="form-group checkbox-group">
            <label for="is_transit">
              <input type="checkbox" id="is_transit" v-model="flight.is_transit" />
              <span>Транзитный рейс</span>
            </label>
          </div>

          <div class="button-group">
            <button type="submit" class="button button-primary">Создать</button>
            <button type="button" @click="$router.push('/flights')" class="button button-secondary">Отмена</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { getRoutes, getPlanes, getCrews, createFlight } from '@/api';

export default {
  name: 'CreateFlight',
  data() {
    return {
      flight: {
        flight_number: null,
        departure_point: '',
        arrival_point:  '',
        departure_datetime: '',
        arrival_datetime: '',
        sold_tickets: null,
        route: '',
        plane: '',
        crew: [],
        is_transit:  false,
      },
      routes: [],
      planes: [],
      crews: [],
      error:  null,
    };
  },
  computed: {
    isAuthenticated() {
      return !!this.$store.state.auth.token;
    },
  },
  async created() {
    try {
      const [routesResponse, planesResponse, crewsResponse] = await Promise. all([
        getRoutes(),
        getPlanes(),
        getCrews(),
      ]);
      this.routes = routesResponse.data;
      this.planes = planesResponse. data;
      this.crews = crewsResponse.data;
    } catch (err) {
      this.error = 'Ошибка загрузки данных.';
      console. error(err);
    }
  },
  methods: {
    async submitForm() {
      try {
        const flightData = {
          ...this.flight,
          departure_datetime: this.formatDate(this.flight. departure_datetime),
          arrival_datetime: this.formatDate(this.flight.arrival_datetime),
        };
        const response = await createFlight(flightData);
        alert('Рейс успешно создан.');
        this.resetForm();
        console.log(response.data);
        this.$router.push('/flights');
      } catch (err) {
        console.error('Ошибка создания рейса:', err);

        if (err.response && err.response. status === 401) {
          alert('Ошибка:  требуется авторизация.');
        } else if (err. response && err.response.status === 403) {
          alert('Ошибка: доступ запрещён.');
        } else if (err.response && err.response.data) {
          alert(`Ошибка создания рейса: ${JSON.stringify(err.response.data)}`);
        } else {
          alert('Ошибка создания рейса.');
        }

        console.error(err);
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
    },
    resetForm() {
      this.flight = {
        flight_number: null,
        departure_point: '',
        arrival_point: '',
        departure_datetime:  '',
        arrival_datetime: '',
        sold_tickets: null,
        route: '',
        plane: '',
        crew: [],
        is_transit: false,
      };
    }
  },
};
</script>

<style scoped>
.create-flight {
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
  font-size:  28px;
}

.warning {
  background-color: #fff3cd;
  border: 1px solid #ffc107;
  border-radius:  8px;
  padding: 15px 20px;
  margin-bottom: 20px;
  color: #856404;
}

.warning p {
  margin: 0;
  font-size: 14px;
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
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color:  #333;
  font-size: 14px;
}

.form-group input,
.form-group select {
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
.form-group select:focus {
  outline: none;
  border-color: #007BFF;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.multi-select {
  min-height: 120px;
}

.form-hint {
  display: block;
  margin-top: 5px;
  font-size: 12px;
  color: #666;
  font-style: italic;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.checkbox-group input[type="checkbox"] {
  width:  18px;
  height:  18px;
  margin-right: 10px;
  cursor: pointer;
  accent-color: #007BFF;
}

.checkbox-group span {
  font-weight: 500;
  color:  #333;
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
  background-color:  #0056b3;
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

  .button-group . button {
    width: 100%;
  }
}
</style>