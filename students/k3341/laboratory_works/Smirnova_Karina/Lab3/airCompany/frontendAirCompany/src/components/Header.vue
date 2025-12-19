<template>
  <header class="main-header">
    <nav class="nav-bar">
      <router-link to="/routes" class="nav-link">Маршруты</router-link>
      <router-link to="/flights" class="nav-link">Рейсы</router-link>
      <router-link to="/airlines" class="nav-link">Компании</router-link>
      <router-link to="/planes" class="nav-link">Самолеты</router-link>
      <router-link to="/crews" class="nav-link">Команды</router-link>

      <template v-if="!isAuthenticated">
        <router-link to="/register" class="nav-link">Регистрация</router-link>
        <router-link to="/login" class="nav-link">Войти</router-link>
      </template>
      <template v-else>
        <router-link to="/profile" class="nav-link">Профиль</router-link>
        <button @click="logout" class="nav-link logout-button">Выход</button>
      </template>

      <button class="menu-button" @click="toggleSidebar">
        <span class="menu-icon">☰</span>
      </button>
    </nav>
    <div class="sidebar" v-if="showSidebar">
      <ul class="sidebar-links">
        <li><router-link to="/create-plane" @click="toggleSidebar">Создать самолет</router-link></li>
        <li><router-link to="/create-company" @click="toggleSidebar">Создать компанию</router-link></li>
        <li><router-link to="/create-route" @click="toggleSidebar">Создать маршрут</router-link></li>
        <li><router-link to="/create-flight" @click="toggleSidebar">Создать рейс</router-link></li>
        <li><router-link to="/create-crew-member" @click="toggleSidebar">Создать работника</router-link></li>
        <li><router-link to="/create-crew" @click="toggleSidebar">Создать команду</router-link></li>
      </ul>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Header',
  data() {
    return {
      showSidebar: false,
    };
  },
  methods: {
    toggleSidebar() {
      this.showSidebar = !this.showSidebar;
    },
    async logout() {
      try {
        await this.$store.dispatch('auth/logout');

        this.$router.push('/login');
      } catch (error) {
        console.error('Ошибка при выходе:', error);
      }
    },
  },
  computed: {
    isAuthenticated() {
      return !!this.$store.state.auth.token;
    },
  },
};
</script>

<style>
.main-header {
  background-color: #0f4c81;
  padding: 10px;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-bar {
  display: flex;
  align-items: center;
}

.nav-link {
  color: white;
  text-decoration: none;
  margin-right: 20px;
  font-size: 18px;
}

.nav-link:hover {
  text-decoration: underline;
}

.menu-button {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
}

.menu-icon {
  display: inline-block;
}

.sidebar {
  position: absolute;
  right: 10px;
  top: 50px;
  background-color: white;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  border-radius: 5px;
  padding: 10px;
  z-index: 10;
}

.sidebar-links {
  list-style: none;
  padding: 0;
}

.sidebar-links li {
  padding: 5px 10px;
}

.sidebar-links a {
  text-decoration: none;
  color: #0f4c81;
  font-size: 16px;
}

.sidebar-links a:hover {
  text-decoration: underline;
}
</style>