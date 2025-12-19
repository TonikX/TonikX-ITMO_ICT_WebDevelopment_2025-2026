<template>
  <div class="create-form">
    <h1>Создать Рейс</h1>

    <div v-if="!isAuthenticated" class="warning">
      <p>Вы должны <router-link to="/login">войти</router-link>, чтобы создать маршрут.</p>
    </div><br/>

    <form @submit.prevent="submitForm">
      <label for="flight-number">Номер рейса:</label>
      <input type="number" id="flight-number" v-model="flight.flight_number" placeholder="Введите номер рейса" required />

      <label for="departure-point">Пункт вылета:</label>
      <input type="text" id="departure-point" v-model="flight.departure_point" placeholder="Введите пункт вылета" required />

      <label for="arrival-point">Пункт прилета:</label>
      <input type="text" id="arrival-point" v-model="flight.arrival_point" placeholder="Введите пункт прилета" required />

      <label for="departure-datetime">Дата и время вылета:</label>
      <input type="datetime-local" id="departure-datetime" v-model="flight.departure_datetime" required />

      <label for="arrival-datetime">Дата и время прилета:</label>
      <input type="datetime-local" id="arrival-datetime" v-model="flight.arrival_datetime" required />

      <label for="sold-tickets">Количество проданных билетов:</label>
      <input type="number" id="sold-tickets" v-model="flight.sold_tickets" placeholder="Введите количество проданных билетов" required />

      <label for="route">Маршрут:</label>
      <select id="route" v-model="flight.route" required>
        <option v-for="route in routes" :value="route.id" :key="route.id">
          {{ route.departure_point }} → {{ route.destination_point }}
        </option>
      </select>

      <label for="plane">Самолет:</label>
      <select id="plane" v-model="flight.plane" required>
        <option v-for="plane in planes" :value="plane.id" :key="plane.id">
          {{ plane.number }} — {{ plane.type }}
        </option>
      </select>

      <label for="crew">Экипаж:</label>
      <select id="crew" multiple v-model="flight.crew" required>
        <option v-for="crew in crews" :value="crew.id" :key="crew.id">
          Команда №{{ crew.id }}
        </option>
      </select>

      <label>
        <input type="checkbox" v-model="flight.is_transit" />
        Транзитный рейс
      </label>

      <button type="submit">Создать</button>
    </form>
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
            arrival_point: '',
            departure_datetime: '',
            arrival_datetime: '',
            sold_tickets: null,
            route: null,
            plane: null,
            crew: [],
            is_transit: false,
        },
        routes: [],
        planes: [],
        crews: [],
        error: null,
    };
  },
  computed: {
    isAuthenticated() {
      return !!this.$store.state.auth.token;
    },
  },
  async created() {
    try {
        const [routesResponse, planesResponse, crewsResponse] = await Promise.all([
        getRoutes(),
        getPlanes(),
        getCrews(),
        ]);
        this.routes = routesResponse.data;
        this.planes = planesResponse.data;
        this.crews = crewsResponse.data;
    } catch (err) {
        this.error = 'Ошибка загрузки данных.';
        console.error(err);
    }
  },
  methods: {
    async submitForm() {
      try {
        const flightData = {
          ...this.flight,
          departure_datetime: this.formatDate(this.flight.departure_datetime),
          arrival_datetime: this.formatDate(this.flight.arrival_datetime),
        };
        const response = await createFlight(flightData);
        alert('Рейс успешно создан.');
        this.resetForm();
        console.log(response.data);
        this.$router.push('/flights');
      } catch (err) {
        console.error('Ошибка создания рейса:', err);

        if (err.response && err.response.status === 401) {
          alert('Ошибка:  требуется авторизация.');
        } else if (err. response && err.response.status === 403) {
          alert('Ошибка: доступ запрещён.');
        } else if (err.response && err.response.data) {
          alert(`Ошибка создания рейса: ${err.response.data}`);
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
        departure_datetime: '',
        arrival_datetime: '',
        sold_tickets: null,
        route: null,
        plane: null,
        crew: [],
        is_transit: false,
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
select {
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