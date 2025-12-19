<template>
  <div class="edit-flight">
    <h1>Редактировать Рейс №{{ flight.flight_number }}</h1>
    <form @submit.prevent="submitForm">
      <label for="departure_point">Пункт вылета:</label>
      <input type="text" id="departure_point" v-model="flight.departure_point" required />

      <label for="arrival_point">Пункт прилета:</label>
      <input type="text" id="arrival_point" v-model="flight.arrival_point" required />

      <label for="departure_datetime">Дата вылета:</label>
      <input type="datetime-local" id="departure_datetime" v-model="flight.departure_datetime" required />

      <label for="arrival_datetime">Дата прилета:</label>
      <input type="datetime-local" id="arrival_datetime" v-model="flight.arrival_datetime" required />

      <label for="sold_tickets">Количество проданных билетов:</label>
      <input type="number" id="sold_tickets" v-model="flight.sold_tickets" required />

      <label for="is_transit">
        Транзитный рейс:
        <input type="checkbox" id="is_transit" v-model="flight.is_transit" />
      </label>

      <button type="submit" class="button">Сохранить</button>
    </form>
  </div>
</template>

<script>
import { getFlight, updateFlight } from '../api/index.js';

export default {
  name: 'EditFlight',
  data() {
    return {
      flight: {
        flight_number: '',
        departure_point: '',
        arrival_point: '',
        departure_datetime: '',
        arrival_datetime: '',
        sold_tickets: '',
        is_transit: false,
      },
      error: null,
    };
  },
  async created() {
    const flightId = this.$route.params.id;
    try {
      const response = await getFlight(flightId);
      const flightData = response.data;

      this.flight.departure_datetime = this.formatDate(flightData.departure_datetime);
      this.flight.arrival_datetime = this.formatDate(flightData.arrival_datetime);

      this.flight = {
        ...flightData,
        departure_datetime: this.flight.departure_datetime,
        arrival_datetime: this.flight.arrival_datetime,
      };
    } catch (err) {
      this.error = 'Ошибка загрузки данных рейса.';
      console.error(err);
    }
  },
  methods: {
    async submitForm() {
      const flightId = this.$route.params.id;

      const updateData = {
            flight_number: this.flight.flight_number,
            departure_point: this.flight.departure_point,
            arrival_point: this.flight.arrival_point,
            departure_datetime: this.formatDate(this.flight.departure_datetime),
            arrival_datetime: this.formatDate(this.flight.arrival_datetime),
            sold_tickets: this.flight.sold_tickets,
            is_transit: this.flight.is_transit,
            plane: this.flight.plane.id,
            route: this.flight.route.id,
            crew: this.flight.crew.map((member) => member.id),
        };

        console.log('Отправляемые данные:', updateData);

        try {
            const response = await updateFlight(flightId, updateData);
            alert('Рейс успешно обновлен.');
            this.$router.push('/flights');
        } catch (err) {
            if (err.response && err.response.data) {
            console.error('Ответ ошибки от сервера:', err.response.data);
            }
            alert('Ошибка обновления.');
            console.error(err);
        }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
    },
  },
};
</script>

<style>
.edit-flight {
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
button {
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