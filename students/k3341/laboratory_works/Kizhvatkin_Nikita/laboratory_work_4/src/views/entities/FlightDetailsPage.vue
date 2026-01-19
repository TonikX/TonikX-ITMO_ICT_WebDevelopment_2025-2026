<template>
  <v-card>
    <v-card-title class="d-flex align-center">
      <div class="text-h6">Рейс #{{ id }}</div>
      <v-spacer />
      <v-btn variant="tonal" prepend-icon="mdi-refresh" @click="load" :loading="loading">Обновить</v-btn>
      <v-btn class="ml-2" color="primary" prepend-icon="mdi-seat" @click="fetchAvailableSeats" :loading="seatsLoading">
        Свободные места
      </v-btn>
    </v-card-title>

    <v-card-text>
      <v-alert v-if="error" type="error" variant="tonal" class="mb-4">{{ error }}</v-alert>

      <div v-if="flight" class="d-flex flex-wrap" style="gap: 12px">
        <v-chip>Номер: {{ flight.flight_number }}</v-chip>
        <v-chip>Маршрут: {{ flight.departure_airport_code }} → {{ flight.arrival_airport_code }}</v-chip>
        <v-chip>Самолёт: {{ flight.aircraft_tail_number }} ({{ flight.aircraft_type }})</v-chip>
        <v-chip>Компания: {{ flight.company_name }}</v-chip>
        <v-chip>Продано: {{ flight.tickets_sold }} / {{ flight.aircraft_capacity }}</v-chip>
      </div>

      <v-divider class="my-4" />

      <v-row>
        <v-col cols="12" md="6">
          <v-card variant="outlined">
            <v-card-title class="text-subtitle-1">Экипаж</v-card-title>
            <v-card-text>
              <div v-if="!flight?.crew_members?.length" class="text-medium-emphasis">
                Экипаж не назначен.
              </div>
              <v-list v-else density="compact">
                <v-list-item v-for="m in flight.crew_members" :key="m.id">
                  <v-list-item-title>
                    {{ m.last_name }} {{ m.first_name }}
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    {{ m.position_display }} • возраст {{ m.age }} • стаж {{ m.experience }}
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="6">
          <v-card variant="outlined">
            <v-card-title class="text-subtitle-1">Транзитные остановки</v-card-title>
            <v-card-text>
              <div v-if="!flight?.transit_stops?.length" class="text-medium-emphasis">
                Нет транзитных остановок.
              </div>
              <v-list v-else density="compact">
                <v-list-item v-for="t in flight.transit_stops" :key="t.id">
                  <v-list-item-title>
                    {{ t.airport_code }} — {{ t.airport_name }}
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    Прибытие: {{ t.arrival_datetime }} • Вылет: {{ t.departure_datetime }}
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-divider class="my-4" />

      <v-alert v-if="seats" type="info" variant="tonal">
        Свободных мест: <b>{{ seats.available_seats }}</b> • загрузка: <b>{{ seats.load_percentage }}%</b>
      </v-alert>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { http } from '../../api/http'
import { endpoints } from '../../api/endpoints'

const props = defineProps({ id: { type: [String, Number], required: true } })

const flight = ref(null)
const loading = ref(false)
const error = ref('')

const seats = ref(null)
const seatsLoading = ref(false)

async function load() {
  loading.value = true
  error.value = ''
  try {
    const res = await http.get(`${endpoints.flights}${props.id}/`)
    flight.value = res.data
  } catch (e) {
    error.value = 'Не удалось загрузить данные рейса'
  } finally {
    loading.value = false
  }
}

async function fetchAvailableSeats() {
  seatsLoading.value = true
  seats.value = null
  try {
    const res = await http.get(`${endpoints.flights}${props.id}/available_seats/`)
    seats.value = res.data
  } catch (e) {
    error.value = 'Не удалось получить свободные места'
  } finally {
    seatsLoading.value = false
  }
}

onMounted(load)
</script>
