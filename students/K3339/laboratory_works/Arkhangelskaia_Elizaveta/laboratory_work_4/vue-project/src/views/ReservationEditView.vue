<template>
  <v-container>
    <v-card>
      <v-card-title>Редактировать бронирование</v-card-title>

      <v-card-text>
        <!-- Дата заезда -->
        <v-menu v-model="startMenu" :close-on-content-click="false">
          <template #activator="{ props }">
            <v-text-field
              v-model="reservation.start_date"
              label="Дата заезда"
              readonly
              outlined
              dense
              v-bind="props"
            />
          </template>

          <v-date-picker
            v-model="startDate"
            locale="ru"
            @update:model-value="onStartDateSelect"
          />
        </v-menu>

        <!-- Дата выезда -->
        <v-menu v-model="endMenu" :close-on-content-click="false">
          <template #activator="{ props }">
            <v-text-field
              v-model="reservation.end_date"
              label="Дата выезда"
              readonly
              outlined
              dense
              v-bind="props"
            />
          </template>

          <v-date-picker
            v-model="endDate"
            locale="ru"
            @update:model-value="onEndDateSelect"
          />
        </v-menu>

        <!-- Клиенты -->
        <v-select
          v-model="reservation.residents"
          :items="residents"
          item-title="full_name"
          item-value="id"
          label="Клиенты"
          multiple
          chips
          outlined
          dense
        />

        <!-- Номера -->
        <v-select
          v-model="reservation.rooms"
          :items="rooms"
          item-title="room_number"
          item-value="id"
          label="Номера"
          multiple
          chips
          outlined
          dense
        />

        <v-btn
          color="green"
          class="mt-4"
          block
          @click="updateReservation"
        >
          Сохранить
        </v-btn>

        <v-alert
          v-if="error"
          type="error"
          class="mt-3"
          dense
        >
          {{ error }}
        </v-alert>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api'

const route = useRoute()
const router = useRouter()

/* состояние */
const reservation = ref({
  start_date: '',
  end_date: '',
  residents: [], // массив ID
  rooms: []      // массив ID
})

const residents = ref([])
const rooms = ref([])

const startMenu = ref(false)
const endMenu = ref(false)
const startDate = ref(null)
const endDate = ref(null)

const error = ref('')

/* формат даты */
const formatDate = (date) => {
  const d = new Date(date)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

/* загрузка клиентов */
const loadResidents = async () => {
  const res = await api.get('residents/')
  residents.value = res.data.map(r => ({
    ...r,
    full_name: `${r.surname} ${r.name} ${r.patronymic}`
  }))
}

/* загрузка номеров */
const loadRooms = async () => {
  const res = await api.get('rooms/')
  rooms.value = res.data
}

/* загрузка бронирования */
const loadReservation = async () => {
  const res = await api.get(`reservations/${route.params.id}/`)

  reservation.value.start_date = res.data.start_date
  reservation.value.end_date = res.data.end_date

  // ✅ ВАЖНО: сервер уже возвращает ID
  reservation.value.residents = res.data.residents
  reservation.value.rooms = res.data.rooms

  startDate.value = new Date(res.data.start_date)
  endDate.value = new Date(res.data.end_date)
}

/* выбор дат */
const onStartDateSelect = (val) => {
  reservation.value.start_date = formatDate(val)
  startDate.value = val
  startMenu.value = false
}

const onEndDateSelect = (val) => {
  reservation.value.end_date = formatDate(val)
  endDate.value = val
  endMenu.value = false
}

/* сохранение */
const updateReservation = async () => {
  error.value = ''

  try {
    await api.patch(`reservations/${route.params.id}/`, {
      start_date: reservation.value.start_date,
      end_date: reservation.value.end_date,
      residents: reservation.value.residents,
      rooms: reservation.value.rooms
    })

    router.push('/reservations')
  } catch (e) {
    console.error(e)
    error.value = 'Ошибка обновления бронирования'
  }
}

onMounted(async () => {
  try {
    await Promise.all([
      loadResidents(),
      loadRooms(),
      loadReservation()
    ])
  } catch {
    error.value = 'Ошибка загрузки данных'
  }
})
</script>
