<template>
  <v-container>
    <v-card>
      <v-card-title>Добавить уборку</v-card-title>

      <v-card-text>
        <v-menu
          v-model="dateMenu"
          :close-on-content-click="false"
          transition="scale-transition"
          offset-y
          min-width="auto"
        >
          <template #activator="{ props }">
            <v-text-field
              v-model="date"
              label="Дата уборки"
              readonly
              v-bind="props"
              outlined
              dense
            ></v-text-field>
          </template>

          <v-date-picker
            v-model="selectedDate"
            locale="ru"
            no-title
            @update:model-value="onDateSelect"
          ></v-date-picker>
        </v-menu>
        <v-text-field
          v-model="time"
          label="Время уборки"
          placeholder="00:00"
          outlined
          dense
        />
        <v-select
          v-model="worker"
          :items="workers"
          item-title="full_name"
          item-value="id"
          label="Уборщик"
          outlined
          dense
        />
        <v-select
          v-model="room"
          :items="rooms"
          item-title="room_number"
          item-value="id"
          label="Номер"
          outlined
          dense
        />
        <v-btn color="green lighten-2" class="mt-3 mr-2" @click="createCleaning">
          Сохранить
        </v-btn>
        <v-btn color="grey lighten-1" class="mt-3" @click="goBack">
          Отмена
        </v-btn>

        <v-alert v-if="error" type="error" class="mt-3" dense>
          {{ error }}
        </v-alert>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'

const router = useRouter()
const error = ref('')
const dateMenu = ref(false)
const selectedDate = ref(null)
const date = ref('') // YYYY-MM-DD
const time = ref('')
const worker = ref(null)
const room = ref(null)
const workers = ref([])
const rooms = ref([])

const formatDate = (val) => {
  const d = new Date(val)
  const yyyy = d.getFullYear()
  const mm = String(d.getMonth() + 1).padStart(2, '0')
  const dd = String(d.getDate()).padStart(2, '0')
  return `${yyyy}-${mm}-${dd}`
}

const onDateSelect = (val) => {
  selectedDate.value = val
  date.value = formatDate(val)
  dateMenu.value = false
}

const loadWorkers = async () => {
  try {
    const res = await api.get('workers/')
    workers.value = res.data.map(w => ({
      ...w,
      full_name: `${w.surname} ${w.name} ${w.patronymic}`
    }))
  } catch (e) {
    console.error('Ошибка загрузки работников', e)
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

const createCleaning = async () => {
  error.value = ''

  if (!date.value || !time.value || !worker.value || !room.value) {
    error.value = 'Заполните все поля'
    return
  }

  const [hours, minutes] = time.value.split(':')
  const localDate = new Date(date.value)
  localDate.setHours(parseInt(hours))
  localDate.setMinutes(parseInt(minutes))
  const isoDate = localDate.toISOString()

  try {
    await api.post('cleaning/', {
      cleaning_date: isoDate,
      worker: worker.value,
      room: room.value
    })
    router.push('/cleaning')
  } catch (e) {
    console.error('Ошибка при создании уборки', e.response?.data || e)
    error.value = 'Ошибка при создании уборки'
  }
}

const goBack = () => {
  router.push('/cleaning')
}

onMounted(() => {
  loadWorkers()
  loadRooms()
})
</script>
