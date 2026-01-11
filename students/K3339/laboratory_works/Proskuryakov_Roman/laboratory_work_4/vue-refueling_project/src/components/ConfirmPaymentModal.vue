Функционал страничек не должен меняться, только стиль. Ещё не должны пропадать какие либо элементы. Постарайся делать в исполняемом коде и расположении элементов минимум изменений, чтобы не возникли баги.

Текущие файлы scss:
```scss:src/styles/variables.scss
// Переменные для темы АЗС
$fuel-primary: #1976D2;
$fuel-secondary: #FF9800;
$fuel-success: #4CAF50;
$fuel-warning: #FB8C00;
$fuel-error: #D32F2F;

// Кастомные классы
.fuel-card {
  border-left: 4px solid $fuel-secondary;
}

.fuel-btn {
  background: linear-gradient(135deg, $fuel-secondary, $fuel-warning) !important;
  color: white !important;
}

.fuel-table {
  th {
    background-color: lighten($fuel-primary, 45%) !important;
  }
  
  tr:hover {
    background-color: lighten($fuel-secondary, 40%) !important;
  }
}
```

```scss:src/styles/main.scss
@import './variables.scss';

// Глобальные стили
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  font-family: 'Roboto', sans-serif;
}

// Кастомные утилиты
.text-fuel {
  color: $fuel-secondary;
}

.bg-fuel {
  background-color: $fuel-secondary;
}

// Анимации
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

// Адаптивные классы
@media (max-width: 600px) {
  .mobile-stack {
    flex-direction: column !important;
  }
  
  .mobile-full-width {
    width: 100% !important;
  }
}
```

Сейчас нам надо адаптировать под vuetify файл ConfirmPaymentModal.vue
```
<template>
  <div v-if="visible" class="modal-overlay" @click="handleOverlayClick">
    <div class="modal-content" @click.stop>
      <h2>Подтверждение оплаты</h2>
      
      <div class="payment-details">
        <p><strong>Топливо:</strong> {{ details.fuelInfo }}</p>
        <p><strong>Количество литров:</strong> {{ details.liters }}</p>
        <p><strong>Цена за литр:</strong> {{ details.pricePerLiter }} ₽</p>
        <p><strong>Начальная сумма:</strong> {{ details.initialAmount }} ₽</p>
        <p><strong>Скидка:</strong> {{ details.discount }} ₽</p>
        <p><strong>Итоговая сумма:</strong> {{ details.finalAmount }} ₽</p>
        <p><strong>Номер карты:</strong> {{ details.cardId }}</p>
      </div>
      
      <div class="modal-actions">
        <button @click="confirm" class="confirm-btn" :disabled="loading">
          <span v-if="loading">Обработка...</span>
          <span v-else>Подтвердить оплату</span>
        </button>
        <button @click="cancel" class="cancel-btn" :disabled="loading">
          Отмена
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  visible: Boolean,
  details: Object,
  loading: Boolean
})

const emit = defineEmits(['confirm', 'cancel'])

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
  max-width: 500px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.modal-content h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #333;
}

.payment-details {
  margin-bottom: 2rem;
}

.payment-details p {
  margin: 0.75rem 0;
  font-size: 1rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.confirm-btn {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  min-width: 180px;
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
```