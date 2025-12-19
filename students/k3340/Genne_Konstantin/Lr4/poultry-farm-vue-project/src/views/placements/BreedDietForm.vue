<template>
  <v-container>
    <v-card>
      <v-card-title>{{ isEdit ? 'Редактировать назначение диеты' : 'Назначить диету породе' }}</v-card-title>
      <v-card-text>
        <v-select
          v-model="form.breed"
          :items="breedOptions"
          item-title="name"
          item-value="id"
          label="Порода"
          :disabled="isEdit"
          required
        />
        <v-select
          v-model="form.diet"
          :items="dietOptions"
          item-title="label"
          item-value="id"
          label="Диета"
          :disabled="isEdit"
          required
        />
        <v-select
          v-model="form.season"
          :items="seasonOptions"
          item-title="label"
          item-value="value"
          label="Сезон"
          :disabled="isEdit"
          required
        />
      </v-card-text>
      <v-card-actions>
        <v-btn @click="save" color="primary">{{ isEdit ? 'Сохранить' : 'Назначить' }}</v-btn>
        <v-btn to="/breed-diets">Отмена</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getBreeds } from '@/api/breeds'
import { getDiets } from '@/api/diets'
import { createBreedDiet, updateBreedDiet, getBreedDiet } from '@/api/breedDiets'

const route = useRoute()
const router = useRouter()
const isEdit = !!route.params.id

const form = ref({
  breed: null,
  diet: null,
  season: 'winter'
})

const seasonOptions = [
  { label: 'Зима', value: 'winter' },
  { label: 'Весна', value: 'spring' },
  { label: 'Лето', value: 'summer' },
  { label: 'Осень', value: 'autumn' }
]

const breedOptions = ref([])
const dietOptions = ref([])

// Загрузка данных при редактировании
onMounted(async () => {
  breedOptions.value = await getBreeds()
  const diets = await getDiets()
  dietOptions.value = diets.map(d => ({ id: d.id, label: `Диета №${d.number}` }))

  if (isEdit) {
    const data = await getBreedDiet(route.params.id)
    form.value = {
      breed: data.breed.id,
      diet: data.diet.id,
      season: data.season
    }
  }
})

const save = async () => {
  try {
    if (isEdit) {
      await updateBreedDiet(route.params.id, form.value)
    } else {
      await createBreedDiet(form.value)
    }
    router.push('/breed-diets')
  } catch (err) {
    const msg = err.response?.data?.error || 'Ошибка сохранения'
    alert(msg)
  }
}
</script>