<template>
  <div class="edit-crew">
    <h1>Редактирование Команды №{{ crew.id }}</h1>
    <form @submit.prevent="submitForm">
      <h3>Участники Команды:</h3>
      <div class="member-checkbox" v-for="member in allMembers" :key="member.id">
        <input
          type="checkbox"
          :id="`member-${member.id}`"
          :value="member.id"
          v-model="selectedMemberIds"
        />
        <label :for="`member-${member.id}`">{{ member.full_name }} ({{ member.position }})</label>
      </div>
      <button type="submit" class="save-crew-button">Сохранить изменения</button>
    </form>
  </div>
</template>

<script>
import { getCrewDetails, updateCrew, getCrewMembers } from '../api/index.js';

export default {
  name: 'EditCrew',
  data() {
    return {
      crew: {
        id: null,
      },
      allMembers: [],
      selectedMemberIds: [],
      error: null,
    };
  },
  async created() {
    const crewId = this.$route.params.id;
    try {
      const [crewResponse, membersResponse] = await Promise.all([
        getCrewDetails(crewId),
        getCrewMembers(),
      ]);

      this.crew = crewResponse.data;
      this.allMembers = membersResponse.data;

      this.selectedMemberIds = this.crew.members.map((member) => member.id);
    } catch (err) {
      this.error = 'Ошибка загрузки данных.';
      console.error(err);
    }
  },
  methods: {
    async submitForm() {
      const crewId = this.$route.params.id;
      try {
        const updatedCrewData = {
          id: crewId,
          member_ids: this.selectedMemberIds,
        };
        await updateCrew(crewId, updatedCrewData);
        alert('Команда успешно обновлена.');
        this.$router.push('/crews');
      } catch (err) {
        alert('Ошибка сохранения изменений.');
        console.error(err);
      }
    },
  },
};
</script>

<style>
.edit-crew {
  margin: 20px;
  font-family: Arial, sans-serif;
}

form {
  display: flex;
  flex-direction: column;
}

.member-checkbox {
  margin-bottom: 10px;
}

label {
  margin-left: 5px;
  font-weight: bold;
}

.save-crew-button {
  margin-top: 20px;
  padding: 10px 15px;
  color: white;
  background-color: #007BFF;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.save-crew-button:hover {
  background-color: #0056b3;
}
</style>