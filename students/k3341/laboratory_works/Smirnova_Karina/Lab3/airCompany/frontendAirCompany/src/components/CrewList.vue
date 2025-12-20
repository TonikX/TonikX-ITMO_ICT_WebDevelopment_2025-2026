<template>
  <div class="crew-list">
    <div class="content-wrapper">
      <h1>Список команд</h1>

      <div class="search-crew">
        <label for="search">Найти команду по номеру:</label>
        <input
          class="search-input"
          type="text"
          id="search"
          v-model="searchId"
          placeholder="Введите номер команды"
        />
        <button @click="searchCrew" class="button button-primary">Найти команду</button>
        <button @click="toggleFilters" class="button button-primary">Фильтры</button>
        <button @click="resetSearch" class="button button-danger">Очистить</button>
      </div>

      <div v-if="filteredCrews.length > 0" class="crews-container">
        <div class="crew-card" v-for="crew in filteredCrews" :key="crew.id">
          <div class="crew-header">
            <h2>Команда №{{ crew.id }}</h2>
            <div class="button-group-header">
              <button @click="editCrew(crew.id)" class="button button-primary button-small">Редактировать команду</button>
              <button @click="deleteCrew(crew.id)" class="button button-danger button-small">Удалить команду</button>
            </div>
          </div>

          <div class="section">
            <h3>Участники команды</h3>
            <div v-if="crew.members && crew.members.length > 0" class="members-grid">
              <div class="member-card" v-for="member in crew.members" :key="member. id">
                <p><strong>ФИО:</strong> {{ member. full_name }}</p>
                <p><strong>Возраст:</strong> {{ member. age }}</p>
                <p><strong>Образование:</strong> {{ member.education }}</p>
                <p><strong>Стаж:</strong> {{ member. work_experience }} лет</p>
                <p><strong>Допуск к рейсу:</strong> {{ member.flight_authorization ?  'Да' : 'Нет' }}</p>
                <p><strong>Должность:</strong> {{ member.position }}</p>
                <div class="button-group">
                  <button @click="editMember(member.id)" class="button button-primary">Редактировать</button>
                  <button @click="deleteMember(member.id, crew.id)" class="button button-danger">Удалить</button>
                </div>
              </div>
            </div>
            <p v-else class="no-data-small">Нет участников в команде</p>
          </div>
        </div>
      </div>
      <p v-else class="no-data">Нет доступных команд</p>
    </div>

    <div v-if="showFilters" class="filters-panel">
      <h2>Фильтр</h2>
      <label>
        ФИО участника:
        <input type="text" v-model="filters. memberName" placeholder="Введите ФИО участника" />
      </label><br/>
      <button @click="applyFilters" class="button button-primary button-full">Найти</button>
    </div>
  </div>
</template>

<script>
import { getCrews, deleteCrew, deleteCrewMember } from '../api/index.js';

export default {
  name: 'CrewList',
  data() {
    return {
      crews: [],
      searchId:  "",
      filteredCrews: [],
      showFilters: false,
      filters: {
        memberName: "",
      },
      error: null,
    };
  },
  async created() {
    await this.loadCrews();
  },
  methods: {
    async loadCrews() {
      try {
        const response = await getCrews();
        this.crews = response.data;
        this.filteredCrews = this.crews;
      } catch (err) {
        this.error = 'Ошибка загрузки информации о командах.';
        console.error(err);
      }
    },
    editCrew(id) {
      this.$router.push(`/edit-crew/${id}`);
    },
    editMember(memberId) {
      this.$router.push(`/edit-crew-member/${memberId}`);
    },
    async deleteCrew(crewId) {
      if (!confirm("Вы уверены, что хотите удалить всю команду?")) {
        return;
      }
      try {
        await deleteCrew(crewId);
        alert("Команда успешно удалена.");
        this.crews = this.crews.filter(crew => crew.id !== crewId);
        this.filteredCrews = this.filteredCrews.filter(crew => crew.id !== crewId);
      } catch (err) {
        alert("Ошибка удаления команды.");
        console.error(err);
      }
    },
    async deleteMember(memberId, crewId) {
      if (!confirm("Вы уверены, что хотите удалить этого участника из команды?")) {
        return;
      }
      try {
        await deleteCrewMember(memberId);
        alert("Участник успешно удален.");
        await this.loadCrews();
      } catch (err) {
        alert("Ошибка удаления участника.");
        console.error(err);
      }
    },
    searchCrew() {
      const crewId = parseInt(this.searchId, 10);
      if (!isNaN(crewId)) {
        this.filteredCrews = this.crews.filter(crew => crew.id === crewId);
      }
    },
    resetSearch() {
      this.searchId = "";
      this.filters = {
        memberName: "",
      };
      this.filteredCrews = this. crews;
    },
    toggleFilters() {
      this.showFilters = !this.showFilters;
    },
    applyFilters() {
      this.filteredCrews = this.crews.filter(crew => {
        const matchesMemberName =
          !this.filters. memberName ||
          (crew.members && crew.members. some(member =>
            member.full_name. toLowerCase().includes(this.filters. memberName.toLowerCase())
          ));

        return matchesMemberName;
      });
      this.showFilters = false;
    },
  },
};
</script>

<style scoped>
.crew-list {
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
  margin-bottom: 30px;
  font-size: 28px;
}

.search-crew {
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-crew label {
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

.crews-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 20px;
}

.crew-card {
  background-color: white;
  border: 1px solid #e0e0e0;
  padding: 25px;
  border-radius:  8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.crew-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.crew-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e0e0e0;
  flex-wrap: wrap;
  gap: 10px;
}

.crew-header h2 {
  margin: 0;
  color:  #333;
  font-size: 24px;
}

.button-group-header {
  display:  flex;
  gap: 10px;
  flex-wrap: wrap;
}

.section {
  margin-top: 20px;
  padding:  15px;
  background-color:  #f8f9fa;
  border-radius: 8px;
  border:  1px solid #e9ecef;
}

.section h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
  font-size: 20px;
}

.members-grid {
  display: grid;
  grid-template-columns:  repeat(auto-fill, minmax(280px, 1fr));
  gap: 15px;
}

.member-card {
  padding: 15px;
  background-color: white;
  border-radius: 6px;
  border: 1px solid #dee2e6;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.member-card:hover {
  transform:  translateY(-2px);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.12);
}

.member-card p {
  margin: 6px 0;
  color:  #555;
  line-height: 1.5;
  font-size: 14px;
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
  background-color:  rgb(210, 37, 37);
}

.button.button-danger:hover {
  background-color: rgb(180, 20, 20);
}

.button-small {
  padding: 8px 15px;
  font-size:  13px;
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
  position:  fixed;
  top: 0;
  right: 0;
  height: 100%;
  width: 300px;
  background-color: white;
  border-left: 1px solid #ddd;
  padding: 20px;
  box-shadow: -5px 0 15px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  z-index:  1000;
}

.filters-panel h2 {
  margin-top: 0;
  color: #333;
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
  font-size:  14px;
}

.filters-panel input:focus {
  outline: none;
  border-color: #007BFF;
}

.filters-panel . button {
  margin-top:  20px;
}

.no-data {
  background-color: white;
  padding:  20px;
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

  .search-crew {
    flex-direction: column;
    align-items: stretch;
  }

  .search-input {
    width: 100%;
  }

  .button {
    width: 100%;
  }

  .crew-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .button-group-header {
    width: 100%;
  }

  .button-group-header.button {
    flex: 1;
  }

  .members-grid {
    grid-template-columns: 1fr;
  }
}
</style>