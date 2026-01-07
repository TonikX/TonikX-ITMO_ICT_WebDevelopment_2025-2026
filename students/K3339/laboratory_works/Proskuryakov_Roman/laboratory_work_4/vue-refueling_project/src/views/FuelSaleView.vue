<template>
  <div class="fuel-sale-container">
    <h1>Продажа топлива</h1>
    
    <!-- Сообщения об ошибках и успехе -->
    <div v-if="error" class="alert alert-error">
      {{ error }}
      <button @click="clearError" class="close-btn">×</button>
    </div>
    
    <div v-if="successMessage" class="alert alert-success">
      {{ successMessage }}
      <button @click="clearSuccessMessage" class="close-btn">×</button>
    </div>
    
    <div class="content-wrapper">
      <!-- Левая часть: таблица с ценами -->
      <div class="prices-section">
        <h2>Доступное топливо</h2>
        
        <div v-if="loading && !stationPrices.length" class="loading">
          Загрузка цен...
        </div>
        
        <div v-else-if="!stationPrices.length" class="no-data">
          Нет доступного топлива на вашей станции
        </div>
        
        <div v-else class="prices-table-container">
          <table class="prices-table">
            <thead>
              <tr>
                <th></th>
                <th>Топливо</th>
                <th>Цена за литр (₽)</th>
                <th>Действует с</th>
                <th>Действует до</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="price in stationPrices" 
                :key="price.id_fuel_price"
                :class="{ 'selected': isSelected(price) }"
                @click="selectPrice(price)"
                class="price-row"
              >
                <td class="radio-cell">
                  <input 
                    type="radio" 
                    name="fuel-price" 
                    :checked="isSelected(price)"
                    @change="selectPrice(price)"
                  />
                </td>
                <td class="fuel-info">{{ price.fuel_info }}</td>
                <td class="price-cell">{{ price.per_liter }}</td>
                <td class="date-cell">{{ formatDate(price.start_time) }}</td>
                <td class="date-cell">{{ price.end_time ? formatDate(price.end_time) : 'Бессрочно' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Правая часть: форма ввода -->
      <div class="form-section">
        <div class="form-group">
          <label for="liters">Количество литров:</label>
          <input
            id="liters"
            v-model="liters"
            type="number"
            step="0.1"
            min="0.1"
            placeholder="Например: 20.5"
            :disabled="!selectedPrice"
            @input="handleLitersChange"
          />
        </div>
        
        <div class="form-group">
          <label for="card-id">Номер карты клиента:</label>
          <div class="card-input-group">
            <input
              id="card-id"
              v-model="cardId"
              type="number"
              min="1"
              placeholder="Введите ID карты"
              :disabled="!selectedPrice || !liters"
            />
            <button 
              @click="applyCard"
              :disabled="!cardId || !selectedPrice || !liters || cardIdLoading"
              class="apply-btn"
            >
              <span v-if="cardIdLoading">...</span>
              <span v-else>Применить</span>
            </button>
          </div>
        </div>
        
        <!-- Информация о расчете -->
        <div v-if="calculatedInitialAmount > 0" class="calculation-section">
          <div class="calculation-header">
            <h3>Расчет</h3>
          </div>
          
          <div v-if="cardApplied && calculation.cardFound && calculation.cardActive" class="calculation-details">
            <div class="calculation-string">
              {{ paymentString }}
            </div>
            
            <div v-if="!calculation.sufficientBalance" class="insufficient-balance">
              Недостаточно средств на карте
            </div>
            
            <div class="final-amount">
              <strong>К оплате:</strong> {{ calculation.finalAmount.toFixed(2) }} ₽
            </div>
            
            <button 
              @click="showConfirmModal"
              :disabled="!canPay"
              class="pay-btn"
            >
              Оплатить
            </button>
          </div>
          
          <div v-else-if="cardApplied && !calculation.cardFound" class="card-error">
            Карта не найдена
          </div>
          
          <div v-else-if="cardApplied && !calculation.cardActive" class="card-error">
            Карта не активна
          </div>
          
          <div v-else class="no-card-info">
            Введите номер карты и нажмите "Применить" для расчета скидки
          </div>
        </div>
        
        <div v-else-if="selectedPrice" class="enter-liters">
          Введите количество литров для расчета
        </div>
        
        <div v-else class="select-fuel">
          Выберите топливо из таблицы
        </div>
      </div>
    </div>
    
    <!-- Модальное окно подтверждения -->
    <ConfirmPaymentModal
      :visible="showModal"
      :details="confirmationDetails"
      :loading="processingPayment"
      @confirm="executePayment"
      @cancel="hideConfirmModal"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useSalesStore } from '../stores/sales'
import ConfirmPaymentModal from '../components/ConfirmPaymentModal.vue'

const salesStore = useSalesStore()

// Реактивные переменные
const showModal = ref(false)
const processingPayment = ref(false)

// Вычисляемые свойства из хранилища
const stationPrices = computed(() => salesStore.stationPrices)
const selectedPrice = computed(() => salesStore.selectedPrice)
const liters = computed({
  get: () => salesStore.liters,
  set: (value) => salesStore.setLiters(value)
})
const cardId = computed({
  get: () => salesStore.cardId,
  set: (value) => salesStore.cardId = value
})
const cardApplied = computed(() => salesStore.cardApplied)
const calculatedInitialAmount = computed(() => salesStore.calculatedInitialAmount)
const calculation = computed(() => salesStore.calculation)
const paymentString = computed(() => salesStore.paymentString)
const canPay = computed(() => salesStore.canPay)
const loading = computed(() => salesStore.loading)
const error = computed(() => salesStore.error)
const successMessage = computed(() => salesStore.successMessage)
const cardIdLoading = computed(() => salesStore.loading)

// Данные для модального окна подтверждения
const confirmationDetails = computed(() => ({
  fuelInfo: selectedPrice.value?.fuel_info || '',
  liters: liters.value || '',
  pricePerLiter: selectedPrice.value?.per_liter || 0,
  initialAmount: calculation.value.initialAmount || 0,
  discount: calculation.value.discount || 0,
  finalAmount: calculation.value.finalAmount || 0,
  cardId: cardId.value || ''
}))

// Методы
const isSelected = (price) => {
  return selectedPrice.value?.id_fuel_price === price.id_fuel_price
}

const selectPrice = (price) => {
  salesStore.selectPrice(price)
}

const handleLitersChange = (event) => {
  const value = event.target.value
  salesStore.setLiters(value)
}

const applyCard = async () => {
  await salesStore.applyCard()
}

const showConfirmModal = () => {
  if (canPay.value) {
    showModal.value = true
  }
}

const hideConfirmModal = () => {
  showModal.value = false
}

const executePayment = async () => {
  processingPayment.value = true
  const result = await salesStore.executePayment()
  processingPayment.value = false
  
  if (result.success) {
    hideConfirmModal()
  }
}

const clearError = () => {
  salesStore.clearError()
}

const clearSuccessMessage = () => {
  salesStore.clearSuccessMessage()
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU')
}

// Загрузка данных при монтировании
onMounted(() => {
  salesStore.loadStationPrices()
})

// Следим за изменениями литров и выбранного топлива
watch([selectedPrice, liters], ([newPrice, newLiters]) => {
  if (newPrice && newLiters) {
    salesStore.recalculateInitialAmount()
  }
})
</script>

<style scoped>
.fuel-sale-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem;
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

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: inherit;
}

.content-wrapper {
  display: flex;
  gap: 2rem;
  margin-top: 2rem;
}

.prices-section, .form-section {
  flex: 1;
}

.prices-section {
  max-height: 600px;
  overflow-y: auto;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

h2 {
  margin-bottom: 1rem;
  color: #333;
}

.loading, .no-data, .select-fuel, .enter-liters, .no-card-info {
  padding: 2rem;
  text-align: center;
  background-color: #f8f9fa;
  border-radius: 8px;
  color: #666;
}

.prices-table-container {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
}

.prices-table {
  width: 100%;
  border-collapse: collapse;
}

.prices-table th {
  background-color: #f8f9fa;
  padding: 1rem;
  text-align: left;
  font-weight: bold;
  border-bottom: 1px solid #ddd;
}

.prices-table td {
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

.price-row {
  cursor: pointer;
  transition: background-color 0.2s;
}

.price-row:hover {
  background-color: #f0f8ff;
}

.price-row.selected {
  background-color: #e7f3ff;
  border-left: 3px solid #007bff;
}

.radio-cell {
  width: 40px;
  text-align: center;
}

.fuel-info {
  min-width: 200px;
}

.price-cell {
  font-weight: bold;
  color: #28a745;
  min-width: 100px;
}

.date-cell {
  min-width: 120px;
  color: #666;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: bold;
  color: #333;
}

.form-group input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.card-input-group {
  display: flex;
  gap: 0.5rem;
}

.apply-btn {
  padding: 0.75rem 1.5rem;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  white-space: nowrap;
}

.apply-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.apply-btn:not(:disabled):hover {
  background-color: #5a6268;
}

.calculation-section {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
}

.calculation-header {
  margin-bottom: 1rem;
}

.calculation-header h3 {
  margin: 0;
  color: #333;
}

.calculation-details {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.calculation-string {
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
  text-align: center;
  padding: 1rem;
  background-color: white;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.insufficient-balance {
  color: #dc3545;
  font-weight: bold;
  text-align: center;
  padding: 0.5rem;
  background-color: #f8d7da;
  border-radius: 4px;
}

.card-error {
  color: #dc3545;
  font-weight: bold;
  text-align: center;
  padding: 1rem;
  background-color: #f8d7da;
  border-radius: 4px;
}

.final-amount {
  font-size: 1.5rem;
  color: #28a745;
  text-align: center;
  padding: 1rem;
  background-color: white;
  border-radius: 4px;
  border: 2px solid #28a745;
}

.pay-btn {
  padding: 1rem;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.pay-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.pay-btn:not(:disabled):hover {
  background-color: #218838;
}

/* Адаптивность */
@media (max-width: 1024px) {
  .content-wrapper {
    flex-direction: column;
  }
  
  .prices-section {
    max-height: 400px;
  }
}
</style>