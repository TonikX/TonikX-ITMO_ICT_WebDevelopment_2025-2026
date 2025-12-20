<template>
  <div class="create-crew-member">
    <div class="content-wrapper">
      <h1>Создать члена экипажа</h1>

      <div v-if="!isAuthenticated" class="warning">
        <p>Вы должны <router-link to="/login">войти</router-link>, чтобы создать члена экипажа.</p>
      </div>

      <div class="form-container">
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label for="full-name">ФИО:</label>
            <input type="text" id="full-name" v-model="crewMember.full_name" placeholder="Введите ФИО" required />
          </div>

          <div class="form-group">
            <label for="age">Возраст:</label>
            <input type="number" id="age" v-model="crewMember.age" placeholder="Введите возраст" required />
          </div>

          <div class="form-group">
            <label for="education">Образование:</label>
            <input type="text" id="education" v-model="crewMember.education" placeholder="Введите образование" required />
          </div>

          <div class="form-group">
            <label for="work-experience">Стаж работы (лет):</label>
            <input type="number" id="work-experience" v-model="crewMember.work_experience" placeholder="Введите стаж" required />
          </div>

          <div class="form-group">
            <label for="passport-info">Паспортные данные:</label>
            <input type="text" id="passport-info" v-model="crewMember.passport_info" placeholder="Введите паспортные данные" required />
          </div>

          <div class="form-group">
            <label for="position">Должность:</label>
            <select id="position" v-model="crewMember.position" required>
              <option value="" disabled selected>Выберите должность</option>
              <option value="командир">Командир</option>
              <option value="второй пилот">Второй пилот</option>
              <option value="штурман">Штурман</option>
              <option value="стюардесса">Стюардесса</option>
              <option value="стюард">Стюард</option>
            </select>
          </div>

          <div class="form-group">
            <label for="company">Компания:</label>
            <select id="company" v-model="crewMember.company_id" required>
              <option value="" disabled selected>Выберите компанию</option>
              <option v-for="company in companies" :value="company.id" :key="company.id">
                {{ company.name }}
              </option>
            </select>
          </div>

          <div class="form-group checkbox-group">
            <label for="flight_authorization">
              <input type="checkbox" id="flight_authorization" v-model="crewMember.flight_authorization" />
              <span>Допуск к рейсу</span>
            </label>
          </div>

          <div class="button-group">
            <button type="submit" class="button button-primary">Создать</button>
            <button type="button" @click="$router.push('/crews')" class="button button-secondary">Отмена</button>
          </div>
        </form>
      </div>
    </div>
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
        work_experience:  null,
        passport_info:  '',
        flight_authorization: false,
        company_id: '',
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
      this.error = 'Ошибка загрузки компаний. ';
      console.error(err);
    }
  },
  computed: {
    isAuthenticated() {
      return !!this.$store.state.auth. token;
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
        console.error('Ошибка создания члена экипажа:', err);

        if (err.response && err.response.status === 401) {
          alert('Ошибка:  требуется авторизация.');
        } else if (err. response && err.response.status === 403) {
          alert('Ошибка: доступ запрещён.');
        } else if (err.response && err.response.data) {
          alert(`Ошибка создания члена экипажа: ${JSON.stringify(err.response.data)}`);
        } else {
          alert('Ошибка создания члена экипажа.');
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
        company_id: '',
        position: '',
      };
    }
  },
};
</script>

<style scoped>
.create-crew-member {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 20px 0;
}

.content-wrapper {
  max-width: 800px;
  margin: 0 auto;
  padding:  0 30px;
}

.content-wrapper h1 {
  color: #333;
  margin-bottom: 30px;
  font-size: 28px;
}

.warning {
  background-color: #fff3cd;
  border:  1px solid #ffc107;
  border-radius: 8px;
  padding: 15px 20px;
  margin-bottom: 20px;
  color: #856404;
}

.warning p {
  margin: 0;
  font-size:  14px;
}

.warning a {
  color: #007BFF;
  text-decoration: none;
  font-weight: 500;
}

.warning a:hover {
  text-decoration: underline;
}

.form-container {
  background-color: white;
  border: 1px solid #e0e0e0;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight:  500;
  color:  #333;
  font-size: 14px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px 15px;
  font-size:  14px;
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
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.checkbox-group label {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.checkbox-group input[type="checkbox"] {
  width:  18px;
  height:  18px;
  margin-right: 10px;
  cursor: pointer;
  accent-color: #007BFF;
}

.checkbox-group span {
  font-weight: 500;
  color: #333;
}

.button {
  display: inline-block;
  padding: 12px 24px;
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
  display:  flex;
  gap: 10px;
  margin-top:  30px;
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