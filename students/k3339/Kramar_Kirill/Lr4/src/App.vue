<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import TokenStore from "./stores/token";

const isAuthenticated = ref(false);
const route = useRoute();

onMounted(() => {
  isAuthenticated.value = TokenStore.isAuthenticated();
});

const handleLogout = () => {
  TokenStore.removeToken();
  isAuthenticated.value = false;
};

const handleLogin = () => {
  isAuthenticated.value = true;
};
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/teachers" class="nav-item">Teachers</RouterLink>
        <RouterLink to="/students" class="nav-item">Students</RouterLink>
        <RouterLink to="/classes" class="nav-item">Classes</RouterLink>
        <RouterLink to="/classrooms" class="nav-item">Classrooms</RouterLink>
        <RouterLink to="/lessons" class="nav-item">Schedule</RouterLink>
        <RouterLink to="/grades" class="nav-item">Grades</RouterLink>
        <RouterLink v-if="!isAuthenticated" to="/login" class="nav-item">Login</RouterLink>
        <RouterLink v-if="!isAuthenticated" to="/register" class="nav-item">Register</RouterLink>
        <RouterLink v-if="isAuthenticated" to="/profile" class="nav-item">Profile</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView :key="route.fullPath" @logout="handleLogout" @login="handleLogin" />
</template>

<style scoped>
header {
  background-color: #f8f9fa;
  padding: 10px 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

nav {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  gap: 20px;
}

.nav-item {
  text-decoration: none;
  color: #333;
  font-size: 16px;
  font-weight: 600;
  padding: 10px 20px;
  border-radius: 5px;
  transition: background-color 0.3s, color 0.3s;
}

.nav-item:hover,
.nav-item.router-link-exact-active {
  background-color: #007bff;
  color: white;
}

.nav-item.router-link-exact-active {
  background-color: #0056b3;
}

@media (max-width: 768px) {
  nav {
    flex-direction: column;
    align-items: flex-start;
  }

  .nav-item {
    font-size: 14px;
    width: 100%;
    padding: 12px;
    text-align: left;
  }
}
</style>
