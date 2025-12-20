<template>
  <div class="create-company">
    <div class="content-wrapper">
      <h1>Создать компанию</h1>

      <div v-if="!isAuthenticated" class="warning">
        <p>Вы должны <router-link to="/login">войти</router-link>, чтобы создать компанию.</p>
      </div>

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
            <button type="submit" class="button button-primary">Создать</button>
            <button type="button" @click="$router.push('/airlines')" class="button button-secondary">Отмена</button>
          </div>
        </form>
      </div>
    </div>
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
  computed: {
    isAuthenticated() {
      return !!this.$store.state. auth.token;
    },
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
        console.log('Результат:', response. data);
        this.resetForm();
        this.$router.push('/airlines');
      } catch (err) {
        console.error('Ошибка создания компании:', err);

        if (err.response && err.response.status === 401) {
          alert('Ошибка:  требуется авторизация.');
        } else if (err. response && err.response.status === 403) {
          alert('Ошибка: доступ запрещён.');
        } else if (err.response && err.response.data) {
          alert(`Ошибка создания компании: ${JSON.stringify(err.response.data)}`);
        } else {
          alert('Ошибка создания компании.');
        }

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

<style scoped>
.create-company {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 20px 0;
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

.warning {
  background-color: #fff3cd;
  border: 1px solid #ffc107;
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
  margin-bottom:  20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
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
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
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

@media (max-width:  768px) {
  .content-wrapper {
    padding:  0 15px;
  }

  .form-container {
    padding: 20px;
  }

  .button-group {
    flex-direction:  column;
  }

  .button-group.button {
    width: 100%;
  }
}
</style>