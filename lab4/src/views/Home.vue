<template>
  <div class="home-page">
    <h1>Добро пожаловать в систему управления хакатонами</h1>
    <div v-if="!isAuthenticated" class="home-content">
      <p>Для начала работы необходимо войти в систему или зарегистрироваться.</p>
      <div class="home-actions">
        <router-link to="/login" class="btn">Войти</router-link>
        <router-link to="/register" class="btn btn-secondary">Регистрироваться</router-link>
      </div>
    </div>
    <div v-else class="home-content">
      <p>Вы вошли как: <strong>{{ user?.username }}</strong></p>
      <p>Роль: <strong>{{ getRoleDisplay(user?.role) }}</strong></p>
      <div class="home-actions">
        <router-link to="/profile" class="btn btn-secondary">Редактировать профиль</router-link>
      </div>
      <div class="home-links">
        <router-link to="/tasks" class="home-link">
          <h3>Задачи</h3>
          <p>Просмотр и управление задачами хакатона</p>
        </router-link>
        <router-link to="/teams" class="home-link">
          <h3>Команды</h3>
          <p>Управление командами и участниками</p>
        </router-link>
        <router-link to="/solutions" class="home-link">
          <h3>Решения</h3>
          <p>Просмотр решений команд</p>
        </router-link>
        <router-link v-if="isJury" to="/evaluations" class="home-link">
          <h3>Оценки</h3>
          <p>Оценивание решений</p>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem('authToken')
    },
    user() {
      const userStr = localStorage.getItem('user')
      return userStr ? JSON.parse(userStr) : null
    },
    isJury() {
      return this.user?.role === 'jury'
    }
  },
  methods: {
    getRoleDisplay(role) {
      const roles = {
        admin: 'Администратор',
        captain: 'Капитан',
        curator: 'Куратор',
        jury: 'Жюри'
      }
      return roles[role] || role
    }
  }
}
</script>

<style scoped>
.home-page {
  max-width: 1000px;
  margin: 0 auto;
}

.home-page h1 {
  text-align: center;
  color: #2d7ef7;
  margin-bottom: 2rem;
}

.home-content {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.home-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.home-links {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.home-link {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  text-decoration: none;
  color: inherit;
  transition: transform 0.2s, box-shadow 0.2s;
}

.home-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.home-link h3 {
  margin: 0 0 0.5rem 0;
  color: #2d7ef7;
}

.home-link p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.btn-secondary {
  background: #6c757d;
}

.btn-secondary:hover {
  background: #5a6268;
}
</style>
