<template>
  <v-container>
    <v-card>
      <v-card-title>Распределение пород по цехам</v-card-title>
      <v-table>
        <thead>
          <tr>
            <th>Цех / Порода</th>
            <th>Количество</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in items" :key="index">
            <td>Цех {{ item.workshop_number }} — {{ item.breed_name }}</td>
            <td>{{ item.count }} кур</td>
          </tr>
        </tbody>
      </v-table>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getBreedDistribution } from '@/api/reports'

const items = ref([])

onMounted(async () => {
  const data = await getBreedDistribution()
  items.value = data
})
</script>