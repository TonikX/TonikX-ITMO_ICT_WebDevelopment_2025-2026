<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-btn color="primary" @click="$router.back()" class="mb-4">
          <v-icon left>mdi-arrow-left</v-icon>
          Назад к списку рейсов
        </v-btn>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <v-icon left>mdi-airplane</v-icon>
            Рейс #{{ flightId }}
          </v-card-title>
          <v-card-text>
            <h3 class="text-h6 mb-4">Доступные места</h3>
            
            <div v-if="loading" class="text-center py-4">
              <v-progress-circular indeterminate color="primary"></v-progress-circular>
            </div>
            
            <div v-else-if="availableSeats.length > 0">
              <v-alert type="success" class="mb-4">
                Доступно мест: {{ availableSeats.length }}
              </v-alert>
              
              <div class="seat-grid">
                <v-chip
                  v-for="seat in availableSeats"
                  :key="seat"
                  color="success"
                  class="ma-1"
                >
                  Место {{ seat }}
                </v-chip>
              </div>
            </div>
            
            <v-alert v-else type="warning">
              Нет доступных мест на этом рейсе
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { dataAPI } from '@/services/api'

const route = useRoute()
const flightId = ref(route.params.id)
const availableSeats = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await dataAPI.getAvailableSeats(flightId.value)
    availableSeats.value = response.data.available_seats
  } catch (error) {
    console.error('Error loading flight details:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.seat-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
</style>