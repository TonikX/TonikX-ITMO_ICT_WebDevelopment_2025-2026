<template>
  <div class="create-form">
    <h1>Создать Члена Экипажа</h1>

    <div v-if="!isAuthenticated" class="warning">
      <p>Вы должны <router-link to="/login">войти</router-link>, чтобы создать маршрут.</p>
    </div><br/>

    <form @submit.prevent="submitForm">
      <label for="full-name">ФИО:</label>
      <input type="text" id="full-name" v-model="crewMember.full_name" placeholder="Введите ФИО" required />

      <label for="age">Возраст:</label>
      <input type="number" id="age" v-model="crewMember.age" placeholder="Введите возраст" required />

      <label for="education">Образование:</label>
      <input type="text" id="education" v-model="crewMember.education" placeholder="Введите образование" required />

      <label for="work-experience">Стаж работы (лет):</label>
      <input type="number" id="work-experience" v-model="crewMember.work_experience" placeholder="Введите стаж" required />

      <label for="passport-info">Паспортные данные:</label>
      <input type="text" id="passport-info" v-model="crewMember.passport_info" placeholder="Введите паспортные данные" required />

      <label for="position">Должность:</label>
      <select id="position" v-model="crewMember.position" required>
        <option value="командир">Командир</option>
        <option value="второй пилот">Второй пилот</option>
        <option value="штурман">Штурман</option>
        <option value="стюардесса">Стюардесса</option>
        <option value="стюард">Стюард</option>
      </select>

      <label for="company">Компания:</label>
      <select id="company" v-model="crewMember.company_id" required>
        <option v-for="company in companies" :value="company.id" :key="company.id">
          {{ company.name }}
        </option>
      </select>

      <label>
        <input type="checkbox" v-model="crewMember.flight_authorization" />
        Допуск к рейсу
      </label>

      <button type="submit">Создать</button>
    </form>
  </div>
</template>

<script>
import { createCrewMember, getAirlineCompanies } from '../api/index.js';

export default {
  name: 'CreateCrewMember',
  data() {
    return {
      crewMember: {
        full_name: '',
        age: null,
        education: '',
        work_experience: null,
        passport_info: '',
        flight_authorization: false,
        company_id: null,
        position: '',
      },
      companies: [],
      error: null,
    };
  },
  async created() {
    try {
      const response = await getAirlineCompanies();
      this.companies = response.data;
    } catch (err) {
      this.error = 'Ошибка загрузки компаний.';
      console.error(err);
    }
  },
  computed: {
    isAuthenticated() {
      return !!this.$store.state.auth.token;
    },
  },
  methods: {
    async submitForm() {
      console.log("Crew member for create:", this.crewMember)
      try {
        const response = await createCrewMember(this.crewMember);
        alert('Член экипажа успешно создан.')
        console.log('Результат:', response.data);
        this.resetForm();
        this.$router.push('/crews');
      } catch(err){
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
      this.crewMember = {
        full_name: '',
        age: null,
        education: '',
        work_experience: null,
        passport_info: '',
        flight_authorization: false,
        company: [],
        position: '',
      };
    }
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