<template>
  <div class="edit-company">
    <h1>Редактирование компании «{{ company.name }}»</h1>
    <form @submit.prevent="submitForm">
      <label for="name">Название компании:</label>
      <input
        type="text"
        id="name"
        v-model="company.name"
        placeholder="Введите название компании"
        required
      />

      <button type="submit" class="edit-button">Сохранить</button>
    </form>
  </div>
</template>

<script>
import { getCompanyDetails, updateCompany } from '../api/index.js';

export default {
  name: 'EditCompany',
  data() {
    return {
      company: {
        name: '',
      },
      error: null,
    };
  },
  async created() {
    const companyId = this.$route.params.id;
    try {
      const response = await getCompanyDetails(companyId);
      this.company = response.data;
    } catch (err) {
      this.error = 'Ошибка загрузки данных компании.';
      console.error(err);
    }
  },
  methods: {
    async submitForm() {
      const companyId = this.$route.params.id;
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

<style>
.edit-company {
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

input {
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