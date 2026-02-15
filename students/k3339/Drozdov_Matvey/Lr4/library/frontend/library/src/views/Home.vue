<template>
  <div class="page">
    <header class="top">
      <div>
        <h1 class="title">Главная</h1>
        <div class="subtitle">
          Добро пожаловать, <b>{{ auth.username }}</b>
        </div>
      </div>

      <button class="btn danger" @click="logout" title="Выйти из аккаунта">
        Выйти
      </button>
    </header>

    <section class="grid">
      <router-link class="card" to="/books">
        <div class="icon">📚</div>
        <div class="card-title">Книги</div>
        <div class="card-sub">Каталог, шифры, фонд по залам</div>
      </router-link>

      <router-link class="card" to="/readers">
        <div class="icon">👤</div>
        <div class="card-title">Читатели</div>
        <div class="card-sub">Профили, билеты, залы, членство</div>
      </router-link>

      <router-link class="card" to="/halls">
        <div class="icon">🏛</div>
        <div class="card-title">Залы</div>
        <div class="card-sub">Вместимость, читатели, фонд</div>
      </router-link>

      <router-link class="card" to="/circulation">
        <div class="icon">🔄</div>
        <div class="card-title">Выдача / Возврат</div>
        <div class="card-sub">Оформление выдач и возвратов</div>
      </router-link>

      <router-link class="card" to="/reports">
        <div class="icon">📊</div>
        <div class="card-title">Отчёты</div>
        <div class="card-sub">Аналитика, просрочки, статистика</div>
      </router-link>
    </section>

  </div>
</template>

<script setup>
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

const auth = useAuthStore();
const router = useRouter();

function logout() {
  auth.logout();
  router.push("/login");
}
</script>

<style scoped>
.page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 16px 14px 28px;
}

.top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 12px 16px;
  border: 1px solid #ddd;
  background: #fff;
}

.title {
  margin: 0;
  font-size: 28px;
}

.subtitle {
  margin-top: 6px;
  opacity: 0.85;
}

.grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(240px, 1fr));
  gap: 12px;
  margin-top: 12px;
}

.card {
  display: block;
  border: 1px solid #ddd;
  padding: 14px;
  text-decoration: none;
  color: inherit;
  background: #fff;
  transition: transform 0.08s ease, border-color 0.08s ease;
}

.card:hover {
  transform: translateY(-1px);
  border-color: teal;
}

.icon {
  font-size: 26px;
}

.card-title {
  margin-top: 10px;
  font-size: 18px;
  font-weight: 700;
}

.card-sub {
  margin-top: 6px;
  font-size: 14px;
  opacity: 0.8;
  line-height: 1.35;
}

.btn {
  padding: 8px 12px;
  border: 1px solid teal;
  background: #fff;
  cursor: pointer;
}

.btn:hover {
  border-color: #0a8;
}

.danger {
  border-color: #c00;
}

.danger:hover {
  border-color: #a00;
}

.footer {
  margin-top: 14px;
  padding: 10px 2px 0;
}

.muted {
  opacity: 0.6;
  font-size: 13px;
}

@media (max-width: 920px) {
  .grid {
    grid-template-columns: repeat(2, minmax(240px, 1fr));
  }
}

@media (max-width: 560px) {
  .grid {
    grid-template-columns: 1fr;
  }
  .top {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>