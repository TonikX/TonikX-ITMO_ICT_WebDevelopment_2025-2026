<template>
  <v-container>
    <v-card>
      <v-card-title>Яйценоскость по характеристикам</v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12" md="4">
            <v-combobox
              v-model="filters.breed"
              :items="breedOptions"
              label="Порода"
              multiple
              chips
              clearable
              hide-details
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
              v-model="filters.weight_category"
              :items="weightCategories"
              label="Категория веса"
              multiple
              chips
              clearable
              hide-details
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
              v-model="filters.age_category"
              :items="ageCategories"
              label="Категория возраста"
              multiple
              chips
              clearable
              hide-details
            />
          </v-col>
        </v-row>
        <v-btn class="mt-4" color="primary" @click="loadData">Применить фильтры</v-btn>
      </v-card-text>
      <v-table class="mt-4">
        <thead>
          <tr>
            <th>ID</th>
            <th>Порода</th>
            <th>Вес (г)</th>
            <th>Возраст (мес)</th>
            <th>Среднее яиц/день</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.hen_id">
            <td>{{ item.hen_id }}</td>
            <td>{{ item.breed_name }}</td>
            <td>{{ item.weight }}</td>
            <td>{{ item.age_months }}</td>
            <td>{{ item.avg_eggs }}</td>
          </tr>
        </tbody>
      </v-table>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {
  getEggsByCharacteristics
} from '@/api/reports'
import { getBreeds } from '@/api/breeds'

const items = ref([])
const filters = ref({
  breed: [],
  weight_category: [],
  age_category: []
})

const breedOptions = ref([])
const weightCategories = [
  { title: 'до 1.5 кг', value: 'до_1.5_кг' },
  { title: '1.5–2.0 кг', value: '1.5-2.0_кг' },
  { title: 'свыше 2.0 кг', value: 'свыше_2.0_кг' }
]
const ageCategories = [
  { title: 'до 6 месяцев', value: 'до_6_месяцев' },
  { title: '6–12 месяцев', value: '6-12_месяцев' },
  { title: 'старше года', value: 'старше_года' }
]

const loadData = async () => {
  const params = {}
  if (filters.value.breed.length) params.breed = filters.value.breed.join(',')
  if (filters.value.weight_category.length) params.weight_category = filters.value.weight_category.join(',')
  if (filters.value.age_category.length) params.age_category = filters.value.age_category.join(',')
  items.value = await getEggsByCharacteristics(params)
}

onMounted(async () => {
  const breeds = await getBreeds()
  breedOptions.value = breeds.map(b => b.name)
  await loadData()
})
</script>