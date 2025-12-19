<template>
  <div class="create-form">
    <h1>Создать Команду</h1>

    <div v-if="!isAuthenticated" class="warning">
      <p>Вы должны <router-link to="/login">войти</router-link>, чтобы создать маршрут.</p>
    </div><br/>

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
import { getCrewMembers, createCrew } from '../api/index.js';

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
  computed: {
    isAuthenticated() {
      return !!this.$store.state.auth.token;
    },
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
        console.error('Ошибка создания рейса:', err);

        if (err.response && err.response.status === 401) {
          alert('Ошибка:  требуется авторизация.');
        } else if (err. response && err.response.status === 403) {
          alert('Ошибка: доступ запрещён.');
        } else if (err.response && err.response.data) {
          alert(`Ошибка создания рейса: ${err.response.data}`);
        } else {
          alert('Ошибка создания рейса.');
        }

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