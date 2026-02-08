<template>
  <div id="app">
    <header class="app-header">
      <h1>Система управления авиакомпанией</h1>

      <!-- Левая часть навигации: только для авторизованных -->
      <nav class="nav-left" v-if="isAuthenticated">
        <RouterLink to="/dashboard">Панель</RouterLink>
        <RouterLink to="/flights">Рейсы</RouterLink>
        <RouterLink to="/fleet">Флот</RouterLink>
        <RouterLink to="/staff">Сотрудники</RouterLink>
      </nav>

      <!-- Правая часть: auth / профиль -->
      <nav class="nav-right">
        <!-- Не авторизован: только вход/регистрация -->
        <template v-if="!isAuthenticated">
          <RouterLink to="/login">Вход</RouterLink>
          <RouterLink to="/register">Регистрация</RouterLink>
        </template>

        <!-- Авторизован: только профиль -->
        <template v-else>
          <RouterLink to="/profile">Профиль</RouterLink>
        </template>
      </nav>
    </header>

    <main class="app-main">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from "vue-router";
import { isAuthenticated } from "./auth";
</script>

<style scoped>
#app {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.app-header {
  padding: 12px 24px;
  background-color: #1976d2;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.nav-left,
.nav-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.nav-left a,
.nav-right a {
  color: white;
  text-decoration: none;
  font-weight: 500;
}

.nav-left a.router-link-active,
.nav-right a.router-link-active {
  text-decoration: underline;
}

.app-main {
  padding: 24px;
}
</style>