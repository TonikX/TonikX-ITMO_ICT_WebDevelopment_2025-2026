<template>
  <v-container>
    <!-- Карточка с фабричным средним -->
    <v-card class="mb-4">
      <v-card-text>
        <div class="d-flex align-center">
          <v-icon color="info" class="mr-3" size="large">mdi-factory</v-icon>
          <div>
            <div class="text-caption text-medium-emphasis">Фабричное среднее яйценоскости</div>
            <div class="text-h4">{{ factoryAvg }} <span class="text-h6 text-medium-emphasis">яиц/день</span></div>
          </div>
        </div>
      </v-card-text>
    </v-card>

    <!-- Карточка с таблицей пород -->
    <v-card>
      <v-card-title>Сравнение пород с фабричным показателем</v-card-title>
      <v-card-text>
        <v-table density="compact">
          <thead>
            <tr>
              <th>Порода</th>
              <th>Яйценоскость (мес)</th>
              <th>Яйценоскость (день)</th>
              <th>Отклонение от фабрики</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in items" :key="item.breed_name">
              <td>
                {{ item.breed_name }}
              </td>
              <td>{{ item.breed_efficiency }}</td>
              <td>{{ item.daily_efficiency }}</td>
              <td>
                <v-chip
                  :color="item.difference >= 0 ? 'success' : 'error'"
                  :prepend-icon="item.difference >= 0 ? 'mdi-arrow-up' : 'mdi-arrow-down'"
                  variant="tonal"
                >
                  {{ item.difference > 0 ? '+' : '' }}{{ item.difference }}
                </v-chip>
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getBreedEfficiencyDiff } from '@/api/reports'

const items = ref([])
const factoryAvg = ref(0)

onMounted(async () => {
  const data = await getBreedEfficiencyDiff()
  
  if (data.length > 0) {
    factoryAvg.value = data[0].factory_avg
    
    items.value = data.map(item => ({
      breed_name: item.breed_name,
      breed_code: item.breed_name.substring(0, 3).toUpperCase(),
      breed_efficiency: item.breed_efficiency,
      daily_efficiency: (item.breed_efficiency / 30).toFixed(1),
      difference: (item.breed_efficiency / 30 - item.factory_avg).toFixed(1)
    }))
  }
})
</script>