<template>
  <v-container>
    <v-card>
      <v-card-title class="d-flex justify-space-between align-center">
        <span>Список номеров</span>
        <v-btn color="success" @click="createRoom">Добавить новый</v-btn>
      </v-card-title>

        <v-data-table
          :headers="headers"
          :items="rooms"
          item-key="id"
        >
        <template #item.room_type="{ item }">
          {{ roomTypes[item.id_room_type] }}
        </template>

        <template #item.actions="{ item }">
          <v-btn color="primary" size="small" class="mr-2" @click="editRoom(item.id)">
            Редактировать
          </v-btn>
          <v-btn color="error" size="small" class="mr-2" @click="deleteRoom(item.id)">
            Удалить
          </v-btn>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'

const router = useRouter()
const rooms = ref([])
const roomTypes = ref({})

const headers = [
  { title: 'Номер комнаты', key: 'room_number' },
  { title: 'Тип номера', key: 'room_type' },
  { title: 'Телефон', key: 'phone_number' },
  { title: 'Этаж', key: 'floor' },
  { title: '', key: 'actions', sortable: false }
]

const loadRooms = async () => {
  try {
    const res = await api.get('rooms/')
    rooms.value = res.data
  } catch (e) {
    console.error('Ошибка загрузки комнат', e)
  }
}

const loadRoomTypes = async () => {
  const res = await api.get('room_types/')
  res.data.forEach(rt => {
    roomTypes.value[rt.id] = `${rt.room_type}-местный`
  })
}

onMounted(async () => {
  try {
    await Promise.all([
      loadRoomTypes(),
      loadRooms()
    ])
  } catch (e) {
    console.error('Ошибка загрузки данных', e)
  }
})

const createRoom = () => {
  router.push('/rooms/new')
}

const editRoom = (id) => {
  router.push(`/rooms/${id}/edit`)
}

const deleteRoom = async (id) => {
  const confirmDelete = confirm('Вы точно хотите удалить этот номер?')
  if (!confirmDelete) return

  try {
    await api.delete(`rooms/${id}/`)
    alert('Номер успешно удалён')
    loadRooms()
  } catch (e) {
    console.error(e)
    alert('Ошибка при удалении номера')
  }
}
</script>
