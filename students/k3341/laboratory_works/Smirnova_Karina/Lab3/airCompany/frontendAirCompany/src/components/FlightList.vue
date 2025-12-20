<template>
  <div class="flight-list">
    <div class="content-wrapper">
      <h1>Список рейсов</h1>

      <div class="search-flight">
        <label for="search">Найти рейс по номеру: </label>
        <input
          class="search-input"
          type="text"
          id="search"
          v-model="searchId"
          placeholder="Введите номер рейса"
        />
        <button @click="searchFlight" class="button button-primary">Найти рейс</button>
        <button @click="toggleFilters" class="button button-primary">Фильтры</button>
        <button @click="resetSearch" class="button button-danger">Очистить</button>
      </div>

      <div v-if="filteredFlights.length > 0" class="flights-container">
        <div class="flight-card" v-for="flight in filteredFlights" :key="flight.id">
          <h2>Рейс №{{ flight.flight_number }}</h2>
          <p v-if="flight.route"><strong>Номер маршрута:</strong> {{ flight.route.id }}</p>
          <p v-else><strong>Маршрута не существует</strong></p>
          <p><strong>Маршрут:</strong> {{ flight.departure_point }} → {{ flight.arrival_point }}</p>
          <p><strong>Транзитный:</strong> {{ flight.is_transit ? 'Да' :  'Нет' }}</p>
          <p><strong>Дата вылета:</strong> {{ flight.departure_datetime }}</p>
          <p><strong>Дата прилета: </strong> {{ flight.arrival_datetime }}</p>
          <p><strong>Количество проданных билетов:</strong> {{ flight.sold_tickets }}</p>
          <p v-if="flight.plane"><strong>Номер самолета:</strong> {{ flight.plane.number }}</p>
          <p v-else><strong>Самолета не существует</strong></p>
          <p v-if="flight.crew.length > 0"><strong>Номера команд:</strong>
            <span v-for="crew in flight.crew" :key="crew.id">
              Команда №{{ crew.id }}{{ flight.crew.indexOf(crew) < flight.crew.length - 1 ? ', ' : '' }}
            </span>
          </p>
          <div class="button-group">
            <button @click="editFlight(flight.id)" class="button button-primary">Редактировать</button>
            <button @click="deleteFlight(flight. id)" class="button button-danger">Удалить</button>
          </div>
          <router-link :to="`/flight/${flight.id}`" class="button button-primary button-full">
            Открыть информацию о рейсе
          </router-link>
        </div>
      </div>
      <p v-else class="no-data">Нет подходящих рейсов.</p>
    </div>

    <div v-if="showFilters" class="filters-panel">
      <h2>Фильтр</h2>
      <label>
        Номер маршрута:
        <input type="number" v-model="filters.routeId" placeholder="Введите номер маршрута" />
      </label><br/>
      <label>
        Пункт вылета:
        <input type="text" v-model="filters.departurePoint" placeholder="Введите пункт вылета" />
      </label><br/>
      <label>
        Пункт прилета:
        <input type="text" v-model="filters.arrivalPoint" placeholder="Введите пункт прилета" />
      </label><br/>
      <label>
        Дата вылета от:
        <input type="datetime-local" v-model="filters.minDepartureDatetime" />
      </label><br/>
      <label>
        Дата вылета до:
        <input type="datetime-local" v-model="filters.maxDepartureDatetime" />
      </label><br/>
      <label>
        Дата прилета от:
        <input type="datetime-local" v-model="filters.minArrivalDatetime" />
      </label><br/>
      <label>
        Дата прилета до:
        <input type="datetime-local" v-model="filters. maxArrivalDatetime" />
      </label><br/>
      <label>
        Количество билетов от:
        <input type="number" v-model="filters.minSoldTickets" placeholder="Минимум проданных билетов" />
      </label><br/>
      <label>
        Количество билетов до:
        <input type="number" v-model="filters.maxSoldTickets" placeholder="Максимум проданных билетов" />
      </label><br/>
      <button @click="applyFilters" class="button button-primary button-full">Найти</button>
    </div>
  </div>
</template>

<script>
import { getFlights, deleteFlight } from "../api/index.js";

export default {
  name: "FlightList",
  data() {
    return {
      flights:  [],
      searchId: "",
      filteredFlights: [],
      showFilters: false,
      filters: {
        routeId: null,
        departurePoint: "",
        arrivalPoint: "",
        minDepartureDatetime: "",
        maxDepartureDatetime: "",
        minArrivalDatetime: "",
        maxArrivalDatetime: "",
        minSoldTickets: null,
        maxSoldTickets: null,
      },
      error: null,
    };
  },
  async created() {
    try {
      const response = await getFlights();
      this.flights = response.data;
      this.filteredFlights = this.flights;
    } catch (err) {
      this.error = "Ошибка загрузки данных рейсов.";
      console.error(err);
    }
  },
  methods: {
    editFlight(id) {
      this.$router.push(`/edit-flight/${id}`);
    },
    async deleteFlight(id) {
      if (!confirm("Вы уверены, что хотите удалить рейс?")) {
        return;
      }
      try {
        await deleteFlight(id);
        alert("Рейс успешно удален.");
        this.flights = this.flights.filter(flight => flight.id !== id);
        this.filteredFlights = this.filteredFlights.filter(flight => flight.id !== id);
      } catch (err) {
        alert("Ошибка удаления рейса.");
        console.error(err);
      }
    },
    searchFlight() {
      const flight_number = parseInt(this.searchId, 10);
      if (!isNaN(flight_number)) {
        this.filteredFlights = this.flights.filter(flight => flight.flight_number === flight_number);
      }
    },
    resetSearch() {
      this.searchId = "";
      this.filters = {
        routeId: null,
        departurePoint: "",
        arrivalPoint: "",
        minDepartureDatetime: "",
        maxDepartureDatetime: "",
        minArrivalDatetime: "",
        maxArrivalDatetime: "",
        minSoldTickets: null,
        maxSoldTickets: null,
      };
      this.filteredFlights = this.flights;
    },
    toggleFilters() {
      this.showFilters = !this.showFilters;
    },
    applyFilters() {
      this.filteredFlights = this.flights.filter(flight => {
        const matchesRouteId = !this. filters.routeId || (flight.route && flight.route.id === this.filters.routeId);
        const matchesDeparturePoint =
          !this. filters.departurePoint || flight. departure_point.includes(this. filters.departurePoint);
        const matchesArrivalPoint =
          !this.filters.arrivalPoint || flight.arrival_point.includes(this.filters.arrivalPoint);
        const matchesDepartureDatetime =
          (!this.filters.minDepartureDatetime ||
            new Date(flight.departure_datetime) >= new Date(this.filters.minDepartureDatetime)) &&
          (!this.filters.maxDepartureDatetime ||
            new Date(flight.departure_datetime) <= new Date(this.filters. maxDepartureDatetime));
        const matchesArrivalDatetime =
          (!this.filters.minArrivalDatetime ||
            new Date(flight.arrival_datetime) >= new Date(this.filters.minArrivalDatetime)) &&
          (!this. filters.maxArrivalDatetime ||
            new Date(flight. arrival_datetime) <= new Date(this.filters.maxArrivalDatetime));
        const matchesSoldTickets =
          (! this.filters.minSoldTickets || flight.sold_tickets >= this.filters.minSoldTickets) &&
          (!this. filters.maxSoldTickets || flight.sold_tickets <= this. filters.maxSoldTickets);

        return (
          matchesRouteId &&
          matchesDeparturePoint &&
          matchesArrivalPoint &&
          matchesDepartureDatetime &&
          matchesArrivalDatetime &&
          matchesSoldTickets
        );
      });
      this.showFilters = false;
    },
  },
};
</script>

<style scoped>
.flight-list {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 20px 0;
}

.content-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 30px;
}

.flights-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.flight-card {
  background-color: white;
  border: 1px solid #e0e0e0;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  transition: box-shadow 0.3s ease;
}

.flight-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.flight-card h2 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
  font-size: 20px;
}

.flight-card p {
  margin: 8px 0;
  color:  #555;
  line-height: 1.5;
}

.search-flight {
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  background-color: white;
  padding: 20px;
  border-radius:  8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-flight label {
  margin-right: 10px;
  font-weight: 500;
  color: #333;
}

.search-input {
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  min-width: 200px;
  font-size: 14px;
}

.search-input:focus {
  outline:  none;
  border-color:  #007BFF;
}

.button {
  display: inline-block;
  padding:  10px 20px;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  text-align: center;
  transition: background-color 0.3s ease;
  white-space: nowrap;
  font-weight: 500;
}

.button.button-primary {
  background-color: #007BFF;
}

.button.button-primary:hover {
  background-color:  #0056b3;
}

.button.button-danger {
  background-color: rgb(210, 37, 37);
}

.button.button-danger:hover {
  background-color: rgb(180, 20, 20);
}

.button-full {
  width: 100%;
  margin-top: 10px;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.button-group.button {
  flex: 1;
}

.filters-panel {
  position: fixed;
  top: 0;
  right: 0;
  height: 100%;
  width: 300px;
  background-color: white;
  border-left: 1px solid #ddd;
  padding: 20px;
  box-shadow:  -5px 0 15px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  z-index: 1000;
}

.filters-panel h2 {
  margin-top: 0;
  color: #333;
}

.filters-panel label {
  display: block;
  margin-bottom: 15px;
  font-weight:  500;
  color: #333;
}

.filters-panel input {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
  font-size: 14px;
}

.filters-panel input:focus {
  outline: none;
  border-color: #007BFF;
}

.filters-panel.button {
  margin-top: 20px;
}

.no-data {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  color: #666;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .flights-container {
    grid-template-columns: 1fr;
  }

  .search-flight {
    flex-direction: column;
    align-items: stretch;
  }

  .search-input {
    width: 100%;
  }

  .button {
    width: 100%;
  }
}
</style>