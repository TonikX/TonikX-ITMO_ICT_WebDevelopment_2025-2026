<template>
  <div class="profile-view">
    <h1>Профиль</h1>

    <!-- Админ: поиск читателей (заглушка) -->
    <div v-if="isAdmin" class="admin-section">
      <h2>Поиск читателя</h2>
    </div>

    <!-- Читатель: свой профиль -->
    <div v-else-if="isAuthenticated" class="reader-section">
      <div v-if="loading" class="loading">Загрузка...</div>

      <!-- Нет привязанного билета -->
      <div v-else-if="!myProfile" class="no-profile">
        <h2>Нет привязанного билета</h2>
        <v-btn color="primary" @click="$router.push('/link-reader')" prepend-icon="mdi-link">
          Привязать билет
        </v-btn>
      </div>

      <!-- Профиль читателя -->
      <div v-else class="reader-profile">
        <h2>Мой профиль</h2>

        <div class="profile-card">
          <!-- Основная информация -->
          <v-card variant="outlined" class="profile-section">
            <v-card-title class="text-h6">📋 Основное</v-card-title>
            <v-card-text>
              <div class="info-item"><span class="label">ФИО:</span> {{ myProfile.full_name }}</div>
              <div class="info-item"><span class="label">Билет:</span> {{ myProfile.library_card_id }}</div>
              <div class="info-item"><span class="label">Паспорт:</span> {{ myProfile.passport }}</div>
              <div class="info-item"><span class="label">Рождён:</span> {{ formatDate(myProfile.birth_date) }}</div>
              <div class="info-item"><span class="label">Образование:</span> {{ getEducationLevel(myProfile.education_level) }}</div>
            </v-card-text>
          </v-card>

          <!-- Контакты с редактированием -->
          <v-card variant="outlined" class="profile-section contacts-section">
            <v-card-title class="text-h6">📞 Контакты</v-card-title>
            <v-card-text>
              <div v-if="!editing">
                <div class="info-item"><span class="label">Телефон:</span> {{ myProfile.phone_number || '—' }}</div>
                <div class="info-item"><span class="label">Адрес:</span> {{ myProfile.home_address || '—' }}</div>
                <div class="info-item"><span class="label">Зал:</span> {{ myProfile.hall_name || myProfile.hall_id }}</div>
                <v-btn color="warning" variant="flat" @click="startEdit" prepend-icon="mdi-pencil" block class="mt-4">
                  Изменить
                </v-btn>
              </div>
              <div v-else>
                <v-text-field v-model="editPhone" label="Телефон" variant="outlined" density="compact" hide-details class="mb-3" />
                <v-text-field v-model="editAddress" label="Адрес" variant="outlined" density="compact" hide-details class="mb-3" />
                <div class="info-item mb-3"><span class="label">Зал:</span> {{ myProfile.hall_name || myProfile.hall_id }}</div>
                <div class="d-flex gap-2">
                  <v-btn color="success" @click="saveContacts" :loading="saving" prepend-icon="mdi-check" block>Сохранить</v-btn>
                  <v-btn color="grey" variant="outlined" @click="cancelEdit" prepend-icon="mdi-close" block>Отмена</v-btn>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </div>

        <!-- Мои книги - КОМПАКТНАЯ ВЕРСИЯ -->
        <v-card variant="outlined" class="loans-section mt-4">
          <v-card-title class="text-h6 py-3">📚 Мои книги ({{ activeLoans.length }})</v-card-title>
          <v-divider></v-divider>

          <div v-if="activeLoans.length" class="loans-compact">
            <div v-for="loan in activeLoans" :key="loan.loan_id" class="loan-row">
              <div class="loan-info">
                <span class="book-title">{{ loan.book_title }}</span>
                <span class="loan-dates">
                  {{ formatDate(loan.issued_at) }} → {{ formatDate(loan.due_date) }}
                  <span class="days-badge">{{ loan.days_on_loan || 0 }} дн.</span>
                </span>
              </div>
              <v-btn
                color="success"
                size="small"
                variant="flat"
                @click="returnBook(loan.loan_id)"
                :loading="returningLoanId === loan.loan_id"
                class="return-btn"
              >
                Вернуть
              </v-btn>
            </div>
          </div>

          <div v-else class="text-center text-grey py-6">
            <v-icon size="40" color="grey-lighten-1">mdi-book-off</v-icon>
            <p class="mt-2">Нет книг на руках</p>
          </div>
        </v-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import apiClient from '../api/client'

const auth = useAuthStore()
const isAdmin = computed(() => auth.isAdmin)
const isAuthenticated = computed(() => auth.isAuthenticated)

// State
const myProfile = ref(null)
const activeLoans = ref([])
const loading = ref(true)
const editing = ref(false)
const saving = ref(false)
const editPhone = ref('')
const editAddress = ref('')
const returningLoanId = ref(null)

// Helpers
const educationMap = { primary: 'Начальное', secondary: 'Среднее', higher: 'Высшее', degree: 'Ученая степень' }
const getEducationLevel = code => educationMap[code] || code || '—'
const formatDate = d => d ? new Date(d).toLocaleDateString('ru-RU') : '—'

// Load profile
const loadMyProfile = async () => {
  loading.value = true
  try {
    const res = await apiClient.get('user/my-profile/')
    myProfile.value = res.data.reader
    activeLoans.value = res.data.active_loans || []
    editPhone.value = myProfile.value.phone_number || ''
    editAddress.value = myProfile.value.home_address || ''
  } catch (e) {
    if (e.response?.status === 404) myProfile.value = null
  } finally { loading.value = false }
}

// Edit contacts
const startEdit = () => { editing.value = true }
const cancelEdit = () => {
  editing.value = false
  editPhone.value = myProfile.value.phone_number || ''
  editAddress.value = myProfile.value.home_address || ''
}
const saveContacts = async () => {
  saving.value = true
  try {
    const res = await apiClient.patch(`readers/${myProfile.value.reader_id}/`, {
      phone_number: editPhone.value,
      home_address: editAddress.value
    })
    myProfile.value = res.data
    editing.value = false
  } catch (e) { alert('Ошибка сохранения') } finally { saving.value = false }
}

// Return book
const returnBook = async (id) => {
  if (!confirm('Вернуть книгу?')) return
  returningLoanId.value = id
  try {
    await apiClient.post('loans/return/', { loan_id: id })
    await loadMyProfile()
  } catch (e) { alert('Ошибка возврата') } finally { returningLoanId.value = null }
}

onMounted(() => { if (!isAdmin.value && isAuthenticated.value) loadMyProfile() })
</script>

<style scoped>
.profile-view { max-width: 1000px; margin: 0 auto; padding: 20px; }
.loading { text-align: center; padding: 40px; color: #6c757d; }
.no-profile { text-align: center; padding: 40px; background: #f8f9fa; border-radius: 8px; }

.profile-card { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; }
.profile-section { height: 100%; }
.info-item { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f1f3f4; }
.info-item:last-child { border-bottom: none; }
.label { font-weight: 600; color: #495057; min-width: 100px; }

/* Компактный список книг */
.loans-compact { display: flex; flex-direction: column; }
.loan-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
}
.loan-row:last-child { border-bottom: none; }

.loan-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.book-title { font-weight: 600; color: #2c3e50; }
.loan-dates { font-size: 0.9rem; color: #6c757d; }
.days-badge {
  display: inline-block;
  margin-left: 8px;
  padding: 2px 6px;
  background: #e9ecef;
  border-radius: 12px;
  font-size: 0.8rem;
  color: #495057;
}

.return-btn { min-width: 90px; }

@media (max-width: 768px) {
  .profile-card { grid-template-columns: 1fr; }
  .loan-row { flex-direction: column; align-items: flex-start; gap: 10px; }
  .return-btn { width: 100%; }
}
</style>