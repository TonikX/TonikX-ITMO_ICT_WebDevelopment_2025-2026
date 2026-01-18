<template>
  <v-container>
    <v-card>
      <v-card-title>Редактировать номер</v-card-title>

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

        <v-btn color="green lighten-2" class="mt-3 mr-2" @click="updateRoom">
          Сохранить
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
import { useRoute, useRouter } from 'vue-router'
import api from '@/api'

const route = useRoute()
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

const loadRoom = async () => {
  try {
    const res = await api.get(`rooms/${route.params.id}/`)
    room.value = res.data
  } catch (e) {
    console.error('Ошибка загрузки комнаты', e)
    error.value = 'Ошибка загрузки данных комнаты'
  }
}

const updateRoom = async () => {
  success.value = ''
  error.value = ''
  try {
    if (!room.value.id_room_type) {
      error.value = 'Выберите тип номера'
      return
    }

    await api.patch(`rooms/${route.params.id}/`, room.value)
    success.value = 'Номер успешно обновлён'
    setTimeout(() => {
      router.push('/rooms')
    }, 1500)
  } catch (e) {
    console.error(e)
    error.value = 'Ошибка при обновлении номера'
  }
}

const cancel = () => {
  router.push('/rooms')
}

onMounted(async () => {
  try {
    await loadRoomTypes()
    await loadRoom()
  } catch (e) {
    console.error('Ошибка при загрузке данных', e)
  }
})
</script>
