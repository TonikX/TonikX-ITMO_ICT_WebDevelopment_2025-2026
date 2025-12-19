<template>
  <div class="crew-list">
    <h1>Список команд</h1>

    <div v-if="crews.length > 0">
      <div class="crew-card" v-for="crew in crews" :key="crew.id">
        <h2>
          Команда №{{ crew.id }}
          <button @click="editCrew(crew.id)" class="edit-button">Редактировать команду</button>
          <button @click="deleteCrew(crew.id)" class="delete-button">Удалить команду</button>
        </h2>

        <div v-if="crew.members && crew.members.length > 0" class="section">
          <h3>Участники команды:</h3>
          <div class="member-card" v-for="member in crew.members" :key="member. id">
            <p><strong>ФИО:</strong> {{ member.full_name }}</p>
            <p><strong>Возраст:</strong> {{ member. age }}</p>
            <p><strong>Образование:</strong> {{ member.education }}</p>
            <p><strong>Стаж:</strong> {{ member. work_experience }} лет</p>
            <p><strong>Допуск к рейсу:</strong> {{ member.flight_authorization ?  'Да' : 'Нет' }}</p>
            <p><strong>Должность:</strong> {{ member.position }}</p>
            <div class="member-actions">
              <button @click="editMember(member. id)" class="edit-button">Редактировать</button>
              <button @click="deleteMember(member.id, crew.id)" class="delete-button">Удалить</button>
            </div>
          </div>
        </div>
        <p v-else>Нет участников в команде</p>
      </div>
    </div>
    <p v-else>Нет доступных команд</p>
  </div>
</template>

<script>
import { getCrews, deleteCrew, deleteCrewMember } from '../api/index.js';

export default {
  name: 'CrewList',
  data() {
    return {
      crews: [],
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
      } catch (err) {
        this.error = 'Ошибка загрузки информации о командах. ';
        console.error(err);
      }
    },
    editCrew(id) {
      this.$router. push(`/edit-crew/${id}`);
    },
    editMember(memberId) {
      this.$router.push(`/edit-crew-member/${memberId}`);
    },
    async deleteCrew(crewId) {
      if (! confirm("Вы уверены, что хотите удалить всю команду? ")) {
        return;
      }
      try {
        await deleteCrew(crewId);
        alert("Команда успешно удалена.");
        this.crews = this.crews.filter(crew => crew.id !== crewId);
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
  },
};
</script>

<style>
.crew-list {
  margin: 20px;
  font-family: Arial, sans-serif;
}

.crew-card {
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

.member-card {
  margin:  10px 0;
  padding: 10px;
  background-color: #e1f5fe;
  border-radius: 5px;
  position: relative;
}

.member-actions {
  margin-top: 10px;
}

h1 {
  font-size:  24px;
  margin-bottom: 20px;
}

h2 {
  font-size: 20px;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
}

h3 {
  font-size: 18px;
  margin-bottom: 10px;
}

.edit-button {
  padding: 8px 12px;
  font-size: 14px;
  color: white;
  background-color: #007BFF;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-left: 10px;
}

.edit-button:hover {
  background-color: #0056b3;
}

.delete-button {
  padding: 8px 12px;
  font-size: 14px;
  color: white;
  background-color: rgb(210, 37, 37);
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-left: 5px;
}

.delete-button:hover {
  background-color: rgb(180, 20, 20);
}
</style>