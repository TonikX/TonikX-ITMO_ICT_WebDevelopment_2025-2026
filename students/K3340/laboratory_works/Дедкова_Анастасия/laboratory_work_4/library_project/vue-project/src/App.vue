<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

const handleLogout = () => {
  auth.logout()
  router.push('/books')
}
</script>

<template>
  <div class="app-shell">
    <header class="main-header">
      <div class="header-inner">
        <div class="logo-block">
          <span class="logo-emoji">📚</span>
          <span class="logo-text">Библиотека</span>
        </div>

        <nav class="main-nav">
          <!-- всегда доступно -->
          <RouterLink to="/books" active-class="active-link">
            Книги
          </RouterLink>

          <!-- профиль только для авторизованных -->
          <RouterLink
            v-if="auth.isAuthenticated"
            to="/profile"
            active-class="active-link"
          >
            Профиль читателя
          </RouterLink>

          <!-- блок только для админа -->
          <template v-if="auth.isAdmin">
            <RouterLink to="/on-loan" active-class="active-link">
              Книги на руках
            </RouterLink>

            <RouterLink to="/manage-loans" active-class="active-link">
              Выдача книг
            </RouterLink>

            <RouterLink to="/copies" active-class="active-link">
              Экземпляры книг
            </RouterLink>

            <RouterLink to="/reports" active-class="active-link">
              Отчёты
            </RouterLink>
          </template>

          <template v-if="!auth.isAuthenticated">
            <RouterLink to="/login" active-class="active-link">
              Войти
            </RouterLink>
            <RouterLink to="/register" active-class="active-link">
              Регистрация
            </RouterLink>
          </template>

          <template v-else>
            <a
              v-if="auth.isAdmin"
              href="http://127.0.0.1:8000/admin/"
              class="admin-link"
              target="_blank"
            >
              Админка
            </a>

            <button class="logout-btn" @click="handleLogout">
              Выйти
            </button>
          </template>
        </nav>
      </div>
    </header>

    <main class="main-container">
      <RouterView />
    </main>
  </div>
</template>

<style>
:root {
  --max-page-width: 1200px;
}

.main-header {
  background: #4f46e5;
  color: white;
  box-shadow: 0 1px 4px rgba(15, 23, 42, 0.25);
  padding-block: 10px;
  position: sticky;
  top: 0;
  z-index: 20;
}

.header-inner {
  width: 100%;
  max-width: var(--max-page-width);
  margin: 0 auto;
  padding-inline: 28px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-block {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-emoji {
  font-size: 26px;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
}

.main-nav {
  display: flex;
  gap: 20px;
}

.main-nav a {
  font-size: 14px;
  font-weight: 500;
  color: #e0e7ff;
  text-decoration: none;
  transition:
    color 0.15s ease,
    border-color 0.15s ease,
    background-color 0.15s ease;
}

.main-nav a:hover {
  color: #ffffff;
}

.main-nav .active-link {
  color: #ffffff;
  border-bottom: 2px solid currentColor;
}

.admin-link {
  border-radius: 999px;
  padding: 4px 10px;
  background: rgba(15, 23, 42, 0.2);
}

.logout-btn {
  background: transparent;
  border: none;
  color: #e0e7ff;
  font: inherit;
  cursor: pointer;
  padding: 0;
}

.logout-btn:hover {
  color: #ffffff;
}

.main-container {
  max-width: var(--max-page-width);
  margin: 32px auto 48px;
  padding-inline: 28px;
}

@media (max-width: 600px) {
  .header-inner,
  .main-container {
    padding-inline: 16px;
  }
}
</style>
