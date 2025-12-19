<template>
  <div class="flight-details">
    <h1>Рейс №{{ flight.flight_number }}</h1>
    <div class="section">
      <h2>Маршрут:</h2>
      <p><strong>Пункт вылета:</strong> {{ flight.departure_point }}</p>
      <p><strong>Пункт назначения:</strong> {{ flight.arrival_point }}</p>
      <p><strong>Транзитный:</strong> {{ flight.is_transit ? 'Да' : 'Нет' }}</p>
      <p><strong>Дата вылета:</strong> {{ flight.departure_datetime }}</p>
      <p><strong>Дата прилета:</strong> {{ flight.arrival_datetime }}</p>
      <p v-if="flight.plane"><strong>Количество проданных билетов:</strong> {{ flight.sold_tickets }} / {{ flight.plane.seats_capacity }}</p>
    </div>
    <div class="section" v-if="flight.plane">
      <h2>Самолет:</h2>
      <p><strong>Номер:</strong> {{ flight.plane.number }}</p>
      <p><strong>Тип:</strong> {{ flight.plane.type }}</p>
      <p><strong>Число мест:</strong> {{ flight.plane.seats_capacity }}</p>
      <p><strong>Скорость полета:</strong> {{ flight.plane.flight_speed }} км/ч</p>
      <p v-if="flight.plane.in_repair"><strong>Состояние:</strong> В ремонте</p>
    </div>
    <div class="section" v-if="flight.crew && flight.crew.length > 0">
      <h2>Команда:</h2>
      <div v-for="crew in flight.crew" :key="crew.id" class="crew-section">
        <h3>Экипаж №{{ crew.id }}</h3>
        <ul>
          <li v-for="member in crew.members" :key="member.id">
            <p><strong>ФИО:</strong> {{ member.full_name }}</p>
            <p><strong>Возраст:</strong> {{ member.age }}</p>
            <p><strong>Образование:</strong> {{ member.education }}</p>
            <p><strong>Стаж работы:</strong> {{ member.work_experience }} лет</p>
            <p><strong>Должность:</strong> {{ member.position }}</p>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from '../api/index.js';

export default {
  name: 'FlightDetails',
  props: ['id'],
  data() {
    return {
      flight: {},
      error: null,
    };
  },
  async created() {
    try {
      const response = await axiosInstance.get(`/api/flights/${this.id}/`);
      this.flight = response.data;
    } catch (err) {
      this.error = 'Ошибка загрузки информации о рейсе.';
      console.error(err);
    }
  },
};
</script>

<style>
.flight-details {
  margin: 20px;
}

.section {
  background-color: white;
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 5px;
  border: 1px solid #ddd;
}

.crew-section {
  margin-top: 10px;
  background-color: #f9f9f9;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ddd;
}
</style>