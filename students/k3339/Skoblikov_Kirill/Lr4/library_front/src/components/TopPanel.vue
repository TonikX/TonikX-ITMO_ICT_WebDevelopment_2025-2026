<template>
  <header class="top-bar">
    <nav class="nav">
      <AppButton @click="go('/app/books')">Книги</AppButton>
      <AppButton @click="go('/app/readers')">Читатели</AppButton>
      <AppButton @click="go('/app/halls')">Залы</AppButton>
      <AppButton @click="go('/app/reading')">Чтение</AppButton>
      <AppButton @click="go('/app/stats')">Статистика</AppButton>
    </nav>

    <AppButton class="logout" @click="logout">
      Выйти
    </AppButton>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'
import AppButton from '@/components/UI/AppButton.vue'
import authAPI from '@/api/api.js'

const router = useRouter()

const go = (path) => {
  router.push(path)
}

const logout = async () => {
  try {
    await authAPI.logout();
  } catch (error) {
    console.warn('Logout error (ignored):', error.message);
  } finally {
    localStorage.removeItem('auth_token');
    await router.push('/login');
  }
};
</script>

<style scoped>
.top-bar {
  position: relative;
  height: 60px;
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(8px);
}

.nav {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 14px;
}

.logout {
  margin-left: auto;
  margin-right: 12px;
}
</style>