<template>
  <div>
    <h1 class="text-h4 mb-6">Отчеты</h1>

    <v-card>
      <v-card-title>
        <v-icon color="primary" class="mr-2">mdi-chart-box</v-icon>
        Квартальный отчет
        <v-spacer></v-spacer>
        <v-select
          v-model="selectedQuarter"
          :items="quarters"
          label="Квартал"
          density="compact"
          style="max-width: 200px"
          class="mr-3"
          @update:model-value="loadReport"
        ></v-select>
        <v-btn
          v-if="report"
          color="primary"
          variant="outlined"
          @click="exportReport"
        >
          <v-icon start>mdi-download</v-icon>
          Экспорт
        </v-btn>
      </v-card-title>
      <v-card-text>
        <v-progress-linear v-if="loading" indeterminate></v-progress-linear>
        <v-alert
          v-else-if="!report"
          type="info"
          variant="tonal"
          class="mb-4"
        >
          Выберите квартал для просмотра отчета
        </v-alert>
        <div v-else-if="report">
          <v-row class="mb-4">
            <v-col cols="12" md="6">
              <v-card>
                <v-card-title>Период</v-card-title>
                <v-card-text>
                  <div>Начало: {{ formatDate(report.period.start) }}</div>
                  <div>Конец: {{ formatDate(report.period.end) }}</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" md="6">
              <v-card>
                <v-card-title>Общий доход</v-card-title>
                <v-card-text class="text-h5">
                  {{ parseFloat(report.total_income).toFixed(2) }} ₽
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <v-card class="mb-4">
            <v-card-title>Читатели по залам</v-card-title>
            <v-card-text>
              <v-data-table
                :headers="readersHeaders"
                :items="report.readers_per_room"
                hide-default-footer
              ></v-data-table>
            </v-card-text>
          </v-card>

          <v-card class="mb-4">
            <v-card-title>Доход по залам</v-card-title>
            <v-card-text>
              <v-data-table
                :headers="incomeHeaders"
                :items="report.income_per_room"
                hide-default-footer
              >
                <template v-slot:item.income="{ item }">
                  {{ parseFloat(item.income).toFixed(2) }} ₽
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>

          <v-card>
            <v-card-title>Залы по этажам</v-card-title>
            <v-card-text>
              <v-data-table
                :headers="floorsHeaders"
                :items="report.rooms_per_floor"
                hide-default-footer
              ></v-data-table>
            </v-card-text>
          </v-card>
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { reportsAPI } from '@/services/api'
import dayjs from 'dayjs'

const selectedQuarter = ref(Math.ceil((dayjs().month() + 1) / 3))
const loading = ref(false)
const report = ref(null)

const quarters = [
  { title: '1 квартал', value: 1 },
  { title: '2 квартал', value: 2 },
  { title: '3 квартал', value: 3 },
  { title: '4 квартал', value: 4 }
]

const readersHeaders = [
  { title: 'Зал', key: 'reading_room' },
  { title: 'Количество читателей', key: 'readers' }
]

const incomeHeaders = [
  { title: 'Зал', key: 'reading_room' },
  { title: 'Доход', key: 'income' }
]

const floorsHeaders = [
  { title: 'Этаж', key: 'floor' },
  { title: 'Количество залов', key: 'count' }
]

const formatDate = (dateStr) => {
  return dayjs(dateStr).format('DD.MM.YYYY HH:mm')
}

const loadReport = async () => {
  try {
    loading.value = true
    const response = await reportsAPI.getQuarterReport(selectedQuarter.value)
    report.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки отчета:', error)
  } finally {
    loading.value = false
  }
}

const exportReport = () => {
  if (!report.value) return

  const reportData = {
    'Квартальный отчет': `Квартал ${selectedQuarter.value}`,
    'Период': {
      'Начало': formatDate(report.value.period.start),
      'Конец': formatDate(report.value.period.end)
    },
    'Общий доход': `${parseFloat(report.value.total_income).toFixed(2)} ₽`,
    'Читатели по залам': report.value.readers_per_room,
    'Доход по залам': report.value.income_per_room.map(item => ({
      'Зал': item.reading_room,
      'Доход': `${parseFloat(item.income).toFixed(2)} ₽`
    })),
    'Залы по этажам': report.value.rooms_per_floor
  }

  const jsonString = JSON.stringify(reportData, null, 2)
  const blob = new Blob([jsonString], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `quarter_report_${selectedQuarter.value}_${dayjs().format('YYYY-MM-DD')}.json`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

onMounted(() => {
  loadReport()
})
</script>

