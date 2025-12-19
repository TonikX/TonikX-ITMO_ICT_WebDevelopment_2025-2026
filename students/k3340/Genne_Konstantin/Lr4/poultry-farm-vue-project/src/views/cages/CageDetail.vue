<template>
  <v-container v-if="cage">
    <v-card>
      <v-card-title>
        Клетка {{ cage.workshop_number }}-{{ cage.row_number }}-{{ cage.in_row_number }}
      </v-card-title>
      <v-card-text>
        <h4>Текущие курицы в клетке ({{ currentHens.length }})</h4>

        <v-table v-if="currentHens.length" density="compact">
          <thead>
            <tr>
              <th>ID</th>
              <th>Порода</th>
              <th>Вес (г)</th>
              <th>Возраст</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="hen in currentHens" :key="hen.id">
              <td>{{ hen.id }}</td>
              <td>{{ hen.breed_name }}</td>
              <td>{{ hen.weight }}</td>
              <td>{{ getAge(hen.birth_date) }} мес</td>
            </tr>
          </tbody>
        </v-table>

        <p v-else>В клетке нет кур.</p>
      </v-card-text>
      <v-card-actions>
        <v-btn to="/cages">Назад к списку</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>

  <v-container v-else>
    <v-row justify="center">
      <v-col cols="auto">
        <v-progress-circular indeterminate color="primary" />
        <div class="mt-2">Загрузка данных о клетке...</div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { getCageDetail } from '@/api/cages'

const route = useRoute()
const cage = ref(null)

// ✅ Просто используем current_hens напрямую
const currentHens = computed(() => {
  return cage.value?.current_hens || []
})

const getAge = (birthDateString) => {
  if (!birthDateString) return '—'
  const birthDate = new Date(birthDateString)
  const today = new Date()
  const diffTime = Math.abs(today - birthDate)
  const diffMonths = Math.floor(diffTime / (1000 * 60 * 60 * 24 * 30.44))
  return diffMonths
}

onMounted(async () => {
  try {
    cage.value = await getCageDetail(route.params.id)
  } catch (err) {
    console.error('Ошибка загрузки клетки:', err)
  }
})
</script>