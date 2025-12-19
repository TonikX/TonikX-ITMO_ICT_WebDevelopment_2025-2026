<template>
  <div class="routes-list">
    <h1>Список маршрутов</h1>

    <div class="search-route">
      <label for="search">Найти маршрут по ID:</label>
      <input
        class="search-input"
        type="text"
        id="search"
        v-model="searchId"
        placeholder="Введите ID маршрута"
      />
      <button @click="searchRoute" class="button">Найти маршрут</button>
      <button @click="toggleFilters" class="button filter-button">Фильтры</button>
      <button @click="clearSearch" class="button clear-button">Очистить</button>
    </div>

    <div v-if="filteredRoutes.length > 0">
      <div class="route-card" v-for="route in filteredRoutes" :key="route. id">
        <h2>Маршрут №{{ route.id }}</h2>
        <p><strong>Пункт вылета:</strong> {{ route. departure_point }}</p>
        <p><strong>Пункт назначения:</strong> {{ route.destination_point }}</p>
        <p><strong>Расстояние:</strong> {{ route.distance }} км</p>
        <p v-if="route.landing_points"><strong>Пункты посадки:</strong> {{ route. landing_points }}</p>
        <p v-if="route. transit_landings"><strong>Транзитные посадки:</strong> {{ route. transit_landings }}</p>
        <button @click="editRoute(route. id)" class="button">Редактировать</button>
        <button @click="deleteRouteItem(route.id)" class="delete-button">Удалить</button>
        <br />
        <router-link :to="`/route/${route.id}`" class="button">Открыть связанные рейсы</router-link>
      </div>
    </div>
    <p v-else>Маршруты с указанными параметрами не найдены. </p>

    <div v-if="showFilters" class="filters-panel">
      <h2>Фильтры</h2>
      <label>
        Пункт вылета:
        <input type="text" v-model="filters.departurePoint" placeholder="Введите пункт вылета" />
      </label><br/>
      <label>
        Пункт назначения:
        <input type="text" v-model="filters.destinationPoint" placeholder="Введите пункт назначения" />
      </label><br/>
      <label>
        Расстояние от (км):
        <input type="number" v-model="filters.minDistance" placeholder="Минимальное расстояние" />
      </label><br/>
      <label>
        Расстояние до (км):
        <input type="number" v-model="filters.maxDistance" placeholder="Максимальное расстояние" />
      </label><br/>
      <button @click="applyFilters" class="button">Найти</button>
    </div>
  </div>
</template>

<script>
import { getRoutes, deleteRoute } from "../api/index.js";

export default {
  name: "RoutesList",
  data() {
    return {
      routes: [],
      searchId: "",
      filteredRoutes: [],
      showFilters: false,
      filters: {
        departurePoint: "",
        destinationPoint: "",
        minDistance:  null,
        maxDistance: null,
      },
      error: null,
    };
  },
  async created() {
    try {
      const response = await getRoutes();
      this.routes = response.data;
      this.filteredRoutes = this.routes;
    } catch (err) {
      this.error = "Ошибка загрузки маршрутов. ";
      console.error(err);
    }
  },
  methods:  {
    editRoute(id) {
      this.$router.push(`/edit-route/${id}`);
    },
    async deleteRouteItem(id) {
      if (! confirm("Вы уверены, что хотите удалить маршрут?")) {
        return;
      }
      console.log("Del route id:", id);
      try {
        await deleteRoute(id);
        alert("Маршрут успешно удален.");
        this.routes = this.routes.filter(route => route.id !== id);
        this.filteredRoutes = this.filteredRoutes.filter(route => route.id !== id);
      } catch (err) {
        alert("Ошибка удаления маршрута.");
        console.error(err);
      }
    },
    searchRoute() {
      const id = parseInt(this.searchId, 10);
      if (!isNaN(id)) {
        this.filteredRoutes = this.routes.filter(route => route.id === id);
      }
    },
    clearSearch() {
      this.searchId = "";
      this.filters = {
        departurePoint:  "",
        destinationPoint: "",
        minDistance: null,
        maxDistance: null,
      };
      this.filteredRoutes = this.routes;
    },
    toggleFilters() {
      this.showFilters = !this.showFilters;
    },
    applyFilters() {
      this.filteredRoutes = this.routes.filter(route => {
        const matchesDeparturePoint =
          ! this.filters.departurePoint ||
          route.departure_point. toLowerCase().includes(this.filters.departurePoint.toLowerCase());

        const matchesDestinationPoint =
          !this.filters. destinationPoint ||
          route.destination_point.toLowerCase().includes(this.filters.destinationPoint.toLowerCase());

        const matchesMinDistance =
          ! this.filters.minDistance || route.distance >= this.filters.minDistance;

        const matchesMaxDistance =
          !this.filters.maxDistance || route.distance <= this. filters.maxDistance;

        return (
          matchesDeparturePoint &&
          matchesDestinationPoint &&
          matchesMinDistance &&
          matchesMaxDistance
        );
      });
      this.showFilters = false;
    },
  },
};
</script>

<style>
.routes-list {
  margin: 20px;
  font-family: Arial, sans-serif;
}

.route-card {
  border: 1px solid #ddd;
  padding: 15px;
  margin-bottom: 15px;
  background-color: #f9f9f9;
  border-radius: 5px;
}

.search-route {
  margin-bottom: 20px;
}

.search-input {
  margin-right: 10px;
}

.button {
  display: inline-block;
  padding: 10px 15px;
  color: white;
  background-color: #007BFF;
  text-decoration:  none;
  border-radius:  5px;
  margin-right: 10px;
  border: none;
  cursor: pointer;
}

.button:hover {
  background-color: #0056b3;
}

.clear-button {
  background-color: #F5F5F5;
  color: black;
  border: 1px solid #ddd;
}

.clear-button:hover {
  background-color: #E0E0E0;
}

.delete-button {
  background-color: rgb(210, 37, 37);
  color: white;
  border-radius: 5px;
  padding: 10px 15px;
  border: none;
  cursor: pointer;
  margin-left: 10px;
}

.delete-button:hover {
  background-color: rgb(180, 20, 20);
}

.filter-button {
  background-color: #28a745;
}

.filter-button:hover {
  background-color: #218838;
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
  z-index: 1000;
}

.filters-panel h2 {
  margin-top: 0;
}

.filters-panel label {
  display: block;
  margin-bottom: 10px;
  font-weight:  bold;
}

.filters-panel input {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  border: 1px solid #ddd;
  border-radius:  5px;
}

.filters-panel .button {
  width: 100%;
  margin-top: 15px;
}
</style>