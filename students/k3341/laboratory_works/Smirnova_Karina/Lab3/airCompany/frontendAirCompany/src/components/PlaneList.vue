<template>
  <div class="plane-list">
    <div class="content-wrapper">
      <h1>Список самолетов</h1>

      <div class="search-plane">
        <label for="search">Найти самолет по номеру: </label>
        <input
          class="search-input"
          type="text"
          id="search"
          v-model="searchId"
          placeholder="Введите номер самолета"
        />
        <button @click="searchPlane" class="button button-primary">Найти самолет</button>
        <button @click="toggleFilters" class="button button-primary">Фильтры</button>
        <button @click="resetSearch" class="button button-danger">Очистить</button>
      </div>

      <div v-if="filteredPlanes.length > 0" class="planes-container">
        <div class="plane-card" v-for="plane in filteredPlanes" :key="plane.id">
          <h2>Самолет №{{ plane.number }}</h2>
          <p><strong>Тип самолета:</strong> {{ plane.type }}</p>
          <p><strong>Число мест:</strong> {{ plane. seats_capacity }}</p>
          <p><strong>Скорость полета:</strong> {{ plane.flight_speed }} км/ч</p>
          <p><strong>Компания:</strong> {{ plane.airline_company. name }}</p>
          <p><strong>В ремонте:</strong> {{ plane.in_repair ? 'Да' :  'Нет' }}</p>
          <div class="button-group">
            <button @click="editPlane(plane.id)" class="button button-primary">Редактировать</button>
            <button @click="deletePlane(plane. id)" class="button button-danger">Удалить</button>
          </div>
        </div>
      </div>
      <p v-else class="no-data">Нет подходящих самолетов.</p>
    </div>

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
        <input type="number" v-model="filters. maxFlightSpeed" placeholder="Максимальная скорость полета" />
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
      <button @click="applyFilters" class="button button-primary button-full">Найти</button>
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
  methods:  {
    editPlane(id) {
      this.$router. push(`/edit-plane/${id}`);
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
      if (planeNumber) {
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
        minFlightSpeed:  null,
        maxFlightSpeed: null,
        companyName: "",
        inRepair:  null,
      };
      this.filteredPlanes = this. planes;
    },
    toggleFilters() {
      this.showFilters = !this.showFilters;
    },
    applyFilters() {
      this.filteredPlanes = this.planes.filter(plane => {
        const matchesType = ! this.filters.type || plane. type.includes(this.filters. type);
        const matchesSeatsCapacity =
          (!this.filters.minSeatsCapacity || plane.seats_capacity >= this.filters.minSeatsCapacity) &&
          (!this.filters.maxSeatsCapacity || plane.seats_capacity <= this.filters.maxSeatsCapacity);
        const matchesFlightSpeed =
          (!this.filters.minFlightSpeed || plane.flight_speed >= this.filters.minFlightSpeed) &&
          (!this.filters.maxFlightSpeed || plane.flight_speed <= this. filters.maxFlightSpeed);
        const matchesCompany = ! this.filters.companyName || plane.airline_company.name. includes(this.filters.companyName);
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

<style scoped>
.plane-list {
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

.planes-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.plane-card {
  background-color: white;
  border:  1px solid #e0e0e0;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  transition: box-shadow 0.3s ease;
}

.plane-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.plane-card h2 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
  font-size: 20px;
}

.plane-card p {
  margin:  8px 0;
  color:  #555;
  line-height: 1.5;
}

.search-plane {
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

.search-plane label {
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
  cursor:  pointer;
  font-size:  14px;
  text-align:  center;
  transition: background-color 0.3s ease;
  white-space: nowrap;
  font-weight: 500;
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

.button-full {
  width:  100%;
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

.filters-panel input,
.filters-panel select {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
  font-size: 14px;
}

.filters-panel input:focus,
.filters-panel select:focus {
  outline:  none;
  border-color:  #007BFF;
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

  .planes-container {
    grid-template-columns: 1fr;
  }

  .search-plane {
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