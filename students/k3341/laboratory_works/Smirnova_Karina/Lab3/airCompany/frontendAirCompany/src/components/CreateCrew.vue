<template>
  <div class="create-form">
    <h1>Создать Команду</h1>
    <form @submit.prevent="submitForm">
      <label for="members">Члены команды:</label>
      <div id="members" class="checkbox-list">
        <div v-for="member in members" :key="member.id">
          <input
            type="checkbox"
            :id="'member-' + member.id"
            :value="member.id"
            v-model="crew.members"
          />
          <label :for="'member-' + member.id">
            {{ member.full_name }} — {{ member.position }}
          </label>
        </div>
      </div>

      <button type="submit">Создать</button>
    </form>
  </div>
</template>

<script>
import { getCrewMembers } from '../api/index.js';
import { createCrew } from '../api/index.js';

export default {
  name: 'CreateCrew',
  data() {
    return {
      crew: {
        members: [],
      },
      members: [],
      error: null,
    };
  },
  async created() {
    try {
      const response = await getCrewMembers();
      this.members = response.data;
    } catch (err) {
      this.error = 'Ошибка загрузки участников экипажа.';
      console.error(err);
    }
  },
  methods: {
    async submitForm() {
      try {
        const response = await createCrew(this.crew);
        alert('Команда успешно создана.');
        console.log('Результат:', response.data);
        this.resetForm();
        this.$router.push('/crews');
      } catch (err) {
        alert('Ошибка создания команды.');
        console.error(err);
      }
    },
    resetForm() {
      this.crew = {
        members: [],
      };
    },
  },
};
</script>

<style>
.create-form {
  margin: 20px;
  font-family: Arial, sans-serif;
}

h1 {
  font-size: 24px;
  margin-bottom: 20px;
}

form {
  display: flex;
  flex-direction: column;
}

.label {
  margin-bottom: 10px;
  font-weight: bold;
}

.checkbox-list {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

.checkbox-list label {
  margin-left: 6px;
}

button {
  padding: 10px 15px;
  font-size: 16px;
  color: white;
  background-color: #007BFF;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>