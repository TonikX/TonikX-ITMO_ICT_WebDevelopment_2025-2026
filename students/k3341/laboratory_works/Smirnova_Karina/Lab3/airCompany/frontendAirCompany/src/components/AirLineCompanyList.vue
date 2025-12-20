<template>
  <div class="company-list">
    <div class="content-wrapper">
      <h1>Список компаний</h1>

      <div class="search-company">
        <label for="search">Найти компанию по названию:</label>
        <input
          class="search-input"
          type="text"
          id="search"
          v-model="searchName"
          placeholder="Введите название компании"
        />
        <button @click="searchCompany" class="button button-primary">Найти компанию</button>
        <button @click="toggleFilters" class="button button-primary">Фильтры</button>
        <button @click="resetSearch" class="button button-danger">Очистить</button>
      </div>

      <div v-if="filteredCompanies.length > 0" class="companies-container">
        <div class="company-card" v-for="company in filteredCompanies" :key="company.id">
          <div class="company-header">
            <h2>{{ company.name }}</h2>
            <div class="button-group-header">
              <button @click="editCompany(company.id)" class="button button-primary button-small">Редактировать</button>
              <button @click="deleteCompanyItem(company.id)" class="button button-danger button-small">Удалить</button>
            </div>
          </div>

          <div class="section">
            <h3>Самолёты</h3>
            <div v-if="company.planes && company.planes.length > 0" class="items-grid">
              <div class="plane-card" v-for="plane in company.planes" :key="plane.id">
                <p><strong>Номер:</strong> {{ plane.number }}</p>
                <p><strong>Тип:</strong> {{ plane.type }}</p>
                <p><strong>Число мест:</strong> {{ plane. seats_capacity }}</p>
                <p><strong>Скорость:</strong> {{ plane. flight_speed }} км/ч</p>
                <p><strong>В ремонте:</strong> {{ plane. in_repair ? 'Да' : 'Нет' }}</p>
                <div class="button-group">
                  <button @click="editPlane(plane.id)" class="button button-primary button-small">Редактировать</button>
                  <button @click="deletePlane(plane.id)" class="button button-danger button-small">Удалить</button>
                </div>
              </div>
            </div>
            <p v-else class="no-data-small">Нет самолётов</p>
          </div>

          <div class="section">
            <h3>Работники</h3>
            <div v-if="company.crew_members && company.crew_members. length > 0" class="items-grid">
              <div class="employee-card" v-for="member in company.crew_members" :key="member.id">
                <p><strong>ФИО:</strong> {{ member.full_name }}</p>
                <p><strong>Возраст:</strong> {{ member.age }}</p>
                <p><strong>Образование:</strong> {{ member.education }}</p>
                <p><strong>Стаж:</strong> {{ member.work_experience }} лет</p>
                <p><strong>Допуск к рейсу:</strong> {{ member.flight_authorization ?  'Да' : 'Нет' }}</p>
                <p><strong>Должность:</strong> {{ member.position }}</p>
                <div class="button-group">
                  <button @click="editMember(member.id)" class="button button-primary button-small">Редактировать</button>
                  <button @click="deleteMember(member.id)" class="button button-danger button-small">Удалить</button>
                </div>
              </div>
            </div>
            <p v-else class="no-data-small">Нет работников</p>
          </div>
        </div>
      </div>
      <p v-else class="no-data">Нет подходящих компаний. </p>
    </div>

    <div v-if="showFilters" class="filters-panel">
      <h2>Фильтры</h2>
      <label>
        Номер самолета:
        <input type="text" v-model="filters.planeNumber" placeholder="Введите номер самолета" />
      </label><br/>
      <label>
        ФИО работника:
        <input type="text" v-model="filters. employeeName" placeholder="Введите ФИО работника" />
      </label><br/>
      <button @click="applyFilters" class="button button-primary button-full">Найти</button>
    </div>
  </div>
</template>

<script>
import { getAirlineCompanies, deleteCompany, deletePlane, deleteCrewMember } from '../api/index.js';

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
        employeeName:  "",
      },
      error: null,
    };
  },
  async created() {
    await this.loadCompanies();
  },
  methods: {
    async loadCompanies() {
      try {
        const response = await getAirlineCompanies();
        this.companies = response.data;
        this. filteredCompanies = this. companies;
      } catch (err) {
        this.error = 'Ошибка загрузки информации о компаниях.';
        console.error(err);
      }
    },
    editCompany(id) {
      this.$router.push(`/edit-company/${id}`);
    },
    async deleteCompanyItem(id) {
      if (!confirm("Вы уверены, что хотите удалить компанию?")) {
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
        await this.loadCompanies();
      } catch (err) {
        alert("Ошибка удаления самолета.");
        console.error(err);
      }
    },
    editMember(memberId) {
      this.$router.push(`/edit-crew-member/${memberId}`);
    },
    async deleteMember(memberId) {
      if (!confirm("Вы уверены, что хотите удалить этого работника?")) {
        return;
      }
      try {
        await deleteCrewMember(memberId);
        alert("Работник успешно удален.");
        await this.loadCompanies();
      } catch (err) {
        alert("Ошибка удаления работника.");
        console.error(err);
      }
    },
    searchCompany() {
      if (this.searchName.trim()) {
        this.filteredCompanies = this.companies.filter(company =>
          company.name.toLowerCase().includes(this.searchName.toLowerCase())
        );
      }
    },
    resetSearch() {
      this.searchName = "";
      this.filters = {
        planeNumber: "",
        employeeName: "",
      };
      this.filteredCompanies = this.companies;
    },
    toggleFilters() {
      this.showFilters = !this. showFilters;
    },
    applyFilters() {
      this.filteredCompanies = this.companies.filter(company => {
        const matchesPlaneNumber =
          !this.filters.planeNumber ||
          (company.planes && company.planes. some(plane =>
            plane.number.toLowerCase().includes(this.filters.planeNumber.toLowerCase())
          ));

        const matchesEmployeeName =
          !this.filters.employeeName ||
          (company.crew_members && company. crew_members.some(member =>
            member.full_name. toLowerCase().includes(this.filters. employeeName.toLowerCase())
          ));

        return matchesPlaneNumber && matchesEmployeeName;
      });
      this.showFilters = false;
    },
  }
};
</script>

<style scoped>
.company-list {
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

.content-wrapper h1 {
  color: #333;
  margin-bottom: 20px;
  font-size: 28px;
}

.companies-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 20px;
}

.company-card {
  background-color: white;
  border:  1px solid #e0e0e0;
  padding: 25px;
  border-radius:  8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.company-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.company-header {
  display: flex;
  justify-content: space-between;
  align-items:  center;
  margin-bottom:  20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e0e0e0;
  flex-wrap: wrap;
  gap: 10px;
}

.company-header h2 {
  margin: 0;
  color:  #333;
  font-size: 24px;
}

.button-group-header {
  display:  flex;
  gap: 10px;
}

.section {
  margin-top: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius:  8px;
  border: 1px solid #e9ecef;
}

.section h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
  font-size: 20px;
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 15px;
}

.plane-card,
.employee-card {
  padding: 15px;
  background-color: white;
  border-radius: 6px;
  border: 1px solid #dee2e6;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.plane-card:hover,
.employee-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.12);
}

.plane-card p,
.employee-card p {
  margin: 6px 0;
  color:  #555;
  line-height: 1.5;
  font-size: 14px;
}

.search-company {
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

.search-company label {
  margin-right: 10px;
  font-weight: 500;
  color: #333;
}

.search-input {
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius:  5px;
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

.button-small {
  padding: 8px 15px;
  font-size:  13px;
}

.button-full {
  width:  100%;
  margin-top: 10px;
}

.button-group {
  display:  flex;
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
  margin-top: 0;
  color:  #333;
}

.filters-panel label {
  display: block;
  margin-bottom: 15px;
  font-weight: 500;
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

.no-data-small {
  color: #666;
  font-style: italic;
  margin:  0;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .company-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .button-group-header {
    width: 100%;
  }

  .button-group-header.button {
    flex: 1;
  }

  .items-grid {
    grid-template-columns: 1fr;
  }

  .search-company {
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