<template>
  <div v-if="visible" class="modal-overlay" @click="handleOverlayClick">
    <div class="modal-content" @click.stop>
      <h2>Подтверждение выдачи карты</h2>
      
      <div class="client-details">
        <h3>Данные клиента:</h3>
        <div class="details-grid">
          <div class="detail-item">
            <span class="label">Фамилия:</span>
            <span class="value">{{ clientData.surname }}</span>
          </div>
          <div class="detail-item">
            <span class="label">Имя:</span>
            <span class="value">{{ clientData.name }}</span>
          </div>
          <div class="detail-item">
            <span class="label">Отчество:</span>
            <span class="value">{{ clientData.patronymic }}</span>
          </div>
          <div class="detail-item">
            <span class="label">Телефон:</span>
            <span class="value">{{ formattedPhone }}</span>
          </div>
          <div class="detail-item">
            <span class="label">Адрес:</span>
            <span class="value">{{ clientData.address }}</span>
          </div>
        </div>
      </div>
      
      <div class="card-details">
        <h3>Параметры карты:</h3>
        <div class="details-grid">
          <div class="detail-item">
            <span class="label">Период действия:</span>
            <span class="value">{{ periodText }}</span>
          </div>
          <div class="detail-item">
            <span class="label">Начало действия:</span>
            <span class="value">{{ formatDate(startDate) }}</span>
          </div>
          <div v-if="endDate" class="detail-item">
            <span class="label">Окончание действия:</span>
            <span class="value">{{ formatDate(endDate) }}</span>
          </div>
          <div v-else class="detail-item">
            <span class="label">Окончание действия:</span>
            <span class="value">Бессрочно</span>
          </div>
        </div>
      </div>
      
      <div class="modal-actions">
        <button @click="confirm" class="confirm-btn" :disabled="loading">
          <span v-if="loading">Создание...</span>
          <span v-else>Выдать карту</span>
        </button>
        <button @click="cancel" class="cancel-btn" :disabled="loading">
          Отмена
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, computed } from 'vue'

const props = defineProps({
  visible: Boolean,
  clientData: Object,
  period: String,
  loading: Boolean
})

const emit = defineEmits(['confirm', 'cancel'])

// Форматирование номера телефона
const formattedPhone = computed(() => {
  let phone = props.clientData.phone_number
  if (!phone) return ''
  
  // Если phone - это число, преобразуем в строку
  if (typeof phone === 'number') {
    phone = phone.toString()
  }
  
  const cleaned = phone.replace(/\D/g, '')
  if (cleaned.length === 11 && (cleaned.startsWith('7') || cleaned.startsWith('8'))) {
    return `+7 (${cleaned.substring(1, 4)}) ${cleaned.substring(4, 7)}-${cleaned.substring(7, 9)}-${cleaned.substring(9, 11)}`
  }
  return phone
})

// Текст периода
const periodText = computed(() => {
  const periods = {
    month: '1 месяц',
    year: '1 год',
    forever: 'Бессрочно'
  }
  return periods[props.period] || '1 месяц'
})

// Даты для карты
const startDate = computed(() => new Date())
const endDate = computed(() => {
  const date = new Date()
  switch (props.period) {
    case 'month':
      date.setMonth(date.getMonth() + 1)
      return date
    case 'year':
      date.setFullYear(date.getFullYear() + 1)
      return date
    case 'forever':
      return null
    default:
      date.setMonth(date.getMonth() + 1)
      return date
  }
})

const formatDate = (date) => {
  return date.toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

const confirm = () => {
  emit('confirm')
}

const cancel = () => {
  emit('cancel')
}

const handleOverlayClick = () => {
  if (!props.loading) {
    cancel()
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.modal-content h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #333;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 0.5rem;
}

.client-details, .card-details {
  margin-bottom: 2rem;
}

.client-details h3, .card-details h3 {
  margin-bottom: 1rem;
  color: #555;
}

.details-grid {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 0.75rem;
  background-color: #f9f9f9;
  padding: 1rem;
  border-radius: 6px;
  border: 1px solid #eee;
}

.detail-item {
  display: contents;
}

.label {
  font-weight: bold;
  color: #666;
  text-align: right;
  padding-right: 1rem;
}

.value {
  color: #333;
  word-break: break-word;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #eee;
}

.confirm-btn {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  min-width: 150px;
}

.confirm-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.confirm-btn:hover:not(:disabled) {
  background-color: #218838;
}

.cancel-btn {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
}

.cancel-btn:hover {
  background-color: #5a6268;
}
</style>