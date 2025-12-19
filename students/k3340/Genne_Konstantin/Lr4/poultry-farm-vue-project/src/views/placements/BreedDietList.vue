<template>
  <v-container>
    <v-card>
      <v-card-title>Диеты пород по сезонам</v-card-title>
      <v-card-actions>
        <v-btn color="primary" to="/breed-diets/new">Назначить диету</v-btn>
        <v-select
          v-model="filters.breed_id"
          :items="breedOptions"
          item-title="name"
          item-value="id"
          label="Фильтр по породе"
          clearable
          hide-details
          style="max-width: 300px"
        />
      </v-card-actions>

      <v-table class="mt-4">
        <thead>
          <tr>
            <th>Порода</th>
            <th>Диета</th>
            <th>Сезон</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>{{ item.breed_name }}</td>
            <td>Диета №{{ item.diet_number }}</td>
            <td>{{ seasonLabels[item.season] ? seasonLabels[item.season] : item.season }}</td>
            <td>
              <v-btn size="small" color="error" @click="deleteItem(item.id)">Удалить</v-btn>
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { getBreeds } from '@/api/breeds'
import { getBreedDiets, deleteBreedDiet } from '@/api/breedDiets'

const items = ref([])
const filters = ref({ breed_id: null })
const breedOptions = ref([])

const seasonLabels = {
  winter: 'Зима',
  spring: 'Весна',
  summer: 'Лето',
  autumn: 'Осень'
}

const loadData = async () => {
  const params = {}
  if (filters.value.breed_id) params.breed_id = filters.value.breed_id
  items.value = await getBreedDiets(params)
}

onMounted(async () => {
  breedOptions.value = await getBreeds()
  await loadData()
})

watch(() => filters.value.breed_id, loadData)

const deleteItem = async (id) => {
  if (confirm('Удалить назначение диеты?')) {
    try {
      await deleteBreedDiet(id)
      items.value = items.value.filter(i => i.id !== id)
    } catch (err) {
      const msg = err.response?.data?.error || 'Ошибка удаления'
      alert(msg)
    }
  }
}
</script>