<template>
  <div class="edit-member">
    <h1>Редактирование участника {{ member.full_name }}</h1>
    <form @submit.prevent="submitForm">
      <label for="full_name">ФИО:</label>
      <input type="text" id="full_name" v-model="member.full_name" required />

      <label for="age">Возраст:</label>
      <input type="number" id="age" v-model="member.age" required />

      <label for="education">Образование:</label>
      <input type="text" id="education" v-model="member.education" required />

      <label for="work_experience">Стаж работы:</label>
      <input type="number" id="work_experience" v-model="member.work_experience" required />

      <label for="passport_info">Паспортные данные:</label>
      <input type="text" id="passport_info" v-model="member.passport_info" required />

      <label for="flight_authorization">Допуск к рейсу:</label>
      <select id="flight_authorization" v-model="member.flight_authorization" required>
        <option :value="true">Да</option>
        <option :value="false">Нет</option>
      </select>

      <label for="position">Должность:</label>
      <input type="text" id="position" v-model="member.position" required />

      <label for="company">Компания:</label>
      <select id="company" v-model="member.company" required>
        <option v-for="company in companies" :value="company.id" :key="company.id">
          {{ company.name }}
        </option>
      </select>

      <button type="submit" class="save-button">Сохранить изменения</button>
    </form>
  </div>
</template>

<script>
import { getCrewMemberDetails, updateCrewMember, getAirlineCompanies } from '../api/index.js';

export default {
  name: 'EditCrewMember',
  data() {
    return {
      member: {
        full_name: '',
        age: null,
        education: '',
        work_experience: null,
        passport_info: '',
        flight_authorization: false,
        position: '',
        company: null,
      },
      companies: [],
      error: null,
    };
  },
  async created() {
    const memberId = this.$route.params.id;
    try {
      const [memberResponse, companiesResponse] = await Promise.all([
        getCrewMemberDetails(memberId),
        getAirlineCompanies(),
      ]);
      this.member = memberResponse.data;
      this.companies = companiesResponse.data;
    } catch (err) {
      this.error = 'Ошибка загрузки данных.';
      console.error(err);
    }
  },
  methods: {
    async submitForm() {
      const memberId = this.$route.params.id;
      const updatedData = {
        ...this.member,
        company_id: this.member.company,
        };
      console.log("Data:", updatedData)
      try {
        await updateCrewMember(memberId, updatedData);
        alert('Информация об участнике успешно обновлена.');
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
.edit-member {
  margin: 20px;
  font-family: Arial, sans-serif;
}

form {
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 5px;
  font-weight: bold;
}

input,
select {
  margin-bottom: 10px;
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.save-button {
  margin-top: 20px;
  padding: 10px 15px;
  color: white;
  background-color: #007BFF;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.save-button:hover {
  background-color: #0056b3;
}
</style>