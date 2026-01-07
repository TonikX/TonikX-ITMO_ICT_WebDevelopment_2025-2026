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
      <!-- Таблица с ценами - занимает фиксированную высоту -->
      <div class="prices-section">
        <h2>Доступное топливо на вашей станции</h2>
        
        <div v-if="loading && !stationPrices.length" class="loading">
          Загрузка цен...
        </div>
        
        <div v-else-if="!stationPrices.length" class="no-data">
          Нет доступного топлива на вашей станции
        </div>
        
        <div v-else class="table-wrapper">
          <div class="table-container">
            <table class="prices-table">
              <thead>
                <tr>
                  <th class="selection-column"></th>
                  <th class="fuel-column">Топливо</th>
                  <th class="brand-column">Бренд</th>
                  <th class="season-column">Сезон</th>
                  <th class="density-column">Плотность</th>
                  <th class="temp-column">Темп. горения</th>
                  <th class="min-temp-column">Мин. темп.</th>
                  <th class="sulfur-column">Сера, %</th>
                  <th class="price-column">Цена за литр (₽)</th>
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
                  <td class="selection-column">
                    <input 
                      type="radio" 
                      name="fuel-price" 
                      :checked="isSelected(price)"
                      @change="selectPrice(price)"
                    />
                  </td>
                  <td class="fuel-column">{{ getFuelTitle(price) }}</td>
                  <td class="brand-column">{{ getFuelBrand(price) }}</td>
                  <td class="season-column">{{ getSeasonText(price) }}</td>
                  <td class="density-column">{{ getFuelDensity(price) }}</td>
                  <td class="temp-column">{{ getBurningTemp(price) }}°C</td>
                  <td class="min-temp-column">{{ getMinTemp(price) }}°C</td>
                  <td class="sulfur-column">{{ getSulfurPercent(price) }}%</td>
                  <td class="price-column">
                    <span class="price-value">{{ price.per_liter }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div v-if="stationPrices.length > 0" class="table-info">
            <div class="selected-info" v-if="selectedPrice">
              <strong>Выбрано:</strong> {{ getFuelTitle(selectedPrice) }} ({{ getFuelBrand(selectedPrice) }})
              <span class="price-info">по {{ selectedPrice.per_liter }} ₽/л</span>
            </div>
            <div class="hint">Выберите топливо кликом по строке таблицы</div>
          </div>
        </div>
      </div>
      
      <!-- Форма ввода - под таблицей, но теперь более компактная -->
      <div class="form-section">
        <div class="form-header">
          <h3>Оформление покупки</h3>
        </div>
        
        <div class="form-grid">
          <div class="form-row">
            <div class="form-group">
              <label for="liters">Количество литров:</label>
              <div class="input-with-unit">
                <input
                  id="liters"
                  v-model="liters"
                  type="number"
                  step="0.1"
                  min="0.1"
                  placeholder="20.5"
                  :disabled="!selectedPrice"
                  @input="handleLitersChange"
                />
                <span class="unit">л</span>
              </div>
              <div class="form-hint" v-if="selectedPrice && liters">
                {{ calculatedInitialAmount.toFixed(2) }} ₽ ({{ selectedPrice.per_liter }} ₽ × {{ liters }} л)
              </div>
            </div>
            
            <div class="form-group">
              <label for="card-id">Номер карты клиента:</label>
              <div class="card-input-group">
                <input
                  id="card-id"
                  v-model="cardId"
                  type="number"
                  min="1"
                  placeholder="12345"
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
              <div class="form-hint">
                Введите номер и нажмите "Применить"
              </div>
            </div>
          </div>
          
          <!-- Расчет и оплата -->
          <div class="calculation-section" v-if="calculatedInitialAmount > 0">
            <div class="calculation-header">
              <h4>Расчет платежа</h4>
            </div>
            
            <div v-if="cardApplied && calculation.cardFound && calculation.cardActive" class="calculation-details">
              <div class="amount-breakdown">
                <div class="amount-row">
                  <span class="label">Начальная сумма:</span>
                  <span class="value">{{ calculation.initialAmount.toFixed(2) }} ₽</span>
                </div>
                <div class="amount-row discount">
                  <span class="label">Скидка:</span>
                  <span class="value">-{{ calculation.discount.toFixed(2) }} ₽</span>
                </div>
                <div class="amount-row total">
                  <span class="label">Итого к оплате:</span>
                  <span class="value">{{ calculation.finalAmount.toFixed(2) }} ₽</span>
                </div>
              </div>
              
              <div class="payment-info">
                <div v-if="!calculation.sufficientBalance" class="insufficient-balance">
                  ⚠️ Недостаточно средств на карте
                </div>
                <div v-else class="balance-ok">
                  ✅ На карте достаточно средств
                </div>
                
                <button 
                  @click="showConfirmModal"
                  :disabled="!canPay"
                  class="pay-btn"
                >
                  <span class="pay-icon">💳</span>
                  Оплатить {{ calculation.finalAmount.toFixed(2) }} ₽
                </button>
              </div>
            </div>
            
            <div v-else-if="cardApplied && !calculation.cardFound" class="card-status error">
              ❌ Карта не найдена
            </div>
            
            <div v-else-if="cardApplied && !calculation.cardActive" class="card-status error">
              ❌ Карта не активна
            </div>
            
            <div v-else class="prompt">
              Введите номер карты и нажмите "Применить" для расчета скидки
            </div>
          </div>
          
          <div v-else-if="selectedPrice && liters" class="prompt">
            Введите номер карты для расчета скидки
          </div>
          
          <div v-else-if="selectedPrice" class="prompt">
            Введите количество литров
          </div>
          
          <div v-else class="prompt">
            Выберите топливо из таблицы
          </div>
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

// Вспомогательные методы для извлечения данных
const getFuelTitle = (price) => {
  return price.sold_fuel?.id_produced_fuel?.id_kind_fuel?.title || 'Неизвестно'
}

const getFuelBrand = (price) => {
  return price.sold_fuel?.id_produced_fuel?.id_kind_fuel?.brand || '-'
}

const getSeasonText = (price) => {
  const season = price.sold_fuel?.id_produced_fuel?.id_kind_fuel?.season
  const seasons = {
    1: 'Лето',
    2: 'Зима',
    3: 'Всесезон'
  }
  return seasons[season] || '-'
}

const getFuelDensity = (price) => {
  return price.sold_fuel?.id_produced_fuel?.id_kind_fuel?.density || '-'
}

const getBurningTemp = (price) => {
  return price.sold_fuel?.id_produced_fuel?.id_kind_fuel?.burning_temp || '-'
}

const getMinTemp = (price) => {
  return price.sold_fuel?.id_produced_fuel?.id_kind_fuel?.min_usage_temp || '-'
}

const getSulfurPercent = (price) => {
  return price.sold_fuel?.id_produced_fuel?.id_kind_fuel?.percent_sulfur || '-'
}

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
  height: calc(100vh - 60px); /* Учитываем высоту навбара */
  display: flex;
  flex-direction: column;
}

.alert {
  padding: 0.75rem 1rem;
  margin-bottom: 1rem;
  border-radius: 4px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
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
  font-size: 1.25rem;
  cursor: pointer;
  color: inherit;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  flex: 1;
  min-height: 0;
}

h1 {
  margin: 0 0 1rem 0;
  font-size: 1.5rem;
  flex-shrink: 0;
}

h2 {
  margin: 0 0 0.75rem 0;
  font-size: 1.25rem;
  color: #333;
}

h3 {
  margin: 0;
  font-size: 1.1rem;
}

h4 {
  margin: 0;
  font-size: 1rem;
}

/* Секция с таблицей */
.prices-section {
  flex: 0 0 auto; /* Фиксированная высота */
  min-height: 300px; /* Минимум на 5 строк */
  max-height: 400px; /* Максимум, чтобы не занимала весь экран */
  display: flex;
  flex-direction: column;
}

.table-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.table-container {
  flex: 1;
  overflow: auto;
  min-height: 200px;
}

.prices-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 800px;
  font-size: 0.9rem;
}

.prices-table th {
  background-color: #f8f9fa;
  padding: 0.6rem 0.5rem;
  text-align: left;
  font-weight: 600;
  border-bottom: 1px solid #dee2e6;
  position: sticky;
  top: 0;
  z-index: 10;
  white-space: nowrap;
  font-size: 0.85rem;
}

.prices-table td {
  padding: 0.6rem 0.5rem;
  border-bottom: 1px solid #f0f0f0;
  white-space: nowrap;
}

/* Стили для колонок */
.selection-column {
  width: 40px;
  text-align: center;
  padding-left: 0.75rem;
}

.fuel-column {
  min-width: 120px;
  font-weight: 500;
}

.brand-column {
  min-width: 100px;
}

.season-column {
  width: 80px;
  text-align: center;
}

.density-column {
  width: 70px;
  text-align: center;
}

.temp-column, .min-temp-column {
  width: 90px;
  text-align: center;
}

.sulfur-column {
  width: 70px;
  text-align: center;
}

.price-column {
  width: 100px;
  text-align: right;
  padding-right: 1rem;
}

.price-row {
  cursor: pointer;
  transition: background-color 0.15s;
}

.price-row:hover {
  background-color: #f8f9fa;
}

.price-row.selected {
  background-color: #e7f3ff;
  border-left: 3px solid #007bff;
}

.price-value {
  font-weight: bold;
  color: #28a745;
  font-size: 1em;
}

.table-info {
  padding: 0.5rem 0.75rem;
  background-color: #f8f9fa;
  border-top: 1px solid #dee2e6;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
}

.selected-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.price-info {
  color: #28a745;
  font-weight: 500;
}

.hint {
  color: #6c757d;
}

/* Секция формы */
.form-section {
  flex: 0 0 auto;
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 1rem;
  border: 1px solid #dee2e6;
}

.form-header {
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #dee2e6;
}

.form-header h3 {
  color: #333;
}

.form-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 0.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.form-group label {
  font-weight: 500;
  color: #333;
  font-size: 0.9rem;
}

.form-group input {
  padding: 0.6rem 0.75rem;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 0.95rem;
  width: 100%;
  transition: border-color 0.15s;
}

.form-group input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.form-group input:disabled {
  background-color: #e9ecef;
  cursor: not-allowed;
}

.input-with-unit {
  position: relative;
  display: flex;
}

.input-with-unit input {
  padding-right: 2.5rem;
}

.unit {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #6c757d;
  font-size: 0.9rem;
}

.card-input-group {
  display: flex;
  gap: 0.5rem;
}

.apply-btn {
  padding: 0.6rem 1rem;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  white-space: nowrap;
  font-size: 0.9rem;
  font-weight: 500;
  transition: background-color 0.15s;
  flex-shrink: 0;
}

.apply-btn:disabled {
  background-color: #adb5bd;
  cursor: not-allowed;
}

.apply-btn:not(:disabled):hover {
  background-color: #5a6268;
}

.form-hint {
  font-size: 0.8rem;
  color: #6c757d;
  min-height: 1rem;
}

/* Секция расчета */
.calculation-section {
  background-color: white;
  border-radius: 6px;
  padding: 1rem;
  border: 1px solid #dee2e6;
}

.calculation-header {
  margin-bottom: 0.75rem;
}

.calculation-header h4 {
  color: #333;
}

.calculation-details {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.amount-breakdown {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.amount-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.4rem 0;
}

.amount-row .label {
  color: #495057;
  font-size: 0.9rem;
}

.amount-row .value {
  font-weight: 500;
  font-size: 0.9rem;
}

.amount-row.discount {
  color: #28a745;
  border-top: 1px dashed #dee2e6;
  padding-top: 0.6rem;
}

.amount-row.total {
  font-weight: bold;
  color: #212529;
  border-top: 2px solid #dee2e6;
  padding-top: 0.6rem;
  font-size: 1rem;
}

.payment-info {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.insufficient-balance, .balance-ok, .card-status {
  padding: 0.5rem;
  border-radius: 4px;
  text-align: center;
  font-size: 0.85rem;
  font-weight: 500;
}

.insufficient-balance {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.balance-ok {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.card-status.error {
  background-color: #fff3cd;
  color: #856404;
  border: 1px solid #ffeaa7;
}

.pay-btn {
  padding: 0.75rem;
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.pay-btn:disabled {
  background: #adb5bd;
  cursor: not-allowed;
  opacity: 0.7;
}

.pay-btn:not(:disabled):hover {
  background: linear-gradient(135deg, #218838, #1ba87e);
  transform: translateY(-1px);
  box-shadow: 0 3px 8px rgba(40, 167, 69, 0.2);
}

.pay-icon {
  font-size: 1.1rem;
}

.prompt {
  padding: 1rem;
  text-align: center;
  color: #6c757d;
  background-color: white;
  border-radius: 6px;
  border: 1px dashed #dee2e6;
  font-size: 0.9rem;
}

/* Состояния загрузки */
.loading, .no-data {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  border-radius: 8px;
  color: #6c757d;
  font-style: italic;
}

/* Адаптивность */
@media (max-width: 1024px) {
  .fuel-sale-container {
    padding: 0.75rem;
    height: auto;
    min-height: calc(100vh - 60px);
  }
  
  .form-row {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .prices-table {
    min-width: 900px;
  }
}

@media (max-width: 768px) {
  .content-wrapper {
    gap: 1rem;
  }
  
  .table-info {
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
  }
  
  .prices-section {
    max-height: 350px;
  }
  
  .prices-table th,
  .prices-table td {
    padding: 0.5rem 0.4rem;
  }
}
</style>