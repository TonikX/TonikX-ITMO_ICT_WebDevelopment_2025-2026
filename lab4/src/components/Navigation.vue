<template>
  <nav class="navigation">
    <div class="nav-container">
      <router-link to="/" class="nav-logo">Хакатон</router-link>
      <div class="nav-links">
        <template v-if="isAuthenticated">
          <router-link to="/profile" class="nav-link">Профиль</router-link>
          <router-link to="/tasks" class="nav-link">Задачи</router-link>
          <router-link to="/teams" class="nav-link">Команды</router-link>
          <router-link to="/solutions" class="nav-link">Решения</router-link>
          <router-link v-if="isJury" to="/evaluations" class="nav-link">Оценки</router-link>
          <span class="nav-user">{{ currentUser?.username }}</span>
          <button @click="handleLogout" class="btn btn-secondary">Выход</button>
        </template>
        <template v-else>
          <router-link to="/login" class="nav-link">Вход</router-link>
          <router-link to="/register" class="nav-link">Регистрация</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script>
import { authAPI } from '@/api'

function readCurrentUserFromStorage() {
  const userStr = localStorage.getItem('user')
  try {
    return userStr ? JSON.parse(userStr) : null
  } catch (_e) {
    return null
  }
}

export default {
  name: 'Navigation',
  data() {
    return {
      authToken: localStorage.getItem('authToken') || '',
      currentUser: readCurrentUserFromStorage()
    }
  },
  computed: {
    isAuthenticated() {
      return !!this.authToken
    },
    isJury() {
      return this.currentUser?.role === 'jury'
    }
  },
  mounted() {
    window.addEventListener('storage', this.syncAuthState)
    window.addEventListener('auth-changed', this.syncAuthState)
  },
  beforeUnmount() {
    window.removeEventListener('storage', this.syncAuthState)
    window.removeEventListener('auth-changed', this.syncAuthState)
  },
  methods: {
    readCurrentUser() {
      return readCurrentUserFromStorage()
    },
    syncAuthState() {
      this.authToken = localStorage.getItem('authToken') || ''
      this.currentUser = this.readCurrentUser()
    },
    async handleLogout() {
      try {
        await authAPI.logout()
      } catch (e) {
        console.error('Ошибка при выходе:', e)
      }
      localStorage.removeItem('authToken')
      localStorage.removeItem('user')
      window.dispatchEvent(new Event('auth-changed'))
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.navigation {
  background: #2d7ef7;
  color: white;
  padding: 1rem 0;
  margin-bottom: 2rem;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background 0.2s;
}

.nav-link:hover,
.nav-link.router-link-active {
  background: rgba(255, 255, 255, 0.2);
}

.nav-user {
  padding: 0.5rem 1rem;
  font-weight: 500;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.2);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.3);
}
</style>
