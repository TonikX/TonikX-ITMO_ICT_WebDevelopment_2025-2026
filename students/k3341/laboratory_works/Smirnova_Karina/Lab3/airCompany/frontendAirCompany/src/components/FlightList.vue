<template>
  <div class="flight-list">
    <h1>Список рейсов</h1>

    <div class="search-flight">
      <label for="search">Найти рейс по номеру:</label>
      <input
        type="text"
        id="search"
        v-model="searchId"
        placeholder="Введите номер рейса"
      />
      <button @click="searchFlight" class="button">Найти рейс</button>
      <button @click="toggleFilters" class="button filter-button">Фильтры</button>
      <button @click="resetSearch" class="red-button">Очистить</button>
    </div>

    <div v-if="filteredFlights.length > 0">
      <div class="flight-card" v-for="flight in filteredFlights" :key="flight.id">
        <h2>Рейс №{{ flight.flight_number }}</h2>
        <p v-if="flight.route"><strong>Номер маршрута:</strong> {{ flight.route.id }}</p>
        <p v-else><strong>Маршрута не существует</strong></p>
        <p><strong>Маршрут:</strong> {{ flight.departure_point }} → {{ flight.arrival_point }}</p>
        <p><strong>Транзитный:</strong> {{ flight.is_transit ? 'Да' : 'Нет' }}</p>
        <p><strong>Дата вылета:</strong> {{ flight.departure_datetime }}</p>
        <p><strong>Дата прилета:</strong> {{ flight.arrival_datetime }}</p>
        <p><strong>Количество проданных билетов:</strong> {{ flight.sold_tickets }}</p>
        <p v-if="flight.plane"><strong>Номер самолета:</strong> {{ flight.plane.number }}</p>
        <p v-else><strong>Самолета не существует</strong></p>
        <p v-if="flight.crew.length > 0"><strong>Номера команд:</strong>
          <span v-for="crew in flight.crew" :key="crew.id">
            Команда №{{ crew.id }}{{ flight.crew.indexOf(crew) < flight.crew.length - 1 ? ', ' : '' }}
          </span>
        </p>
        <button @click="editFlight(flight.id)" class="button">Редактировать</button>
        <button @click="deleteFlight(flight.id)" class="delete-button">Удалить</button>
        <br />
        <router-link :to="`/flight/${flight.id}`" class="button">Открыть информацию о рейсе</router-link>
      </div>
    </div>
    <p v-else>Нет подходящих рейсов.</p>

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
        <input type="datetime-local" v-model="filters.maxArrivalDatetime" />
      </label><br/>
      <label>
        Количество билетов от:
        <input type="number" v-model="filters.minSoldTickets" placeholder="Минимум проданных билетов" />
      </label><br/>
      <label>
        Количество билетов до:
        <input type="number" v-model="filters.maxSoldTickets" placeholder="Максимум проданных билетов" />
      </label><br/>
      <button @click="applyFilters" class="button">Найти</button>
    </div>
  </div>
</template>

<script>
import { getFlights, deleteFlight } from "../api/index.js";

export default {
  name: "FlightList",
  data() {
    return {
      flights: [],
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
        const matchesRouteId = !this.filters.routeId || (flight.route && flight.route.id === this.filters.routeId);
        const matchesDeparturePoint =
          !this.filters.departurePoint || flight.departure_point.includes(this.filters.departurePoint);
        const matchesArrivalPoint =
          !this.filters.arrivalPoint || flight.arrival_point.includes(this.filters.arrivalPoint);
        const matchesDepartureDatetime =
          (!this.filters.minDepartureDatetime ||
            new Date(flight.departure_datetime) >= new Date(this.filters.minDepartureDatetime)) &&
          (!this.filters.maxDepartureDatetime ||
            new Date(flight.departure_datetime) <= new Date(this.filters.maxDepartureDatetime));
        const matchesArrivalDatetime =
          (!this.filters.minArrivalDatetime ||
            new Date(flight.arrival_datetime) >= new Date(this.filters.minArrivalDatetime)) &&
          (!this.filters.maxArrivalDatetime ||
            new Date(flight.arrival_datetime) <= new Date(this.filters.maxArrivalDatetime));
        const matchesSoldTickets =
          (!this.filters.minSoldTickets || flight.sold_tickets >= this.filters.minSoldTickets) &&
          (!this.filters.maxSoldTickets || flight.sold_tickets <= this.filters.maxSoldTickets);

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

<style>
.flight-list {
  margin: 20px;
}

.flight-card {
  border: 1px solid #ddd;
  padding: 15px;
  margin-bottom: 15px;
  background-color: #f9f9f9;
  border-radius: 5px;
}

.search-flight {
  margin-bottom: 20px;
}

.filters-panel {
  position: fixed;
  top: 0;
  right: 0;
  height: 100%;
  width: 300px;
  background-color: #f1f1f1;
  border-left: 1px solid #ddd;
  padding: 15px;
  box-shadow: -5px 0 10px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
}

.button {
  display: inline-block;
  margin: 10px;
}

.red-button {
  background-color: rgb(210, 37, 37);
  color: white;
  border-radius: 5px;
  padding: 10px 15px;
}

.filter-button {
  margin-left: auto;
}
</style>