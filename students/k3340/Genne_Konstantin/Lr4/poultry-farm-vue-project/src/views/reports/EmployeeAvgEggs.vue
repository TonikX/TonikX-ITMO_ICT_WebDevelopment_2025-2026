<template>
  <v-container>
    <v-card>
      <v-card-title>Средняя яйценоскость на работника (яиц/день)</v-card-title>
      <v-table>
        <thead>
          <tr>
            <th>ID</th>
            <th>ФИО</th>
            <th>Яйценоскость (в среднем за день)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.employee_id">
            <td>{{ item.employee_id }}</td>
            <td>{{ item.employee_name }}</td>
            <td>{{ item.avg_eggs_per_day }}</td>
          </tr>
        </tbody>
      </v-table>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getEmployeeAvgEggs } from '@/api/reports'

const items = ref([])

onMounted(async () => {
  items.value = await getEmployeeAvgEggs()
})
</script>