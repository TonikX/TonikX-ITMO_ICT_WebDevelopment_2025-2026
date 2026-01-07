<template>
  <div id="app">
        <nav v-if="isAuthenticated" class="navbar">
      <div class="nav-content">
        <div class="nav-info">
          <div class="nav-info-item">
            <span class="label">Станция:</span>
            <span class="value">{{ companyTitle }}</span>
          </div>
          <div class="nav-info-item">
            <span class="label">Адрес:</span>
            <span class="value">{{ stationAddress }}</span>
          </div>
          <div class="nav-info-item">
            <span class="label">Пользователь:</span>
            <span class="value">{{ userData?.username }}</span>
          </div>
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
const stationAddress = computed(() => authStore.stationAddress)
const companyTitle = computed(() => authStore.companyTitle)
const userData = computed(() => authStore.userData)

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
  padding: 0.8rem 0;
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.nav-info {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.nav-info-item {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.nav-info-item .label {
  font-weight: bold;
  color: #ccc;
  font-size: 0.9rem;
}

.nav-info-item .value {
  color: white;
  font-size: 0.9rem;
}

.separator {
  color: #666;
  font-size: 0.9rem;
}

.logout-btn {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
  white-space: nowrap;
}

.logout-btn:hover {
  background-color: #c82333;
}

main {
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* Для адаптивности на мобильных устройствах */
@media (max-width: 768px) {
  .nav-content {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .nav-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .separator {
    display: none;
  }
  
  .logout-btn {
    align-self: flex-end;
    width: auto;
  }
}
</style>