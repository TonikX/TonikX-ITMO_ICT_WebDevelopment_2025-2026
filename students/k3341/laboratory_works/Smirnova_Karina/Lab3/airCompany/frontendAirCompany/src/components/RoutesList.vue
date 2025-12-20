<template>
  <div class="routes-list">
    <div class="content-wrapper">
      <h1>Список маршрутов</h1>

      <div class="search-route">
        <label for="search">Найти маршрут по ID: </label>
        <input
          class="search-input"
          type="text"
          id="search"
          v-model="searchId"
          placeholder="Введите ID маршрута"
        />
        <button @click="searchRoute" class="button button-primary">Найти маршрут</button>
        <button @click="toggleFilters" class="button button-primary">Фильтры</button>
        <button @click="clearSearch" class="button button-danger">Очистить</button>
      </div>

      <div v-if="filteredRoutes.length > 0" class="routes-container">
        <div class="route-card" v-for="route in filteredRoutes" :key="route.id">
          <h2>Маршрут №{{ route. id }}</h2>
          <p><strong>Пункт вылета:</strong> {{ route.departure_point }}</p>
          <p><strong>Пункт назначения:</strong> {{ route.destination_point }}</p>
          <p><strong>Расстояние:</strong> {{ route.distance }} км</p>
          <p v-if="route.landing_points"><strong>Пункты посадки:</strong> {{ route.landing_points }}</p>
          <p v-if="route.transit_landings"><strong>Транзитные посадки:</strong> {{ route.transit_landings }}</p>
          <div class="button-group">
            <button @click="editRoute(route. id)" class="button button-primary">Редактировать</button>
            <button @click="deleteRouteItem(route.id)" class="button button-danger">Удалить</button>
          </div>
          <router-link :to="`/route/${route.id}`" class="button button-primary button-full">Открыть связанные рейсы</router-link>
        </div>
      </div>
      <p v-else>Маршруты с указанными параметрами не найдены.</p>
    </div>

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
        <input type="number" v-model="filters. minDistance" placeholder="Минимальное расстояние" />
      </label><br/>
      <label>
        Расстояние до (км):
        <input type="number" v-model="filters.maxDistance" placeholder="Максимальное расстояние" />
      </label><br/>
      <button @click="applyFilters" class="button button-primary button-full">Найти</button>
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
        departurePoint:  "",
        destinationPoint: "",
        minDistance: null,
        maxDistance: null,
      },
      error: null,
    };
  },
  async created() {
    try {
      const response = await getRoutes();
      this.routes = response.data;
      this. filteredRoutes = this.routes;
    } catch (err) {
      this.error = "Ошибка загрузки маршрутов. ";
      console.error(err);
    }
  },
  methods: {
    editRoute(id) {
      this.$router.push(`/edit-route/${id}`);
    },
    async deleteRouteItem(id) {
      if (!confirm("Вы уверены, что хотите удалить маршрут?")) {
        return;
      }
      console. log("Del route id:", id);
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
          route.departure_point. toLowerCase().includes(this.filters. departurePoint.toLowerCase());

        const matchesDestinationPoint =
          !this.filters.destinationPoint ||
          route.destination_point.toLowerCase().includes(this.filters.destinationPoint.toLowerCase());

        const matchesMinDistance =
          !this.filters. minDistance || route.distance >= this.filters.minDistance;

        const matchesMaxDistance =
          !this.filters.maxDistance || route.distance <= this.filters. maxDistance;

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

.routes-container {
  display: grid;
  grid-template-columns:  repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top:  20px;
}

.route-card {
  background-color: white;
  border:  1px solid #e0e0e0;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  transition: box-shadow 0.3s ease;
}

.route-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.route-card h2 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
  font-size: 20px;
}

.route-card p {
  margin:  8px 0;
  color:  #555;
  line-height: 1.5;
}

.search-route {
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

.search-route label {
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

.search-input: focus {
  outline: none;
  border-color: #007BFF;
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
  font-weight: 500;
}

.button-primary {
  background-color: #007BFF;
}

.button-primary:hover {
  background-color: #0056b3;
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
  box-shadow: -5px 0 15px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  z-index: 1000;
}

.filters-panel h2 {
  margin-top:  0;
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

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .routes-container {
    grid-template-columns: 1fr;
  }

  .search-route {
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