<template>
  <div class="page">
    <!-- шапка страницы -->
    <header class="page-header">
      <div>
        <h1>Каталог книг</h1>
        <p class="subtitle">
          Список книг из вашей библиотеки. Можно фильтровать, искать и обновлять данные.
        </p>
      </div>

      <button
        class="primary-btn"
        @click="loadBooks"
        :disabled="loading"
      >
        <span v-if="loading">Загружаем…</span>
        <span v-else>Обновить список</span>
      </button>
    </header>

    <!-- панель фильтров -->
    <section class="filters">
      <div class="search-wrapper">
        <input
          v-model="searchQuery"
          type="search"
          class="search-input"
          placeholder="Поиск по названию, автору или разделу…"
        />
      </div>
    </section>

    <p v-if="error" class="status status-error">
      {{ error }}
    </p>
    <p v-else-if="loading" class="status status-loading">
      Загружаем книги…
    </p>

    <section v-if="!loading && !error">
      <div v-if="filteredBooks.length" class="card">
        <table class="table">
          <thead>
            <tr>
              <th>Название</th>
              <th>Авторы</th>
              <th>Год</th>
              <th>Издательство</th>
              <th>Раздел</th>
              <!-- зал виден всем авторизованным -->
              <th v-if="auth.isAuthenticated">Зал</th>
              <!-- статус только для админа -->
              <th v-if="auth.isAdmin">Статус</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="book in filteredBooks"
              :key="book.book_id"
            >
              <td class="cell-title">
                <div class="title-main">{{ book.title }}</div>
              </td>

              <td>
                <span v-if="book.authors && book.authors.length">
                  {{ book.authors.map(a => a.full_name).join(', ') }}
                </span>
                <span v-else class="muted">—</span>
              </td>

              <td>{{ book.publication_year }}</td>
              <td>{{ book.publisher }}</td>
              <td>{{ book.section }}</td>

              <td v-if="auth.isAuthenticated">
                <span v-if="book.halls && book.halls.length">
                  {{ book.halls.join(', ') }}
                </span>
                <span v-else class="muted">—</span>
              </td>

              <td v-if="auth.isAdmin">
                <span
                  class="badge"
                  :class="book.is_active ? 'badge-ok' : 'badge-bad'"
                >
                  {{ book.is_active ? 'В наличии' : 'Нет в наличии' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <p v-else class="status status-empty">
        Книг пока нет. Попробуйте нажать «Обновить список» или добавить книги через админку.
      </p>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import apiClient from '@/api/client'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

const books = ref([])
const loading = ref(false)
const error = ref(null)

const searchQuery = ref('')
const adminStatusFilter = ref('all')

const loadBooks = async () => {
  loading.value = true
  error.value = null
  try {
    const config = {}

    if (auth.token) {
      config.headers = {
        Authorization: `Bearer ${auth.token}`,
      }
    }

    const response = await apiClient.get('books/', config)
    const data = response.data
    books.value = Array.isArray(data?.results) ? data.results : data
  } catch (e) {
    console.error(e)
    error.value = 'Не удалось загрузить список книг. Попробуйте обновить страницу позже.'
  } finally {
    loading.value = false
  }
}


const filteredBooks = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()

  return books.value
    .filter((book) => {
      //  Не админ (гость или обычный пользователь): показываем только книги "в наличии"
      if (!auth.isAdmin && !book.is_active) {
        return false
      }

      // Поиск
      if (!q) return true

      const inTitle = book.title?.toLowerCase().includes(q)
      const inSection = book.section?.toLowerCase().includes(q)
      const inPublisher = book.publisher?.toLowerCase().includes(q)
      const authors = (book.authors || [])
        .map((a) => a.full_name?.toLowerCase() || '')
        .join(' ')
      const inAuthors = authors.includes(q)

      return inTitle || inSection || inPublisher || inAuthors
    })
    .sort((a, b) => a.title.localeCompare(b.title, 'ru'))
})


onMounted(loadBooks)
</script>

<style scoped>
.page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 16px 48px;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  color: #0f172a;
}

/* header */

.page-header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 24px;
}

h1 {
  font-size: 28px;
  font-weight: 700;
  margin: 0;
}

.subtitle {
  margin-top: 4px;
  font-size: 14px;
  color: #64748b;
}


.primary-btn {
  border: none;
  background: linear-gradient(135deg, #4f46e5, #6366f1);
  color: white;
  padding: 10px 18px;
  border-radius: 999px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  box-shadow: 0 10px 20px rgba(79, 70, 229, 0.35);
  transition: transform 0.12s ease, box-shadow 0.12s ease, opacity 0.12s ease;
}

.primary-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 14px 28px rgba(79, 70, 229, 0.4);
}

.primary-btn:active {
  transform: translateY(0);
  box-shadow: 0 6px 14px rgba(79, 70, 229, 0.35);
}

.primary-btn:disabled {
  opacity: 0.65;
  cursor: default;
  transform: none;
  box-shadow: 0 6px 14px rgba(148, 163, 184, 0.4);
}


.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 12px 20px;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.search-wrapper {
  flex: 1 1 220px;
  max-width: 420px;
}

.search-input {
  width: 100%;
  padding: 9px 12px;
  border-radius: 999px;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  font-size: 14px;
  outline: none;
  transition: border-color 0.12s ease, box-shadow 0.12s ease, background 0.12s ease;
}

.search-input::placeholder {
  color: #94a3b8;
}

.search-input:focus {
  border-color: #6366f1;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
}


.status {
  margin: 8px 0 16px;
  font-size: 14px;
  padding: 10px 12px;
  border-radius: 12px;
}

.status-loading {
  background: #eff6ff;
  color: #1d4ed8;
}

.status-error {
  background: #fef2f2;
  color: #b91c1c;
}

.status-empty {
  color: #64748b;
}


.card {
  width: 100%;
  max-width: 1200px;
  background: white;
  border-radius: 18px;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
  overflow: hidden;
  border: 1px solid #e2e8f0;
}

/* таблица */

.table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.table thead {
  background: #f8fafc;
}

.table th,
.table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.table th {
  font-weight: 600;
  color: #475569;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.table tbody tr:hover {
  background: #f9fafb;
}

.cell-title .title-main {
  font-weight: 600;
  color: #0f172a;
}

.muted {
  color: #94a3b8;
}


.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
}

.badge-ok {
  background: #dcfce7;
  color: #166534;
}

.badge-bad {
  background: #fee2e2;
  color: #991b1b;
}

@media (max-width: 768px) {
  .page {
    padding-inline: 12px;
  }

  .table th:nth-child(4),
  .table td:nth-child(4),
  .table th:nth-child(5),
  .table td:nth-child(5) {
    display: none;
  }
}
</style>
