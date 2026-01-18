<template>
  <v-container>
    <v-card>
      <v-card-title class="d-flex justify-space-between align-center">
        <span>Список бронирований</span>
        <v-btn color="success" @click="createReservation">Добавить новое бронирование</v-btn>
      </v-card-title>

      <v-data-table
        :headers="headers"
        :items="reservations"
        item-key="id"
      >
        <template #item.rooms="{ item }">
          {{ getRoomNumbers(item.rooms) }}
        </template>
        <template #item.actions="{ item }">
          <v-btn color="primary" size="small" class="mr-2" @click="goToReservation(item.id)">
            Подробнее
          </v-btn>
          <v-btn color="secondary" size="small" class="mr-2" @click="editReservation(item.id)">
            Редактировать
          </v-btn>
          <v-btn color="error" size="small" class="mr-2" @click="deleteReservation(item.id)">
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
const reservations = ref([])
const roomsMap = ref({})
const headers = [
  { title: 'Номера', key: 'rooms' },
  { title: 'Дата заезда', key: 'start_date' },
  { title: 'Дата выезда', key: 'end_date' },
  { title: '', key: 'actions', sortable: false }
]

onMounted(() => {
  loadReservations()
  loadRooms()
})

const loadReservations = async () => {
  try {
    const res = await api.get('reservations/')
    reservations.value = res.data
  } catch (e) {
    console.error('Ошибка загрузки бронирований', e)
  }
}

const loadRooms = async () => {
  const res = await api.get('rooms/')
  res.data.forEach(r => {
    roomsMap.value[r.id] = r.room_number
  })
}

const createReservation = () => {
  router.push('/reservations/new')
}

const goToReservation = (id) => {
  router.push(`/reservations/${id}`)
}

const editReservation = (id) => {
  router.push(`/reservations/${id}/edit`)
}

const deleteReservation = async (id) => {
  const confirmDelete = confirm('Вы точно хотите удалить это бронирование?')
  if (!confirmDelete) return

  try {
    await api.delete(`reservations/${id}/`)
    alert('Бронирование успешно удалено')
    loadReservations()
  } catch (e) {
    console.error(e)
    alert('Ошибка при удалении бронирования')
  }
}

const getRoomNumbers = (ids) => {
  return ids
    .map(id => roomsMap.value[id])
    .filter(Boolean)
    .join(', ')
}

</script>
