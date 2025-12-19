<template>
  <v-container>
    <v-card>
      <v-card-title>{{ isEdit ? 'Редактировать диету' : 'Создать диету' }}</v-card-title>
      <v-card-text>
        <v-text-field v-model.number="form.number" type="number" label="Номер диеты" required />
        <v-textarea v-model="form.structure" label="Описание диеты" required />
      </v-card-text>
      <v-card-actions>
        <v-btn @click="save" color="primary">Сохранить</v-btn>
        <v-btn to="/diets">Отмена</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { createDiet, updateDiet, getDiet } from '@/api/diets'

const route = useRoute()
const router = useRouter()
const isEdit = !!route.params.id
const form = ref({ number: null, structure: '' })

onMounted(async () => {
  if (isEdit) {
    const data = await getDiet(route.params.id)
    form.value = data
  }
})

const save = async () => {
  try {
    if (isEdit) {
      await updateDiet(route.params.id, form.value)
    } else {
      await createDiet(form.value)
    }
    router.push('/diets')
    // Уведомление о успешном сохранении убрано
  } catch (err) {
    // Обработка ошибок оставлена, но без Snackbar
    console.error(err.response?.data?.error || 'Ошибка сохранения')
    alert(err.response?.data?.error || 'Ошибка сохранения')
  }
}
</script>