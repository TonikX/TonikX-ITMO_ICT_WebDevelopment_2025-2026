<script setup>
/**
 * ReportsView.vue - Страница аналитики и отчетов.
 * Позволяет администратору видеть финансовые показатели и 
 * загруженность отеля за выбранный период времени.
 */
import { ref, onMounted, watch } from 'vue'
import api from '../services/api'

const loading = ref(false)
const tab = ref('quarterly')
const error = ref('')

// --- Квартальный отчет ---
const reportData = ref(null)
const selectedQuarter = ref('1')
const selectedYear = ref(new Date().getFullYear())

// --- Инфо-запросы ---
const infoResult = ref(null)
const cities = ref([])
const guests = ref([])
const queryParams = ref({
  type: 'free_rooms',
  room: '',
  start: new Date().toISOString().substr(0, 10),
  end: new Date().toISOString().substr(0, 10),
  city_id: null,
  guest_id: null,
  day: 'mon'
})

const queryTypes = [
  { title: 'Свободные номера (сейчас)', value: 'free_rooms' },
  { title: 'Клиенты в номере за период', value: 'clients_in_room' },
  { title: 'Кол-во клиентов из города', value: 'clients_by_city' },
  { title: 'Кто убирал номер клиента?', value: 'cleaner_info' },
  { title: 'Список соседей (пересечение дат)', value: 'overlapping_guests' }
]

const days = [
  { title: 'Понедельник', value: 'mon' }, { title: 'Вторник', value: 'tue' },
  { title: 'Среда', value: 'wed' }, { title: 'Четверг', value: 'thu' },
  { title: 'Пятница', value: 'fri' }, { title: 'Суббота', value: 'sat' },
  { title: 'Воскресенье', value: 'sun' }
]

async function fetchQuarterlyReport() {
  loading.value = true
  try {
    const res = await api.get('/api/analytics/', {
      params: { type: 'quarterly_report', quarter: selectedQuarter.value, year: selectedYear.value }
    })
    reportData.value = res.data
  } catch (e) {
    error.value = 'Ошибка загрузки отчета'
  } finally {
    loading.value = false
  }
}

async function runInfoQuery() {
  loading.value = true
  infoResult.value = null
  error.value = ''
  try {
    const res = await api.get('/api/analytics/', { params: queryParams.value })
    infoResult.value = res.data
  } catch (e) {
    error.value = e.response?.data?.error || 'Ошибка выполнения запроса'
  } finally {
    loading.value = false
  }
}

async function loadHelperData() {
  try {
    const [cRes, gRes] = await Promise.all([api.get('/api/cities/'), api.get('/api/guests/')])
    cities.value = cRes.data
    guests.value = gRes.data
  } catch (e) { console.error(e) }
}

onMounted(() => {
  fetchQuarterlyReport()
  loadHelperData()
})

watch([selectedQuarter, selectedYear], fetchQuarterlyReport)
</script>

<template>
  <v-container>
    <v-tabs v-model="tab" color="indigo-darken-3" align-tabs="center" class="mb-6">
      <v-tab value="quarterly">Квартальный отчет</v-tab>
      <v-tab value="info">Инфо-запросы</v-tab>
    </v-tabs>

    <v-window v-model="tab">
      <!-- Квартальный отчет -->
      <v-window-item value="quarterly">
        <v-row class="mb-4">
          <v-col cols="12" md="3">
            <v-select v-model="selectedQuarter" label="Квартал" :items="['1', '2', '3', '4']" variant="outlined"
              density="compact"></v-select>
          </v-col>
          <v-col cols="12" md="2">
            <v-text-field v-model="selectedYear" label="Год" type="number" variant="outlined"
              density="compact"></v-text-field>
          </v-col>
        </v-row>

        <v-row v-if="reportData">
          <v-col cols="12" md="4">
            <v-card color="indigo-darken-4" class="text-white pa-4 mb-4">
              <div class="text-overline">Итоговый доход</div>
              <div class="text-h4 font-weight-bold">{{ reportData.total_hotel_income.toLocaleString() }} ₽</div>
            </v-card>
            <v-card title="Этажи" border flat>
              <v-table density="compact">
                <thead>
                  <tr>
                    <th>Этаж</th>
                    <th class="text-right">Номеров</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="f in reportData.floors_structure" :key="f.number">
                    <td>{{ f.number }} этаж</td>
                    <td class="text-right">{{ f.rooms_count }}</td>
                  </tr>
                </tbody>
              </v-table>
            </v-card>
          </v-col>
          <v-col cols="12" md="8">
            <v-card title="Статистика по номерам" border flat>
              <v-data-table :items="reportData.rooms_efficiency" density="compact"
                :headers="[{ title: '№', key: 'number' }, { title: 'Клиентов', key: 'clients_count', align: 'center' }, { title: 'Доход', key: 'income', align: 'end' }]">
                <template v-slot:item.income="{ item }"><b>{{ item.income || 0 }} ₽</b></template>
              </v-data-table>
            </v-card>
          </v-col>
        </v-row>
      </v-window-item>

      <!-- Информационные запросы -->
      <v-window-item value="info">
        <v-card border flat class="pa-4 mb-4">
          <v-row dense>
            <v-col cols="12" md="6">
              <v-select v-model="queryParams.type" :items="queryTypes" label="Выберите запрос" variant="outlined"
                density="compact"></v-select>
            </v-col>

            <!-- Динамические поля -->
            <v-col cols="12" md="3" v-if="queryParams.type === 'clients_in_room'">
              <v-text-field v-model="queryParams.room" label="Номер комнаты" variant="outlined"
                density="compact"></v-text-field>
            </v-col>
            <v-col cols="12" md="3" v-if="queryParams.type === 'clients_in_room'">
              <v-text-field v-model="queryParams.start" label="С даты" type="date" variant="outlined"
                density="compact"></v-text-field>
            </v-col>
            <v-col cols="12" md="3" v-if="queryParams.type === 'clients_in_room'">
              <v-text-field v-model="queryParams.end" label="По дату" type="date" variant="outlined"
                density="compact"></v-text-field>
            </v-col>
            <v-col cols="12" md="3" v-if="queryParams.type === 'clients_by_city'">
              <v-select v-model="queryParams.city_id" :items="cities" item-title="name" item-value="id" label="Город"
                variant="outlined" density="compact"></v-select>
            </v-col>
            <v-col cols="12" md="4" v-if="['cleaner_info', 'overlapping_guests'].includes(queryParams.type)">
              <v-autocomplete v-model="queryParams.guest_id" :items="guests"
                :item-title="g => `${g.last_name} ${g.first_name}`" item-value="id" label="Гость" variant="outlined"
                density="compact"></v-autocomplete>
            </v-col>
            <v-col cols="12" md="2" v-if="queryParams.type === 'cleaner_info'">
              <v-select v-model="queryParams.day" :items="days" label="День недели" variant="outlined"
                density="compact"></v-select>
            </v-col>

            <v-col cols="12" class="d-flex justify-end">
              <v-btn color="indigo" prepend-icon="mdi-magnify" @click="runInfoQuery" :loading="loading">Получить
                данные</v-btn>
            </v-col>
          </v-row>
        </v-card>

        <div v-if="infoResult" class="mt-4">
          <v-alert v-if="infoResult.free_rooms_count !== undefined" type="success" variant="tonal">Свободных номеров: {{
            infoResult.free_rooms_count }}</v-alert>
          <v-alert v-if="infoResult.count !== undefined" type="info" variant="tonal">Клиентов из города: {{
            infoResult.count
          }}</v-alert>

          <v-card v-if="Array.isArray(infoResult)" border flat>
            <v-list lines="two">
              <v-list-item v-for="(item, i) in infoResult" :key="i" border>
                <v-list-item-title class="font-weight-bold">{{ item.fio }}</v-list-item-title>
                <v-list-item-subtitle v-if="item.period">Период: {{ item.period }} | Номер: {{ item.room
                }}</v-list-item-subtitle>
                <v-list-item-subtitle v-else-if="item.from">Жил с {{ item.from }} по {{ item.to
                }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item v-if="infoResult.length === 0">Ничего не найдено</v-list-item>
            </v-list>
          </v-card>

          <v-alert v-if="infoResult.cleaners" type="success" variant="tonal">
            Номер {{ infoResult.room }} убирают: <strong>{{ infoResult.cleaners.join(', ') || 'Нет данных' }}</strong>
          </v-alert>
        </div>
      </v-window-item>
    </v-window>

    <v-alert v-if="error" type="error" variant="tonal" class="mt-4">{{ error }}</v-alert>
  </v-container>
</template>