<template>
  <div class="page">
    <!-- шапка страницы -->
    <header class="page-header">
      <div>
        <h1>Книги на руках</h1>
        <p class="subtitle">
          Список экземпляров, которые сейчас находятся на руках у читателей.
        </p>
      </div>

      <button
        class="primary-btn"
        @click="loadLoans"
        :disabled="loading"
      >
        <span v-if="loading">Загружаем…</span>
        <span v-else>Обновить список</span>
      </button>
    </header>

    <p v-if="error" class="status status-error">
      {{ error }}
    </p>
    <p v-else-if="loading" class="status status-loading">
      Загружаем список выдач…
    </p>

    <section v-if="!loading && !error">
      <div v-if="loans.length" class="card">
        <table class="table">
          <thead>
            <tr>
              <th>ID экз.</th>
              <th>Название</th>
              <th>Авторы</th>
              <th>Зал</th>
              <th>Читатель</th>
              <th>Сколько дней на руках</th>
              <th>Статус</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="loan in loans"
              :key="loan.loan_id"
            >
              <td>{{ loan.copy_id }}</td>

              <!-- Название книги -->
              <td>
                <span v-if="loan.book && loan.book.title">
                  {{ loan.book.title }}
                </span>
                <span v-else class="muted">—</span>
              </td>

              <!-- Авторы -->
              <td>
                <span
                  v-if="loan.book && loan.book.authors && loan.book.authors.length"
                >
                  {{ loan.book.authors.join(', ') }}
                </span>
                <span v-else class="muted">—</span>
              </td>

              <!-- Зал -->
              <td>
                <span v-if="loan.hall">
                  {{ loan.hall }}
                </span>
                <span v-else class="muted">—</span>
              </td>

              <!-- Читатель -->
              <td>
                <span v-if="loan.reader && loan.reader.full_name">
                  {{ loan.reader.full_name }}
                </span>
                <span v-else class="muted">—</span>
              </td>

              <!-- Сколько дней на руках -->
              <td>
                <span v-if="loan.days_on_loan !== null && loan.days_on_loan !== undefined">
                  {{ loan.days_on_loan }} дн.
                </span>
                <span v-else class="muted">—</span>
              </td>

              <!-- Статус -->
              <td>
                <span
                  class="badge badge-bad"
                >
                  На руках
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <p v-else class="status status-empty">
        Сейчас нет книг на руках.
      </p>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/api/client'

const loans = ref([])
const loading = ref(false)
const error = ref(null)

const loadLoans = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await apiClient.get('loans/active/')
    loans.value = response.data
  } catch (e) {
    console.error(e)
    error.value = 'Не удалось загрузить список. Попробуйте обновить страницу позже.'
  } finally {
    loading.value = false
  }
}

onMounted(loadLoans)
</script>

<style scoped>
.page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 16px 48px;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  color: #0f172a;
}

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

.badge-bad {
  background: #fee2e2;
  color: #b91c1c;
}
</style>
