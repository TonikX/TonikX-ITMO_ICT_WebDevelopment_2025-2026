<template>
  <v-app>
    <v-main>
      <v-container>
        <v-card>
          <v-card-title>Добавить бронирование</v-card-title>
          <v-card-text>
            <v-menu v-model="startMenu" :close-on-content-click="false" offset-y min-width="auto">
              <template #activator="{ props }">
                <v-text-field
                  v-model="reservation.start_date"
                  label="Дата заезда"
                  readonly
                  v-bind="props"
                  outlined
                  dense
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="startDate"
                @update:model-value="onStartDateSelect"
                locale="ru"
                no-title
              ></v-date-picker>
            </v-menu>

            <v-menu v-model="endMenu" :close-on-content-click="false" offset-y min-width="auto">
              <template #activator="{ props }">
                <v-text-field
                  v-model="reservation.end_date"
                  label="Дата выезда"
                  readonly
                  v-bind="props"
                  outlined
                  dense
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="endDate"
                @update:model-value="onEndDateSelect"
                locale="ru"
                no-title
              ></v-date-picker>
            </v-menu>

            <v-select
              v-model="selectedResidents"
              :items="residents"
              item-title="full_name"
              item-value="id"
              label="Клиенты"
              multiple
              chips
              outlined
              dense
            />

            <v-select
              v-model="selectedRooms"
              :items="rooms"
              item-title="room_number"
              item-value="id"
              label="Номера"
              multiple
              chips
              outlined
              dense
            />

            <v-btn color="success" class="mt-3" type="button" @click="addReservation">
              Добавить
            </v-btn>

            <v-alert
              v-if="success"
              type="success"
              class="mt-2"
              dense
            >
              {{ success }}
            </v-alert>

            <v-alert
              v-if="error"
              type="error"
              class="mt-2"
              dense
            >
              {{ error }}
            </v-alert>
          </v-card-text>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import {ref, onMounted} from 'vue'
import {useRouter} from 'vue-router'
import api from '@/api'

const router = useRouter()

const reservation = ref({start_date: '', end_date: '', residents: [], rooms: []})
const startMenu = ref(false)
const endMenu = ref(false)
const startDate = ref(null)
const endDate = ref(null)
const success = ref('')
const error = ref('')
const residents = ref([])
const rooms = ref([])

const selectedResidents = ref([])
const selectedRooms = ref([])

// форматируем дату в YYYY-MM-DD
const formatDate = (date) => {
  const d = new Date(date)
  const yyyy = d.getFullYear()
  const mm = String(d.getMonth() + 1).padStart(2, '0')
  const dd = String(d.getDate()).padStart(2, '0')
  return `${yyyy}-${mm}-${dd}`
}

const loadResidents = async () => {
  try {
    const res = await api.get('residents/')
    residents.value = res.data.map(r => ({
      ...r,
      full_name: `${r.surname} ${r.name} ${r.patronymic}`
    }))
  } catch (e) {
    console.error('Ошибка загрузки клиентов', e)
  }
}

const loadRooms = async () => {
  try {
    const res = await api.get('rooms/')
    rooms.value = res.data
  } catch (e) {
    console.error('Ошибка загрузки комнат', e)
  }
}

onMounted(() => {
  loadResidents()
  loadRooms()
})

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

const addReservation = async () => {
  if (!reservation.value.start_date || !reservation.value.end_date || selectedResidents.value.length === 0 || selectedRooms.value.length === 0) {
    error.value = 'Заполните все поля'
    success.value = ''
    return
  }

  const payload = {
    start_date: reservation.value.start_date,
    end_date: reservation.value.end_date,
    residents: selectedResidents.value,
    rooms: selectedRooms.value
  }

  try {
    await api.post('reservations/', payload)
    success.value = 'Бронирование успешно добавлено!'
    error.value = ''

    setTimeout(() => {
      router.push('/reservations')
    }, 1500)
  } catch (e) {
    console.error(e)
    error.value = 'Ошибка при добавлении бронирования'
    success.value = ''
  }
}
</script>
