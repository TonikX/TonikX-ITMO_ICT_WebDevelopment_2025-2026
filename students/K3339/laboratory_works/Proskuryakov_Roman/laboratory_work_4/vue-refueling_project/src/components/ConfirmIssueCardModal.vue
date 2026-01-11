<template>
  <v-dialog
    :model-value="visible"
    max-width="600"
    persistent
    @click:outside="handleOverlayClick"
  >
    <v-card>
      <v-toolbar color="primary" dark>
        <v-toolbar-title>Подтверждение выдачи карты</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon @click="cancel">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-toolbar>

      <v-card-text class="pt-4">
        <!-- Данные клиента -->
        <v-card variant="outlined" class="mb-4">
          <v-card-title class="text-subtitle-1 font-weight-bold">
            <v-icon icon="mdi-account" class="mr-2"></v-icon>
            Данные клиента
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="6" sm="4" class="font-weight-bold text-right">Фамилия:</v-col>
              <v-col cols="6" sm="8">{{ clientData.surname || '—' }}</v-col>
            </v-row>
            <v-row>
              <v-col cols="6" sm="4" class="font-weight-bold text-right">Имя:</v-col>
              <v-col cols="6" sm="8">{{ clientData.name || '—' }}</v-col>
            </v-row>
            <v-row>
              <v-col cols="6" sm="4" class="font-weight-bold text-right">Отчество:</v-col>
              <v-col cols="6" sm="8">{{ clientData.patronymic || '—' }}</v-col>
            </v-row>
            <v-row>
              <v-col cols="6" sm="4" class="font-weight-bold text-right">Телефон:</v-col>
              <v-col cols="6" sm="8">{{ formattedPhone || '—' }}</v-col>
            </v-row>
            <v-row>
              <v-col cols="6" sm="4" class="font-weight-bold text-right">Адрес:</v-col>
              <v-col cols="6" sm="8">{{ clientData.address || '—' }}</v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <!-- Параметры карты -->
        <v-card variant="outlined">
          <v-card-title class="text-subtitle-1 font-weight-bold">
            <v-icon icon="mdi-card-account-details" class="mr-2"></v-icon>
            Параметры карты
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="6" sm="4" class="font-weight-bold text-right">Период действия:</v-col>
              <v-col cols="6" sm="8">{{ periodText }}</v-col>
            </v-row>
            <v-row>
              <v-col cols="6" sm="4" class="font-weight-bold text-right">Начало действия:</v-col>
              <v-col cols="6" sm="8">{{ formatDate(startDate) }}</v-col>
            </v-row>
            <v-row>
              <v-col cols="6" sm="4" class="font-weight-bold text-right">Окончание действия:</v-col>
              <v-col cols="6" sm="8">{{ endDate ? formatDate(endDate) : 'Бессрочно' }}</v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions class="px-4 py-3">
        <v-spacer></v-spacer>
        <v-btn
          color="grey-darken-1"
          variant="tonal"
          @click="cancel"
          :disabled="loading"
        >
          Отмена
        </v-btn>
        <v-btn
          color="primary"
          variant="flat"
          @click="confirm"
          :loading="loading"
          :disabled="loading"
          class="fuel-btn"
        >
          <template v-slot:prepend>
            <v-icon>mdi-check</v-icon>
          </template>
          Выдать карту
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
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
  if (!props.period) return new Date()
  
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
  if (!date) return '—'
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
/* Сохраняем только минимальные стили, так как Vuetify уже предоставляет стили */
:deep(.v-toolbar) {
  border-radius: 8px 8px 0 0;
}

:deep(.v-card) {
  border-radius: 8px;
}

/* Адаптивность для текста */
@media (max-width: 600px) {
  :deep(.text-right) {
    text-align: left !important;
    font-size: 0.875rem;
  }
  
  :deep(.v-col) {
    padding-top: 4px;
    padding-bottom: 4px;
  }
}
</style>