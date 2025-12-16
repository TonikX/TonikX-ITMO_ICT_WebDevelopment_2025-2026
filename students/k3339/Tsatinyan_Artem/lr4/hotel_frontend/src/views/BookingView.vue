<template>
  <v-container>
    <h1 class="text-h4 font-weight-bold mb-6">Подобрать номер</h1>

    <v-card class="mb-8" elevation="3" rounded="lg">
      <v-card-text class="pa-6">
        <v-form @submit.prevent="searchRooms">
          <v-row align="center">
            <v-col cols="12" md="4">
              <v-text-field
                v-model="dates.check_in"
                label="Дата заезда"
                type="date"
                variant="outlined"
                density="comfortable"
                hide-details
                prepend-inner-icon="mdi-calendar-arrow-right"
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="dates.check_out"
                label="Дата выезда"
                type="date"
                variant="outlined"
                density="comfortable"
                hide-details
                prepend-inner-icon="mdi-calendar-arrow-left"
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-btn
                size="large"
                color="primary"
                type="submit"
                :loading="searching"
                block
                prepend-icon="mdi-magnify"
                class="text-none"
              >
                Найти свободные
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>

    <v-expand-transition>
      <div v-if="searched">
        <div class="d-flex justify-space-between align-center mb-4">
          <h2 class="text-h5">Результаты поиска</h2>
          <v-chip color="primary" variant="flat">{{ rooms.length }} доступно</v-chip>
        </div>

        <v-alert v-if="rooms.length === 0" type="warning" variant="tonal" border="start" class="mb-4">
          Нет свободных номеров на эти даты. Попробуйте изменить период.
        </v-alert>

        <v-row>
          <v-col v-for="room in rooms" :key="room.id" cols="12" md="4" sm="6">
            <v-card hover border elevation="1" rounded="lg" class="h-100 d-flex flex-column">
              <v-card-item>
                <template v-slot:append>
                  <v-chip size="small" color="grey">{{ room.floor }} этаж</v-chip>
                </template>
                <v-card-title class="text-h6">Комната {{ room.number }}</v-card-title>
                <v-card-subtitle>{{ room.room_type_display || room.room_type }}</v-card-subtitle>
              </v-card-item>

              <v-card-text class="py-4">
                <div class="d-flex align-baseline">
                  <span class="text-h4 font-weight-bold text-primary mr-1">{{ room.daily_price }}</span>
                  <span class="text-subtitle-1 text-grey">₽ / сутки</span>
                </div>
              </v-card-text>

              <v-spacer></v-spacer>

              <v-card-actions class="pa-4 pt-0">
                <v-btn
                  color="primary"
                  variant="flat"
                  block
                  size="large"
                  @click="selectRoom(room)"
                >
                  Забронировать
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </div>
    </v-expand-transition>

    <v-dialog v-model="showDialog" max-width="600" persistent>
      <v-card rounded="lg">
        <v-card-title class="bg-primary text-white py-3">Оформление гостя</v-card-title>
        <v-card-subtitle class="pt-4 pb-2 text-h6">
          Номер {{ selectedRoom?.number }}
          <span class="text-subtitle-1 text-grey ml-2">{{ dates.check_in }} — {{ dates.check_out }}</span>
        </v-card-subtitle>

        <v-card-text>
          <v-form @submit.prevent="confirmBooking">
            <v-row dense class="mt-2">
              <v-col cols="12"><div class="text-subtitle-2 mb-2">ПАСПОРТНЫЕ ДАННЫЕ</div></v-col>
              <v-col cols="6"><v-text-field v-model="client.passport_number" label="Паспорт" variant="outlined" density="compact" required/></v-col>
              <v-col cols="6"><v-text-field v-model="client.city" label="Город" variant="outlined" density="compact" required/></v-col>
              <v-col cols="4"><v-text-field v-model="client.last_name" label="Фамилия" variant="outlined" density="compact" required/></v-col>
              <v-col cols="4"><v-text-field v-model="client.first_name" label="Имя" variant="outlined" density="compact" required/></v-col>
              <v-col cols="4"><v-text-field v-model="client.patronymic" label="Отчество" variant="outlined" density="compact" /></v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="showDialog = false">Отмена</v-btn>
          <v-btn color="primary" variant="flat" :loading="bookingLoading" @click="confirmBooking">Подтвердить заселение</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="3000">
      {{ snackbar.text }}
      <template v-slot:actions>
        <v-btn variant="text" @click="snackbar.show = false">Закрыть</v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/api'

const router = useRouter()
const searching = ref(false)
const searched = ref(false)
const rooms = ref([])
const showDialog = ref(false)
const selectedRoom = ref(null)
const bookingLoading = ref(false)

const dates = reactive({
  check_in: new Date().toISOString().substr(0, 10),
  check_out: new Date(new Date().setDate(new Date().getDate() + 1)).toISOString().substr(0, 10)
})

const client = reactive({
  passport_number: '', last_name: '', first_name: '', patronymic: '', city: ''
})

const snackbar = reactive({ show: false, text: '', color: 'success' })

const searchRooms = async () => {
  searching.value = true
  rooms.value = []
  searched.value = false
  try {
    const { data } = await api.get('/api/reports/free-rooms/', {
      params: { check_in: dates.check_in, check_out: dates.check_out }
    })
    rooms.value = data
    searched.value = true
  } catch (e) {
    alert('Ошибка поиска')
  } finally {
    searching.value = false
  }
}

const selectRoom = (room) => {
  selectedRoom.value = room
  showDialog.value = true
}

const confirmBooking = async () => {
  bookingLoading.value = true
  try {
    await api.post('/api/actions/check-in/', {
      ...client,
      room_number: selectedRoom.value.number,
      check_in: dates.check_in,
      check_out: dates.check_out
    })
    snackbar.text = 'Успешно заселено!'
    snackbar.color = 'success'
    snackbar.show = true
    showDialog.value = false

    setTimeout(() => router.push('/stays'), 1000)
  } catch (e) {
    snackbar.text = e.response?.data?.detail || 'Ошибка заселения'
    snackbar.color = 'error'
    snackbar.show = true
  } finally {
    bookingLoading.value = false
  }
}
</script>
