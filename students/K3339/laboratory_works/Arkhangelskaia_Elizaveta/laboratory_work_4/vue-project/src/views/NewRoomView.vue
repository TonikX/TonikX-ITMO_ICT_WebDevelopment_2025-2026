<template>
  <v-container>
    <v-card>
      <v-card-title>Добавить номер</v-card-title>

      <v-card-text>
        <v-select
          v-model="room.id_room_type"
          :items="roomTypes"
          item-title="label"
          item-value="id"
          label="Тип номера"
          outlined
          dense
        ></v-select>

        <v-text-field
          v-model="room.room_number"
          label="Номер комнаты"
          type="number"
          outlined
          dense
        ></v-text-field>

        <v-text-field
          v-model="room.phone_number"
          label="Телефон"
          outlined
          dense
        ></v-text-field>

        <v-text-field
          v-model="room.floor"
          label="Этаж"
          type="number"
          outlined
          dense
        ></v-text-field>

        <v-btn color="green lighten-2" class="mt-3 mr-2" @click="addRoom">
          Добавить
        </v-btn>

        <v-btn color="grey lighten-1" class="mt-3" @click="cancel">
          Отмена
        </v-btn>

        <v-alert
          v-if="success"
          type="success"
          dense
          class="mt-3"
          color="green lighten-2"
        >
          {{ success }}
        </v-alert>

        <v-alert
          v-if="error"
          type="error"
          dense
          class="mt-3"
        >
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

const room = ref({
  id_room_type: null,
  room_number: '',
  phone_number: '',
  floor: ''
})

const roomTypes = ref([])
const success = ref('')
const error = ref('')

const loadRoomTypes = async () => {
  try {
    const res = await api.get('room_types/')
    roomTypes.value = res.data.map(rt => ({
      id: rt.id,
      label: `${rt.room_type}-местный`
    }))
  } catch (e) {
    console.error('Ошибка загрузки типов номеров', e)
  }
}

const addRoom = async () => {
  success.value = ''
  error.value = ''

  if (!room.value.id_room_type || !room.value.room_number || !room.value.phone_number || !room.value.floor) {
    error.value = 'Заполните все поля'
    return
  }

  try {
    await api.post('rooms/', room.value)
    success.value = 'Номер успешно добавлен!'
    setTimeout(() => {
      router.push('/rooms')
    }, 1500)
  } catch (e) {
    console.error(e)
    error.value = 'Ошибка при добавлении номера'
  }
}

const cancel = () => {
  router.push('/rooms')
}

onMounted(() => {
  loadRoomTypes()
})
</script>
