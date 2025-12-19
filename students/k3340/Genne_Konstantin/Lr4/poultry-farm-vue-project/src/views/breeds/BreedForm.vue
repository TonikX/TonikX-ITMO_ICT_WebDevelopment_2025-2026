<template>
  <v-container>
    <v-card>
      <v-card-title>{{ isEdit ? 'Редактировать породу' : 'Создать породу' }}</v-card-title>
      <v-card-text>
        <v-text-field v-model="form.name" label="Название породы" required />
        <v-text-field v-model.number="form.efficiency" type="number" label="Среднее количество яиц в месяц" required />
        <v-text-field v-model.number="form.mean_weight" type="number" label="Средний вес (г)" required />
      </v-card-text>
      <v-card-actions>
        <v-btn @click="save" color="primary">Сохранить</v-btn>
        <v-btn to="/breeds">Отмена</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { createBreed, updateBreed, getBreed } from '@/api/breeds'

const route = useRoute()
const router = useRouter()
const isEdit = !!route.params.id
const form = ref({ name: '', efficiency: null, mean_weight: null })

onMounted(async () => {
  if (isEdit) {
    const data = await getBreed(route.params.id)
    form.value = data
  }
})

const save = async () => {
  try {
    if (isEdit) {
      await updateBreed(route.params.id, form.value)
    } else {
      await createBreed(form.value)
    }
    router.push('/breeds')
  } catch (err) {
    // Обработка ошибок оставлена, но без Snackbar
    console.error(err.response?.data?.error || 'Ошибка сохранения')
    alert(err.response?.data?.error || 'Ошибка сохранения')
  }
}
</script>