<template>
  <h1 class="mb-4">Fleet Report</h1>
  <v-row class="mb-4">
    <v-col cols="4">
      <v-card>
        <v-card-text>
          <div class="text-h6">Total Route Duration</div>
          <div class="text-h4">{{ totalLength }} min</div>
        </v-card-text>
      </v-card>
    </v-col>
    <v-col cols="4">
      <v-card>
        <v-card-text>
          <div class="text-h6">Drivers by Class</div>
          <div v-for="d in driversByClass" :key="d.driver_class">
            Class {{ d.driver_class }}: {{ d.count }}
          </div>
        </v-card-text>
      </v-card>
    </v-col>
    <v-col cols="4">
      <v-card>
        <v-card-text>
          <div class="text-h6">Route Times</div>
          <div v-for="r in routeTimes" :key="r.number" class="text-body-2">
            #{{ r.number }}: {{ r.start_time }} — {{ r.end_time }}
          </div>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
  <h2 class="mb-3">By Bus Type</h2>
  <v-expansion-panels>
    <v-expansion-panel v-for="(r, i) in report" :key="i" :title="r.bus_type">
      <v-expansion-panel-text>
        <p>Buses: {{ r.bus_count }} | Drivers: {{ r.driver_count }} | Total duration: {{ r.total_duration }} min</p>
        <p v-if="r.avg_experience">Avg experience: {{ r.avg_experience?.toFixed(1) }} years</p>
        <div v-for="(route, j) in r.routes" :key="j" class="mt-3">
          <v-chip color="primary" size="small" class="mr-2">Route {{ route.route.number }}</v-chip>
          {{ route.route.start_point }} → {{ route.route.end_point }}
          <div class="ml-4 text-body-2 mt-1" v-if="route.drivers.length">
            Drivers: {{ route.drivers.map(d => d.last_name + ' ' + d.first_name).join(', ') }}
          </div>
          <div class="ml-4 text-body-2" v-if="route.buses.length">
            Buses: {{ route.buses.map(b => b.reg_number).join(', ') }}
          </div>
        </div>
      </v-expansion-panel-text>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
const report = ref([])
const totalLength = ref(0)
const driversByClass = ref([])
const routeTimes = ref([])
onMounted(async () => {
  report.value = (await api.get('/api/fleet-report/')).data
  totalLength.value = (await api.get('/api/total-route-length/')).data.total_duration_minutes
  driversByClass.value = (await api.get('/api/drivers-by-class/')).data
  routeTimes.value = (await api.get('/api/route-times/')).data
})
</script>
