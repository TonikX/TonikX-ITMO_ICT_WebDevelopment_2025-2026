<template>
  <v-row>
    <v-col cols="12" md="6" lg="4">
      <v-card>
        <v-card-title class="text-h6">номер {{ room?.number }}</v-card-title>
        <v-card-text>
          <v-alert v-if="error" type="error" density="compact" class="mb-2">
            {{ error }}
          </v-alert>
          <div v-if="!room && !error">загрузка...</div>
          <template v-else>
            <div>тип: {{ roomTypeLabel(room.room_type) }}</div>
            <div>этаж: {{ room.floor }}</div>
            <div>цена: {{ room.price }} ₽/сутки</div>
            <div>телефон: {{ room.phone || '-' }}</div>
          </template>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="$router.push($route.params.id + '/book')">
            забронировать
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { apiGetRoom } from '../api'

// страница с подробной информацией о номере
const route = useRoute()

const room = ref(null)
const error = ref('')

const roomTypeLabels = { single: 'одноместный', tuple: 'двухместный', triple: 'трехместный' }
const roomTypeLabel = (value) => roomTypeLabels[value] || value

const loadData = async () => {
  error.value = ''
  const id = route.params.id
  try {
    const roomResp = await apiGetRoom(id)
    room.value = roomResp.data
  } catch (e) {
    error.value = 'не удалось загрузить данные по номеру'
  }
}

onMounted(loadData)
</script>
