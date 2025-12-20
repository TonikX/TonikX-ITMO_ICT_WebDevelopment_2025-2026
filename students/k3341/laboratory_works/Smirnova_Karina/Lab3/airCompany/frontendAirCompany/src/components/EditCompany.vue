<template>
  <div class="edit-company">
    <div class="content-wrapper">
      <h1>Редактирование компании «{{ company.name }}»</h1>

      <div class="form-container">
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label for="name">Название компании:</label>
            <input
              type="text"
              id="name"
              v-model="company.name"
              placeholder="Введите название компании"
              required
            />
          </div>

          <div class="button-group">
            <button type="submit" class="button button-primary">Сохранить</button>
            <button type="button" @click="$router. push('/airlines')" class="button button-secondary">Отмена</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { getCompanyDetails, updateCompany } from '../api/index.js';

export default {
  name:  'EditCompany',
  data() {
    return {
      company: {
        name:  '',
      },
      error:  null,
    };
  },
  async created() {
    const companyId = this.$route.params.id;
    try {
      const response = await getCompanyDetails(companyId);
      this.company = response. data;
    } catch (err) {
      this.error = 'Ошибка загрузки данных компании. ';
      console.error(err);
    }
  },
  methods: {
    async submitForm() {
      const companyId = this.$route.params. id;
      try {
        await updateCompany(companyId, this.company);
        alert('Компания успешно обновлена.');
        this.$router.push('/airlines');
      } catch (err) {
        alert('Ошибка обновления компании.');
        console.error(err);
      }
    },
  },
};
</script>

<style scoped>
.edit-company {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height:  100vh;
  padding:  20px 0;
}

.content-wrapper {
  max-width:  800px;
  margin:  0 auto;
  padding: 0 30px;
}

.content-wrapper h1 {
  color: #333;
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
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color:  #333;
  font-size: 14px;
}

.form-group input {
  width: 100%;
  padding: 10px 15px;
  font-size:  14px;
  border:  1px solid #ddd;
  border-radius: 5px;
  box-sizing:  border-box;
  font-family: Arial, sans-serif;
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #007BFF;
  box-shadow:  0 0 0 3px rgba(0, 123, 255, 0.1);
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
  background-color:  #0056b3;
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

  .button-group.button {
    width: 100%;
  }
}
</style>