<template>
  <div class="crew-details">
    <h1>Детали команды №{{ crewId }}</h1>
    <ul>
      <li v-for="member in crewMembers" :key="member.id">
        ФИО: {{ member.full_name }}
        | Возраст: {{ member.age }}
        | Должность: {{ member.position }}
      </li>
    </ul>
    <p v-if="crewMembers.length === 0">Данные о команде недоступны</p>
  </div>
</template>

<script>
import { getCrewDetail } from '../api/index.js';
export default {
  name: 'CrewDetails',
  props: ['id'],
  data() {
    return {
      crewId: this.id,
      crewMembers: [],
      error: null,
    };
  },
  async created() {
    try {
      const response = await getCrewDetail(this.crewId);
      this.crewMembers = response.data.members;
    } catch (err) {
      this.error = 'Ошибка загрузки данных экипажа.';
      console.error(err);
    }
  },
};
</script>

<style>
.crew-details {
  margin: 20px;
}

h1 {
  font-size: 24px;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
}
</style>