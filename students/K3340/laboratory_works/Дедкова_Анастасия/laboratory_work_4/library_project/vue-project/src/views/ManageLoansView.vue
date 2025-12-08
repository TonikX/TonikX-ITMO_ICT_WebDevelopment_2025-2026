<template>
  <div class="page">
    <section v-if="!isAdmin" class="card">
      <h1>Недостаточно прав</h1>
      <p class="subtitle">
        Страница выдачи книг доступна только администраторам.
      </p>
    </section>

    <template v-else>
      <header class="page-header">
        <div>
          <h1>Выдача и возврат книг</h1>
          <p class="subtitle">
            Здесь можно оформить выдачу книги читателю и принять уже выданные книги.
          </p>
        </div>
      </header>

      <!-- форма выдачи -->
      <section class="card">
        <h2>Выдать книгу</h2>
        <form class="form" @submit.prevent="createLoan">
          <div class="form-row">
            <label class="label">
              Читатель
              <select
                v-model="selectedReaderId"
                class="select"
                required
              >
                <option value="" disabled>Выберите читателя…</option>
                <option
                  v-for="r in readers"
                  :key="r.reader_id"
                  :value="r.reader_id"
                >
                  {{ r.full_name }} — билет {{ r.card_number }}
                </option>
              </select>
            </label>
          </div>

          <div class="form-row">
            <label class="label">
              Экземпляр книги
              <select
                v-model="selectedCopyId"
                class="select"
                required
              >
                <option value="" disabled>Выберите экземпляр…</option>
                <option
                  v-for="c in availableCopies"
                  :key="c.copy_id"
                  :value="c.copy_id"
                >
                  Экз. {{ c.copy_id }} — {{ c.book_title }} (зал {{ c.hall_name }})
                </option>
              </select>
            </label>
          </div>

          <div class="form-actions">
            <button
              type="submit"
              class="primary-btn"
              :disabled="issueLoading || !selectedReaderId || !selectedCopyId"
            >
              <span v-if="issueLoading">Оформляем…</span>
              <span v-else>Выдать книгу</span>
            </button>
          </div>
        </form>

        <p v-if="issueError" class="status status-error">
          {{ issueError }}
        </p>
        <p v-if="issueSuccess" class="status status-ok">
          {{ issueSuccess }}
        </p>
      </section>

      <!-- активные выдачи -->
      <section class="card">
        <div class="card-header">
          <h2>Книги на руках</h2>
          <button
            class="secondary-btn"
            type="button"
            @click="loadActiveLoans"
            :disabled="loansLoading"
          >
            Обновить список
          </button>
        </div>

        <p v-if="loansError" class="status status-error">
          {{ loansError }}
        </p>

        <p v-else-if="loansLoading" class="status status-loading">
          Загружаем активные выдачи…
        </p>

        <p v-else-if="!activeLoans.length" class="status status-empty">
          Сейчас нет активных выдач.
        </p>

        <table v-else class="table">
          <thead>
            <tr>
              <th>ID выдачи</th>
              <th>Экз.</th>
              <th>Книга</th>
              <th>Читатель</th>
              <th>Зал</th>
              <th>Дней на руках</th>
              <th>Действие</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="loan in activeLoans" :key="loan.loan_id">
              <td>{{ loan.loan_id }}</td>
              <td>{{ loan.copy_id }}</td>
              <td>{{ loan.book.title }}</td>
              <td>{{ loan.reader.full_name }}</td>
              <td>{{ loan.hall }}</td>
              <td>{{ loan.days_on_loan }}</td>
              <td>
                <button
                  class="danger-btn"
                  type="button"
                  @click="returnLoan(loan)"
                  :disabled="returningId === loan.loan_id"
                >
                  <span v-if="returningId === loan.loan_id">Принимаем…</span>
                  <span v-else>Принять книгу</span>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </section>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import apiClient from '@/api/client'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const isAdmin = computed(() => auth.isAdmin)

const readers = ref([])
const availableCopies = ref([])

const selectedReaderId = ref('')
const selectedCopyId = ref('')

const issueLoading = ref(false)
const issueError = ref(null)
const issueSuccess = ref(null)

const activeLoans = ref([])
const loansLoading = ref(false)
const loansError = ref(null)
const returningId = ref(null)

const loadReaders = async () => {
  try {
    const resp = await apiClient.get('readers/')
    const data = resp.data
    const items = Array.isArray(data?.results) ? data.results : data
    readers.value = items || []
  } catch (e) {
    console.error(e)
  }
}

// загрузка экземпляров книг и фильтр по статусу
const loadCopies = async () => {
  try {
    const resp = await apiClient.get('copies/')
    const data = resp.data
    const items = Array.isArray(data?.results) ? data.results : data
    const all = items || []

    availableCopies.value = all
      .filter(c => c.status === 'available')
      .map(c => ({
        copy_id: c.copy_id,
        hall_name: c.hall_name || (c.hall && c.hall.name) || '',
        book_title:
          c.book_title ||
          (c.book && (c.book.title || '')) ||
          `Книга ${c.book}`,
      }))
  } catch (e) {
    console.error(e)
  }
}

// загрузка активных выдач
const loadActiveLoans = async () => {
  loansLoading.value = true
  loansError.value = null
  try {
    const resp = await apiClient.get('loans/active/')
    activeLoans.value = resp.data || []
  } catch (e) {
    console.error(e)
    loansError.value = 'Не удалось загрузить список активных выдач.'
  } finally {
    loansLoading.value = false
  }
}

const createLoan = async () => {
  if (!selectedReaderId.value || !selectedCopyId.value) return

  issueLoading.value = true
  issueError.value = null
  issueSuccess.value = null

  try {
    await apiClient.post('loans/', {
      reader: selectedReaderId.value,
      copy: selectedCopyId.value,
    })

    issueSuccess.value = 'Книга успешно выдана.'
    // сбрасываем форму
    selectedCopyId.value = ''
    // обновляем списки
    await Promise.all([loadCopies(), loadActiveLoans()])
  } catch (e) {
    console.error(e)
    const resp = e.response || null
    if (resp && resp.data && resp.data.detail) {
      issueError.value = resp.data.detail
    } else {
      issueError.value = 'Не удалось оформить выдачу. Попробуйте позже.'
    }
  } finally {
    issueLoading.value = false
  }
}

const returnLoan = async (loan) => {
  if (!loan || !loan.loan_id) return

  if (!confirm(`Принять книгу "${loan.book.title}" от читателя ${loan.reader.full_name}?`)) {
    return
  }

  returningId.value = loan.loan_id

  try {
    const nowIso = new Date().toISOString()
    await apiClient.patch(`loans/${loan.loan_id}/`, {
      returned_at: nowIso,
    })

    await Promise.all([loadCopies(), loadActiveLoans()])
  } catch (e) {
    console.error(e)
    alert('Не удалось принять книгу. Попробуйте ещё раз.')
  } finally {
    returningId.value = null
  }
}

onMounted(() => {
  if (!isAdmin.value) return
  loadReaders()
  loadCopies()
  loadActiveLoans()
})
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
  margin-bottom: 20px;
}

h1 {
  font-size: 28px;
  font-weight: 700;
  margin: 0;
}

h2 {
  font-size: 18px;
  margin: 0 0 12px;
}

.subtitle {
  margin-top: 4px;
  font-size: 14px;
  color: #64748b;
}

.card {
  background: white;
  border-radius: 18px;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
  border: 1px solid #e2e8f0;
  padding: 20px 18px;
  margin-bottom: 16px;
}

.form {
  display: flex;
  flex-wrap: wrap;
  gap: 12px 24px;
  align-items: flex-end;
}

.form-row {
  flex: 1 1 260px;
}

.label {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 14px;
  color: #475569;
}

.select {
  padding: 9px 12px;
  border-radius: 999px;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  font-size: 14px;
  outline: none;
  transition: border-color 0.12s ease, box-shadow 0.12s ease, background 0.12s ease;
}

.select:focus {
  border-color: #6366f1;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
}

.form-actions {
  display: flex;
  align-items: center;
}


.primary-btn {
  border: none;
  background: linear-gradient(135deg, #4f46e5, #6366f1);
  color: white;
  padding: 9px 18px;
  border-radius: 999px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 20px rgba(79, 70, 229, 0.35);
  transition: transform 0.12s ease, box-shadow 0.12s ease, opacity 0.12s ease;
}

.primary-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 14px 28px rgba(79, 70, 229, 0.4);
}

.primary-btn:disabled {
  opacity: 0.65;
  cursor: default;
  transform: none;
  box-shadow: 0 6px 14px rgba(148, 163, 184, 0.4);
}

.secondary-btn {
  border-radius: 999px;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  padding: 6px 14px;
  font-size: 13px;
  cursor: pointer;
}

.secondary-btn:hover {
  background: #eef2ff;
}

.danger-btn {
  border-radius: 999px;
  border: none;
  padding: 6px 12px;
  font-size: 13px;
  cursor: pointer;
  background: #fee2e2;
  color: #b91c1c;
}

.danger-btn:disabled {
  opacity: 0.6;
  cursor: default;
}

/* статусы */

.status {
  margin-top: 10px;
  font-size: 14px;
  padding: 8px 10px;
  border-radius: 12px;
}

.status-error {
  background: #fef2f2;
  color: #b91c1c;
}

.status-ok {
  background: #ecfdf5;
  color: #15803d;
}

.status-loading {
  background: #eff6ff;
  color: #1d4ed8;
}

.status-empty {
  color: #64748b;
}

.table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.table th,
.table td {
  padding: 10px 12px;
  border-bottom: 1px solid #e2e8f0;
  text-align: left;
}

.table thead {
  background: #f8fafc;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

@media (max-width: 800px) {
  .form {
    flex-direction: column;
    align-items: stretch;
  }

  .form-actions {
    justify-content: flex-start;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>
