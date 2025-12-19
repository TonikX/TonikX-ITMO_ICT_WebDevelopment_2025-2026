<!-- src/views/hens/HenForm.vue -->
<template>
  <v-container>
    <v-card>
      <v-card-title>{{ isEdit ? 'Редактировать курицу' : 'Добавить курицу' }}</v-card-title>
      <v-card-text>
        <v-select
          v-model="form.breed"
          :items="breeds"
          item-title="name"
          item-value="id"
          label="Порода"
          required
        />
        <v-text-field
          v-model.number="form.weight"
          type="number"
          label="Вес (г)"
          required
        />
        <v-date-picker v-model="form.birth_date" label="Дата рождения" />
      </v-card-text>
      <v-card-actions>
        <v-btn @click="save" color="primary">Сохранить</v-btn>
        <v-btn to="/hens">Отмена</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getBreeds } from '@/api/breeds'
import { createHen, updateHen } from '@/api/hens'

const router = useRouter()
const route = useRoute()
const isEdit = !!route.params.id // будет false для /hens/new

const form = ref({ breed: null, weight: null, birth_date: new Date().toISOString().split('T')[0] })
const breeds = ref([])

onMounted(async () => {
  breeds.value = await getBreeds()
  // Если редактирование — загрузить данные (не нужно для /new)
})

const save = async () => {
  if (isEdit) {
    await updateHen(route.params.id, form.value)
  } else {
    await createHen(form.value)
  }
  router.push('/hens')
}
</script>