<template>
  <v-container>
    <v-card>
      <v-card-title>Живые курицы</v-card-title>
      <v-card-actions>
        <v-btn to="/hens/new" color="primary">Добавить курицу</v-btn>
      </v-card-actions>
      <v-table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Порода</th>
            <th>Вес (г)</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="hen in hens" :key="hen.id">
            <td>{{ hen.id }}</td>
            <td>{{ hen.breed_name }}</td>
            <td>{{ hen.weight }}</td>
            <td>
              <v-btn size="small" :to="`/hens/${hen.id}`">Подробнее</v-btn>
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getHens } from '@/api/hens'

const hens = ref([])

onMounted(async () => {
  hens.value = await getHens()
})
</script>