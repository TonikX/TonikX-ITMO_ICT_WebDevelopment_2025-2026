<template>
  <div class="edit-plane">
    <h1>Редактирование самолета №{{ plane.number }}</h1>
    <form @submit.prevent="submitForm">
      <label for="number">Номер:</label>
      <input type="text" id="number" v-model="plane.number" placeholder="Введите номер самолета" required />

      <label for="type">Тип:</label>
      <input type="text" id="type" v-model="plane.type" placeholder="Введите тип самолета" required />

      <label for="seats_capacity">Число мест:</label>
      <input type="number" id="seats_capacity" v-model="plane.seats_capacity" placeholder="Введите число мест" required />

      <label for="flight_speed">Скорость полета:</label>
      <input type="number" id="flight_speed" v-model="plane.flight_speed" placeholder="Введите скорость полета" required />

      <label for="in_repair">В ремонте:</label>
      <select id="in_repair" v-model="plane.in_repair" required>
        <option :value="true">Да</option>
        <option :value="false">Нет</option>
      </select>

      <label for="airline_company">Компания:</label>
      <select id="airline_company" v-model="plane.airline_company" required>
        <option v-for="company in companies" :value="company.id" :key="company.id">
          {{ company.name }}
        </option>
      </select>

      <button type="submit" class="edit-button">Сохранить</button>
    </form>
  </div>
</template>

<script>
import { getPlaneDetails, updatePlane, getAirlineCompanies } from '../api/index.js';

export default {
  name: 'EditPlane',
  data() {
    return {
      plane: {
        number: '',
        type: '',
        seats_capacity: null,
        flight_speed: null,
        in_repair: false,
        airline_company: null,
      },
      companies: [],
      error: null,
    };
  },
  async created() {
    const planeId = this.$route.params.id;
    try {
      const [planeResponse, companiesResponse] = await Promise.all([
        getPlaneDetails(planeId),
        getAirlineCompanies(),
      ]);
      this.plane = planeResponse.data;
      this.companies = companiesResponse.data;
    } catch (err) {
      this.error = 'Ошибка загрузки данных.';
      console.error(err);
    }
  },
  methods: {
    async submitForm() {
      const planeId = this.$route.params.id;
      try {
        await updatePlane(planeId, this.plane);
        alert('Самолет успешно обновлен.');
        this.$router.push('/planes');
      } catch (err) {
        alert('Ошибка сохранения изменений.');
        console.error(err);
      }
    },
  },
};
</script>

<style>
.edit-plane {
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
select,
button {
  margin-bottom: 10px;
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.edit-button {
  padding: 10px 15px;
  font-size: 16px;
  color: white;
  background-color: #007BFF;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.edit-button:hover {
  background-color: #0056b3;
}
</style>