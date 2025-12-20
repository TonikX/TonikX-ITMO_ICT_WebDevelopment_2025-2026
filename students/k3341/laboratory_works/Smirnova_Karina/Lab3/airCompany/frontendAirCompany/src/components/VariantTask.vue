<template>
  <div class="variant-task">
    <h1>Задания варианта</h1>

    <!-- Задание 1: Самая популярная марка самолета на маршруте -->
    <div class="task-section">
      <h2>1. Самая популярная марка самолета на маршруте</h2>

      <div class="input-group">
        <label for="route-select-1">Выберите маршрут:</label>
        <select id="route-select-1" v-model="task1.selectedRouteId" @change="fetchMostPopularPlane">
          <option value="" disabled>Выберите маршрут</option>
          <option v-for="route in routes" :value="route.id" :key="route.id">
            Маршрут №{{ route.id }}: {{ route.departure_point }} → {{ route.destination_point }}
          </option>
        </select>
      </div>

      <div v-if="task1.result" class="result-card success">
        <h3>Результат:</h3>
        <p><strong>Маршрут:</strong> {{ getSelectedRoute(task1.selectedRouteId)?.departure_point }} → {{ getSelectedRoute(task1.selectedRouteId)?.destination_point }}</p>
        <p><strong>Самая популярная марка самолета:</strong> {{ task1.result.plane_type }}</p>
        <p><strong>Количество рейсов:</strong> {{ task1.result.flight_count }}</p>
      </div>

      <div v-if="task1.noData" class="result-card warning">
        <p>Для выбранного маршрута нет данных о рейсах.</p>
      </div>

      <div v-if="task1.error" class="result-card error">
        <p>{{ task1.error }}</p>
      </div>
    </div>

    <!-- Задание 2: Маршруты с заполненностью менее XX% -->
    <div class="task-section">
        <h2>2. Маршрут/маршруты, по которым летают рейсы, заполненные менее чем на XX%</h2>

        <div class="input-group">
            <label for="percentage-input">Введите процент заполненности: </label>
            <input
            type="number"
            id="percentage-input"
            v-model.number="task2.percentage"
            placeholder="Например, 50"
            min="0"
            max="100"
            />
            <button @click="fetchRoutesBelowCapacity" class="search-button">Найти</button>
        </div>

        <div v-if="task2.result && task2.result.length > 0" class="result-card success">
            <h3>Найдено маршрутов:   {{ task2.result.length }}</h3>
            <div v-for="route in task2.result" :key="route.route_id" class="route-item">
                <p><strong>Маршрут №{{ route.route_id }}: </strong> {{ route.departure_point }} → {{ route.destination_point }}</p>
                <p><strong>Средняя заполненность:</strong>
                    {{ route.average_occupancy != null ? route.average_occupancy.toFixed(2) + '%' : 'Н/Д' }}
                </p>
            </div>
        </div>

        <div v-if="task2.result && task2.result.length === 0" class="result-card warning">
            <p>Маршруты с заполненностью менее {{ task2.percentage }}% не найдены.</p>
        </div>

        <div v-if="task2.error" class="result-card error">
            <p>{{ task2.error }}</p>
        </div>
    </div>

    <!-- Задание 3: Наличие свободных мест на рейс -->
    <div class="task-section">
      <h2>3. Наличие свободных мест на заданный рейс</h2>

      <div class="input-group">
        <label for="flight-select">Выберите рейс: </label>
        <select id="flight-select" v-model="task3.selectedFlightId" @change="fetchAvailableSeats">
          <option value="" disabled>Выберите рейс</option>
          <option v-for="flight in flights" :value="flight.id" :key="flight.id">
            Рейс №{{ flight.flight_number }}: {{ flight.departure_point }} → {{ flight.arrival_point }}
          </option>
        </select>
      </div>

      <div v-if="task3.result" class="result-card success">
        <h3>Результат: </h3>
        <p><strong>Свободных мест:</strong> {{ task3.result.available_seats }}</p>
      </div>

      <div v-if="task3.error" class="result-card error">
        <p>{{ task3.error }}</p>
      </div>
    </div>

    <!-- Задание 4: Количество самолетов в ремонте -->
    <div class="task-section">
      <h2>4. Количество самолетов, находящихся в ремонте</h2>

      <button @click="fetchPlanesUnderRepair" class="search-button">Получить данные</button>

      <div v-if="task4.result !== null" class="result-card success">
        <h3>Результат:</h3>
        <p><strong>Самолетов в ремонте:</strong> {{ task4.result.planes_under_repair }}</p>
      </div>

      <div v-if="task4.error" class="result-card error">
        <p>{{ task4.error }}</p>
      </div>
    </div>

    <!-- Задание 5: Количество работников компании -->
    <div class="task-section">
      <h2>5. Количество работников компании-авиаперевозчика</h2>

      <div class="input-group">
        <label for="company-select">Выберите компанию:</label>
        <select id="company-select" v-model="task5.selectedCompanyId" @change="fetchTotalEmployees">
          <option value="" disabled>Выберите компанию</option>
          <option v-for="company in companies" :value="company.id" :key="company.id">
            {{ company.name }}
          </option>
        </select>
      </div>

      <div v-if="task5.result" class="result-card success">
        <h3>Результат:</h3>
        <p><strong>Количество работников:</strong> {{ task5.result.total_employees }}</p>
      </div>

      <div v-if="task5.error" class="result-card error">
        <p>{{ task5.error }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { getRoutes, getFlights, getAirlineCompanies } from '@/api';
import axiosInstance from '@/api';

export default {
  name:  'VariantTask',
  data() {
    return {
      routes: [],
      flights: [],
      companies: [],

      // Задание 1
      task1: {
        selectedRouteId: '',
        result: null,
        noData: false,
        error: null,
      },

      // Задание 2
      task2: {
        percentage: null,
        result: null,
        error: null,
      },

      // Задание 3
      task3: {
        selectedFlightId: '',
        result: null,
        error:  null,
      },

      // Задание 4
      task4: {
        result: null,
        error: null,
      },

      // Задание 5
      task5: {
        selectedCompanyId: '',
        result:  null,
        error: null,
      },
    };
  },
  async created() {
    try {
      const [routesResponse, flightsResponse, companiesResponse] = await Promise.all([
        getRoutes(),
        getFlights(),
        getAirlineCompanies(),
      ]);
      this.routes = routesResponse.data;
      this.flights = flightsResponse.data;
      this. companies = companiesResponse.data;
    } catch (err) {
      console.error('Ошибка загрузки данных:', err);
    }
  },
  methods: {
    // Вспомогательные методы для получения объектов
    getSelectedRoute(routeId) {
      return this.routes.find(route => route.id === routeId);
    },
    getSelectedFlight(flightId) {
      return this.flights.find(flight => flight.id === flightId);
    },
    getSelectedCompany(companyId) {
      return this.companies.find(company => company.id === companyId);
    },

    // Задание 1: Самая популярная марка самолета
    async fetchMostPopularPlane() {
      this.task1.result = null;
      this.task1.noData = false;
      this.task1.error = null;

      if (!this.task1.selectedRouteId) return;

      try {
        const response = await axiosInstance.get(`/api/most_popular_plane_type/${this.task1.selectedRouteId}/`);
        this.task1.result = response.data;
      } catch (err) {
        console.error('Ошибка получения данных:', err);
        if (err.response && err.response.status === 404) {
          this.task1.noData = true;
        } else {
          this.task1.error = 'Произошла ошибка при получении данных. ';
        }
      }
    },

    // Задание 2: Маршруты с заполненностью менее XX%
    async fetchRoutesBelowCapacity() {
      this.task2.result = null;
      this.task2.error = null;

      if (!this.task2.percentage && this.task2.percentage !== 0) {
        this.task2.error = 'Введите процент заполненности. ';
        return;
      }

      try {
        console.log('Запрос на получение маршрутов с заполненностью менее', this.task2.percentage, '%');
        const response = await axiosInstance.get(`/api/routes_below_capacity/${this.task2.percentage}/`);
        console.log('Ответ сервера:', response.data);
        if (response.data && response.data.under_capacity_routes) {
            this.task2.result = response.data.under_capacity_routes;
        } else {
            this.task2.result = [];
        }
      } catch (err) {
        console.error('Ошибка получения данных:', err);
        this.task2.error = 'Произошла ошибка при получении данных.';
      }
    },

    // Задание 3: Наличие свободных мест на рейс
    async fetchAvailableSeats() {
      this.task3.result = null;
      this.task3.error = null;

      if (!this.task3.selectedFlightId) return;

      try {
        const response = await axiosInstance.get(`/api/available_seats/${this.task3.selectedFlightId}/`);
        this.task3.result = response.data;
      } catch (err) {
        console.error('Ошибка получения данных:', err);
        this.task3.error = 'Произошла ошибка при получении данных. ';
      }
    },

    // Задание 4: Количество самолетов в ремонте
    async fetchPlanesUnderRepair() {
      this.task4.result = null;
      this. task4.error = null;

      try {
        const response = await axiosInstance.get('/api/planes_under_repair/');
        this.task4.result = response.data;
      } catch (err) {
        console.error('Ошибка получения данных:', err);
        this.task4.error = 'Произошла ошибка при получении данных.';
      }
    },

    // Задание 5: Количество работников компании
    async fetchTotalEmployees() {
      this.task5.result = null;
      this.task5.error = null;

      if (!this.task5.selectedCompanyId) return;

      try {
        const response = await axiosInstance.get(`/api/total_employees/${this.task5.selectedCompanyId}/`);
        this.task5.result = response.data;
      } catch (err) {
        console.error('Ошибка получения данных:', err);
        this.task5.error = 'Произошла ошибка при получении данных. ';
      }
    },
  },
};
</script>

<style scoped>
. variant-task {
  margin:  20px;
  font-family: Arial, sans-serif;
  max-width: 1200px;
}

h1 {
  font-size:  32px;
  margin-bottom: 30px;
  color: #0f4c81;
  text-align: center;
}

.task-section {
  background-color: #f9f9f9;
  border:  1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  margin-bottom:  30px;
}

h2 {
  font-size: 22px;
  margin-bottom:  10px;
  color: #0f4c81;
}

.task-description {
  color: #666;
  margin-bottom: 15px;
  font-style: italic;
}

.input-group {
  margin-bottom: 20px;
}

. input-group label {
  display: block;
  margin-bottom: 8px;
  font-weight:  bold;
  font-size: 16px;
}

.input-group select,
.input-group input {
  width: 100%;
  max-width: 500px;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
  margin-bottom: 10px;
}

.search-button {
  padding: 10px 20px;
  font-size: 16px;
  color: white;
  background-color: #0f4c81;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.search-button:hover {
  background-color: #083a5e;
}

.result-card {
  padding: 20px;
  border-radius: 5px;
  margin-top: 15px;
}

.result-card h3 {
  margin-top: 0;
  margin-bottom: 15px;
}

.result-card p {
  margin:  8px 0;
  font-size: 16px;
}

.result-card.success {
  background-color: #e8f5e9;
  border-left: 4px solid #4caf50;
}

. result-card.warning {
  background-color: #fff3cd;
  border-left: 4px solid #ffc107;
  color: #856404;
}

.result-card.error {
  background-color: #f8d7da;
  border-left: 4px solid #dc3545;
  color: #721c24;
}

.route-item {
  background-color: white;
  padding: 10px;
  margin:  10px 0;
  border-radius: 5px;
  border: 1px solid #ddd;
}

.route-item p {
  margin: 5px 0;
}
</style>