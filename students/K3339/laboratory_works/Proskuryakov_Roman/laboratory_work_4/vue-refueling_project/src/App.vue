<template>
  <div id="app">
    <nav v-if="isAuthenticated" class="navbar">
      <div class="nav-content">
        <div class="nav-info">
          <span>Станция: {{ stationAddress }}</span>
        </div>
        <button @click="handleLogout" class="logout-btn">
          Выйти
        </button>
      </div>
    </nav>
    
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()

const isAuthenticated = computed(() => authStore.isAuthenticated)
const stationAddress = computed(() => authStore.stationAddress || 'Не назначена')

const handleLogout = () => {
  authStore.logout()
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
}

.navbar {
  background-color: #333;
  color: white;
  padding: 1rem;
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.logout-btn {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.logout-btn:hover {
  background-color: #c82333;
}

main {
  padding: 1rem;
}
</style>