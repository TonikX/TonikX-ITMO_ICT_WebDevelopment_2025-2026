<template>
  <div class="page">
    <header class="page-header">
      <div>
        <h1>{{ titleText }}</h1>
        <p class="subtitle">
          {{ subtitleText }}
        </p>
      </div>
    </header>

    <section
      v-if="!isAdmin"
      class="card form-card"
    >
      <form @submit.prevent="loadProfile" class="form">
        <div class="form-row">
          <label class="label">
            Номер читательского билета
            <input
              v-model="cardNumber"
              type="text"
              class="input"
              placeholder="Например, 12345"
              required
            />
          </label>
        </div>

        <div class="form-row">
          <label class="label">
            Номер паспорта
            <input
              v-model="passportNumber"
              type="text"
              class="input"
              placeholder="Например, 1234 567890"
              required
            />
          </label>
        </div>

        <div class="form-actions">
          <button
            type="submit"
            class="primary-btn"
            :disabled="loading"
          >
            <span v-if="loading">Ищем…</span>
            <span v-else>Найти профиль</span>
          </button>
        </div>

        <p v-if="error" class="status status-error">
          {{ error }}
        </p>
      </form>

      <!-- подсказка для только что зарегистрированных -->
      <p
        v-if="!reader && !error && !loading"
        class="profile-hint"
      >
        Если вы только что зарегистрировали аккаунт, но читательский билет вам ещё не
        оформили, обратитесь к библиотекарю. После того как вас внесут в систему и
        выдадут номер билета, вы сможете увидеть здесь свой профиль и список книг.
      </p>
    </section>

    <section
      v-else
      class="card form-card admin-top-card"
    >
      <div class="admin-top-inner">
        <div class="admin-top-text">
          <p class="admin-top-title">Работа с читателями</p>
          <p class="admin-top-subtitle">
            Ниже — список всех читателей с поиском по ФИО, билету и телефону.
            Для добавления нового читателя используйте кнопку справа.
          </p>
        </div>
        <a
          href="http://127.0.0.1:8000/admin/library_app/reader/"
          target="_blank"
          class="primary-btn admin-top-btn"
        >
          Добавить читателя
        </a>
      </div>
    </section>

    <!-- блок с профилем найденного читателя (виден только не-админу) -->
    <section v-if="reader && !isAdmin" class="grid">
      <div class="card">
        <h2>Данные читателя</h2>
        <div class="info-row">
          <span class="info-label">ФИО:</span>
          <span>{{ reader.full_name }}</span>
        </div>
        <div class="info-row">
          <span class="info-label">Читательский билет:</span>
          <span>{{ reader.card_number }}</span>
        </div>
        <div class="info-row">
          <span class="info-label">Паспорт:</span>
          <span>{{ reader.passport_number }}</span>
        </div>
        <div class="info-row">
          <span class="info-label">Зал:</span>
          <span>{{ reader.hall || '—' }}</span>
        </div>
        <div class="info-row">
          <span class="info-label">Образование:</span>
          <span>{{ reader.education_level || '—' }}</span>
        </div>
        <div class="info-row">
          <span class="info-label">Учёная степень:</span>
          <span>{{ reader.has_academic_degree ? 'Есть' : 'Нет' }}</span>
        </div>

        <!-- редактируемые контакты -->
        <div class="info-row">
          <span class="info-label">Телефон:</span>
          <span v-if="!isEditingContacts">
            {{ reader.phone || '—' }}
          </span>
          <input
            v-else
            v-model="editContacts.phone"
            class="input-inline"
            type="text"
            placeholder="Телефон"
          />
        </div>

        <div class="info-row">
          <span class="info-label">Адрес:</span>
          <span v-if="!isEditingContacts">
            {{ reader.address || '—' }}
          </span>
          <input
            v-else
            v-model="editContacts.address"
            class="input-inline"
            type="text"
            placeholder="Адрес"
          />
        </div>

        <!-- кнопки управления -->
        <div class="edit-actions" v-if="!isEditingContacts">
          <button
            type="button"
            class="secondary-btn"
            @click="startEditContacts"
          >
            Изменить контакты
          </button>
        </div>

        <div class="edit-actions" v-else>
          <button
            type="button"
            class="primary-btn"
            @click="saveContacts"
            :disabled="savingContacts"
          >
            <span v-if="savingContacts">Сохраняем…</span>
            <span v-else>Сохранить</span>
          </button>
          <button
            type="button"
            class="ghost-btn"
            @click="cancelEditContacts"
            :disabled="savingContacts"
          >
            Отмена
          </button>
        </div>
      </div>

      <!-- активные книги -->
      <div class="card">
        <h2>Книги на руках</h2>

        <p v-if="!activeLoans.length" class="status status-empty">
          Сейчас у читателя нет активных выдач.
        </p>

        <table v-else class="table">
          <thead>
            <tr>
              <th>Название книги</th>
              <th>Дата выдачи</th>
              <th>Дней на руках</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="loan in activeLoans"
              :key="loan.loan_id"
              :class="{ 'row-overdue': loan.is_overdue }"
            >
              <td>{{ loan.book_title }}</td>
              <td>{{ loan.assigned_at }}</td>
              <td>
                {{ loan.days_on_loan }}
                <span v-if="loan.is_overdue" class="overdue-label">
                  (больше 10 дней)
                </span>
              </td>
            </tr>
          </tbody>
        </table>

        <p v-if="activeLoans.some(l => l.is_overdue)" class="hint">
          Книги, которые находятся на руках больше 10 дней, подсвечены красным.
        </p>
      </div>
    </section>

    <!--список всех читателей-->
    <section v-if="isAdmin" class="admin-block">
      <div class="card">
        <div class="admin-header">
          <h2>Все читатели</h2>
          <div class="admin-search-wrap">
            <input
              v-model="readersSearch"
              type="search"
              class="input admin-search-input"
              placeholder="Поиск по ФИО, билету или телефону…"
            />
            <button
              type="button"
              class="secondary-btn"
              @click="loadReaders"
              :disabled="readersLoading"
            >
              <span v-if="readersLoading">Обновляем…</span>
              <span v-else>Обновить список</span>
            </button>
          </div>
        </div>

        <p v-if="readersError" class="status status-error">
          {{ readersError }}
        </p>

        <p
          v-else-if="!readersLoading && !filteredReaders.length"
          class="status status-empty"
        >
          Читателей не найдено.
        </p>

        <table v-else class="table">
          <thead>
            <tr>
              <th>ФИО</th>
              <th>Билет</th>
              <th>Телефон</th>
              <th>Зал</th>
              <th>Книги на руках</th>
              <th>Макс. дней на руках</th>
              <th>Активен</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in filteredReaders" :key="r.reader_id || r.id">
              <td>{{ r.full_name }}</td>
              <td>{{ r.card_number }}</td>
              <td>{{ r.phone || '—' }}</td>
              <td>{{ r.hall_name || '—' }}</td>
              <td>{{ (statsByReader[r.reader_id || r.id]?.count) ?? 0 }}</td>
              <td>
                <span
                  :class="{
                    'overdue-text':
                      (statsByReader[r.reader_id || r.id]?.maxDays || 0) > 10
                  }"
                >
                  {{ (statsByReader[r.reader_id || r.id]?.maxDays) ?? 0 }}
                </span>
              </td>
              <td>
                <span :class="r.is_active ? 'badge-ok' : 'badge-bad'">
                  {{ r.is_active ? 'Да' : 'Нет' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import apiClient from '@/api/client'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const isAdmin = computed(function () {
  return auth.isAdmin
})

const titleText = computed(function () {
  return isAdmin.value ? 'Читатели' : 'Профиль читателя'
})

const subtitleText = computed(function () {
  if (isAdmin.value) {
    return 'Список читателей библиотеки. Можно искать по ФИО, номеру билета и телефону, а также добавлять новых читателей через админку.'
  }
  return 'Введите номер читательского билета и паспорт для просмотра профиля и активных книг. Если вы только что зарегистрировали аккаунт и не можете найти себя — обратитесь к библиотекарю, чтобы вам выдали читательский билет и внесли данные в систему.'
})

const cardNumber = ref('')
const passportNumber = ref('')

const loading = ref(false)
const error = ref(null)

const reader = ref(null)
const activeLoans = ref([])

// редактирование контактов
const isEditingContacts = ref(false)
const savingContacts = ref(false)

const editContacts = ref({
  phone: '',
  address: '',
})

const startEditContacts = () => {
  if (!reader.value) return
  isEditingContacts.value = true
  editContacts.value.phone = reader.value.phone || ''
  editContacts.value.address = reader.value.address || ''
}

const cancelEditContacts = () => {
  isEditingContacts.value = false
}

const saveContacts = async () => {
  if (!reader.value) return


  const readerId = reader.value.reader_id ?? reader.value.id
  if (!readerId) {
    console.error('Нет идентификатора читателя в объекте', reader.value)
    alert('Невозможно сохранить: не найден идентификатор читателя.')
    return
  }

  savingContacts.value = true
  try {
    const payload = {
      phone: editContacts.value.phone,
      address: editContacts.value.address,
    }
    const resp = await apiClient.patch(`readers/${readerId}/`, payload)
    reader.value = resp.data
    isEditingContacts.value = false
  } catch (e) {
    console.error(e)
    alert('Не удалось сохранить контакты. Попробуйте позже.')
  } finally {
    savingContacts.value = false
  }
}

const loadProfile = async () => {
  if (isAdmin.value) return // админам форма не нужна

  error.value = null
  reader.value = null
  activeLoans.value = []
  isEditingContacts.value = false

  loading.value = true

  try {
    const response = await apiClient.get('readers/find-by-card/', {
      params: {
        card_number: cardNumber.value,
        passport_number: passportNumber.value,
      },
    })

    reader.value = response.data.reader
    activeLoans.value = response.data.active_loans || []
  } catch (e) {
    console.error(e)

    const resp = e.response || null
    const status = resp ? resp.status : null

    if (status === 404) {
      error.value = 'Читатель с такими данными не найден.'
    } else if (resp && resp.data && resp.data.detail) {
      error.value = resp.data.detail
    } else {
      error.value = 'Ошибка при загрузке профиля. Попробуйте позже.'
    }
  } finally {
    loading.value = false
  }
}

const readers = ref([])
const readersLoading = ref(false)
const readersError = ref(null)
const readersSearch = ref('')

// reader_id / id -> { count, maxDays }
const statsByReaderRef = ref({})

const loadReaders = async () => {
  if (!isAdmin.value) return

  readersLoading.value = true
  readersError.value = null

  try {
    const responses = await Promise.all([
      apiClient.get('readers/'),
      apiClient.get('loans/active/'),
    ])

    const readersResp = responses[0]
    const loansResp = responses[1]

    const data = readersResp.data
    const items = (data && data.results) ? data.results : data
    const safeItems = items || []

    readers.value = safeItems.map(function (r) {
      return Object.assign({}, r, {
        hall_name: r.hall_name || r.hall || null,
      })
    })

    const loans = loansResp.data || []
    const stats = {}

    loans.forEach(function (l) {
      const readerObj = l.reader || null
      // active loans endpoint кладёт id в reader.id
      const rid = readerObj ? (readerObj.reader_id ?? readerObj.id) : null
      if (!rid) return

      if (!stats[rid]) {
        stats[rid] = { count: 0, maxDays: 0 }
      }

      stats[rid].count += 1

      if (typeof l.days_on_loan === 'number') {
        if (l.days_on_loan > stats[rid].maxDays) {
          stats[rid].maxDays = l.days_on_loan
        }
      }
    })

    statsByReaderRef.value = stats
  } catch (e) {
    console.error(e)
    readersError.value = 'Не удалось загрузить список читателей.'
  } finally {
    readersLoading.value = false
  }
}

const filteredReaders = computed(function () {
  const q = readersSearch.value.trim().toLowerCase()
  if (!q) return readers.value

  return readers.value.filter(function (r) {
    const fio = (r.full_name || '').toLowerCase()
    const card = (r.card_number || '').toLowerCase()
    const phone = (r.phone || '').toLowerCase()

    return (
      fio.indexOf(q) !== -1 ||
      card.indexOf(q) !== -1 ||
      phone.indexOf(q) !== -1
    )
  })
})

const statsByReader = computed(function () {
  return statsByReaderRef.value
})

onMounted(function () {
  if (isAdmin.value) {
    loadReaders()
  }
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

.profile-hint {
  margin-top: 10px;
  font-size: 13px;
  color: #64748b;
  line-height: 1.4;
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
  flex: 1 1 240px;
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
  transition: border-color 0.12s ease, box-shadow 0.12s ease, background 0.12s ease;
}

.input:focus {
  border-color: #6366f1;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
}

.input-inline {
  flex: 1 1 auto;
  min-width: 0;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid #cbd5e1;
  background: #f8fafc;
  font-size: 14px;
  outline: none;
}

.input-inline:focus {
  border-color: #6366f1;
  background: #ffffff;
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25);
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

.status-empty {
  color: #64748b;
}

/* инфо-блок */

.info-row {
  display: flex;
  gap: 8px;
  margin-bottom: 6px;
  font-size: 14px;
  align-items: center;
}

.info-label {
  min-width: 140px;
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

.row-overdue {
  background: #fef2f2;
}

.overdue-label {
  color: #b91c1c;
  font-weight: 600;
  margin-left: 4px;
}

.hint {
  margin-top: 8px;
  font-size: 13px;
  color: #64748b;
}

.grid {
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(0, 1.2fr);
  gap: 16px;
  align-items: flex-start;
}


.admin-block {
  margin-top: 24px;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.admin-search-wrap {
  display: flex;
  gap: 8px;
  align-items: center;
}

.admin-search-input {
  min-width: 260px;
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

.secondary-btn:disabled {
  opacity: 0.6;
  cursor: default;
}


.ghost-btn {
  border-radius: 999px;
  border: 1px solid #cbd5e1;
  background: white;
  color: #0f172a;
  padding: 8px 14px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  margin-left: 8px;
}


.badge-ok {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 999px;
  background: #dcfce7;
  color: #166534;
  font-size: 12px;
  font-weight: 600;
}

.badge-bad {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 999px;
  background: #fee2e2;
  color: #991b1b;
  font-size: 12px;
  font-weight: 600;
}

.overdue-text {
  color: #b91c1c;
  font-weight: 600;
}


.admin-top-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.admin-top-title {
  font-weight: 600;
  margin-bottom: 4px;
}

.admin-top-subtitle {
  font-size: 14px;
  color: #64748b;
  margin: 0;
}

.admin-top-btn {
  white-space: nowrap;
}

/

.admin-top-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.admin-top-title {
  font-weight: 600;
  margin-bottom: 4px;
}

.admin-top-subtitle {
  font-size: 14px;
  color: #64748b;
  margin: 0;
}

.admin-top-btn {
  white-space: nowrap;
}


.edit-actions {
  margin-top: 10px;
}

@media (max-width: 800px) {
  .grid {
    grid-template-columns: minmax(0, 1fr);
  }

  .form {
    flex-direction: column;
    align-items: stretch;
  }

  .form-actions {
    justify-content: flex-start;
  }

  .admin-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .admin-search-wrap {
    width: 100%;
  }

  .admin-search-input {
    flex: 1 1 auto;
    min-width: 0;
  }

  .admin-top-inner {
    flex-direction: column;
    align-items: flex-start;
  }

  .admin-top-btn {
    align-self: stretch;
    justify-content: center;
  }
}
</style>
