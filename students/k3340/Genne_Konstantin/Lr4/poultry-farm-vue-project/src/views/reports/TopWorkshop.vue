<template>
  <v-container>
    <v-card>
      <v-card-title>Цех с наибольшим количеством кур породы</v-card-title>
      <v-card-text>
        <v-select
          v-model="selectedBreed"
          :items="breedOptions"
          label="Выберите породу"
          @update:model-value="loadData"
        />
        <v-table v-if="items.length" class="mt-4">
          <thead>
            <tr>
              <th>Номер цеха</th>
              <th>Количество кур</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in items" :key="item.workshop_number">
              <td>{{ item.workshop_number }}</td>
              <td>{{ item.breed_count }}</td>
            </tr>
          </tbody>
        </v-table>
        <v-alert v-else type="info" class="mt-4">Выберите породу</v-alert>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getTopWorkshop } from '@/api/reports'
import { getBreeds } from '@/api/breeds'

const items = ref([])
const selectedBreed = ref(null)
const breedOptions = ref([])

const loadData = async () => {
  if (!selectedBreed.value) return
  items.value = await getTopWorkshop(selectedBreed.value)
}

onMounted(async () => {
  const breeds = await getBreeds()
  breedOptions.value = breeds.map(b => b.name)
})
</script>