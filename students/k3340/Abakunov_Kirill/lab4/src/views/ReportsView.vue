<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4">
          <v-icon class="mr-2">mdi-chart-bar</v-icon>
          Отчёты
        </h1>
      </v-col>
    </v-row>

    <!-- Параметры отчёта -->
    <v-card class="mb-4 pa-4">
      <v-card-title>Квартальный отчёт</v-card-title>
      <v-card-text>
        <v-row align="center">
          <v-col cols="12" sm="4">
            <v-text-field
              v-model.number="year"
              label="Год"
              type="number"
              :rules="[rules.required]"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="4">
            <v-select
              v-model="quarter"
              label="Квартал"
              :items="quarters"
              item-title="text"
              item-value="value"
            ></v-select>
          </v-col>
          <v-col cols="12" sm="4">
            <v-btn 
              color="primary" 
              @click="loadReport" 
              :loading="loading" 
              block
              size="large"
            >
              <v-icon left>mdi-file-chart</v-icon>
              Сформировать отчёт
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <v-progress-linear v-if="loading" indeterminate color="primary"></v-progress-linear>

    <!-- Результаты отчёта -->
    <template v-if="report">
      <!-- Общая информация -->
      <v-row class="mb-4">
        <v-col cols="12" md="4">
          <v-card color="primary" class="pa-4 text-white">
            <div class="text-h6">Период</div>
            <div class="text-body-1">
              {{ report.period.start_date }} — {{ report.period.end_date }}
            </div>
            <div class="text-body-2 mt-2">
              {{ report.period.year }} год, {{ quarter }} квартал
            </div>
          </v-card>
        </v-col>
        <v-col cols="12" md="4">
          <v-card color="success" class="pa-4 text-white">
            <div class="text-h6">Общий доход</div>
            <div class="text-h4">{{ formatCurrency(report.total_income) }}</div>
          </v-card>
        </v-col>
        <v-col cols="12" md="4">
          <v-card color="info" class="pa-4 text-white">
            <div class="text-h6">Всего номеров</div>
            <div class="text-h4">{{ report.total_rooms }}</div>
          </v-card>
        </v-col>
      </v-row>

      <!-- Статистика по этажам -->
      <v-card class="mb-4">
        <v-card-title>
          <v-icon class="mr-2">mdi-stairs</v-icon>
          Статистика по этажам
        </v-card-title>
        <v-card-text>
          <v-row>
            <v-col 
              v-for="floor in report.floors_statistics" 
              :key="floor.floor" 
              cols="6" 
              sm="4" 
              md="2"
            >
              <v-card variant="outlined" class="text-center pa-3">
                <div class="text-h5 text-primary">{{ floor.floor }}</div>
                <div class="text-caption">этаж</div>
                <v-divider class="my-2"></v-divider>
                <div class="text-h6">{{ floor.rooms_count }}</div>
                <div class="text-caption">номеров</div>
              </v-card>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Детальная информация по номерам -->
      <v-card>
        <v-card-title>
          <v-icon class="mr-2">mdi-door</v-icon>
          Доход по номерам
        </v-card-title>
        <v-card-text>
          <v-data-table
            :headers="roomHeaders"
            :items="report.rooms"
            :items-per-page="10"
            class="elevation-1"
          >
            <template v-slot:item.income="{ item }">
              <v-chip :color="item.income > 0 ? 'success' : 'grey'" variant="tonal">
                {{ formatCurrency(item.income) }}
              </v-chip>
            </template>

            <template v-slot:item.guests_count="{ item }">
              <v-chip :color="item.guests_count > 0 ? 'primary' : 'grey'" size="small">
                {{ item.guests_count }}
              </v-chip>
            </template>
          </v-data-table>
        </v-card-text>
      </v-card>

      <!-- Диаграмма доходов -->
      <v-card class="mt-4">
        <v-card-title>
          <v-icon class="mr-2">mdi-chart-pie</v-icon>
          Визуализация доходов
        </v-card-title>
        <v-card-text>
          <v-row>
            <v-col 
              v-for="room in topRooms" 
              :key="room.room_number" 
              cols="12" 
              sm="6" 
              md="4"
            >
              <v-progress-linear
                :model-value="(room.income / maxIncome) * 100"
                color="primary"
                height="25"
                class="mb-2"
              >
                <template v-slot:default>
                  <span class="text-white text-caption">
                    {{ room.room_number }}: {{ formatCurrency(room.income) }}
                  </span>
                </template>
              </v-progress-linear>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </template>

    <v-alert v-else-if="!loading && reportRequested" type="info" class="mt-4">
      Нет данных для выбранного периода
    </v-alert>
  </div>
</template>

<script setup>
import { ref, computed, inject } from 'vue'
import { reportsAPI } from '@/api'

const showSnackbar = inject('showSnackbar')

const year = ref(new Date().getFullYear())
const quarter = ref(Math.ceil((new Date().getMonth() + 1) / 3))
const loading = ref(false)
const report = ref(null)
const reportRequested = ref(false)

const quarters = [
  { value: 1, text: '1 квартал (янв-мар)' },
  { value: 2, text: '2 квартал (апр-июн)' },
  { value: 3, text: '3 квартал (июл-сен)' },
  { value: 4, text: '4 квартал (окт-дек)' },
]

const roomHeaders = [
  { title: 'Номер', key: 'room_number' },
  { title: 'Тип', key: 'room_type' },
  { title: 'Этаж', key: 'floor' },
  { title: 'Гостей', key: 'guests_count' },
  { title: 'Доход', key: 'income' },
]

const rules = {
  required: (v) => !!v || 'Обязательное поле',
}

const topRooms = computed(() => {
  if (!report.value) return []
  return [...report.value.rooms]
    .sort((a, b) => b.income - a.income)
    .slice(0, 10)
})

const maxIncome = computed(() => {
  if (!topRooms.value.length) return 1
  return Math.max(...topRooms.value.map(r => r.income)) || 1
})

const formatCurrency = (value) => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    minimumFractionDigits: 0,
  }).format(value)
}

const loadReport = async () => {
  loading.value = true
  reportRequested.value = true
  try {
    const response = await reportsAPI.getQuarterly(year.value, quarter.value)
    report.value = response.data
    showSnackbar('Отчёт сформирован', 'success')
  } catch (error) {
    report.value = null
    showSnackbar('Ошибка формирования отчёта', 'error')
  } finally {
    loading.value = false
  }
}
</script>
