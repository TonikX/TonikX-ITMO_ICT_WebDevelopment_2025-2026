<template>
  <div>
    <h1>Список номеров</h1>

    <v-alert v-if="error" type="error" class="mb-4">{{ error }}</v-alert>

    <v-row>
      <v-col
        v-for="room in rooms"
        :key="room.id"
        cols="12" md="4"
      >
        <v-card>
          <v-card-title>
            Номер {{ room.number }}
          </v-card-title>
          <v-card-subtitle>
            Этаж: {{ room.floor }} · Тип: {{ room.room_type }}
          </v-card-subtitle>
          <v-card-text>
            Цена за сутки: {{ room.daily_price }} ₽<br>
            Телефон: {{ room.phone_number }}
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/api'

const rooms = ref([])
const error = ref('')

onMounted(async () => {
  try {
    const { data } = await api.get('/api/rooms/')
    rooms.value = data
  } catch (e) {
    error.value = 'Не удалось получить список номеров (проверьте авторизацию и CORS).'
  }
})
</script>
