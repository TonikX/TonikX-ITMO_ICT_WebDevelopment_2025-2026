<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-4">Управление рейсами</h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>Фильтр рейсов</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-slider
                  v-model="occupancyThreshold"
                  label="Заполненность менее (%)"
                  min="0"
                  max="100"
                  step="5"
                  thumb-label
                  @update:model-value="loadFlights"
                ></v-slider>
              </v-col>
              <v-col cols="12" md="6" class="d-flex align-center">
                <v-btn color="primary" @click="loadFlights" :loading="loading">
                  <v-icon left>mdi-filter</v-icon>
                  Применить фильтр
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title>Список рейсов</v-card-title>
          <v-card-text>
            <v-table v-if="flights.length > 0">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Откуда</th>
                  <th>Куда</th>
                  <th>Вылет</th>
                  <th>Прилет</th>
                  <th>Статус</th>
                  <th>Действия</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="flight in flights" :key="flight.id">
                  <td>{{ flight.id }}</td>
                  <td>{{ flight.departure_airport }}</td>
                  <td>{{ flight.destination_airport }}</td>
                  <td>{{ formatDateTime(flight.departure_time) }}</td>
                  <td>{{ formatDateTime(flight.arrival_time) }}</td>
                  <td>
                    <v-chip :color="getStatusColor(flight.status)" size="small">
                      {{ flight.status }}
                    </v-chip>
                  </td>
                  <td>
                    <v-btn 
                      size="small" 
                      color="primary" 
                      :to="`/flights/${flight.id}`"
                    >
                      Подробнее
                    </v-btn>
                  </td>
                </tr>
              </tbody>
            </v-table>
            
            <div v-else-if="loading" class="text-center py-4">
              <v-progress-circular indeterminate color="primary"></v-progress-circular>
            </div>
            
            <v-alert v-else type="info">
              Рейсы не найдены
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { dataAPI } from '@/services/api'

const flights = ref([])
const occupancyThreshold = ref(50)
const loading = ref(true)

const formatDateTime = (dateString) => {
  if (!dateString) return 'Н/Д'
  return new Date(dateString).toLocaleString('ru-RU')
}

const getStatusColor = (status) => {
  const colors = {
    'scheduled': 'info',
    'boarding': 'warning',
    'departed': 'success',
    'arrived': 'success',
    'cancelled': 'error',
    'delayed': 'warning'
  }
  return colors[status] || 'default'
}

const loadFlights = async () => {
  loading.value = true
  try {
    const response = await dataAPI.getFlightsWithLowOccupancy(occupancyThreshold.value / 100)
    flights.value = response.data.flights
  } catch (error) {
    console.error('Error loading flights:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadFlights()
})
</script>