<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-4">Управление флотом</h1>
      </v-col>
    </v-row>

    <!-- Статистика по маркам -->
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <v-icon left>mdi-chart-bar</v-icon>
            Статистика по маркам самолетов
          </v-card-title>
          <v-card-text>
            <v-alert v-if="topMark" type="info" class="mb-4">
              Самая популярная марка: <strong>{{ topMark }}</strong>
            </v-alert>
            
            <v-table v-if="marks.length > 0">
              <thead>
                <tr>
                  <th>Марка</th>
                  <th>Количество самолетов</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="mark in marks" :key="mark.mark" 
                    :class="{ 'bg-success': mark.mark === topMark }">
                  <td>{{ mark.mark }}</td>
                  <td>{{ mark.count_boards }}</td>
                </tr>
              </tbody>
            </v-table>
            
            <div v-else class="text-center py-4">
              <v-progress-circular indeterminate color="primary"></v-progress-circular>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Самолеты в ремонте -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <v-icon left>mdi-wrench</v-icon>
            Самолеты в ремонте
          </v-card-title>
          <v-card-text>
            <v-table v-if="planesInRepair.length > 0">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Марка</th>
                  <th>Компания</th>
                  <th>Статус</th>
                  <th>Длительность полета (ч)</th>
                  <th>Последнее ТО</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="plane in planesInRepair" :key="plane.id">
                  <td>{{ plane.id }}</td>
                  <td>{{ plane.mark }}</td>
                  <td>{{ plane.company }}</td>
                  <td>
                    <v-chip color="warning" size="small">{{ plane.status }}</v-chip>
                  </td>
                  <td>{{ plane.flight_duration }}</td>
                  <td>{{ formatDate(plane.last_technical_service) }}</td>
                </tr>
              </tbody>
            </v-table>
            
            <div v-else-if="loading" class="text-center py-4">
              <v-progress-circular indeterminate color="primary"></v-progress-circular>
            </div>
            
            <v-alert v-else type="info">
              Нет самолетов в ремонте
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

const marks = ref([])
const topMark = ref('')
const planesInRepair = ref([])
const loading = ref(true)

const formatDate = (dateString) => {
  if (!dateString) return 'Н/Д'
  return new Date(dateString).toLocaleDateString('ru-RU')
}

onMounted(async () => {
  try {
    const [marksRes, topMarkRes, planesRes] = await Promise.all([
      dataAPI.getAllMarks(),
      dataAPI.getTopMark(),
      dataAPI.getPlanesInRepair()
    ])

    marks.value = marksRes.data.marks
    topMark.value = topMarkRes.data.top_mark
    planesInRepair.value = planesRes.data.planes
  } catch (error) {
    console.error('Error loading fleet data:', error)
  } finally {
    loading.value = false
  }
})
</script>