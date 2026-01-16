<template>
  <v-container>
    <v-card>
      <v-card-title>Бронирование #{{ reservation.id }}</v-card-title>

      <v-card-text>
        <p>
          <strong>Даты:</strong>
          {{ reservation.start_date }} — {{ reservation.end_date }}
        </p>

        <p>
          <strong>Номера: </strong>
          <span v-if="rooms.length">
            {{ rooms.join(', ') }}
          </span>
        </p>

        <p>
          <strong>Клиенты: </strong>
          <span v-if="residents.length">
            {{ residents.join(', ') }}
          </span>
        </p>
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

const reservation = ref({ rooms: [], residents: [] })
const rooms = ref([])
const residents = ref([])

onMounted(async () => {
  const id = route.params.id

  try {
    // 1️⃣ получаем бронирование
    const res = await api.get(`reservations/${id}/`)
    reservation.value = res.data

    // 2️⃣ подгружаем номера
    const roomRequests = reservation.value.rooms.map(roomId =>
      api.get(`rooms/${roomId}/`)
    )

    const roomResponses = await Promise.all(roomRequests)
    rooms.value = roomResponses.map(r => r.data.room_number)

    // 3️⃣ подгружаем клиентов
    const residentRequests = reservation.value.residents.map(residentId =>
      api.get(`residents/${residentId}/`)
    )

    const residentResponses = await Promise.all(residentRequests)
    residents.value = residentResponses.map(r =>
      `${r.data.surname} ${r.data.name} ${r.data.patronymic}`
    )

  } catch (e) {
    console.error('Ошибка загрузки бронирования', e)
    router.push('/reservations')
  }
})
</script>
