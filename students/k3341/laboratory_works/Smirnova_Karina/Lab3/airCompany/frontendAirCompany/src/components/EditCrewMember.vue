<template>
  <div class="edit-member">
    <div class="content-wrapper">
      <h1>Редактирование участника {{ member.full_name }}</h1>

      <div class="form-container">
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label for="full_name">ФИО:</label>
            <input type="text" id="full_name" v-model="member.full_name" placeholder="Введите ФИО" required />
          </div>

          <div class="form-group">
            <label for="age">Возраст:</label>
            <input type="number" id="age" v-model="member.age" placeholder="Введите возраст" required />
          </div>

          <div class="form-group">
            <label for="education">Образование:</label>
            <input type="text" id="education" v-model="member.education" placeholder="Введите образование" required />
          </div>

          <div class="form-group">
            <label for="work_experience">Стаж работы (лет):</label>
            <input type="number" id="work_experience" v-model="member.work_experience" placeholder="Введите стаж работы" required />
          </div>

          <div class="form-group">
            <label for="passport_info">Паспортные данные:</label>
            <input type="text" id="passport_info" v-model="member.passport_info" placeholder="Введите паспортные данные" required />
          </div>

          <div class="form-group">
            <label for="flight_authorization">Допуск к рейсу:</label>
            <select id="flight_authorization" v-model="member. flight_authorization" required>
              <option :value="true">Да</option>
              <option :value="false">Нет</option>
            </select>
          </div>

          <div class="form-group">
            <label for="position">Должность:</label>
            <select id="position" v-model="member.position" required>
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
            <select id="company" v-model="member.company" required>
              <option v-for="company in companies" :value="company.id" :key="company.id">
                {{ company.name }}
              </option>
            </select>
          </div>

          <div class="button-group">
            <button type="submit" class="button button-primary">Сохранить изменения</button>
            <button type="button" @click="$router.push('/crews')" class="button button-secondary">Отмена</button>
          </div>
        </form>
      </div>
    </div>
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
        education:  '',
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
  methods:  {
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

<style scoped>
.edit-member {
  font-family:  Arial, sans-serif;
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
    padding:  20px;
  }

  .button-group {
    flex-direction: column;
  }

  .button-group . button {
    width: 100%;
  }
}
</style>