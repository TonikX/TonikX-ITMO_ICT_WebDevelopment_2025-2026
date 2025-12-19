<template>
  <div class="create-form">
    <h1>Создать Компанию</h1>
    <form @submit.prevent="submitForm">
      <label for="name">Название компании:</label>
      <input
        type="text"
        id="name"
        v-model="company.name"
        placeholder="Введите название компании"
        required
      />
      <button type="submit">Создать</button>
    </form>
  </div>
</template>

<script>
import { createCompany } from '../api/index.js';

export default {
  name: 'CreateCompany',
  data() {
    return {
      company: {
        name: '',
      },
    };
  },
  methods: {
    async submitForm() {
      if (!this.company.name.trim()) {
        alert('Название компании не может быть пустым.');
        return;
      }
      try {
        const response = await createCompany(this.company);
        alert('Компания успешно создана.');
        console.log('Результат:', response.data);
        this.resetForm();
        this.$router.push('/airlines');
      } catch (err) {
        alert('Ошибка создания компании.');
        console.error(err);
      }
    },
    resetForm() {
      this.company = {
        name: '',
      };
    },
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

input {
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