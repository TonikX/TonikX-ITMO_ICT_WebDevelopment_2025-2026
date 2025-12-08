<template>
  <div class="page">
    <header class="page-header">
      <div>
        <h1>Экземпляры книг</h1>
        <p class="subtitle">
          Здесь можно добавлять новые экземпляры книг и списывать существующие
          (доступно только администратору).
        </p>
      </div>

      <!-- Кнопка для создания новой книги в админке -->
      <a
        href="http://127.0.0.1:8000/admin/library_app/book/add/"
        target="_blank"
        class="primary-btn add-book-btn"
      >
        ➕ Добавить новую книгу
      </a>
    </header>

    <!-- Форма добавления экземпляра -->
    <section class="card">
      <h2>Добавить экземпляр книги</h2>

      <form class="form" @submit.prevent="createCopy">
        <div class="form-row">
          <label class="label">
            Книга
            <select v-model="newCopy.book" class="input" required>
              <option value="" disabled>Выберите книгу…</option>
              <option
                v-for="b in books"
                :key="b.book_id || b.id"
                :value="b.book_id || b.id"
              >
                {{ b.title }} ({{ b.publication_year }})
              </option>
            </select>
          </label>
        </div>

        <div class="form-row">
          <label class="label">
            Зал
            <select v-model="newCopy.hall" class="input" required>
              <option value="" disabled>Выберите зал…</option>
              <option
                v-for="h in halls"
                :key="h.hall_id || h.id"
                :value="h.hall_id || h.id"
              >
                {{ h.number }} — {{ h.name }}
              </option>
            </select>
          </label>
        </div>

        <div class="form-row">
          <label class="label">
            Дата поступления
            <input
              v-model="newCopy.date_received"
              type="date"
              class="input"
              required
            />
          </label>
        </div>

        <div class="form-actions">
          <button type="submit" class="primary-btn" :disabled="creating">
            <span v-if="creating">Сохраняем…</span>
            <span v-else>Добавить экземпляр</span>
          </button>
        </div>
      </form>

      <p v-if="createError" class="status status-error">
        {{ createError }}
      </p>
      <p v-if="createSuccess" class="status status-success">
        Экземпляр успешно добавлен.
      </p>
    </section>

    <!-- Таблица всех экземпляров -->
    <section class="card">
      <div class="table-header">
        <h2>Все экземпляры</h2>
        <div class="table-controls">
          <select v-model="statusFilter" class="input small-input">
            <option value="all">Все статусы</option>
            <option value="available">Доступен</option>
            <option value="on_loan">На руках</option>
            <option value="written_off">Списан</option>
          </select>

          <button
            type="button"
            class="secondary-btn"
            @click="loadCopies"
            :disabled="loadingCopies"
          >
            <span v-if="loadingCopies">Обновляем…</span>
            <span v-else>Обновить список</span>
          </button>
        </div>
      </div>

      <p v-if="copiesError" class="status status-error">
        {{ copiesError }}
      </p>

      <p
        v-else-if="!loadingCopies && !filteredCopies.length"
        class="status status-empty"
      >
        Экземпляров не найдено.
      </p>

      <table v-else class="table">
        <thead>
          <tr>
            <th>ID экз.</th>
            <th>Книга</th>
            <th>Зал</th>
            <th>Статус</th>
            <th>Дата поступления</th>
            <th>Дата списания</th>
            <th>Действие</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in filteredCopies" :key="c.copy_id || c.id">
            <td>{{ c.copy_id || c.id }}</td>
            <td>
              {{ c.book?.title || '—' }}
              <span v-if="c.book?.publication_year">
                ({{ c.book.publication_year }})
              </span>
            </td>
            <td>{{ c.hall?.name || '—' }}</td>
            <td>
              <span :class="['badge', badgeClass(c.status)]">
                {{ statusLabel(c.status) }}
              </span>
            </td>
            <td>{{ c.date_received }}</td>
            <td>{{ c.date_written_off || '—' }}</td>
            <td>
              <button
                class="danger-btn"
                type="button"
                @click="writeOff(c)"
                :disabled="
                  c.status === 'written_off' ||
                  writingOffId === (c.copy_id || c.id)
                "
              >
                <span v-if="writingOffId === (c.copy_id || c.id)">
                  Списываем…
                </span>
                <span v-else>
                  {{ c.status === 'written_off' ? 'Списан' : 'Списать' }}
                </span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import apiClient from '@/api/client'

const books = ref([])
const halls = ref([])

const copies = ref([])
const loadingCopies = ref(false)
const copiesError = ref(null)
const statusFilter = ref('all')

const newCopy = ref({
  book: '',
  hall: '',
  date_received: new Date().toISOString().slice(0, 10),
})
const creating = ref(false)
const createError = ref(null)
const createSuccess = ref(false)

const writingOffId = ref(null)

const loadDictionaries = async () => {
  try {
    const [booksResp, hallsResp] = await Promise.all([
      apiClient.get('books/'),
      apiClient.get('halls/'),
    ])

    const booksData = booksResp.data
    books.value = booksData.results ? booksData.results : booksData

    const hallsData = hallsResp.data
    halls.value = hallsData.results ? hallsData.results : hallsData
  } catch (e) {
    console.error('Ошибка при загрузке справочников', e)
  }
}

const loadCopies = async () => {
  loadingCopies.value = true
  copiesError.value = null
  try {
    const resp = await apiClient.get('copies/')
    const data = resp.data
    copies.value = data.results ? data.results : data
  } catch (e) {
    console.error(e)
    copiesError.value = 'Не удалось загрузить список экземпляров.'
  } finally {
    loadingCopies.value = false
  }
}

const createCopy = async () => {
  createError.value = null
  createSuccess.value = false
  creating.value = true

  try {
    const payload = {
      book: newCopy.value.book,
      hall: newCopy.value.hall,
      status: 'available',
      date_received: newCopy.value.date_received,
    }

    await apiClient.post('copies/', payload)

    createSuccess.value = true
    await loadCopies()

    newCopy.value.book = ''
    newCopy.value.hall = ''
  } catch (e) {
    console.error(e)
    if (e.response?.data) {
      const data = e.response.data
      const msgs = []
      for (const [field, msg] of Object.entries(data)) {
        if (Array.isArray(msg)) msgs.push(`${field}: ${msg.join(', ')}`)
        else msgs.push(String(msg))
      }
      createError.value = msgs.join(' | ')
    } else {
      createError.value = 'Не удалось создать экземпляр. Попробуйте позже.'
    }
  } finally {
    creating.value = false
  }
}

const writeOff = async (copy) => {
  const id = copy.copy_id || copy.id
  if (!id) return
  if (copy.status === 'written_off') return

  if (!confirm('Списать этот экземпляр книги?')) return

  writingOffId.value = id
  try {
    const today = new Date().toISOString().slice(0, 10)
    const payload = {
      status: 'written_off',
      date_written_off: today,
    }
    await apiClient.patch(`copies/${id}/`, payload)
    await loadCopies()
  } catch (e) {
    console.error(e)
    alert('Не удалось списать экземпляр. Попробуйте позже.')
  } finally {
    writingOffId.value = null
  }
}

const filteredCopies = computed(() => {
  if (statusFilter.value === 'all') return copies.value
  return copies.value.filter((c) => c.status === statusFilter.value)
})

const statusLabel = (status) => {
  switch (status) {
    case 'available':
      return 'Доступен'
    case 'on_loan':
      return 'На руках'
    case 'written_off':
      return 'Списан'
    default:
      return status || '—'
  }
}

const badgeClass = (status) => {
  switch (status) {
    case 'available':
      return 'badge-ok'
    case 'on_loan':
      return 'badge-warn'
    case 'written_off':
      return 'badge-bad'
    default:
      return ''
  }
}

onMounted(() => {
  loadDictionaries()
  loadCopies()
})
</script>

<style scoped>
.page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 16px 48px;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI',
    sans-serif;
  color: #0f172a;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

h1 {
  font-size: 26px;
  font-weight: 700;
  margin: 0 0 4px;
}

.subtitle {
  font-size: 14px;
  color: #64748b;
  margin: 0;
}


.card {
  background: #ffffff;
  border-radius: 18px;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
  border: 1px solid #e2e8f0;
  padding: 20px 18px;
  margin-bottom: 18px;
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

.input {
  padding: 9px 12px;
  border-radius: 999px;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  font-size: 14px;
  outline: none;
  transition:
    border-color 0.12s ease,
    box-shadow 0.12s ease,
    background 0.12s ease;
}

.input:focus {
  border-color: #6366f1;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
}

.small-input {
  border-radius: 999px;
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
  transition:
    transform 0.12s ease,
    box-shadow 0.12s ease,
    opacity 0.12s ease;
  text-decoration: none;
}

.primary-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 14px 28px rgba(79, 70, 229, 0.4);
}

.primary-btn:disabled {
  opacity: 0.65;
  cursor: default;
  transform: none;
  box-shadow: 0 6px 14px rgba(148, 163, 184, 0.4);
}

.add-book-btn {
  white-space: nowrap;
}

.secondary-btn {
  border-radius: 999px;
  border: 1px solid #6366f1;
  background: white;
  color: #4f46e5;
  padding: 8px 14px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
}

.danger-btn {
  border-radius: 999px;
  border: 1px solid #ef4444;
  background: #fee2e2;
  color: #b91c1c;
  padding: 6px 12px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
}

.danger-btn:disabled {
  opacity: 0.6;
  cursor: default;
}


.status {
  margin-top: 10px;
  font-size: 13px;
  padding: 8px 10px;
  border-radius: 12px;
}

.status-error {
  background: #fef2f2;
  color: #b91c1c;
}

.status-success {
  background: #ecfdf3;
  color: #166534;
}

.status-empty {
  color: #64748b;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
}

.table-controls {
  display: flex;
  gap: 8px;
  align-items: center;
}

.table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.table th,
.table td {
  padding: 8px 10px;
  border-bottom: 1px solid #e2e8f0;
  text-align: left;
}


.badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
}

.badge-ok {
  background: #dcfce7;
  color: #166534;
}

.badge-warn {
  background: #fef9c3;
  color: #92400e;
}

.badge-bad {
  background: #fee2e2;
  color: #991b1b;
}

@media (max-width: 800px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .form {
    flex-direction: column;
    align-items: stretch;
  }

  .table-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .table-controls {
    width: 100%;
  }
}
</style>
