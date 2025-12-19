<template>
  <div class="company-list">
    <h1>Список компаний</h1>

    <div class="search-company">
      <label for="search">Найти компанию по названию:</label>
      <input
        type="text"
        id="search"
        v-model="searchName"
        placeholder="Введите название компании"
      />
      <button @click="searchCompany" class="button">Найти компанию</button>
      <button @click="toggleFilters" class="button filter-button">Фильтры</button>
      <button @click="resetSearch" class="red-button">Очистить</button>
    </div>

    <div v-if="filteredCompanies.length > 0">
      <div class="company-card" v-for="company in filteredCompanies" :key="company.id">
        <h2>
          Компания: {{ company.name }}
          <button @click="editCompany(company. id)" class="edit-button">Редактировать</button>
          <button @click="deleteCompanyItem(company.id)" class="delete-button">Удалить</button>
        </h2>
        <div class="section">
          <h3>Самолёты: </h3>
          <div v-if="company.planes && company.planes.length > 0">
            <div class="plane-card" v-for="plane in company.planes" :key="plane.id">
              <p><strong>Номер:</strong> {{ plane.number }}</p>
              <p><strong>Тип:</strong> {{ plane.type }}</p>
              <p><strong>Число мест:</strong> {{ plane.seats_capacity }}</p>
              <p><strong>Скорость:</strong> {{ plane.flight_speed }} км/ч</p>
              <p><strong>В ремонте:</strong> {{ plane. in_repair ? 'Да' : 'Нет' }}</p>
            </div>
          </div>
          <p v-else>Нет самолётов</p>
        </div>
        <div v-if="company.crew_members && company.crew_members. length > 0" class="section">
          <h3>Работники:</h3>
          <div class="employee-card" v-for="member in company.crew_members" :key="member.id">
            <p><strong>ФИО:</strong> {{ member.full_name }}</p>
            <p><strong>Возраст:</strong> {{ member. age }}</p>
            <p><strong>Образование:</strong> {{ member.education }}</p>
            <p><strong>Стаж:</strong> {{ member. work_experience }} лет</p>
            <p><strong>Допуск к рейсу:</strong> {{ member. flight_authorization ?  'Да' : 'Нет' }}</p>
            <p><strong>Должность:</strong> {{ member.position }}</p>
          </div>
        </div>
        <div v-else class="section">
          <h3>Работники:</h3>
          <p>Нет работников</p>
        </div>
      </div>
    </div>
    <p v-else>Нет подходящих компаний. </p>

    <div v-if="showFilters" class="filters-panel">
      <h2>Фильтры</h2>
      <label>
        Номер самолета:
        <input type="text" v-model="filters.planeNumber" placeholder="Введите номер самолета" />
      </label><br/>
      <label>
        ФИО работника:
        <input type="text" v-model="filters.employeeName" placeholder="Введите ФИО работника" />
      </label><br/>
      <button @click="applyFilters" class="button">Найти</button>
    </div>
  </div>
</template>

<script>
import { getAirlineCompanies, deleteCompany } from '../api/index.js';

export default {
  name: 'AirlineCompanyList',
  data() {
    return {
      companies: [],
      searchName: "",
      filteredCompanies: [],
      showFilters: false,
      filters: {
        planeNumber: "",
        employeeName: "",
      },
      error: null,
    };
  },
  async created() {
    try {
      const response = await getAirlineCompanies();
      this.companies = response.data;
      this. filteredCompanies = this. companies;
    } catch (err) {
      this.error = 'Ошибка загрузки информации о компаниях. ';
      console.error(err);
    }
  },
  methods:  {
    editCompany(id) {
      this.$router.push(`/edit-company/${id}`);
    },
    async deleteCompanyItem(id) {
      if (! confirm("Вы уверены, что хотите удалить компанию?")) {
        return;
      }
      try {
        await deleteCompany(id);
        alert("Компания успешно удалена.");
        this.companies = this.companies.filter(company => company.id !== id);
        this.filteredCompanies = this.filteredCompanies.filter(company => company.id !== id);
      } catch (err) {
        alert("Ошибка удаления компании.");
        console.error(err);
      }
    },
    searchCompany() {
      if (this.searchName. trim()) {
        this.filteredCompanies = this.companies.filter(company =>
          company.name.toLowerCase().includes(this.searchName.toLowerCase())
        );
      }
    },
    resetSearch() {
      this.searchName = "";
      this.filters = {
        planeNumber:  "",
        employeeName: "",
      };
      this.filteredCompanies = this.companies;
    },
    toggleFilters() {
      this.showFilters = !this.showFilters;
    },
    applyFilters() {
      this.filteredCompanies = this.companies.filter(company => {
        const matchesPlaneNumber =
          ! this.filters.planeNumber ||
          (company.planes && company.planes. some(plane =>
            plane.number. toLowerCase().includes(this.filters.planeNumber.toLowerCase())
          ));

        const matchesEmployeeName =
          !this.filters.employeeName ||
          (company. crew_members && company.crew_members.some(member =>
            member.full_name.toLowerCase().includes(this.filters.employeeName.toLowerCase())
          ));

        return matchesPlaneNumber && matchesEmployeeName;
      });
      this.showFilters = false;
    },
  }
};
</script>

<style>
.company-list {
  margin: 20px;
  font-family: Arial, sans-serif;
}

.company-card {
  border: 1px solid #ddd;
  margin-bottom: 15px;
  background-color: #e3f2fd;
  padding: 15px;
  border-radius: 5px;
}

.section {
  margin-top: 10px;
  padding: 10px;
  background-color: #bbdefb;
  border-radius: 5px;
}

.plane-card,
.employee-card {
  margin:  10px 0;
  padding:  10px;
  background-color: #e1f5fe;
  border-radius: 5px;
}

h1 {
  font-size: 24px;
  margin-bottom: 20px;
}

h2 {
  font-size: 20px;
  margin-bottom:  10px;
}

h3 {
  font-size: 18px;
  margin-bottom: 10px;
}

.search-company {
  margin-bottom:  20px;
}

. button {
  display: inline-block;
  padding: 10px 15px;
  color: white;
  background-color: #007BFF;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-right: 10px;
}

.button:hover {
  background-color: #0056b3;
}

.edit-button {
  margin-left: 10px;
  padding: 5px 10px;
  font-size: 14px;
  color: white;
  background-color: #007BFF;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

. edit-button:hover {
  background-color: #0056b3;
}

.delete-button {
  margin-left: 10px;
  padding: 5px 10px;
  font-size: 14px;
  color: white;
  background-color: rgb(210, 37, 37);
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.delete-button:hover {
  background-color: rgb(180, 20, 20);
}

.red-button {
  background-color: rgb(210, 37, 37);
  color: white;
  border-radius: 5px;
  padding: 10px 15px;
  border: none;
  cursor: pointer;
}

.red-button:hover {
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
  font-weight: bold;
}

.filters-panel input {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  border: 1px solid #ddd;
  border-radius:  5px;
}

.filters-panel . button {
  width: 100%;
  margin-top: 15px;
}
</style>