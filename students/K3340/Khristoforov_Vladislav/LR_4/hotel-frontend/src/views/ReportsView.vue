<script setup>
/**
 * ReportsView.vue - Страница аналитики и отчетов.
 * Позволяет администратору видеть финансовые показатели и 
 * загруженность отеля за выбранный период времени.
 */
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'

// --- Состояние ---
const bookings = ref([])
const rooms = ref([])
const loading = ref(false)

// Фильтры даты (по умолчанию: с 1 января текущего года по сегодняшнее число)
const dateStart = ref(new Date(new Date().getFullYear(), 0, 1).toISOString().substr(0, 10))
const dateEnd = ref(new Date().toISOString().substr(0, 10))

/**
 * Загрузка первичных данных (бронирования и номера).
 * Вся аналитика считается "на лету" из этих массивов.
 */
async function loadData() {
  loading.value = true
  try {
    const [bRes, rRes] = await Promise.all([
      api.get('/api/bookings/'),
      api.get('/api/rooms/')
    ])
    bookings.value = bRes.data
    rooms.value = rRes.data
  } catch (e) {
    console.error('Ошибка при загрузке данных для отчета:', e)
  } finally {
    loading.value = false
  }
}

// --- Вычисляемые свойства (Аналитика) ---

/**
 * 1. Список бронирований, попавших в выбранный временной интервал.
 */
const filteredBookings = computed(() => {
  return bookings.value.filter((b) => {
    return b.check_in >= dateStart.value && b.check_in <= dateEnd.value
  })
})

/**
 * 2. Общий финансовый результат за период.
 */
const totalIncome = computed(() => {
  return filteredBookings.value.reduce((sum, b) => sum + Number(b.total_cost || 0), 0)
})

/**
 * 3. Статистика эффективности по каждому номеру.
 */
const roomStats = computed(() => {
  const map = {}

  // Сначала добавляем все существующие комнаты с нулевыми показателями
  rooms.value.forEach((r) => {
    map[r.number] = { number: r.number, income: 0, clients: 0 }
  })

  // Распределяем доход из отфильтрованных бронирований
  filteredBookings.value.forEach((b) => {
    const num = b.room_details?.number
    if (num && map[num]) {
      map[num].income += Number(b.total_cost || 0)
      map[num].clients += 1
    }
  })

  // Превращаем объект в массив и сортируем по убыванию дохода
  return Object.values(map).sort((a, b) => b.income - a.income)
})

/**
 * 4. Статистика распределения номерного фонда по этажам.
 */
const floorStats = computed(() => {
  const map = {}
  rooms.value.forEach((r) => {
    const floor = r.floor_details?.number || r.floor || '?'
    if (!map[floor]) map[floor] = 0
    map[floor] += 1
  })

  return Object.keys(map)
    .map((f) => ({ floor: f, count: map[f] }))
    .sort((a, b) => a.floor - b.floor)
})

// Загружаем данные при монтировании компонента
onMounted(loadData)
</script>

<template>
  <v-container>
    <!-- Заголовок страницы -->
    <div class="d-flex align-center justify-space-between mb-6">
      <div>
        <h1 class="text-h4 font-weight-bold text-indigo-darken-3">Финансовые отчеты</h1>
        <p class="text-subtitle-1 text-grey">Аналитика выручки и использования фонда</p>
      </div>
      <v-btn icon="mdi-refresh" variant="tonal" color="indigo" @click="loadData" :loading="loading"></v-btn>
    </div>

    <!-- Блок фильтрации и Итоговых показателей -->
    <v-card class="mb-6 pa-6 rounded-lg shadow-2" border>
      <v-row align="center">
        <v-col cols="12" md="3">
          <v-text-field v-model="dateStart" label="Начало периода" type="date" hide-details variant="outlined"
            density="comfortable"></v-text-field>
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field v-model="dateEnd" label="Конец периода" type="date" hide-details variant="outlined"
            density="comfortable"></v-text-field>
        </v-col>
        <v-divider vertical class="mx-4 d-none d-md-flex"></v-divider>
        <v-col cols="12" md="5" class="text-md-right text-center">
          <div class="text-subtitle-1 text-grey-darken-1">Доход за выбранный период</div>
          <div class="text-h3 font-weight-black text-success">{{ totalIncome.toLocaleString() }} ₽</div>
          <div class="text-subtitle-2 text-indigo mt-1">
            <v-icon icon="mdi-account-group" size="small" class="mr-1"></v-icon>
            Всего активных сделок: {{ filteredBookings.length }}
          </div>
        </v-col>
      </v-row>
    </v-card>

    <v-row>
      <!-- Таблица эффективности номеров -->
      <v-col cols="12" md="8">
        <v-card class="rounded-lg shadow-1" border>
          <v-card-title class="bg-grey-lighten-4 pa-4 font-weight-bold d-flex align-center">
            <v-icon icon="mdi-star-outline" class="mr-2" color="amber-darken-2"></v-icon>
            Рейтинг доходности номеров
          </v-card-title>

          <v-data-table :headers="[
            { title: 'Номер', key: 'number' },
            { title: 'Заселений', key: 'clients', align: 'center' },
            { title: 'Выручка', key: 'income', align: 'end' },
          ]" :items="roomStats" density="comfortable" hover :loading="loading"
            no-data-text="Нет данных за выбранный период">
            <template v-slot:item.number="{ item }">
              <span class="font-weight-medium">№ {{ item.number }}</span>
            </template>
            <template v-slot:item.income="{ item }">
              <span class="font-weight-bold text-success">{{ item.income.toLocaleString() }} ₽</span>
            </template>
            <template v-slot:item.clients="{ item }">
              <v-chip size="small" variant="flat" :color="item.clients > 0 ? 'indigo-lighten-4' : 'grey-lighten-3'">
                {{ item.clients }}
              </v-chip>
            </template>
          </v-data-table>
        </v-card>
      </v-col>

      <!-- Инфо-панель: Структура фонда (Этажи) -->
      <v-col cols="12" md="4">
        <v-card class="rounded-lg shadow-1" border>
          <v-card-title class="bg-grey-lighten-4 pa-4 font-weight-bold d-flex align-center">
            <v-icon icon="mdi-layers-outline" class="mr-2" color="indigo"></v-icon>
            Состав фонда
          </v-card-title>
          <v-table density="comfortable">
            <thead>
              <tr>
                <th class="text-left">Этаж</th>
                <th class="text-right">Кол-во номеров</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="f in floorStats" :key="f.floor">
                <td class="font-weight-medium">{{ f.floor }} этаж</td>
                <td class="text-right">
                  <v-badge color="indigo-lighten-4" :content="f.count" inline text-color="indigo-darken-4"
                    class="font-weight-bold"></v-badge>
                </td>
              </tr>
              <tr v-if="floorStats.length === 0">
                <td colspan="2" class="text-center text-grey pa-4">Данные отсутствуют</td>
              </tr>
            </tbody>
          </v-table>
          <v-divider></v-divider>
          <v-card-text class="text-caption text-grey text-center pt-4 italic">
            * Данные по этажам рассчитываются на основе всего номерного фонда отеля.
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.v-card-title {
  font-size: 1.1rem !important;
}

.shadow-1 {
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05) !important;
}

.shadow-2 {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08) !important;
}

.italic {
  font-style: italic;
}
</style>