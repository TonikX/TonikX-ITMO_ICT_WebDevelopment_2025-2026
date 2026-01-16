<template>
  <v-container>
    <v-card>
      <v-card-title>Свободные номера</v-card-title>

      <v-card-text>
        <!-- Даты -->
        <v-row dense>
          <v-col cols="12" md="6">
            <v-menu v-model="startMenu" :close-on-content-click="false">
              <template #activator="{ props }">
                <v-text-field
                  v-model="startDate"
                  label="Дата заезда"
                  readonly
                  v-bind="props"
                  outlined
                  dense
                />
              </template>
              <v-date-picker
                v-model="startPicker"
                @update:model-value="setStart"
              />
            </v-menu>
          </v-col>

          <v-col cols="12" md="6">
            <v-menu v-model="endMenu" :close-on-content-click="false">
              <template #activator="{ props }">
                <v-text-field
                  v-model="endDate"
                  label="Дата выезда"
                  readonly
                  v-bind="props"
                  outlined
                  dense
                />
              </template>
              <v-date-picker
                v-model="endPicker"
                @update:model-value="setEnd"
              />
            </v-menu>
          </v-col>
        </v-row>

        <v-btn color="primary" class="mt-3" @click="loadRooms">
          Показать
        </v-btn>

        <div v-if="error" class="mt-2" style="color:red">
          {{ error }}
        </div>

        <!-- РЕЗУЛЬТАТ -->
        <v-row v-if="rooms.length" class="mt-4" dense>
          <v-col
            v-for="room in rooms"
            :key="room.room_number"
            cols="12"
            md="4"
          >
            <v-card variant="outlined">
              <v-card-title>
                Номер {{ room.room_number }}
              </v-card-title>

              <v-card-text>
                <div>Этаж: {{ room.floor }}</div>
                <div>Телефон: {{ room.phone_number }}</div>
                <div>Гостей: {{ room.guests }}</div>
                <div><b>Цена: {{ room.price }} ₽</b></div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-container>
</template>
<script setup>
import { ref } from 'vue'
import api from '@/api'

const startDate = ref('')
const endDate = ref('')
const startPicker = ref(null)
const endPicker = ref(null)
const startMenu = ref(false)
const endMenu = ref(false)

const rooms = ref([])
const error = ref('')

// формат YYYY-MM-DD
const formatDate = (date) => {
  const d = new Date(date)
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
}

const setStart = (val) => {
  startDate.value = formatDate(val)
  startPicker.value = val
  startMenu.value = false
}

const setEnd = (val) => {
  endDate.value = formatDate(val)
  endPicker.value = val
  endMenu.value = false
}

const loadRooms = async () => {
  error.value = ''
  rooms.value = []

  if (!startDate.value || !endDate.value) {
    error.value = 'Выберите даты'
    return
  }

  try {
    const res = await api.get(
      `req/available_rooms/?start_date=${startDate.value}&end_date=${endDate.value}`
    )

    // подгружаем типы номеров
    const result = []

    for (const room of res.data) {
      const typeRes = await api.get(`room_types/${room.id_room_type}/`)

      result.push({
        room_number: room.room_number,
        phone_number: room.phone_number,
        floor: room.floor,
        guests: typeRes.data.room_type,
        price: typeRes.data.price
      })
    }

    rooms.value = result
  } catch (e) {
    console.error(e)
    error.value = 'Ошибка загрузки номеров'
  }
}
</script>
