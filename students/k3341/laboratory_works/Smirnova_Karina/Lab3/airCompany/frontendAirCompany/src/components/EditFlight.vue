<template>
  <div class="edit-flight">
    <div class="content-wrapper">
      <h1>Редактировать рейс №{{ flight.flight_number }}</h1>

      <div class="form-container">
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label for="departure_point">Пункт вылета:</label>
            <input type="text" id="departure_point" v-model="flight.departure_point" required />
          </div>

          <div class="form-group">
            <label for="arrival_point">Пункт прилета:</label>
            <input type="text" id="arrival_point" v-model="flight.arrival_point" required />
          </div>

          <div class="form-group">
            <label for="departure_datetime">Дата вылета:</label>
            <input type="datetime-local" id="departure_datetime" v-model="flight.departure_datetime" required />
          </div>

          <div class="form-group">
            <label for="arrival_datetime">Дата прилета:</label>
            <input type="datetime-local" id="arrival_datetime" v-model="flight.arrival_datetime" required />
          </div>

          <div class="form-group">
            <label for="sold_tickets">Количество проданных билетов:</label>
            <input type="number" id="sold_tickets" v-model="flight.sold_tickets" required />
          </div>

          <div class="form-group checkbox-group">
            <label for="is_transit">
              <input type="checkbox" id="is_transit" v-model="flight.is_transit" />
              <span>Транзитный рейс</span>
            </label>
          </div>

          <div class="button-group">
            <button type="submit" class="button button-primary">Сохранить</button>
            <button type="button" @click="$router.push('/flights')" class="button button-secondary">Отмена</button>
          </div>
        </form>
      </div>
    </div>
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
        departure_point:  '',
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

      this.flight.departure_datetime = this.formatDate(flightData. departure_datetime);
      this.flight.arrival_datetime = this. formatDate(flightData.arrival_datetime);

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
        flight_number: this.flight. flight_number,
        departure_point: this.flight.departure_point,
        arrival_point:  this.flight.arrival_point,
        departure_datetime: this. formatDate(this.flight.departure_datetime),
        arrival_datetime: this.formatDate(this. flight.arrival_datetime),
        sold_tickets: this.flight. sold_tickets,
        is_transit: this.flight.is_transit,
        plane: this. flight.plane.id,
        route: this.flight.route. id,
        crew: this. flight.crew.map((member) => member.id),
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

<style scoped>
.edit-flight {
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
  font-weight: 500;
  color:  #333;
  font-size: 14px;
}

.form-group input[type="text"],
.form-group input[type="number"],
.form-group input[type="datetime-local"] {
  width: 100%;
  padding: 10px 15px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #007BFF;
  box-shadow:  0 0 0 3px rgba(0, 123, 255, 0.1);
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