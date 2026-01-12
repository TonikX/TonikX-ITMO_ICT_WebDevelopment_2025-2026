<template>
  <v-container class="issue-card-container" fluid>
    <!-- 1. Заголовок в отдельной карточке -->
    <v-card elevation="2" class="pa-4 mb-4">
      <div class="d-flex align-center justify-space-between">
        <h1 class="text-h5 text-primary">Выдача карт клиентам</h1>
      </div>
    </v-card>
    
    <!-- Сообщения об ошибках -->
    <div v-if="error" class="alert alert-error">
      {{ error }}
      <button @click="clearError" class="close-btn">×</button>
    </div>
    
    <!-- Сообщение об успешной выдаче карты -->
    <div v-if="createdCard" class="alert alert-success success-card">
      <div class="success-message">
        <div class="success-header">
          <h3>🎉 Спасибо что стали нашим клиентом!</h3>
        </div>
        <div class="card-details">
          <div class="card-number">
            <span class="label">Ваш номер карты:</span>
            <span class="value highlight">{{ createdCard.id_card }}</span>
          </div>
          <div class="client-info">
            <span class="label">Клиент:</span>
            <span class="value">
              {{ createdCard.client.surname }} 
              {{ createdCard.client.name }} 
              {{ createdCard.client.patronymic }}
            </span>
          </div>
          <div class="card-info">
            <span class="label">Дата начала:</span>
            <span class="value">{{ formatDate(createdCard.start_date) }}</span>
          </div>
          <div v-if="createdCard.end_date" class="card-info">
            <span class="label">Дата окончания:</span>
            <span class="value">{{ formatDate(createdCard.end_date) }}</span>
          </div>
          <div v-else class="card-info">
            <span class="label">Срок действия:</span>
            <span class="value">Бессрочно</span>
          </div>
          <div class="balance-info">
            <span class="label">Начальный баланс:</span>
            <span class="value">{{ createdCard.balance }} ₽</span>
          </div>
        </div>
        <div class="success-actions">
          <button @click="clearCreatedCard" class="continue-btn">
            Выдать ещё одну карту
          </button>
          <button @click="printCardInfo" class="print-btn">
            Распечатать информацию
          </button>
        </div>
      </div>
    </div>
    
    <div v-else>
      <!-- 2. Карточка выбора/создания клиента -->
      <v-card elevation="2" class="mb-4">
        <v-card-title class="bg-primary text-white">
          <v-icon icon="mdi-account" class="mr-2"></v-icon>
          Данные клиента
        </v-card-title>
        
        <v-card-text>
          <div class="content-wrapper">
            <!-- Выбор типа клиента -->
            <div class="client-type-section">
              <div class="checkbox-group">
                <input
                  id="new-client"
                  type="checkbox"
                  v-model="isNewClient"
                  @change="toggleNewClient"
                />
                <label for="new-client">Новый клиент</label>
              </div>
              
              <div class="client-type-hint">
                {{ isNewClient ? 'Заполните данные нового клиента' : 'Найдите существующего клиента по номеру телефона' }}
              </div>
            </div>
            
            <!-- Форма для нового клиента -->
            <div v-if="isNewClient" class="new-client-form">
              <h2>Данные нового клиента</h2>
              
              <div class="form-grid">
                <div class="form-group">
                  <label for="surname">Фамилия *</label>
                  <input
                    id="surname"
                    v-model="newClient.surname"
                    type="text"
                    placeholder="Иванов"
                    required
                  />
                </div>
                
                <div class="form-group">
                  <label for="name">Имя *</label>
                  <input
                    id="name"
                    v-model="newClient.name"
                    type="text"
                    placeholder="Иван"
                    required
                  />
                </div>
                
                <div class="form-group">
                  <label for="patronymic">Отчество *</label>
                  <input
                    id="patronymic"
                    v-model="newClient.patronymic"
                    type="text"
                    placeholder="Иванович"
                    required
                  />
                </div>
                
                <div class="form-group">
                  <label for="phone">Телефон *</label>
                  <input
                    id="phone"
                    v-model="newClient.phone_number"
                    type="tel"
                    placeholder="79991234567"
                    required
                    @input="formatPhoneInput"
                  />
                  <small class="hint">Введите 11 цифр, начиная с 7 или 8</small>
                </div>
                
                <div class="form-group full-width">
                  <label for="address">Адрес *</label>
                  <input
                    id="address"
                    v-model="newClient.address"
                    type="text"
                    placeholder="г. Москва, ул. Примерная, д. 1"
                    required
                  />
                </div>
              </div>
            </div>
            
            <!-- Поиск существующего клиента -->
            <div v-else class="existing-client-form">
              <h2>Поиск клиента</h2>
              
              <div class="search-section">
                <div class="search-input-group">
                  <input
                    v-model="searchPhone"
                    type="tel"
                    placeholder="Введите номер телефона"
                    @input="handlePhoneSearch"
                    @keyup.enter="searchClients"
                  />
                  <button 
                    @click="searchClients" 
                    :disabled="!searchPhone.trim() || loading"
                    class="search-btn"
                  >
                    <span v-if="loading">Поиск...</span>
                    <span v-else>Найти</span>
                  </button>
                </div>
                
                <div v-if="foundClients.length > 0" class="found-clients">
                  <h3>Найденные клиенты:</h3>
                  <div class="clients-table-container">
                    <table class="clients-table">
                      <thead>
                        <tr>
                          <th>ФИО</th>
                          <th>Телефон</th>
                          <th>Адрес</th>
                          <th>Действие</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr 
                          v-for="client in foundClients" 
                          :key="client.id_client"
                          :class="{ 'selected': isSelected(client) }"
                        >
                          <td>{{ client.surname }} {{ client.name }} {{ client.patronymic }}</td>
                          <td>{{ formatDisplayPhone(client.phone_number) }}</td>
                          <td>{{ client.address }}</td>
                          <td>
                            <button 
                              @click="selectClient(client)"
                              class="select-btn"
                            >
                              {{ isSelected(client) ? 'Выбрано' : 'Выбрать' }}
                            </button>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
                
                <div v-else-if="searchPhone && !loading" class="no-clients">
                  Клиенты с таким номером телефона не найдены
                </div>
              </div>
            </div>
          </div>
        </v-card-text>
      </v-card>

      <!-- 3. Карточка выбора времени и кнопки подтверждения -->
      <v-card elevation="2">
        <v-card-title class="bg-secondary text-white">
          <v-icon icon="mdi-card-account-details" class="mr-2"></v-icon>
          Оформление карты
        </v-card-title>
        
        <v-card-text>
          <div v-if="canIssueCard" class="card-period-section">
            <h2>Выберите период действия карты</h2>
            
            <div class="period-options">
              <div 
                v-for="option in periodOptions" 
                :key="option.value"
                :class="['period-option', { 'selected': cardPeriod === option.value }]"
                @click="selectPeriod(option.value)"
              >
                <div class="period-icon">{{ option.icon }}</div>
                <div class="period-info">
                  <div class="period-title">{{ option.title }}</div>
                  <div class="period-desc">{{ option.description }}</div>
                </div>
              </div>
            </div>
            
            <div class="issue-action">
              <button 
                @click="showConfirmModal"
                class="issue-btn"
                :disabled="!canIssueCard || creatingCard"
              >
                <span v-if="creatingCard">Создание...</span>
                <span v-else>Оформить карту</span>
              </button>
              <div class="selected-period-hint">
                Выбран период: <strong>{{ selectedPeriodText }}</strong>
              </div>
            </div>
          </div>
          
          <div v-else class="fill-data-hint">
            Заполните данные клиента, чтобы продолжить
          </div>
        </v-card-text>
      </v-card>
    </div>
    
    <!-- Модальное окно подтверждения -->
    <ConfirmIssueCardModal
      :visible="showModal"
      :client-data="isNewClient ? newClient : selectedClient"
      :period="cardPeriod"
      :loading="creatingCard"
      @confirm="issueCard"
      @cancel="hideConfirmModal"
    />
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useClientsStore } from '../stores/clients'
import ConfirmIssueCardModal from '../components/ConfirmIssueCardModal.vue'

const clientsStore = useClientsStore()

// Реактивные переменные
const showModal = ref(false)

// Вычисляемые свойства из хранилища
const isNewClient = computed({
  get: () => clientsStore.isNewClient,
  set: (value) => clientsStore.toggleNewClient(value)
})
const newClient = computed(() => clientsStore.newClient)
const searchPhone = computed({
  get: () => clientsStore.searchPhone,
  set: (value) => clientsStore.searchPhone = value
})
const foundClients = computed(() => clientsStore.foundClients)
const selectedClient = computed(() => clientsStore.selectedClient)
const cardPeriod = computed(() => clientsStore.cardPeriod)
const canIssueCard = computed(() => clientsStore.canIssueCard)
const creatingCard = computed(() => clientsStore.creatingCard)
const createdCard = computed(() => clientsStore.createdCard)
const loading = computed(() => clientsStore.loading)
const error = computed(() => clientsStore.error)

// Опции периода
const periodOptions = [
  {
    value: 'month',
    title: '1 месяц',
    description: 'Карта действует 30 дней',
    icon: '📅'
  },
  {
    value: 'year',
    title: '1 год',
    description: 'Карта действует 365 дней',
    icon: '📆'
  },
  {
    value: 'forever',
    title: 'Бессрочно',
    description: 'Карта без срока действия',
    icon: '∞'
  }
]

// Текст выбранного периода
const selectedPeriodText = computed(() => {
  const option = periodOptions.find(opt => opt.value === cardPeriod.value)
  return option ? option.title : 'не выбран'
})

// Методы
const toggleNewClient = () => {
  clientsStore.toggleNewClient(isNewClient.value)
}

const formatPhoneInput = (event) => {
  let value = event.target.value.replace(/\D/g, '')
  
  // Ограничиваем длину
  if (value.length > 11) {
    value = value.substring(0, 11)
  }
  
  // Если номер начинается с 8, меняем на 7
  if (value.length === 11 && value.startsWith('8')) {
    value = '7' + value.substring(1)
  }
  
  if (isNewClient.value) {
    clientsStore.newClient.phone_number = value
  } else {
    clientsStore.searchPhone = value
  }
}

const handlePhoneSearch = () => {
  // Дебаунс для поиска
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    const phoneDigits = searchPhone.value.replace(/\D/g, '')
    if (phoneDigits.length >= 10) {
      clientsStore.searchClients()
    } else if (phoneDigits.length > 0) {
      clientsStore.foundClients = []
      clientsStore.selectedClient = null
    }
  }, 500)
}

let searchTimeout = null

const searchClients = () => {
  clientsStore.searchClients()
}

const selectClient = (client) => {
  clientsStore.selectClient(client)
}

const isSelected = (client) => {
  return selectedClient.value?.id_client === client.id_client
}

const formatDisplayPhone = (phone) => {
  const cleaned = phone.toString().replace(/\D/g, '')
  if (cleaned.length === 11 && cleaned.startsWith('7')) {
    return `+7 (${cleaned.substring(1, 4)}) ${cleaned.substring(4, 7)}-${cleaned.substring(7, 9)}-${cleaned.substring(9, 11)}`
  }
  return phone
}

const selectPeriod = (period) => {
  clientsStore.setCardPeriod(period)
}

const showConfirmModal = () => {
  showModal.value = true
}

const hideConfirmModal = () => {
  showModal.value = false
}

const issueCard = async () => {
  const result = await clientsStore.issueCard()
  if (result.success) {
    hideConfirmModal()
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU')
}

const clearError = () => {
  clientsStore.clearError()
}

const clearCreatedCard = () => {
  clientsStore.clearCreatedCard()
}

const printCardInfo = () => {
  window.print()
}

// Инициализация при монтировании
onMounted(() => {
  clientsStore.resetAll()
})
</script>

<style scoped>
/* Сохранены все оригинальные стили без изменений */
.issue-card-container {
  max-width: 100%;
  margin: 0 auto;
  padding: 12px;
}

.alert {
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 4px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.alert-error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.alert-success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.success-card {
  padding: 2rem;
  margin: 2rem 0;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.success-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.success-header h3 {
  color: #155724;
  font-size: 1.5rem;
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.card-details {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  border: 1px solid #c3e6cb;
}

.card-details > div {
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.card-details > div:last-child {
  margin-bottom: 0;
}

.card-details .label {
  font-weight: bold;
  color: #555;
  min-width: 180px;
  text-align: right;
}

.card-details .value {
  color: #333;
  font-size: 1rem;
}

.card-details .value.highlight {
  font-size: 1.8rem;
  font-weight: bold;
  color: #28a745;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #d4edda, #c3e6cb);
  border-radius: 8px;
  border: 2px solid #28a745;
}

.client-info .value {
  font-weight: bold;
  font-size: 1.1rem;
}

.card-info .value {
  color: #666;
}

.balance-info .value {
  color: #17a2b8;
  font-weight: bold;
}

.success-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.continue-btn {
  padding: 0.75rem 2rem;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.continue-btn:hover {
  background-color: #218838;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
}

.print-btn {
  padding: 0.75rem 2rem;
  background-color: #17a2b8;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.print-btn:hover {
  background-color: #138496;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(23, 162, 184, 0.3);
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: inherit;
}

.content-wrapper {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 2rem;
  margin-top: 1rem;
}

.client-type-section {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #dee2e6;
}

.checkbox-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.checkbox-group input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.checkbox-group label {
  font-size: 1.1rem;
  font-weight: bold;
  color: #333;
  cursor: pointer;
}

.client-type-hint {
  color: #666;
  font-size: 0.9rem;
}

.new-client-form, .existing-client-form {
  margin-bottom: 2rem;
}

h2 {
  margin-bottom: 1.5rem;
  color: #333;
  font-size: 1.3rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  font-weight: bold;
  color: #555;
}

.form-group input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.hint {
  color: #666;
  font-size: 0.8rem;
}

.search-section {
  margin-top: 1rem;
}

.search-input-group {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.search-input-group input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.search-btn {
  padding: 0.75rem 1.5rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  white-space: nowrap;
}

.search-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.search-btn:not(:disabled):hover {
  background-color: #0056b3;
}

.found-clients h3 {
  margin-bottom: 1rem;
  color: #555;
  font-size: 1.1rem;
}

.clients-table-container {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
}

.clients-table {
  width: 100%;
  border-collapse: collapse;
}

.clients-table th {
  background-color: #f8f9fa;
  padding: 1rem;
  text-align: left;
  font-weight: bold;
  border-bottom: 2px solid #dee2e6;
}

.clients-table td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #eee;
}

.clients-table tr:last-child td {
  border-bottom: none;
}

.clients-table tr:hover {
  background-color: #f5f5f5;
}

.clients-table tr.selected {
  background-color: #e7f3ff;
}

.select-btn {
  padding: 0.5rem 1rem;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.select-btn:hover {
  background-color: #218838;
}

.no-clients {
  padding: 2rem;
  text-align: center;
  color: #666;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px dashed #ddd;
}

.card-period-section {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #dee2e6;
}

.period-options {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1rem;
}

.period-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 1.5rem 1rem;
  border: 2px solid #ddd;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.period-option:hover {
  border-color: #667eea;
  background-color: #f8f9ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.period-option.selected {
  border-color: #28a745;
  background-color: #f0fff4;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(40, 167, 69, 0.2);
}

.period-icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.period-info {
  flex: 1;
}

.period-title {
  font-weight: bold;
  color: #333;
  margin-bottom: 0.25rem;
  font-size: 1.1rem;
}

.period-desc {
  font-size: 0.85rem;
  color: #666;
  line-height: 1.3;
}

.issue-action {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.issue-btn {
  padding: 1rem 3rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  min-width: 250px;
}

.issue-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.issue-btn:active:not(:disabled) {
  transform: translateY(0);
}

.issue-btn:disabled {
  background: linear-gradient(135deg, #cccccc 0%, #999999 100%);
  cursor: not-allowed;
  box-shadow: none;
  transform: none;
}

.selected-period-hint {
  color: #666;
  font-size: 0.9rem;
  text-align: center;
  padding: 0.5rem 1rem;
  background-color: #f8f9fa;
  border-radius: 20px;
  border: 1px solid #dee2e6;
}

.selected-period-hint strong {
  color: #28a745;
}

.fill-data-hint {
  padding: 2rem;
  text-align: center;
  color: #666;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px dashed #ddd;
  margin-top: 2rem;
}

.text-h5 {
  font-size: 1.4rem !important;
}

/* Стили для карточек */
.v-card-title.bg-primary {
  background: linear-gradient(135deg, var(--v-theme-primary), var(--v-theme-primary-darken-1));
  padding: 12px 16px;
  font-size: 1rem;
}

.v-card-title.bg-secondary {
  background: linear-gradient(135deg, var(--v-theme-secondary), var(--v-theme-secondary-darken-1));
  padding: 12px 16px;
  font-size: 1rem;
}

/* Стили для печати */
@media print {
  .navbar, 
  .filters-section, 
  .form-section, 
  .card-period-section,
  .modal-overlay,
  .alert-error,
  .close-btn,
  .continue-btn,
  .print-btn {
    display: none !important;
  }
  
  .success-card {
    box-shadow: none;
    border: 1px solid #000;
    margin: 0;
    padding: 1rem;
  }
  
  .alert-success {
    background-color: white !important;
    border: 2px solid #000 !important;
  }
  
  .value.highlight {
    background: white !important;
    border: 2px solid #000 !important;
  }
}

/* Адаптивность для сообщения об успехе */
@media (max-width: 768px) {
  .success-card {
    padding: 1rem;
  }
  
  .success-header h3 {
    font-size: 1.2rem;
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .card-details {
    padding: 1rem;
  }
  
  .card-details > div {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }
  
  .card-details .label {
    min-width: auto;
    text-align: left;
    font-size: 0.9rem;
  }
  
  .card-details .value.highlight {
    font-size: 1.5rem;
    text-align: center;
    width: 100%;
  }
  
  .success-actions {
    flex-direction: column;
  }
  
  .continue-btn, .print-btn {
    width: 100%;
  }
}

/* Адаптивность */
@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .period-options {
    grid-template-columns: 1fr;
  }
  
  .issue-btn {
    width: 100%;
    min-width: auto;
  }
}
</style>