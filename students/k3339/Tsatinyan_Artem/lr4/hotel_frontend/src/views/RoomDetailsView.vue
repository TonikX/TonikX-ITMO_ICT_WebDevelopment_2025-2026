<template>
  <v-container v-if="room">
    <v-btn variant="text" to="/rooms" class="mb-4" prepend-icon="mdi-arrow-left">Назад к списку</v-btn>

    <v-row>
      <v-col cols="12" md="4">
        <v-card class="pa-4 sticky-card" elevation="3" rounded="lg">
          <div class="d-flex justify-space-between align-start">
            <div>
              <h2 class="text-h4 font-weight-bold text-primary">№ {{ room.number }}</h2>
              <div class="text-subtitle-1 text-grey">{{ room.room_type }}</div>
            </div>
            <v-icon size="40" color="grey-lighten-2">mdi-bed</v-icon>
          </div>

          <v-divider class="my-4"></v-divider>

          <div class="d-flex flex-column gap-3">
            <div class="d-flex justify-space-between">
              <span class="text-grey-darken-1"><v-icon size="small" class="mr-1">mdi-layers</v-icon> Этаж</span>
              <span class="font-weight-medium">{{ room.floor }}</span>
            </div>
            <div class="d-flex justify-space-between">
              <span class="text-grey-darken-1"><v-icon size="small" class="mr-1">mdi-phone</v-icon> Телефон</span>
              <span class="font-weight-medium">{{ room.phone_number }}</span>
            </div>
            <div class="d-flex justify-space-between align-center mt-2">
              <span class="text-grey-darken-1">Цена за сутки</span>
              <span class="text-h5 text-green-darken-2 font-weight-bold">{{ room.daily_price }} ₽</span>
            </div>
          </div>

          <v-btn block color="primary" size="large" class="mt-6" @click="showBookingDialog = true" elevation="2">
            Заселить гостя
          </v-btn>
        </v-card>
      </v-col>

      <v-col cols="12" md="8">
        <v-card class="pa-6" elevation="2" rounded="lg">
          <h3 class="text-h6 mb-4 font-weight-regular">
            <v-icon start>mdi-calendar-month</v-icon>
            Занятость на 30 дней
          </h3>

          <div class="calendar-grid">
            <div
              v-for="day in calendarDays"
              :key="day.dateStr"
              class="calendar-day d-flex flex-column align-center justify-center"
              :class="{ 'busy': day.isBusy, 'free': !day.isBusy }"
              v-tooltip:top="day.dateStr + (day.isBusy ? ' (Занято)' : ' (Свободно)')"
            >
              <div class="day-number">{{ day.dayNumber }}</div>
              <v-icon size="small" v-if="day.isBusy" color="red-darken-4">mdi-lock</v-icon>
            </div>
          </div>

          <div class="d-flex mt-6 align-center justify-center gap-4">
            <div class="d-flex align-center">
              <div class="legend-box free mr-2"></div> <span class="text-caption">Свободно</span>
            </div>
            <div class="d-flex align-center">
              <div class="legend-box busy mr-2"></div> <span class="text-caption">Занято/Бронь</span>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="showBookingDialog" max-width="600" persistent>
      <v-card rounded="lg">
        <v-card-title class="bg-primary text-white py-3">
          Заселение в номер {{ room.number }}
        </v-card-title>

        <v-card-text class="pt-4">
          <v-form @submit.prevent="submitBooking">
            <v-row>
              <v-col cols="12" sm="6">
                <v-text-field v-model="form.check_in" type="date" label="Заезд" required variant="outlined" density="comfortable"/>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field v-model="form.check_out" type="date" label="Выезд" variant="outlined" density="comfortable"/>
              </v-col>

              <v-col cols="12">
                <div class="text-subtitle-2 text-uppercase text-grey mb-2 mt-2">Данные гостя</div>
                <v-divider class="mb-4"></v-divider>
              </v-col>

              <v-col cols="6">
                <v-text-field v-model="form.passport_number" label="Паспорт" required variant="outlined" density="compact"/>
              </v-col>
              <v-col cols="6">
                <v-text-field v-model="form.city" label="Город" required variant="outlined" density="compact"/>
              </v-col>
              <v-col cols="12">
                <v-row dense>
                  <v-col cols="4">
                    <v-text-field v-model="form.last_name" label="Фамилия" required variant="outlined" density="compact"/>
                  </v-col>
                  <v-col cols="4">
                    <v-text-field v-model="form.first_name" label="Имя" required variant="outlined" density="compact"/>
                  </v-col>
                  <v-col cols="4">
                    <v-text-field v-model="form.patronymic" label="Отчество" variant="outlined" density="compact"/>
                  </v-col>
                </v-row>
              </v-col>
            </v-row>

            <v-alert v-if="errorMsg" type="error" variant="tonal" class="mt-2">
              {{ errorMsg }}
            </v-alert>
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="showBookingDialog = false">Отмена</v-btn>
          <v-btn color="primary" variant="flat" @click="submitBooking" :loading="loading">Подтвердить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api/api'

const route = useRoute()
const room = ref(null)
const stays = ref([])
const showBookingDialog = ref(false)
const loading = ref(false)
const errorMsg = ref('')

const form = reactive({
  passport_number: '',
  last_name: '',
  first_name: '',
  patronymic: '',
  city: '',
  check_in: new Date().toISOString().substr(0, 10),
  check_out: ''
})

const calendarDays = computed(() => {
  const days = []
  const today = new Date()

  for (let i = 0; i < 30; i++) {
    const current = new Date(today)
    current.setDate(today.getDate() + i)
    const dateStr = current.toISOString().substr(0, 10)

    const isBusy = stays.value.some(stay => {
      const start = stay.check_in
      const end = stay.check_out || '2099-12-31'
      return dateStr >= start && dateStr < end
    })

    days.push({
      dateStr,
      dayNumber: current.getDate(),
      isBusy
    })
  }
  return days
})

const loadData = async () => {
  try {
    const roomId = route.params.id
    const roomRes = await api.get(`/api/rooms/${roomId}/`)
    room.value = roomRes.data
    const staysRes = await api.get(`/api/stays/?room=${roomId}`)
    stays.value = staysRes.data
  } catch (e) {
    console.error(e)
  }
}

const submitBooking = async () => {
  loading.value = true
  errorMsg.value = ''
  try {
    await api.post('/api/actions/check-in/', {
      ...form,
      room_number: room.value.number
    })
    showBookingDialog.value = false
    await loadData()
    form.passport_number = ''
    form.last_name = ''
    form.first_name = ''
  } catch (e) {
    errorMsg.value = e.response?.data?.detail || 'Ошибка заселения'
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>

<style scoped>
.sticky-card {
  position: sticky;
  top: 80px;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(45px, 1fr));
  gap: 12px;
}
.calendar-day {
  height: 50px;
  border-radius: 12px;
  font-weight: bold;
  font-size: 0.9rem;
  transition: all 0.2s;
  cursor: default;
}
.busy {
  background-color: #ffebee;
  color: #c62828;
  border: 1px solid #ffcdd2;
}
.free {
  background-color: #e8f5e9;
  color: #2e7d32;
  border: 1px solid #c8e6c9;
}
.free:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.legend-box {
  width: 20px;
  height: 20px;
  border-radius: 4px;
}
</style>
