<template>
  <div class="create-form">
    <h1>Создать Самолет</h1>

    <div v-if="!isAuthenticated" class="warning">
      <p>Вы должны <router-link to="/login">войти</router-link>, чтобы создать маршрут.</p>
    </div><br/>

    <form @submit.prevent="submitForm">
      <label for="number">Номер самолета:</label>
      <input type="text" id="number" v-model="plane.number" placeholder="Введите номер самолета" required />

      <label for="type">Тип самолета:</label>
      <input type="text" id="type" v-model="plane.type" placeholder="Введите тип самолета" required />

      <label for="seats_capacity">Число мест:</label>
      <input type="number" id="seats_capacity" v-model="plane.seats_capacity" placeholder="Введите число мест" required />

      <label for="flight_speed">Скорость полета:</label>
      <input type="number" id="flight_speed" v-model="plane.flight_speed" placeholder="Введите скорость полета" required />

      <label for="airline_company">Компания-авиаперевозчик:</label>
      <select id="airline_company" v-model="plane.airline_company" required>
        <option v-for="company in companies" :value="company.id" :key="company.id">
          {{ company.name }}
        </option>
      </select>

      <label>
        <input type="checkbox" v-model="plane.in_repair" />
        В ремонте
      </label>

      <button type="submit">Создать</button>
    </form>
  </div>
</template>

<script>
import { getAirlineCompanies, createPlane } from '../api/index.js';

export default {
  name: 'CreatePlane',
  data() {
    return {
      plane: {
        number: '',
        type: '',
        seats_capacity: null,
        flight_speed: null,
        airline_company: null,
        in_repair: false,
      },
      companies: [],
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
      const response = await getAirlineCompanies();
      this.companies = response.data;
    } catch (err) {
      this.error = 'Ошибка загрузки компаний.';
      console.error(err);
    }
  },
  methods: {
    async submitForm() {
      try {
        const response = await createPlane(this.plane);
        alert('Самолет успешно создан.')
        console.log('Результат:', response.data);
        this.resetForm();
        this.$router.push('/planes');
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
      this.plane = {
        number: '',
        type: '',
        seats_capacity: null,
        flight_speed: null,
        airline_company: null,
        in_repair: false,
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