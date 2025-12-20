<template>
  <div class="flight-details">
    <div class="content-wrapper">
      <div class="header-section">
        <h1>Рейс №{{ flight.flight_number }}</h1>
        <div class="button-group-header">
          <button @click="editFlight" class="button button-primary button-small">Редактировать</button>
          <button @click="deleteFlight" class="button button-danger button-small">Удалить</button>
        </div>
      </div>

      <div class="details-container">
        <div class="section">
          <h2>Маршрут</h2>
          <div class="info-grid">
            <p><strong>Пункт вылета:</strong> {{ flight.departure_point }}</p>
            <p><strong>Пункт назначения:</strong> {{ flight. arrival_point }}</p>
            <p><strong>Транзитный:</strong> {{ flight.is_transit ? 'Да' : 'Нет' }}</p>
            <p><strong>Дата вылета:</strong> {{ flight.departure_datetime }}</p>
            <p><strong>Дата прилета:</strong> {{ flight. arrival_datetime }}</p>
            <p v-if="flight.plane"><strong>Количество проданных билетов:</strong> {{ flight.sold_tickets }} / {{ flight.plane.seats_capacity }}</p>
          </div>
        </div>

        <div class="section" v-if="flight.plane">
          <h2>Самолет</h2>
          <div class="info-grid">
            <p><strong>Номер:</strong> {{ flight.plane.number }}</p>
            <p><strong>Тип: </strong> {{ flight.plane.type }}</p>
            <p><strong>Число мест:</strong> {{ flight.plane.seats_capacity }}</p>
            <p><strong>Скорость полета:</strong> {{ flight.plane.flight_speed }} км/ч</p>
            <p v-if="flight.plane.in_repair"><strong>Состояние:</strong> <span class="status-repair">В ремонте</span></p>
          </div>
        </div>

        <div class="section" v-if="flight.crew && flight.crew.length > 0">
          <h2>Команда</h2>
          <div v-for="crew in flight.crew" :key="crew.id" class="crew-section">
            <h3>Экипаж №{{ crew.id }}</h3>
            <div class="members-grid">
              <div class="member-card" v-for="member in crew. members" :key="member.id">
                <p><strong>ФИО:</strong> {{ member.full_name }}</p>
                <p><strong>Возраст:</strong> {{ member. age }}</p>
                <p><strong>Образование:</strong> {{ member.education }}</p>
                <p><strong>Стаж работы:</strong> {{ member.work_experience }} лет</p>
                <p><strong>Должность: </strong> {{ member.position }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="back-button-container">
          <button @click="goBack" class="button button-secondary button-full">Вернуться к списку рейсов</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from '../api/index.js';
import { deleteFlight } from '../api/index.js';

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
    await this.loadFlight();
  },
  methods: {
    async loadFlight() {
      try {
        const response = await axiosInstance.get(`/api/flights/${this.id}/`);
        this.flight = response.data;
      } catch (err) {
        this.error = 'Ошибка загрузки информации о рейсе.';
        console.error(err);
        alert('Ошибка загрузки информации о рейсе.');
      }
    },
    editFlight() {
      this.$router.push(`/edit-flight/${this.id}`);
    },
    async deleteFlight() {
      if (!confirm("Вы уверены, что хотите удалить этот рейс?")) {
        return;
      }
      try {
        await deleteFlight(this.id);
        alert("Рейс успешно удален.");
        this.$router. push('/flights');
      } catch (err) {
        alert("Ошибка удаления рейса.");
        console.error(err);
      }
    },
    goBack() {
      this.$router.push('/flights');
    }
  },
};
</script>

<style scoped>
.flight-details {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 20px 0;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 30px;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding:  20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  flex-wrap: wrap;
  gap: 15px;
}

.header-section h1 {
  margin: 0;
  color: #333;
  font-size: 28px;
}

.button-group-header {
  display:  flex;
  gap: 10px;
  flex-wrap: wrap;
}

.details-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section {
  background-color: white;
  padding:  25px;
  border-radius:  8px;
  border: 1px solid #e0e0e0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.section h2 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #333;
  font-size: 22px;
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 10px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
}

.info-grid p {
  margin: 0;
  color: #555;
  line-height: 1.6;
  font-size: 14px;
}

.info-grid strong {
  color: #333;
}

.status-repair {
  color:  #dc3545;
  font-weight: 500;
}

.crew-section {
  margin-top:  20px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.crew-section:first-child {
  margin-top: 0;
}

.crew-section h3 {
  margin-top: 0;
  margin-bottom:  15px;
  color:  #333;
  font-size: 18px;
}

.members-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 15px;
}

.member-card {
  padding: 15px;
  background-color: white;
  border-radius: 6px;
  border: 1px solid #dee2e6;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.member-card p {
  margin: 6px 0;
  color:  #555;
  line-height: 1.5;
  font-size: 14px;
}

.member-card strong {
  color: #333;
}

.button {
  display: inline-block;
  padding: 10px 20px;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  text-align: center;
  transition: background-color 0.3s ease;
  white-space: nowrap;
  font-weight:  500;
}

.button.button-primary {
  background-color: #007BFF;
}

.button.button-primary:hover {
  background-color: #0056b3;
}

.button.button-danger {
  background-color: rgb(210, 37, 37);
}

.button.button-danger:hover {
  background-color: rgb(180, 20, 20);
}

.button.button-secondary {
  background-color: #6c757d;
}

.button.button-secondary:hover {
  background-color: #5a6268;
}

.button-small {
  padding: 8px 15px;
  font-size:  13px;
}

.button-full {
  width: 100%;
}

.back-button-container {
  margin-top: 20px;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .header-section {
    flex-direction: column;
    align-items: flex-start;
  }

  .button-group-header {
    width: 100%;
  }

  .button-group-header.button {
    flex: 1;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .members-grid {
    grid-template-columns: 1fr;
  }
}
</style>