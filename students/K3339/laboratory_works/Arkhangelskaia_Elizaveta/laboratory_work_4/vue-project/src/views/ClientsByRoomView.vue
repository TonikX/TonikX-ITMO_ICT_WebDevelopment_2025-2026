<template>
  <v-container>
    <v-card>
      <v-card-title>Поиск клиентов по комнате и датам</v-card-title>
      <v-card-text>
        <v-row dense>
          <v-col cols="12" md="4">
            <v-select
              v-model="roomNumber"
              :items="rooms"
              item-title="room_number"
              item-value="room_number"
              label="Номер комнаты"
              outlined
              dense
            ></v-select>

          </v-col>

          <v-col cols="12" md="4">
            <v-menu v-model="startMenu" :close-on-content-click="false" transition="scale-transition" offset-y>
              <template #activator="{ props }">
                <v-text-field
                  v-model="startDate"
                  label="Дата начала"
                  readonly
                  v-bind="props"
                  outlined
                  dense
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="startDatePicker"
                @update:model-value="val => { startDate = formatDate(val); startDatePicker = val; startMenu=false }"
                locale="ru"
                no-title
              ></v-date-picker>
            </v-menu>
          </v-col>

          <v-col cols="12" md="4">
            <v-menu v-model="endMenu" :close-on-content-click="false" transition="scale-transition" offset-y>
              <template #activator="{ props }">
                <v-text-field
                  v-model="endDate"
                  label="Дата окончания"
                  readonly
                  v-bind="props"
                  outlined
                  dense
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="endDatePicker"
                @update:model-value="val => { endDate = formatDate(val); endDatePicker = val; endMenu=false }"
                locale="ru"
                no-title
              ></v-date-picker>
            </v-menu>
          </v-col>
        </v-row>

        <v-btn color="#1B5E20" class="mt-3" @click="searchClients">Поиск</v-btn>

        <div v-if="error" class="mt-2" style="color:red">{{ error }}</div>

        <!-- Таблица результатов -->
        <v-data-table
          v-if="clients.length"
          :headers="headers"
          :items="clients"
          class="mt-3"
        ></v-data-table>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'

const roomNumber = ref(null)
const rooms = ref([])
const startDate = ref('')
const endDate = ref('')

const startMenu = ref(false)
const endMenu = ref(false)
const startDatePicker = ref(null)
const endDatePicker = ref(null)

const clients = ref([])
const error = ref('')

const headers = [
  { title: 'Фамилия', key: 'surname' },
  { title: 'Имя', key: 'name' },
  { title: 'Отчество', key: 'patronymic' },
  { title: 'Паспорт', key: 'passport_number' },
  { title: 'Город', key: 'city' }
]

const formatDate = (date) => {
  const d = new Date(date)
  const yyyy = d.getFullYear()
  const mm = String(d.getMonth() + 1).padStart(2, '0')
  const dd = String(d.getDate()).padStart(2, '0')
  return `${yyyy}-${mm}-${dd}`
}

onMounted(() => {
  loadRooms()
})


const loadRooms = async () => {
  try {
    const res = await api.get('rooms/')
    rooms.value = res.data
  } catch (e) {
    console.error('Ошибка загрузки номеров', e)
  }
}

// поиск клиентов
const searchClients = async () => {
  error.value = ''
  clients.value = []

  if (!roomNumber.value || !startDate.value || !endDate.value) {
    error.value = 'Заполните все поля'
    return
  }

  try {
    const res = await api.get(
      `req/clients/?room_number=${roomNumber.value}&start_date=${startDate.value}&end_date=${endDate.value}`
    )
    clients.value = res.data
  } catch (e) {
    console.error(e)
    error.value = 'Ошибка при получении данных'
  }
}
</script>
