<template>
  <v-container>
    <div class="d-flex flex-wrap justify-space-between align-center mb-6 gap-2">
      <h1 class="text-h4 font-weight-bold">Номера</h1>
      <div class="d-flex align-center" style="gap: 12px">
        <v-text-field
          v-model="search"
          density="compact"
          variant="outlined"
          label="Поиск номера"
          prepend-inner-icon="mdi-magnify"
          hide-details
          style="min-width: 200px"
        />
        <v-btn color="primary" height="40" prepend-icon="mdi-plus" @click="showAddDialog = true">
          Добавить
        </v-btn>
      </div>
    </div>

    <v-row>
      <v-col
        v-for="room in filteredRooms"
        :key="room.id"
        cols="12" md="4" sm="6"
      >
        <v-card
          hover
          elevation="2"
          rounded="lg"
          class="h-100 d-flex flex-column transition-swing"
          @click="$router.push(`/rooms/${room.id}`)"
        >
          <div class="pa-4 d-flex justify-space-between align-start">
            <div>
              <div class="text-overline text-grey-darken-1 mb-1">
                {{ getRoomTypeLabel(room.room_type) }}
              </div>
              <div class="text-h4 font-weight-bold text-primary">№ {{ room.number }}</div>
            </div>
            <v-chip size="small" variant="tonal" color="secondary">
              {{ room.floor }} этаж
            </v-chip>
          </div>

          <v-divider></v-divider>

          <v-card-text class="flex-grow-1 py-4">
            <div class="d-flex align-center mb-2">
              <v-icon color="grey" size="small" class="mr-2">mdi-phone</v-icon>
              <span class="text-body-2">{{ room.phone_number }}</span>
            </div>
            <div class="d-flex align-baseline mt-4">
              <span class="text-h5 font-weight-bold mr-1">{{ room.daily_price }}</span>
              <span class="text-body-2 text-grey">₽ / сутки</span>
            </div>
          </v-card-text>

          <v-card-actions class="bg-grey-lighten-5 pa-3">
            <v-spacer></v-spacer>
            <v-btn
              icon="mdi-trash-can-outline"
              color="grey"
              variant="text"
              size="small"
              v-tooltip="'Удалить номер'"
              @click.stop="deleteRoom(room)"
            ></v-btn>
            <v-icon color="primary" class="ml-2">mdi-arrow-right</v-icon>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="showAddDialog" max-width="500">
      <v-card rounded="lg">
        <v-card-title class="bg-primary text-white py-3">Новый номер</v-card-title>
        <v-card-text class="pt-4">
          <v-form @submit.prevent="createRoom">
            <v-text-field v-model="newRoom.number" label="Номер (напр. 101)" variant="outlined" required />
            <v-select
              v-model="newRoom.room_type"
              label="Тип"
              :items="roomTypes"
              variant="outlined"
              required
            />
            <v-row>
              <v-col cols="6">
                <v-text-field v-model="newRoom.floor" label="Этаж" type="number" variant="outlined" required />
              </v-col>
              <v-col cols="6">
                <v-text-field v-model="newRoom.daily_price" label="Цена (₽)" type="number" step="0.01" variant="outlined" required />
              </v-col>
            </v-row>
            <v-text-field v-model="newRoom.phone_number" label="Телефон" variant="outlined" required />

            <v-btn type="submit" color="primary" block size="large" :loading="creating" class="mt-2">Создать</v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import api from '../api/api'

const rooms = ref([])
const search = ref('')
const showAddDialog = ref(false)
const creating = ref(false)

const newRoom = reactive({
  number: '', floor: '', room_type: 'single', daily_price: '', phone_number: ''
})

const roomTypes = [
  {title:'Одноместный', value:'single'},
  {title:'Двухместный', value:'double'},
  {title:'Трехместный', value:'triple'}
]

const loadRooms = async () => {
  const { data } = await api.get('/api/rooms/')
  rooms.value = data
}

const filteredRooms = computed(() => {
  if (!search.value) return rooms.value
  const s = search.value.toLowerCase()
  return rooms.value.filter(r => r.number.toLowerCase().includes(s))
})

const createRoom = async () => {
  creating.value = true
  try {
    await api.post('/api/rooms/', newRoom)
    showAddDialog.value = false
    Object.assign(newRoom, { number: '', floor: '', daily_price: '', phone_number: '' })
    loadRooms()
  } catch (e) {
    alert('Ошибка создания (возможно номер уже занят)')
  } finally {
    creating.value = false
  }
}

const deleteRoom = async (room) => {
  if (!confirm(`Удалить номер ${room.number}?`)) return
  try {
    await api.delete(`/api/rooms/${room.id}/`)
    loadRooms()
  } catch (e) {
    alert('Не удалось удалить. Возможно, есть активные брони.')
  }
}

const getRoomTypeLabel = (val) => roomTypes.find(t => t.value === val)?.title || val

onMounted(loadRooms)
</script>

<style scoped>
.gap-2 { gap: 8px; }
</style>
