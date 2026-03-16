<template>
  <v-row>
    <v-col cols="12" md="3">
      <v-card class="mb-4">
        <v-card-title class="text-h6">фильтры</v-card-title>
        <v-card-text>
          <v-select
            v-model="filters.room_type"
            :items="roomTypeItems"
            item-title="title"
            item-value="value"
            label="тип номера"
            variant="filled"
            density="comfortable"
            clearable
            bg-color="grey-lighten-4"
            rounded="lg"
          />
          <v-text-field
            v-model.number="filters.floor"
            type="number"
            label="этаж"
            variant="filled"
            density="comfortable"
            bg-color="grey-lighten-4"
            rounded="lg"
          />
          <v-btn color="primary" class="mt-2" @click="loadRooms">применить</v-btn>
          <v-btn variant="text" class="mt-2" @click="resetFilters">сбросить</v-btn>
        </v-card-text>
      </v-card>

      <v-card>
        <v-card-title class="text-h6">свободные номера сегодня</v-card-title>
        <v-card-text>
          <div v-if="availableRooms.length === 0">нет свободных номеров</div>
          <div v-else>
            <div v-for="room in availableRooms" :key="'a-' + room.id">
              № {{ room.number }} (этаж {{ room.floor }})
            </div>
          </div>
        </v-card-text>
      </v-card>
    </v-col>

    <v-col cols="12" md="9">
      <v-card>
        <v-card-title class="text-h6">все номера</v-card-title>
        <v-card-text>
          <v-alert v-if="error" type="error" density="compact" class="mb-2">
            {{ error }}
          </v-alert>
          <v-progress-linear v-if="loading" indeterminate color="primary" class="mb-2" />

          <v-row>
            <v-col
              v-for="room in rooms"
              :key="room.id"
              cols="12"
              sm="6"
              md="4"
            >
              <v-card>
                <v-card-title class="text-subtitle-1">
                  номер {{ room.number }}
                </v-card-title>
                <v-card-text>
                  <div>тип: {{ roomTypeLabel(room.room_type) }}</div>
                  <div>этаж: {{ room.floor }}</div>
                  <div>цена: {{ room.price }} ₽/сутки</div>
                  <div v-if="isRoomAvailable(room.id)" class="text-success mt-1">
                    свободен сегодня
                  </div>
                </v-card-text>
                <v-card-actions>
                  <v-btn variant="text" @click="$router.push('/rooms/' + room.id)">подробнее</v-btn>
                  <v-btn color="primary" @click="$router.push('/rooms/' + room.id + '/book')">
                    забронировать
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { apiGetRooms, apiGetAvailableRooms } from '../api'

// страница со списком номеров
const rooms = ref([])
const availableRooms = ref([])
const loading = ref(false)
const error = ref('')

const filters = reactive({
  room_type: null,
  floor: null
})

const roomTypeItems = [
  { title: 'одноместный', value: 'single' },
  { title: 'двухместный', value: 'tuple' },
  { title: 'трехместный', value: 'triple' }
]

// подпись типа номера для отображения на сайте
const roomTypeLabel = (value) => {
  const item = roomTypeItems.find((i) => i.value === value)
  return item ? item.title : value
}

const loadRooms = async () => {
  loading.value = true
  error.value = ''
  try {
    const params = {}
    if (filters.room_type) params.room_type = filters.room_type
    if (filters.floor) params.floor = filters.floor

    const [roomsResp] = await Promise.all([
      apiGetRooms(params)
    ])
    rooms.value = roomsResp.data
  } catch (e) {
    error.value = 'не удалось загрузить список номеров'
  } finally {
    loading.value = false
  }
}

const loadAvailableRooms = async () => {
  try {
    const resp = await apiGetAvailableRooms()
    availableRooms.value = resp.data
  } catch (e) {
    // если не получилось, просто оставим список пустым
  }
}

const resetFilters = () => {
  filters.room_type = null
  filters.floor = null
  loadRooms()
}

const isRoomAvailable = (roomId) => {
  return availableRooms.value.some((r) => r.id === roomId)
}

onMounted(async () => {
  await loadRooms()
  await loadAvailableRooms()
})
</script>

