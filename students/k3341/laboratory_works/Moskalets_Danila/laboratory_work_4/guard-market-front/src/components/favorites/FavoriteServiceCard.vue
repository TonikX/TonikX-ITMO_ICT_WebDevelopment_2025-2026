<template>
  <v-card class="h-100 favorite-card">
    <v-card-title class="text-h6">
      {{ service.name }}
    </v-card-title>

    <v-card-subtitle class="mb-2">
      <v-chip
          color="primary"
          variant="outlined"
          size="small"
          class="mr-2"
      >
        <v-icon start icon="mdi-office-building"></v-icon>
        {{ service.company?.name || 'Неизвестная компания' }}
      </v-chip>

      <!-- Бейдж скидки -->
      <v-chip
          v-if="hasActiveDiscount"
          color="red"
          text-color="white"
          size="small"
          class="mr-2"
      >
        <v-icon start icon="mdi-sale" size="x-small"></v-icon>
        -{{ activeDiscountPercent }}%
      </v-chip>
    </v-card-subtitle>

    <v-card-text>
      <p class="text-body-2 mb-4 line-clamp-3">
        {{ service.description || 'Нет описания' }}
      </p>

      <div class="d-flex align-center">
        <div>
          <!-- Старая цена (перечеркнутая) при наличии активной скидки -->
          <div v-if="hasActiveDiscount && service.price" class="d-flex align-center">
            <div class="text-body-2 text-decoration-line-through text-grey mr-2">
              {{ formatPrice(service.price) }}
            </div>
            <div class="text-h5 font-weight-bold text-red">
              {{ formatPrice(calculatedPrice) }}
            </div>
          </div>

          <!-- Обычная цена без скидки -->
          <div v-else>
            <div class="text-h5 font-weight-bold">
              {{ formatPrice(service.price || service.current_price) }}
            </div>
          </div>

          <!-- Информация о скидке -->
          <div v-if="hasActiveDiscount" class="text-caption text-red mt-1">
            <v-icon small icon="mdi-clock-outline" class="mr-1"></v-icon>
            Скидка действует до: {{ formatDiscountEndDate }}
          </div>
        </div>

        <v-spacer></v-spacer>

        <v-btn
            color="primary"
            @click="$emit('create-request', service)"
            size="small"
        >
          <v-icon start icon="mdi-message-text"></v-icon>
          Заявка
        </v-btn>
      </div>
    </v-card-text>

    <v-card-actions>
      <v-btn
          @click="$emit('remove-from-favorites', favoriteId)"
          variant="text"
          color="pink"
          size="small"
          :loading="loading"
      >
        <v-icon start icon="mdi-heart"></v-icon>
        Удалить
      </v-btn>

      <v-spacer></v-spacer>

      <v-btn
          v-if="service.company?.id"
          :to="`/companies/${service.company.id}`"
          variant="text"
          size="small"
          color="primary"
          class="mr-2"
      >
        <v-icon start icon="mdi-office-building"></v-icon>
        К компании
      </v-btn>

      <v-btn
          :to="`/services/${service.id}`"
          variant="text"
          size="small"
          color="secondary"
      >
        <v-icon start icon="mdi-information"></v-icon>
        Подробнее
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  favoriteId: {
    type: Number,
    required: true
  },
  service: {
    type: Object,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

defineEmits(['create-request', 'remove-from-favorites'])

// Computed свойства
const hasActiveDiscount = computed(() => {
  const discount = props.service.current_discount

  if (!discount) return false

  // Проверяем, что скидка активна
  const now = new Date()
  const startDate = discount.start_date ? new Date(discount.start_date) : null
  const endDate = discount.end_date ? new Date(discount.end_date) : null

  // Если есть дата начала и она в будущем - скидка еще не началась
  if (startDate && startDate > now) return false

  // Если есть дата окончания и она в прошлом - скидка уже закончилась
  if (endDate && endDate < now) return false

  // Проверяем наличие процента скидки
  return discount.discount_percent && parseFloat(discount.discount_percent) > 0
})

const activeDiscountPercent = computed(() => {
  if (!hasActiveDiscount.value || !props.service.current_discount) return 0
  return parseFloat(props.service.current_discount.discount_percent).toFixed(0)
})

const calculatedPrice = computed(() => {
  if (!hasActiveDiscount.value || !props.service.price) return props.service.price

  const price = parseFloat(props.service.price)
  const discountPercent = parseFloat(props.service.current_discount.discount_percent)

  if (isNaN(price) || isNaN(discountPercent)) return props.service.price

  const discountedPrice = price * (1 - discountPercent / 100)
  return discountedPrice.toFixed(2)
})

const formatDiscountEndDate = computed(() => {
  if (!hasActiveDiscount.value || !props.service.current_discount?.end_date) return ''

  const date = new Date(props.service.current_discount.end_date)
  return date.toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})

// Вспомогательные функции
const formatPrice = (price) => {
  if (!price && price !== 0) return 'Цена не указана'

  const num = parseFloat(price)
  if (isNaN(num)) return price

  // Форматируем число с разделителями тысяч
  return new Intl.NumberFormat('ru-RU', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(num) + ' ₽'
}
</script>

<style scoped>
.h-100 {
  height: 100%;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.v-card {
  transition: transform 0.2s;
}

.v-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1) !important;
}

.favorite-card {
  border-left: 4px solid #FF4081;
}

.text-red {
  color: #f44336 !important;
}

.text-decoration-line-through {
  text-decoration: line-through;
  opacity: 0.7;
}

/* Стили для кнопок */
.v-btn {
  text-transform: none !important;
}

/* Адаптивные стили */
@media (max-width: 600px) {
  .v-card-title {
    font-size: 1.1rem !important;
  }

  .text-h5 {
    font-size: 1.25rem !important;
  }
}
</style>