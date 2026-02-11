<template>
  <div class="profile-view">
    <h1>Профиль читателя</h1>

    <div v-if="!isAdmin" class="reader-search">
      <h2>Поиск профиля</h2>
      <form @submit.prevent="searchReader" class="search-form">
        <div class="form-row">
          <div class="form-group">
            <label for="cardNumber">Номер читательского билета:</label>
            <input
              id="cardNumber"
              v-model="cardNumber"
              type="text"
              required
              placeholder="Пример: Б-26-0001"
              :disabled="loading"
            />
          </div>

          <div class="form-group">
            <label for="passport">Номер паспорта:</label>
            <input
              id="passport"
              v-model="passport"
              type="text"
              required
              placeholder="Пример: 1234 567890"
              :disabled="loading"
            />
          </div>
        </div>

        <button type="submit" :disabled="loading" class="submit-btn">
          {{ loading ? 'Поиск...' : 'Найти профиль' }}
        </button>
      </form>

      <div v-if="searchError" class="error-message">
        {{ searchError }}
      </div>

      <!-- Подсказка для новых пользователей -->
      <div v-if="!reader && !loading" class="hint">
        <p><strong>Нет читательского билета?</strong></p>
        <p>Если вы только что зарегистрировали аккаунт, но читательский билет вам ещё не оформили, обратитесь к библиотекарю. После того как вас внесут в систему и выдадут номер билета, вы сможете увидеть здесь свой профиль и список книг.</p>
      </div>
    </div>

    <!-- Для администраторов -->
    <div v-else class="admin-info">
      <h2>Вы вошли как администратор</h2>
      <p>Для работы с читателями используйте админ-панель Django.</p>
      <a href="http://127.0.0.1:8000/admin/" target="_blank" class="admin-link">
        Перейти в админ-панель
      </a>
    </div>

    <!-- Отображение найденного читателя -->
    <div v-if="reader" class="reader-profile">
      <h2>Данные читателя</h2>

      <div class="profile-card">
        <div class="profile-section">
          <h3>Основная информация</h3>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">ФИО:</span>
              <span class="value">{{ reader.full_name }}</span>
            </div>
            <div class="info-item">
              <span class="label">Читательский билет:</span>
              <span class="value">{{ reader.library_card_id }}</span>
            </div>
            <div class="info-item">
              <span class="label">Паспорт:</span>
              <span class="value">{{ reader.passport }}</span>
            </div>
            <div class="info-item">
              <span class="label">Дата рождения:</span>
              <span class="value">{{ formatDate(reader.birth_date) }}</span>
            </div>
            <div class="info-item">
              <span class="label">Образование:</span>
              <span class="value">{{ getEducationLevel(reader.education_level) }}</span>
            </div>
          </div>
        </div>

        <div class="profile-section">
          <h3>Контактная информация</h3>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">Телефон:</span>
              <span v-if="!editingContacts" class="value">{{ reader.phone_number || reader.phone || 'Не указан' }}</span>
              <input v-else v-model="editPhone" type="text" class="edit-input" placeholder="Телефон">
            </div>
            <div class="info-item">
              <span class="label">Адрес:</span>
              <span v-if="!editingContacts" class="value">{{ reader.home_address || reader.address || 'Не указан' }}</span>
              <input v-else v-model="editAddress" type="text" class="edit-input" placeholder="Адрес">
            </div>
            <div class="info-item">
              <span class="label">Зал:</span>
              <span class="value">{{ reader.hall_name || reader.hall_id || 'Не закреплен' }}</span>
            </div>
          </div>

          <div class="contact-actions">
            <button v-if="!editingContacts" @click="startEditContacts" class="edit-btn">
              Изменить контакты
            </button>
            <div v-else class="edit-buttons">
              <button @click="saveContacts" :disabled="savingContacts" class="save-btn">
                {{ savingContacts ? 'Сохранение...' : 'Сохранить' }}
              </button>
              <button @click="cancelEditContacts" :disabled="savingContacts" class="cancel-btn">
                Отмена
              </button>
            </div>
          </div>
        </div>
      </div> <!-- ДОБАВЬ ЭТУ СТРОКУ - закрывает <div class="profile-card"> -->

      <!-- Активные книги -->
      <div v-if="activeLoans.length > 0" class="loans-section">
        <h3>Книги на руках</h3>
        <div class="loans-list">
          <div v-for="loan in activeLoans" :key="loan.loan_id" class="loan-item">
            <div class="loan-info">
              <h4>{{ loan.book_title }}</h4>
              <p><strong>Выдана:</strong> {{ formatDate(loan.issued_at) }}</p>
              <p><strong>Срок:</strong> {{ formatDate(loan.due_date) }}</p>
              <p><strong>Дней на руках:</strong> {{ loan.days_on_loan || 0 }}</p>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="no-loans">
        <h3>Активные выдачи</h3>
        <p>У читателя нет активных выдач книг.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import apiClient from '../api/client'

const auth = useAuthStore()
const isAdmin = computed(() => auth.isAdmin)

// Поиск читателя
const cardNumber = ref('')
const passport = ref('')
const loading = ref(false)
const searchError = ref('')
const reader = ref(null)
const activeLoans = ref([])

// Редактирование контактов
const editingContacts = ref(false)
const savingContacts = ref(false)
const editPhone = ref('')
const editAddress = ref('')

const educationLevels = {
  'primary': 'Начальное',
  'secondary': 'Среднее',
  'higher': 'Высшее',
  'degree': 'Ученая степень'
}

const getEducationLevel = (code) => {
  return educationLevels[code] || code || 'Не указано'
}

const formatDate = (dateString) => {
  if (!dateString) return 'Не указано'
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU')
}

const searchReader = async () => {
  loading.value = true
  searchError.value = ''
  reader.value = null
  activeLoans.value = []

  try {
    // Способ 1: Попробуем получить всех читателей и найти нужного
    const response = await apiClient.get('readers/')
    const allReaders = Array.isArray(response.data) ? response.data : response.data.results || []

    // Ищем читателя по номеру билета и паспорту
    const foundReader = allReaders.find(r =>
      (r.library_card_id === cardNumber.value || r.card_number === cardNumber.value) &&
      r.passport === passport.value
    )

    if (!foundReader) {
      // Способ 2: Если не нашли, попробуем отдельный эндпоинт
      try {
        // Попробуем разные варианты эндпоинтов
        const endpoints = [
          `readers/find/?card_number=${cardNumber.value}&passport=${passport.value}`,
          `reader/find/?card_number=${cardNumber.value}&passport=${passport.value}`,
          `readers/find-by-card/?card_number=${cardNumber.value}&passport_number=${passport.value}`
        ]

        let readerResponse = null
        for (const endpoint of endpoints) {
          try {
            readerResponse = await apiClient.get(endpoint)
            if (readerResponse.data) break
          } catch (e) {
            continue // Пробуем следующий эндпоинт
          }
        }

        if (readerResponse?.data) {
          // В зависимости от структуры ответа
          if (readerResponse.data.reader) {
            reader.value = readerResponse.data.reader
            activeLoans.value = readerResponse.data.active_loans || []
          } else {
            reader.value = readerResponse.data
          }
        } else {
          throw new Error('Читатель не найден')
        }

      } catch (innerError) {
        searchError.value = 'Читатель с такими данными не найден.'
        return
      }
    } else {
      reader.value = foundReader

//       // Пробуем получить активные выдачи для этого читателя
//       try {
//         const loansResponse = await apiClient.get(`loans/active/?reader_id=${foundReader.reader_id || foundReader.id}`)
//         activeLoans.value = loansResponse.data || []
//       } catch (loanError) {
//         console.log('Не удалось загрузить активные выдачи:', loanError)
//         activeLoans.value = []
//       }
    }

  } catch (error) {
    console.error('Ошибка поиска читателя:', error)

    if (error.response?.status === 404) {
      searchError.value = 'Читатель с такими данными не найден.'
    } else if (error.response?.data?.detail) {
      searchError.value = error.response.data.detail
    } else {
      searchError.value = 'Ошибка при поиске читателя. Попробуйте позже.'
    }

  } finally {
    loading.value = false
  }
}

const startEditContacts = () => {
  if (!reader.value) return
  editingContacts.value = true
  // Используем phone_number и home_address из API
  editPhone.value = reader.value.phone_number || reader.value.phone || ''
  editAddress.value = reader.value.home_address || reader.value.address || ''
}

const cancelEditContacts = () => {
  editingContacts.value = false
}

const saveContacts = async () => {
  if (!reader.value) return

  savingContacts.value = true

  try {
    const readerId = reader.value.reader_id || reader.value.id
    // Отправляем правильные поля: phone_number и home_address
    const response = await apiClient.patch(`readers/${readerId}/`, {
      phone_number: editPhone.value,
      home_address: editAddress.value
    })

    reader.value = response.data
    editingContacts.value = false

  } catch (error) {
    console.error('Ошибка сохранения контактов:', error)
    alert('Не удалось сохранить контакты. Попробуйте позже.')
  } finally {
    savingContacts.value = false
  }
}
</script>

<style scoped>
.profile-view {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.reader-search {
  margin-bottom: 40px;
  padding: 25px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.search-form {
  margin-top: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 0;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #495057;
}

.form-group input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 15px;
}

.form-group input:focus {
  border-color: #80bdff;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25);
}

.submit-btn {
  padding: 12px 30px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
}

.submit-btn:hover:not(:disabled) {
  background: #0069d9;
}

.submit-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.error-message {
  margin-top: 15px;
  padding: 10px 15px;
  background: #f8d7da;
  color: #721c24;
  border-radius: 4px;
  border: 1px solid #f5c6cb;
}

.hint {
  margin-top: 25px;
  padding: 15px;
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 4px;
  color: #856404;
}

.hint p {
  margin: 5px 0;
}

.admin-info {
  text-align: center;
  padding: 40px;
  background: #e8f4fd;
  border-radius: 8px;
  border: 1px solid #b3d7ff;
}

.admin-info h2 {
  color: #0056b3;
  margin-bottom: 15px;
}

.admin-link {
  display: inline-block;
  margin-top: 15px;
  padding: 10px 20px;
  background: #28a745;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 500;
}

.admin-link:hover {
  background: #218838;
}

.reader-profile {
  margin-top: 30px;
}

.profile-card {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-bottom: 40px;
}

.profile-section {
  padding: 25px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e9ecef;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.profile-section h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #495057;
  border-bottom: 2px solid #dee2e6;
  padding-bottom: 10px;
}

.info-grid {
  display: grid;
  gap: 15px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f1f3f4;
}

.info-item:last-child {
  border-bottom: none;
}

.info-item .label {
  font-weight: 600;
  color: #495057;
  min-width: 120px;
}

.info-item .value {
  color: #212529;
  text-align: right;
  flex: 1;
  margin-left: 15px;
}

.edit-input {
  padding: 6px 10px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 14px;
  width: 100%;
  box-sizing: border-box;
}

.contact-actions {
  margin-top: 25px;
  padding-top: 15px;
  border-top: 1px solid #e9ecef;
}

.edit-btn, .save-btn, .cancel-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.edit-btn {
  background: #6c757d;
  color: white;
}

.edit-btn:hover {
  background: #5a6268;
}

.save-btn {
  background: #28a745;
  color: white;
  margin-right: 10px;
}

.save-btn:hover:not(:disabled) {
  background: #218838;
}

.cancel-btn {
  background: #dc3545;
  color: white;
}

.cancel-btn:hover:not(:disabled) {
  background: #c82333;
}

.save-btn:disabled, .cancel-btn:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.loans-section, .no-loans {
  margin-top: 30px;
  padding: 25px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.loans-list {
  display: grid;
  gap: 15px;
}

.loan-item {
  padding: 15px;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  background: #f8f9fa;
}

.loan-info h4 {
  margin: 0 0 10px 0;
  color: #212529;
}

.loan-info p {
  margin: 5px 0;
  color: #6c757d;
  font-size: 14px;
}

.no-loans {
  text-align: center;
  color: #6c757d;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .profile-card {
    grid-template-columns: 1fr;
  }

  .info-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .info-item .value {
    text-align: left;
    margin-left: 0;
    margin-top: 5px;
  }
}
</style>