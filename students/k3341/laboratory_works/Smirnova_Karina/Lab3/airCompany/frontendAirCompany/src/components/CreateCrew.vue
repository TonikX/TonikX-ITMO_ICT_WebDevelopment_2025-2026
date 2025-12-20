<template>
  <div class="create-crew">
    <div class="content-wrapper">
      <h1>Создать команду</h1>

      <div v-if="!isAuthenticated" class="warning">
        <p>Вы должны <router-link to="/login">войти</router-link>, чтобы создать команду.</p>
      </div>

      <div class="form-container">
        <form @submit.prevent="submitForm">
          <div class="form-section">
            <h3>Члены команды</h3>
            <p class="section-description">Выберите участников, которые входят в состав команды</p>

            <div class="members-list">
              <div class="member-checkbox" v-for="member in members" :key="member.id">
                <label :for="'member-' + member.id" class="checkbox-label">
                  <input
                    type="checkbox"
                    :id="'member-' + member.id"
                    :value="member.id"
                    v-model="crew.members"
                  />
                  <span class="member-info">
                    <span class="member-name">{{ member.full_name }}</span>
                    <span class="member-position">{{ member.position }}</span>
                  </span>
                </label>
              </div>
            </div>

            <p v-if="members.length === 0" class="no-data-small">Нет доступных участников</p>
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
import { getCrewMembers, createCrew } from '../api/index.js';

export default {
  name: 'CreateCrew',
  data() {
    return {
      crew: {
        members: [],
      },
      members: [],
      error: null,
    };
  },
  computed: {
    isAuthenticated() {
      return !!this.$store.state.auth. token;
    },
  },
  async created() {
    try {
      const response = await getCrewMembers();
      this.members = response.data;
    } catch (err) {
      this.error = 'Ошибка загрузки участников экипажа. ';
      console.error(err);
    }
  },
  methods: {
    async submitForm() {
      try {
        const response = await createCrew(this.crew);
        alert('Команда успешно создана.');
        console.log('Результат:', response.data);
        this.resetForm();
        this.$router.push('/crews');
      } catch (err) {
        console.error('Ошибка создания команды:', err);

        if (err.response && err.response. status === 401) {
          alert('Ошибка:   требуется авторизация.');
        } else if (err. response && err.response.status === 403) {
          alert('Ошибка: доступ запрещён.');
        } else if (err.response && err.response.data) {
          alert(`Ошибка создания команды: ${JSON.stringify(err.response.data)}`);
        } else {
          alert('Ошибка создания команды.');
        }

        console.error(err);
      }
    },
    resetForm() {
      this.crew = {
        members: [],
      };
    },
  },
};
</script>

<style scoped>
.create-crew {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 20px 0;
}

.content-wrapper {
  max-width:  800px;
  margin:  0 auto;
  padding:  0 30px;
}

.content-wrapper h1 {
  color: #333;
  margin-bottom: 30px;
  font-size:  28px;
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
  font-size: 14px;
}

.warning a {
  color: #007BFF;
  text-decoration: none;
  font-weight: 500;
}

.warning a:hover {
  text-decoration:  underline;
}

.form-container {
  background-color: white;
  border: 1px solid #e0e0e0;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-section {
  margin-bottom: 30px;
}

.form-section h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #333;
  font-size: 20px;
}

.section-description {
  margin-bottom: 20px;
  color: #666;
  font-size: 14px;
}

.members-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 400px;
  overflow-y:  auto;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #e9ecef;
}

.member-checkbox {
  background-color: white;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  padding: 12px 15px;
  transition: all 0.2s ease;
}

.member-checkbox:hover {
  background-color: #f8f9fa;
  border-color: #007BFF;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
  margin:  0;
  font-weight: normal;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  margin-right: 12px;
  cursor: pointer;
  accent-color: #007BFF;
  flex-shrink: 0;
}

.member-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.member-name {
  font-weight:  500;
  color: #333;
  font-size:  14px;
}

.member-position {
  color:  #666;
  font-size: 13px;
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
  margin-top:  30px;
}

.button-group.button {
  flex: 1;
}

.no-data-small {
  color: #666;
  font-style: italic;
  margin:  0;
  padding: 20px;
  text-align: center;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .form-container {
    padding: 20px;
  }

  .members-list {
    max-height: 300px;
  }

  .button-group {
    flex-direction: column;
  }

  .button-group.button {
    width: 100%;
  }
}
</style>