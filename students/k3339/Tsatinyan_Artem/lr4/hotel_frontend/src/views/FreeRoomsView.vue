<template>
  <div>
    <h1>Свободные номера</h1>

    <v-form @submit.prevent="onSubmit" style="max-width: 300px;">
      <v-text-field
        v-model="date"
        label="Дата (YYYY-MM-DD)"
        placeholder="2025-01-01"
      />
      <v-btn type="submit" color="primary" class="mt-2">
        Показать свободные номера
      </v-btn>
    </v-form>

    <v-alert v-if="error" type="error" class="mt-4">
      {{ error }}
    </v-alert>

    <div v-if="result">
      <h2 class="mt-4">Дата: {{ result.date }}</h2>
      <v-row class="mt-2">
        <v-col
          v-for="room in result.free_rooms"
          :key="room.id"
          cols="12" md="4"
        >
          <v-card>
            <v-card-title>Номер {{ room.number }}</v-card-title>
            <v-card-subtitle>Этаж {{ room.floor }}</v-card-subtitle>
            <v-card-text>
              Тип: {{ room.room_type }}<br>
              Цена: {{ room.daily_price }} ₽
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api/api'

const date = ref('')
const result = ref(null)
const error = ref('')

const onSubmit = async () => {
  error.value = ''
  result.value = null
  try {
    const params = {}
    if (date.value) params.date = date.value
    const { data } = await api.get('/api/reports/free-rooms/', { params })
    result.value = data
  } catch (e) {
    error.value = 'Не удалось получить список свободных номеров'
  }
}
</script>
