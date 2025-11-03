<template>
  <div>
    <h1 class="text-h4 mb-6">Панель управления</h1>

    <v-row>
      <v-col cols="12" sm="6" md="4">
        <v-card>
          <v-card-text>
            <div class="d-flex align-center">
              <v-icon size="40" color="primary" class="mr-4">mdi-book-open-page-variant</v-icon>
              <div>
                <div class="text-h6">{{ stats.totalReadingRooms }}</div>
                <div class="text-caption">Всего залов</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="4">
        <v-card>
          <v-card-text>
            <div class="d-flex align-center">
              <v-icon size="40" color="success" class="mr-4">mdi-account</v-icon>
              <div>
                <div class="text-h6">{{ stats.totalReaders }}</div>
                <div class="text-caption">Всего читателей</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="4">
        <v-card>
          <v-card-text>
            <div class="d-flex align-center">
              <v-icon size="40" color="info" class="mr-4">mdi-calendar-clock</v-icon>
              <div>
                <div class="text-h6">{{ stats.activeReservations }}</div>
                <div class="text-caption">Активных бронирований</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="4">
        <v-card>
          <v-card-text>
            <div class="d-flex align-center">
              <v-icon size="40" color="warning" class="mr-4">mdi-account-tie</v-icon>
              <div>
                <div class="text-h6">{{ stats.totalLibrarians }}</div>
                <div class="text-caption">Библиотекарей</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="4">
        <v-card>
          <v-card-text>
            <div class="d-flex align-center">
              <v-icon size="40" color="success" class="mr-4">mdi-check-circle</v-icon>
              <div>
                <div class="text-h6">{{ stats.freeReadingRooms }}</div>
                <div class="text-caption">Свободных залов</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="4">
        <v-card>
          <v-card-text>
            <div class="d-flex align-center">
              <v-icon size="40" color="primary" class="mr-4">mdi-currency-rub</v-icon>
              <div>
                <div class="text-h6">{{ stats.totalIncome }} ₽</div>
                <div class="text-caption">Доход за квартал</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="d-flex align-center flex-wrap">
            <span class="mr-4">Свободные залы</span>
            <v-spacer></v-spacer>
            <div class="d-flex align-center">
              <v-menu
                v-model="dateMenu"
                :close-on-content-click="false"
                transition="scale-transition"
                offset-y
                min-width="auto"
              >
                <template v-slot:activator="{ props }">
                  <v-text-field
                    :model-value="formattedDate"
                    label="Дата и время"
                    prepend-inner-icon="mdi-calendar-clock"
                    readonly
                    v-bind="props"
                    variant="outlined"
                    density="compact"
                    hide-details
                    style="max-width: 250px"
                    class="mr-3"
                  ></v-text-field>
                </template>
                <v-card>
                  <v-card-text class="pa-0">
                    <v-date-picker
                      v-model="datePickerValue"
                      @update:model-value="updateSelectedDate"
                      locale="ru"
                      hide-header
                    ></v-date-picker>
                    <v-divider></v-divider>
                    <div class="pa-4">
                      <v-text-field
                        v-model="timeValue"
                        label="Время"
                        type="time"
                        variant="outlined"
                        density="compact"
                        @update:model-value="updateSelectedDate"
                      ></v-text-field>
                    </div>
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn text @click="dateMenu = false">Закрыть</v-btn>
                  </v-card-actions>
                </v-card>
              </v-menu>
              <v-btn @click="loadFreeReadingRooms" color="primary">
                <v-icon start>mdi-refresh</v-icon>
                Обновить
              </v-btn>
            </div>
          </v-card-title>
          <v-card-text>
            <v-data-table
              :headers="freeReadingRoomsHeaders"
              :items="freeReadingRooms"
              :loading="loading"
              hide-default-footer
              no-data-text="Нет данных"
              loading-text="Загрузка..."
            ></v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Последние бронирования</v-card-title>
          <v-card-text>
            <v-data-table
              :headers="reservationsHeaders"
              :items="recentReservations"
              :loading="loading"
              hide-default-footer
              no-data-text="Нет данных"
              loading-text="Загрузка..."
            ></v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { readingRoomsAPI, readersAPI, reservationsAPI, librariansAPI, reportsAPI } from '@/services/api'
import dayjs from 'dayjs'

const stats = ref({
  totalReadingRooms: 0,
  totalReaders: 0,
  activeReservations: 0,
  totalLibrarians: 0,
  freeReadingRooms: 0,
  totalIncome: 0
})

const freeReadingRooms = ref([])
const recentReservations = ref([])
const loading = ref(true)
const selectedDate = ref(dayjs().format('YYYY-MM-DDTHH:mm'))
const dateMenu = ref(false)
const datePickerValue = ref(new Date())
const timeValue = ref(dayjs().format('HH:mm'))

const formattedDate = computed(() => {
  return dayjs(selectedDate.value).format('DD.MM.YYYY HH:mm')
})

const updateSelectedDate = () => {
  const dateStr = dayjs(datePickerValue.value).format('YYYY-MM-DD')
  selectedDate.value = `${dateStr}T${timeValue.value}`
}

const freeReadingRoomsHeaders = [
  { title: 'Номер', key: 'number' },
  { title: 'Этаж', key: 'floor' },
  { title: 'Тип', key: 'room_type_display' },
  { title: 'Вместимость', key: 'capacity' },
  { title: 'Цена/час', key: 'hourly_rate' }
]

const reservationsHeaders = [
  { title: 'Читатель', key: 'reader_name' },
  { title: 'Зал', key: 'reading_room_number' },
  { title: 'Начало', key: 'reserved_from' },
  { title: 'Статус', key: 'is_active' }
]

const loadDashboardData = async () => {
  try {
    loading.value = true
    const [roomsRes, readersRes, reservationsRes, librariansRes] = await Promise.all([
      readingRoomsAPI.getAll(),
      readersAPI.getAll(),
      reservationsAPI.getAll(),
      librariansAPI.getAll()
    ])

    const readingRooms = roomsRes.data.results || roomsRes.data
    const readers = readersRes.data.results || readersRes.data
    const reservations = reservationsRes.data.results || reservationsRes.data
    const librarians = librariansRes.data.results || librariansRes.data

    stats.value = {
      totalReadingRooms: readingRooms.length,
      totalReaders: readers.length,
      activeReservations: reservations.filter(r => r.is_active).length,
      totalLibrarians: librarians.length,
      freeReadingRooms: 0,
      totalIncome: 0
    }

    recentReservations.value = reservations.slice(0, 5).map(r => ({
      ...r,
      reserved_from: dayjs(r.reserved_from).format('DD.MM.YYYY HH:mm'),
      is_active: r.is_active ? 'Активно' : 'Завершено'
    }))

    const currentQuarter = Math.ceil((dayjs().month() + 1) / 3)
    try {
      const reportRes = await reportsAPI.getQuarterReport(currentQuarter)
      stats.value.totalIncome = parseFloat(reportRes.data.total_income).toFixed(2)
    } catch (error) {
      console.log('Не удалось загрузить отчет о доходах')
    }
  } catch (error) {
    console.error('Ошибка загрузки данных:', error)
  } finally {
    loading.value = false
  }
}

    const loadFreeReadingRooms = async () => {
      try {
        const response = await readingRoomsAPI.getFreeReadingRooms(selectedDate.value)
        freeReadingRooms.value = (response.data.free_reading_rooms || []).slice(0, 5)
        stats.value.freeReadingRooms = response.data.free_count
      } catch (error) {
        console.error('Ошибка загрузки свободных залов:', error)
      }
    }

onMounted(() => {
  loadDashboardData()
  loadFreeReadingRooms()
})
</script>

