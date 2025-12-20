<template>
  <div class="edit-plane">
    <div class="content-wrapper">
      <h1>Редактирование самолета №{{ plane.number }}</h1>

      <div class="form-container">
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label for="number">Номер:</label>
            <input type="text" id="number" v-model="plane.number" placeholder="Введите номер самолета" required />
          </div>

          <div class="form-group">
            <label for="type">Тип:</label>
            <input type="text" id="type" v-model="plane.type" placeholder="Введите тип самолета" required />
          </div>

          <div class="form-group">
            <label for="seats_capacity">Число мест: </label>
            <input type="number" id="seats_capacity" v-model="plane.seats_capacity" placeholder="Введите число мест" required />
          </div>

          <div class="form-group">
            <label for="flight_speed">Скорость полета (км/ч):</label>
            <input type="number" id="flight_speed" v-model="plane.flight_speed" placeholder="Введите скорость полета" required />
          </div>

          <div class="form-group">
            <label for="in_repair">В ремонте:</label>
            <select id="in_repair" v-model="plane.in_repair" required>
              <option :value="true">Да</option>
              <option :value="false">Нет</option>
            </select>
          </div>

          <div class="form-group">
            <label for="airline_company">Компания:</label>
            <select id="airline_company" v-model="plane.airline_company" required>
              <option v-for="company in companies" :value="company.id" :key="company.id">
                {{ company.name }}
              </option>
            </select>
          </div>

          <div class="button-group">
            <button type="submit" class="button button-primary">Сохранить</button>
            <button type="button" @click="$router.push('/planes')" class="button button-secondary">Отмена</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { getPlaneDetails, updatePlane, getAirlineCompanies } from '../api/index.js';

export default {
  name:  'EditPlane',
  data() {
    return {
      plane: {
        number:  '',
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
      this.plane = planeResponse. data;
      this.companies = companiesResponse.data;
    } catch (err) {
      this.error = 'Ошибка загрузки данных.';
      console.error(err);
    }
  },
  methods: {
    async submitForm() {
      const planeId = this.$route. params.id;
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

<style scoped>
.edit-plane {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height:  100vh;
  padding:  20px 0;
}

.content-wrapper {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 30px;
}

.content-wrapper h1 {
  color:  #333;
  margin-bottom: 30px;
  font-size: 28px;
}

.form-container {
  background-color: white;
  border: 1px solid #e0e0e0;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom:  20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
  font-size: 14px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px 15px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
  transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #007BFF;
  box-shadow:  0 0 0 3px rgba(0, 123, 255, 0.1);
}

.button {
  display: inline-block;
  padding:  12px 24px;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  text-align: center;
  transition: background-color 0.3s ease;
  font-weight: 500;
}

.button.button-primary {
  background-color: #007BFF;
}

.button.button-primary:hover {
  background-color: #0056b3;
}

.button.button-secondary {
  background-color: #6c757d;
}

.button.button-secondary:hover {
  background-color: #5a6268;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 30px;
}

.button-group.button {
  flex: 1;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .form-container {
    padding: 20px;
  }

  .button-group {
    flex-direction: column;
  }

  .button-group.button {
    width: 100%;
  }
}
</style>