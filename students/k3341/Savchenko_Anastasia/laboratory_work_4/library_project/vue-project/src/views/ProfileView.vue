<template>
  <div class="profile-view">
    <h1>Профиль</h1>

    <!-- АДМИН: поиск читателей -->
    <div v-if="isAdmin" class="admin-section">
      <h2>Поиск профиля читателя</h2>
      <!-- Форма поиска для админа -->
    </div>

    <!-- ЧИТАТЕЛЬ: свой профиль -->
    <div v-else-if="isAuthenticated" class="reader-section">
      <div v-if="loading" class="loading">Загрузка профиля...</div>

      <!-- Нет привязанного билета -->
      <div v-else-if="!myProfile && !loading" class="no-profile">
        <h2>У вас нет привязанного читательского билета</h2>
        <p>Чтобы пользоваться библиотекой, привяжите существующий читательский билет.</p>
        <router-link to="/link-reader" class="link-btn">Привязать читательский билет</router-link>
      </div>

      <!-- Профиль читателя -->
      <div v-else-if="myProfile" class="reader-profile">
        <h2>Мой читательский профиль</h2>

        <div class="profile-card">
          <!-- Основная информация -->
          <div class="profile-section">
            <h3>Основная информация</h3>
            <div class="info-grid">
              <div class="info-item"><span class="label">ФИО:</span><span class="value">{{ myProfile.full_name }}</span></div>
              <div class="info-item"><span class="label">Читательский билет:</span><span class="value">{{ myProfile.library_card_id }}</span></div>
              <div class="info-item"><span class="label">Паспорт:</span><span class="value">{{ myProfile.passport }}</span></div>
              <div class="info-item"><span class="label">Дата рождения:</span><span class="value">{{ formatDate(myProfile.birth_date) }}</span></div>
              <div class="info-item"><span class="label">Образование:</span><span class="value">{{ getEducationLevel(myProfile.education_level) }}</span></div>
            </div>
          </div>

          <!-- Контактная информация -->
          <div class="profile-section">
            <h3>Контактная информация</h3>
            <div class="info-grid">
              <div class="info-item">
                <span class="label">Телефон:</span>
                <span v-if="!editingContacts" class="value">{{ myProfile.phone_number || 'Не указан' }}</span>
                <input v-else v-model="editPhone" type="text" class="edit-input">
              </div>
              <div class="info-item">
                <span class="label">Адрес:</span>
                <span v-if="!editingContacts" class="value">{{ myProfile.home_address || 'Не указан' }}</span>
                <input v-else v-model="editAddress" type="text" class="edit-input">
              </div>
              <div class="info-item"><span class="label">Зал:</span><span class="value">{{ myProfile.hall_name || myProfile.hall_id }}</span></div>
            </div>

            <div class="contact-actions">
              <button v-if="!editingContacts" @click="startEditContacts" class="edit-btn">Изменить контакты</button>
              <div v-else class="edit-buttons">
                <button @click="saveMyContacts" :disabled="saving" class="save-btn">{{ saving ? 'Сохранение...' : 'Сохранить' }}</button>
                <button @click="cancelEditContacts" class="cancel-btn">Отмена</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Активные книги с кнопкой возврата -->
        <div v-if="activeLoans.length > 0" class="loans-section">
          <h3>Мои книги</h3>
          <div class="loans-list">
            <div v-for="loan in activeLoans" :key="loan.loan_id" class="loan-item">
              <div class="loan-info">
                <h4>{{ loan.book_title }}</h4>
                <p><strong>Выдана:</strong> {{ formatDate(loan.issued_at) }}</p>
                <p><strong>Срок возврата:</strong> {{ formatDate(loan.due_date) }}</p>
                <p><strong>Дней на руках:</strong> {{ loan.days_on_loan || 0 }}</p>
                <v-btn
                  color="success"
                  size="small"
                  prepend-icon="mdi-book-check"
                  @click="returnBook(loan.loan_id)"
                  :loading="returningLoanId === loan.loan_id"
                  class="mt-2"
                >Вернуть книгу</v-btn>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="no-loans"><h3>Мои книги</h3><p>У вас нет книг на руках</p></div>
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

// Данные читателя
const myProfile = ref(null)
const activeLoans = ref([])
const loading = ref(true)

// Редактирование контактов
const editingContacts = ref(false)
const saving = ref(false)
const editPhone = ref('')
const editAddress = ref('')

// Возврат книги
const returningLoanId = ref(null)

const educationLevels = {
  'primary': 'Начальное', 'secondary': 'Среднее',
  'higher': 'Высшее', 'degree': 'Ученая степень'
}
const getEducationLevel = (code) => educationLevels[code] || code || 'Не указано'
const formatDate = (dateString) => dateString ? new Date(dateString).toLocaleDateString('ru-RU') : 'Не указано'

// Загрузка профиля
const loadMyProfile = async () => {
  loading.value = true
  try {
    const res = await apiClient.get('user/my-profile/')
    myProfile.value = res.data.reader
    activeLoans.value = res.data.active_loans || []
    editPhone.value = myProfile.value.phone_number || ''
    editAddress.value = myProfile.value.home_address || ''
  } catch (error) {
    if (error.response?.status === 404) myProfile.value = null
    console.error('Ошибка загрузки профиля:', error)
  } finally { loading.value = false }
}

// Редактирование контактов
const startEditContacts = () => { editingContacts.value = true }
const cancelEditContacts = () => {
  editingContacts.value = false
  editPhone.value = myProfile.value.phone_number || ''
  editAddress.value = myProfile.value.home_address || ''
}
const saveMyContacts = async () => {
  saving.value = true
  try {
    const res = await apiClient.patch(`readers/${myProfile.value.reader_id}/`, {
      phone_number: editPhone.value,
      home_address: editAddress.value
    })
    myProfile.value = res.data
    editingContacts.value = false
  } catch (error) {
    console.error('Ошибка сохранения:', error)
    alert('Не удалось сохранить контакты')
  } finally { saving.value = false }
}

// Возврат книги
const returnBook = async (loanId) => {
  if (!confirm('Вернуть книгу в библиотеку?')) return
  returningLoanId.value = loanId
  try {
    await apiClient.post('loans/return/', { loan_id: loanId })
    await loadMyProfile()
  } catch (error) {
    console.error('Ошибка возврата:', error)
    alert('Не удалось вернуть книгу')
  } finally { returningLoanId.value = null }
}

onMounted(() => {
  if (!isAdmin.value && isAuthenticated.value) loadMyProfile()
})
</script>

<style scoped>
.profile-view { max-width: 1000px; margin: 0 auto; padding: 20px; }
.reader-search { margin-bottom: 40px; padding: 25px; background: #f8f9fa; border-radius: 8px; border: 1px solid #e9ecef; }
.search-form { margin-top: 20px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
.form-group { margin-bottom: 0; }
.form-group label { display: block; margin-bottom: 8px; font-weight: 500; color: #495057; }
.form-group input { width: 100%; padding: 10px 12px; border: 1px solid #ced4da; border-radius: 4px; font-size: 15px; }
.form-group input:focus { border-color: #80bdff; outline: 0; box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25); }
.submit-btn { padding: 12px 30px; background: #007bff; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; }
.submit-btn:hover:not(:disabled) { background: #0069d9; }
.submit-btn:disabled { background: #6c757d; cursor: not-allowed; }
.error-message { margin-top: 15px; padding: 10px 15px; background: #f8d7da; color: #721c24; border-radius: 4px; border: 1px solid #f5c6cb; }
.hint { margin-top: 25px; padding: 15px; background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 4px; color: #856404; }
.hint p { margin: 5px 0; }
.admin-info { text-align: center; padding: 40px; background: #e8f4fd; border-radius: 8px; border: 1px solid #b3d7ff; }
.admin-info h2 { color: #0056b3; margin-bottom: 15px; }
.admin-link { display: inline-block; margin-top: 15px; padding: 10px 20px; background: #28a745; color: white; text-decoration: none; border-radius: 4px; }
.admin-link:hover { background: #218838; }
.reader-profile { margin-top: 30px; }
.profile-card { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 40px; }
.profile-section { padding: 25px; background: white; border-radius: 8px; border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.profile-section h3 { margin-top: 0; margin-bottom: 20px; color: #495057; border-bottom: 2px solid #dee2e6; padding-bottom: 10px; }
.info-grid { display: grid; gap: 15px; }
.info-item { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #f1f3f4; }
.info-item:last-child { border-bottom: none; }
.info-item .label { font-weight: 600; color: #495057; min-width: 120px; }
.info-item .value { color: #212529; text-align: right; flex: 1; margin-left: 15px; }
.edit-input { padding: 6px 10px; border: 1px solid #ced4da; border-radius: 4px; font-size: 14px; width: 100%; box-sizing: border-box; }
.contact-actions { margin-top: 25px; padding-top: 15px; border-top: 1px solid #e9ecef; }
.edit-btn, .save-btn, .cancel-btn { padding: 8px 16px; border: none; border-radius: 4px; font-size: 14px; font-weight: 500; cursor: pointer; transition: all 0.2s; }
.edit-btn { background: #6c757d; color: white; }
.edit-btn:hover { background: #5a6268; }
.save-btn { background: #28a745; color: white; margin-right: 10px; }
.save-btn:hover:not(:disabled) { background: #218838; }
.cancel-btn { background: #dc3545; color: white; }
.cancel-btn:hover:not(:disabled) { background: #c82333; }
.save-btn:disabled, .cancel-btn:disabled { opacity: 0.65; cursor: not-allowed; }
.loans-section, .no-loans { margin-top: 30px; padding: 25px; background: white; border-radius: 8px; border: 1px solid #e9ecef; }
.loans-list { display: grid; gap: 15px; }
.loan-item { padding: 15px; border: 1px solid #e9ecef; border-radius: 4px; background: #f8f9fa; }
.loan-info h4 { margin: 0 0 10px 0; color: #212529; }
.loan-info p { margin: 5px 0; color: #6c757d; font-size: 14px; }
.no-loans { text-align: center; color: #6c757d; }
@media (max-width: 768px) {
  .form-row { grid-template-columns: 1fr; }
  .profile-card { grid-template-columns: 1fr; }
  .info-item { flex-direction: column; align-items: flex-start; }
  .info-item .value { text-align: left; margin-left: 0; margin-top: 5px; }
}
</style>