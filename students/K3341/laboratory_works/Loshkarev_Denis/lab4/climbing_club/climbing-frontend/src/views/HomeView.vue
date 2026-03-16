<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h3 mb-4">Наши Скалодромы</h1>
      </v-col>
    </v-row>

    <!-- Показываем загрузку, пока ждем данные от Django -->
    <v-row v-if="loading">
      <v-col class="text-center">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
      </v-col>
    </v-row>

    <!-- Выводим список залов (когда они загрузятся) -->
    <v-row v-else>
      <v-col v-for="center in centers" :key="center.id" cols="12" sm="6" md="4">
        <v-card elevation="2">
          <v-card-title>{{ center.name }}</v-card-title>
          <v-card-subtitle>{{ center.location }}</v-card-subtitle>
          <v-card-text>
            <p><strong>Часы работы:</strong> {{ center.opening_hours }}</p>
            <p><strong>Контакт:</strong> {{ center.contact_info }}</p>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" variant="text">Подробнее</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api' 

const centers = ref([])
const loading = ref(true)

const fetchCenters = async () => {
  try {
    const response = await api.get('climbing/centers/')
    centers.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки скалодромов:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCenters()
})
</script>
