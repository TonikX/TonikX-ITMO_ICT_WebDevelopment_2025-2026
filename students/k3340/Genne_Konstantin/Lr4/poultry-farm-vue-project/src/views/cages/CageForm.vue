<template>
  <v-container>
    <v-card>
      <v-card-title>Создать клетку</v-card-title>
      <v-card-text>
        <v-text-field v-model.number="form.workshop_number" type="number" label="Номер цеха" required />
        <v-text-field v-model.number="form.row_number" type="number" label="Номер ряда" required />
        <v-text-field v-model.number="form.in_row_number" type="number" label="Номер клетки в ряду" required />
      </v-card-text>
      <v-card-actions>
        <v-btn @click="save" color="primary">Создать</v-btn>
        <v-btn to="/cages">Отмена</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { createCage } from '@/api/cages'

const router = useRouter()
const form = ref({ workshop_number: null, row_number: null, in_row_number: null })

const save = async () => {
  try {
    await createCage(form.value)
    router.push('/cages')
    // Уведомление о успешном создании убрано
  } catch (err) {
    // Обработка ошибок оставлена, но без Snackbar
    console.error(err.response?.data?.error || 'Ошибка создания')
    alert(err.response?.data?.error || 'Ошибка создания')
  }
}
</script>