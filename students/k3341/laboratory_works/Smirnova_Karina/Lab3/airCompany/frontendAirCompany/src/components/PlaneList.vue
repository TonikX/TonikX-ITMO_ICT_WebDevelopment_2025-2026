<template>
  <div class="plane-list">
    <h1>Список самолетов</h1>

    <div class="search-plane">
      <label for="search">Найти самолет по номеру:</label>
      <input
        type="text"
        id="search"
        v-model="searchId"
        placeholder="Введите номер самолета"
      />
      <button @click="searchPlane" class="button">Найти самолет</button>
      <button @click="toggleFilters" class="button filter-button">Фильтры</button>
      <button @click="resetSearch" class="red-button">Очистить</button>
    </div>

    <div v-if="filteredPlanes.length > 0">
      <div class="plane-card" v-for="plane in filteredPlanes" :key="plane.id">
        <h2>Самолет №{{ plane.number }}</h2>
        <p><strong>Тип самолета:</strong> {{ plane.type }}</p>
        <p><strong>Число мест:</strong> {{ plane.seats_capacity }}</p>
        <p><strong>Скорость полета:</strong> {{ plane.flight_speed }} км/ч</p>
        <p><strong>Компания:</strong> {{ plane.airline_company.name }}</p>
        <p><strong>В ремонте:</strong> {{ plane.in_repair ? 'Да' : 'Нет' }}</p>
        <button @click="editPlane(plane.id)" class="button">Редактировать</button>
        <button @click="deletePlane(plane.id)" class="delete-button">Удалить</button>
      </div>
    </div>
    <p v-else>Нет подходящих самолетов.</p>

    <div v-if="showFilters" class="filters-panel">
      <h2>Фильтры самолетов</h2>
      <label>
        Тип самолета:
        <input type="text" v-model="filters.type" placeholder="Введите тип самолета" />
      </label><br/>
      <label>
        Число мест от:
        <input type="number" v-model="filters.minSeatsCapacity" placeholder="Минимальное число мест" />
      </label><br/>
      <label>
        Число мест до:
        <input type="number" v-model="filters.maxSeatsCapacity" placeholder="Максимальное число мест" />
      </label><br/>
      <label>
        Скорость полета от (км/ч):
        <input type="number" v-model="filters.minFlightSpeed" placeholder="Минимальная скорость полета" />
      </label><br/>
      <label>
        Скорость полета до (км/ч):
        <input type="number" v-model="filters.maxFlightSpeed" placeholder="Максимальная скорость полета" />
      </label><br/>
      <label>
        Компания:
        <input type="text" v-model="filters.companyName" placeholder="Введите название компании" />
      </label><br/>
      <label>
        В ремонте:
        <select v-model="filters.inRepair">
          <option :value="null">Неважно</option>
          <option :value="true">Да</option>
          <option :value="false">Нет</option>
        </select>
      </label><br/>
      <button @click="applyFilters" class="button">Найти</button>
    </div>
  </div>
</template>

<script>
import { getPlanes, deletePlane } from "../api/index.js";

export default {
  name: "PlaneList",
  data() {
    return {
      planes: [],
      searchId: "",
      filteredPlanes: [],
      showFilters: false,
      filters: {
        type: "",
        minSeatsCapacity: null,
        maxSeatsCapacity: null,
        minFlightSpeed: null,
        maxFlightSpeed: null,
        companyName: "",
        inRepair: null,
      },
      error: null,
    };
  },
  async created() {
    try {
      const response = await getPlanes();
      this.planes = response.data;
      this.filteredPlanes = this.planes;
    } catch (err) {
      this.error = "Ошибка загрузки данных самолетов.";
      console.error(err);
    }
  },
  methods: {
    editPlane(id) {
      this.$router.push(`/edit-plane/${id}`);
    },
    async deletePlane(id) {
      if (!confirm("Вы уверены, что хотите удалить самолет?")) {
        return;
      }
      try {
        await deletePlane(id);
        alert("Самолет успешно удален.");
        this.planes = this.planes.filter(plane => plane.id !== id);
        this.filteredPlanes = this.filteredPlanes.filter(plane => plane.id !== id);
      } catch (err) {
        alert("Ошибка удаления самолета.");
        console.error(err);
      }
    },
    searchPlane() {
      const planeNumber = this.searchId.trim();
      console.log("planeNumber: ", planeNumber)
      if (!isNaN(planeNumber)) {
        this.filteredPlanes = this.planes.filter(plane => plane.number === planeNumber);
      }
      console.log("filteredPlanes:", this.filteredPlanes)
    },
    resetSearch() {
      this.searchId = "";
      this.filters = {
        type: "",
        minSeatsCapacity: null,
        maxSeatsCapacity: null,
        minFlightSpeed: null,
        maxFlightSpeed: null,
        companyName: "",
        inRepair: null,
      };
      this.filteredPlanes = this.planes;
    },
    toggleFilters() {
      this.showFilters = !this.showFilters;
    },
    applyFilters() {
      this.filteredPlanes = this.planes.filter(plane => {
        const matchesType = !this.filters.type || plane.type.includes(this.filters.type);
        const matchesSeatsCapacity =
          (!this.filters.minSeatsCapacity || plane.seats_capacity >= this.filters.minSeatsCapacity) &&
          (!this.filters.maxSeatsCapacity || plane.seats_capacity <= this.filters.maxSeatsCapacity);
        const matchesFlightSpeed =
          (!this.filters.minFlightSpeed || plane.flight_speed >= this.filters.minFlightSpeed) &&
          (!this.filters.maxFlightSpeed || plane.flight_speed <= this.filters.maxFlightSpeed);
        const matchesCompany = !this.filters.companyName || plane.airline_company.name.includes(this.filters.companyName);
        const matchesInRepair =
          this.filters.inRepair === null || plane.in_repair === this.filters.inRepair;

        return (
          matchesType &&
          matchesSeatsCapacity &&
          matchesFlightSpeed &&
          matchesCompany &&
          matchesInRepair
        );
      });
      this.showFilters = false;
    },
  },
};
</script>

<style>
.plane-list {
  margin: 20px;
}

.plane-card {
  border: 1px solid #ddd;
  padding: 15px;
  margin-bottom: 15px;
  background-color: #e3f2fd;
  border-radius: 5px;
}

.search-plane {
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
  margin-top: 10px;
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