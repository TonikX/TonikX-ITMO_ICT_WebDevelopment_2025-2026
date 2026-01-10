<template>
  <v-container class="fuel-sale-container" fluid>
    <!-- Заголовок -->
    <v-card elevation="2" class="pa-4 mb-4">
      <div class="d-flex align-center justify-space-between">
        <h1 class="text-h5 text-primary">Продажа топлива</h1>
        <v-chip color="primary" prepend-icon="mdi-gas-station" variant="flat" size="small">
          АЗС: {{ stationAddress }}
        </v-chip>
      </div>
    </v-card>

    <!-- Сообщения об ошибках и успехе -->
    <div v-if="error || successMessage" class="mb-4">
      <v-alert
        v-if="error"
        type="error"
        variant="tonal"
        closable
        @click:close="clearError"
        icon="mdi-alert-circle"
        class="fuel-alert mb-2"
      >
        {{ error }}
      </v-alert>
      
      <v-alert
        v-if="successMessage"
        type="success"
        variant="tonal"
        closable
        @click:close="clearSuccessMessage"
        icon="mdi-check-circle"
        class="fuel-alert mb-2"
      >
        {{ successMessage }}
      </v-alert>
    </div>

    <!-- Секция таблицы с ценами -->
    <v-card elevation="2" class="mb-4">
      <v-card-title class="bg-primary text-white">
        <v-icon icon="mdi-gas-cylinder" class="mr-2"></v-icon>
        Доступное топливо на вашей станции
      </v-card-title>
      
      <v-card-text class="pa-0">
        <div v-if="loading && !stationPrices.length" class="d-flex align-center justify-center py-8">
          <v-progress-circular indeterminate color="primary" size="48" width="4"></v-progress-circular>
          <span class="ml-3 text-body-1 text-grey">Загрузка цен...</span>
        </div>
        
        <div v-else-if="!stationPrices.length" class="d-flex align-center justify-center py-8">
          <v-icon icon="mdi-gas-station-off" size="48" class="text-grey mr-3"></v-icon>
          <div>
            <div class="text-body-1 text-grey">Нет доступного топлива</div>
            <div class="text-caption text-grey">На вашей станции нет доступного топлива</div>
          </div>
        </div>
        
        <div v-else>
          <!-- Обертка для горизонтальной прокрутки таблицы -->
          <div class="table-wrapper">
            <v-table 
              class="fuel-table"
              hover
            >
              <thead>
                <tr>
                  <th class="text-center" width="60">Выбор</th>
                  <th>Топливо</th>
                  <th>Бренд</th>
                  <th class="text-center">Сезон</th>
                  <th class="text-center">Плотность</th>
                  <th class="text-center">Горение</th>
                  <th class="text-center">Мин. темп.</th>
                  <th class="text-center">Сера</th>
                  <th class="text-center">Цена (₽/л)</th>
                </tr>
              </thead>
              <tbody>
                <tr 
                  v-for="price in stationPrices" 
                  :key="price.id_fuel_price"
                  :class="{ 'selected-row': isSelected(price) }"
                  @click="selectPrice(price)"
                  class="price-row cursor-pointer"
                >
                  <td class="text-center">
                    <v-radio
                      :model-value="selectedPrice?.id_fuel_price"
                      :value="price.id_fuel_price"
                      @click="selectPrice(price)"
                      hide-details
                      density="compact"
                    ></v-radio>
                  </td>
                  <td class="font-weight-medium">{{ getFuelTitle(price) }}</td>
                  <td>{{ getFuelBrand(price) }}</td>
                  <td class="text-center">
                    <v-chip 
                      :color="getSeasonColor(price)" 
                      size="small"
                      label
                      variant="flat"
                    >
                      {{ getSeasonText(price) }}
                    </v-chip>
                  </td>
                  <td class="text-center">{{ getFuelDensity(price) }}</td>
                  <td class="text-center">{{ getBurningTemp(price) }}°C</td>
                  <td class="text-center">{{ getMinTemp(price) }}°C</td>
                  <td class="text-center">{{ getSulfurPercent(price) }}%</td>
                  <td class="text-center">
                    <v-chip color="success" variant="flat" class="font-weight-bold">
                      {{ price.per_liter }}
                    </v-chip>
                  </td>
                </tr>
              </tbody>
            </v-table>
          </div>
          
          <v-divider></v-divider>
          
          <div class="pa-3 bg-grey-lighten-4">
            <div v-if="selectedPrice" class="d-flex flex-column">
              <div class="d-flex align-center mb-1">
                <v-icon icon="mdi-check-circle" color="success" class="mr-2"></v-icon>
                <span class="font-weight-medium">Выбрано:</span>
                <span class="ml-2">{{ getFuelTitle(selectedPrice) }} ({{ getFuelBrand(selectedPrice) }})</span>
              </div>
              <div class="d-flex align-center">
                <v-chip color="success" variant="outlined" size="small" class="mr-2">
                  {{ selectedPrice.per_liter }} ₽/л
                </v-chip>
                <div class="text-caption text-grey">
                  Выберите топливо кликом по строке таблицы
                </div>
              </div>
            </div>
            <div v-else class="text-center text-grey">
              <v-icon icon="mdi-information" class="mr-2"></v-icon>
              Выберите топливо из таблицы для продолжения
            </div>
          </div>
        </div>
      </v-card-text>
    </v-card>

    <!-- Секция формы оформления -->
    <v-card elevation="2">
      <v-card-title class="bg-secondary text-white">
        <v-icon icon="mdi-cart" class="mr-2"></v-icon>
        Оформление покупки
      </v-card-title>
      
      <v-card-text class="pa-4">
        <v-form @submit.prevent ref="form">
          <!-- Количество литров -->
          <v-text-field
            v-model="liters"
            label="Количество литров"
            type="number"
            step="0.1"
            min="0.1"
            :disabled="!selectedPrice"
            variant="outlined"
            prepend-inner-icon="mdi-water"
            suffix="л"
            class="mb-3"
            @input="handleLitersChange"
            :rules="[
              v => !!v || 'Обязательное поле',
              v => (v && parseFloat(v) > 0) || 'Введите положительное число'
            ]"
          >
            <template v-slot:append v-if="selectedPrice && liters">
              <v-chip size="small" color="info" variant="flat">
                {{ calculatedInitialAmount.toFixed(2) }} ₽
              </v-chip>
            </template>
          </v-text-field>

          <!-- Номер карты -->
          <div class="mb-4">
            <v-text-field
              v-model="cardId"
              label="Номер карты клиента"
              type="number"
              min="1"
              :disabled="!selectedPrice || !liters"
              variant="outlined"
              prepend-inner-icon="mdi-credit-card"
              placeholder="12345"
              class="mb-1"
              @input="handleCardIdChange"
              :rules="[v => !!v || 'Обязательное поле']"
            >
              <template v-slot:append>
                <v-btn
                  @click="applyCard"
                  :disabled="!cardId || !selectedPrice || !liters || cardIdLoading"
                  color="primary"
                  variant="tonal"
                  size="small"
                  :loading="cardIdLoading"
                >
                  Применить
                </v-btn>
              </template>
            </v-text-field>
            <div class="text-caption text-grey pl-4">
              Введите номер и нажмите "Применить"
            </div>
          </div>

          <!-- Расчет платежа -->
          <div v-if="calculatedInitialAmount > 0" class="calculation-section">
            <v-card variant="outlined" class="mb-3">
              <v-card-title class="bg-grey-lighten-4 py-2">
                <v-icon icon="mdi-calculator" class="mr-2" size="small"></v-icon>
                <span class="text-body-1">Расчет платежа</span>
              </v-card-title>
              
              <v-card-text class="pa-3">
                <div v-if="cardApplied && calculation.cardFound && calculation.cardActive" class="calculation-details">
                  <!-- Суммы -->
                  <div class="amount-breakdown mb-3">
                    <div class="d-flex justify-space-between mb-1">
                      <span class="text-body-2">Начальная сумма:</span>
                      <span class="text-body-2 font-weight-medium">{{ calculation.initialAmount.toFixed(2) }} ₽</span>
                    </div>
                    <div class="d-flex justify-space-between mb-1">
                      <span class="text-body-2 text-success">Скидка:</span>
                      <span class="text-body-2 font-weight-medium text-success">-{{ calculation.discount.toFixed(2) }} ₽</span>
                    </div>
                    <v-divider class="my-1"></v-divider>
                    <div class="d-flex justify-space-between">
                      <span class="text-body-1 font-weight-bold">Итого к оплате:</span>
                      <span class="text-body-1 font-weight-bold text-primary">{{ calculation.finalAmount.toFixed(2) }} ₽</span>
                    </div>
                  </div>

                  <!-- Статус баланса -->
                  <div class="payment-info">
                    <v-alert
                      v-if="!calculation.sufficientBalance"
                      type="warning"
                      variant="tonal"
                      icon="mdi-alert"
                      density="compact"
                      class="mb-3"
                    >
                      Недостаточно средств на карте
                    </v-alert>
                    <v-alert
                      v-else
                      type="success"
                      variant="tonal"
                      icon="mdi-check"
                      density="compact"
                      class="mb-3"
                    >
                      На карте достаточно средств
                    </v-alert>

                    <v-btn
                      @click="showConfirmModal"
                      :disabled="!canPay"
                      color="success"
                      size="large"
                      block
                      class="fuel-btn mb-2"
                      prepend-icon="mdi-credit-card-check"
                    >
                      Оплатить {{ calculation.finalAmount.toFixed(2) }} ₽
                    </v-btn>
                  </div>
                </div>

                <div v-else-if="cardApplied && !calculation.cardFound">
                  <v-alert
                    type="error"
                    variant="tonal"
                    icon="mdi-card-off"
                    density="compact"
                    title="Карта не найдена"
                    class="mb-3"
                  >
                    Проверьте правильность номера карты
                  </v-alert>
                </div>

                <div v-else-if="cardApplied && !calculation.cardActive">
                  <v-alert
                    type="warning"
                    variant="tonal"
                    icon="mdi-card-remove"
                    density="compact"
                    title="Карта не активна"
                    class="mb-3"
                  >
                    Карта клиента не активна или срок действия истек
                  </v-alert>
                </div>

                <div v-else-if="selectedPrice && liters">
                  <v-alert
                    type="info"
                    variant="tonal"
                    icon="mdi-information"
                    density="compact"
                    class="mb-3"
                  >
                    Введите номер карты и нажмите "Применить" для расчета скидки
                  </v-alert>
                </div>

                <div v-else-if="selectedPrice">
                  <v-alert
                    type="info"
                    variant="tonal"
                    icon="mdi-information"
                    density="compact"
                    class="mb-3"
                  >
                    Введите количество литров для продолжения
                  </v-alert>
                </div>

                <div v-else>
                  <v-alert
                    type="info"
                    variant="tonal"
                    icon="mdi-information"
                    density="compact"
                    class="mb-3"
                  >
                    Выберите топливо из таблицы для начала оформления
                  </v-alert>
                </div>
              </v-card-text>
            </v-card>
          </div>
        </v-form>
      </v-card-text>
    </v-card>

    <!-- Модальное окно подтверждения -->
    <ConfirmPaymentModal
      :visible="showModal"
      :details="confirmationDetails"
      :loading="processingPayment"
      @confirm="executePayment"
      @cancel="hideConfirmModal"
    />
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useSalesStore } from '../stores/sales'
import { useAuthStore } from '../stores/auth'
import ConfirmPaymentModal from '../components/ConfirmPaymentModal.vue'

const salesStore = useSalesStore()
const authStore = useAuthStore()

// Реактивные переменные
const showModal = ref(false)
const processingPayment = ref(false)

// Вычисляемые свойства из хранилища
const stationPrices = computed(() => salesStore.stationPrices)
const selectedPrice = computed(() => salesStore.selectedPrice)
const liters = computed({
  get: () => salesStore.liters > 0 ? salesStore.liters : '',
  set: (value) => salesStore.setLiters(value)
})
const cardId = computed({
  get: () => salesStore.cardId,
  set: (value) => salesStore.setCardId(value)
})
const cardApplied = computed(() => salesStore.cardApplied)
const calculatedInitialAmount = computed(() => salesStore.calculatedInitialAmount)
const calculation = computed(() => salesStore.calculation)
const canPay = computed(() => salesStore.canPay)
const loading = computed(() => salesStore.loading)
const error = computed(() => salesStore.error)
const successMessage = computed(() => salesStore.successMessage)
const cardIdLoading = computed(() => salesStore.loading)
const stationAddress = computed(() => authStore.stationAddress || 'Не указана')

// Данные для модального окна подтверждения
const confirmationDetails = computed(() => ({
  fuelInfo: selectedPrice.value ? getFuelTitle(selectedPrice.value) : '',
  liters: liters.value || '',
  pricePerLiter: selectedPrice.value?.per_liter || 0,
  initialAmount: calculation.value.initialAmount || 0,
  discount: calculation.value.discount || 0,
  finalAmount: calculation.value.finalAmount || 0,
  cardId: cardId.value || ''
}))

// Вспомогательные методы для извлечения данных
const getFuelTitle = (price) => {
  return price.sold_fuel?.produced_fuel?.fuel?.title || 
         price.sold_fuel?.id_produced_fuel?.id_kind_fuel?.title || 
         'Неизвестно'
}

const getFuelBrand = (price) => {
  return price.sold_fuel?.produced_fuel?.fuel?.brand || 
         price.sold_fuel?.id_produced_fuel?.id_kind_fuel?.brand || 
         '-'
}

const getSeasonText = (price) => {
  const season = price.sold_fuel?.produced_fuel?.fuel?.season || 
                 price.sold_fuel?.id_produced_fuel?.id_kind_fuel?.season
  const seasons = {
    1: 'Лето',
    2: 'Зима',
    3: 'Всесезон'
  }
  return seasons[season] || '-'
}

const getSeasonColor = (price) => {
  const season = price.sold_fuel?.produced_fuel?.fuel?.season || 
                 price.sold_fuel?.id_produced_fuel?.id_kind_fuel?.season
  const colors = {
    1: 'blue',    // Лето
    2: 'cyan',    // Зима
    3: 'green'    // Всесезон
  }
  return colors[season] || 'grey'
}

const getFuelDensity = (price) => {
  return price.sold_fuel?.produced_fuel?.fuel?.density || 
         price.sold_fuel?.id_produced_fuel?.id_kind_fuel?.density || 
         '-'
}

const getBurningTemp = (price) => {
  return price.sold_fuel?.produced_fuel?.fuel?.burning_temp || 
         price.sold_fuel?.id_produced_fuel?.id_kind_fuel?.burning_temp || 
         '-'
}

const getMinTemp = (price) => {
  return price.sold_fuel?.produced_fuel?.fuel?.min_usage_temp || 
         price.sold_fuel?.id_produced_fuel?.id_kind_fuel?.min_usage_temp || 
         '-'
}

const getSulfurPercent = (price) => {
  return price.sold_fuel?.produced_fuel?.fuel?.percent_sulfur || 
         price.sold_fuel?.id_produced_fuel?.id_kind_fuel?.percent_sulfur || 
         '-'
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

const handleCardIdChange = (event) => {
  const value = event.target.value
  salesStore.setCardId(value)
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
  max-width: 100%;
  margin: 0 auto;
  padding: 12px;
}

/* Обертка для горизонтальной прокрутки таблицы */
.table-wrapper {
  width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

/* Минимальная ширина для таблицы чтобы все колонки были видны */
.fuel-table {
  min-width: 900px; /* Минимальная ширина для отображения всех колонок */
  width: 100%;
}

/* Стили для выбранной строки */
.selected-row {
  background-color: rgba(var(--v-theme-primary), 0.08) !important;
  border-left: 3px solid rgb(var(--v-theme-primary)) !important;
}

.price-row:hover {
  background-color: rgba(var(--v-theme-primary), 0.04) !important;
}

.cursor-pointer {
  cursor: pointer;
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

/* Кастомные классы из переменных SCSS */
.fuel-alert {
  border-left: 4px solid var(--v-theme-secondary);
}

.fuel-btn {
  background: linear-gradient(135deg, var(--v-theme-secondary), var(--v-theme-warning));
  color: white !important;
}

.fuel-table th {
  background-color: rgba(var(--v-theme-primary), 0.08);
  font-weight: 600;
  white-space: nowrap;
  padding: 8px 12px;
  font-size: 0.85rem;
}

.fuel-table td {
  padding: 8px 12px;
  font-size: 0.9rem;
  white-space: nowrap;
}

.fuel-table tr:hover {
  background-color: rgba(var(--v-theme-secondary), 0.08);
}

/* Адаптивные шрифты */
.text-h5 {
  font-size: 1.25rem !important;
}

.text-body-1 {
  font-size: 1rem !important;
}

.text-body-2 {
  font-size: 0.875rem !important;
}

.text-caption {
  font-size: 0.75rem !important;
}

/* Отступы для мобильных устройств */
.pa-4 {
  padding: 16px !important;
}

.pa-3 {
  padding: 12px !important;
}

.mb-4 {
  margin-bottom: 16px !important;
}

.mb-3 {
  margin-bottom: 12px !important;
}

.mb-2 {
  margin-bottom: 8px !important;
}

.mb-1 {
  margin-bottom: 4px !important;
}

/* Компактные чипы */
.v-chip--size-small {
  height: 24px !important;
  font-size: 0.75rem !important;
}
</style>