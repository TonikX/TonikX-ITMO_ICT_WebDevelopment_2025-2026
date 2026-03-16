<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { readersApi, type Reader } from '../shared/api/library'

const youngCount = ref<number | null>(null)
const educationStats = ref<{ primary: number; secondary: number; higher: number; degree: number } | null>(null)
const oldAssignmentsReaders = ref<Reader[]>([])
const rareBooksReaders = ref<Reader[]>([])
const loading = ref({ young: false, education: false, old: false, rare: false })
const error = ref('')

onMounted(async () => {
  try {
    loading.value.young = true
    const r = await readersApi.youngReaders()
    youngCount.value = r.count
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Ошибка'
  } finally {
    loading.value.young = false
  }
  try {
    loading.value.education = true
    educationStats.value = await readersApi.educationStats()
  } catch {
    // ignore
  } finally {
    loading.value.education = false
  }
  try {
    loading.value.old = true
    oldAssignmentsReaders.value = await readersApi.oldAssignments()
  } catch {
    // ignore
  } finally {
    loading.value.old = false
  }
  try {
    loading.value.rare = true
    rareBooksReaders.value = await readersApi.withRareBooks()
  } catch {
    // ignore
  } finally {
    loading.value.rare = false
  }
})
</script>

<template>
  <div>
    <h1 class="text-h4 mb-4">Запросы</h1>
    <v-alert v-if="error" type="error">{{ error }}</v-alert>

    <v-card class="mb-4">
      <v-card-title>Читатели младше 20 лет</v-card-title>
      <v-card-text>
        <v-progress-linear v-if="loading.young" indeterminate />
        <span v-else class="text-h5">{{ youngCount ?? 0 }}</span>
      </v-card-text>
    </v-card>

    <v-card class="mb-4">
      <v-card-title>Статистика по образованию (%)</v-card-title>
      <v-card-text>
        <v-progress-linear v-if="loading.education" indeterminate />
        <v-table v-else-if="educationStats" density="compact">
          <tbody>
            <tr><td>Начальное</td><td>{{ educationStats.primary }}%</td></tr>
            <tr><td>Среднее</td><td>{{ educationStats.secondary }}%</td></tr>
            <tr><td>Высшее</td><td>{{ educationStats.higher }}%</td></tr>
            <tr><td>Учёная степень</td><td>{{ educationStats.degree }}%</td></tr>
          </tbody>
        </v-table>
      </v-card-text>
    </v-card>

    <v-card class="mb-4">
      <v-card-title>Читатели, взявшие книгу более месяца назад</v-card-title>
      <v-card-text>
        <v-progress-linear v-if="loading.old" indeterminate />
        <v-table v-else density="compact">
          <thead><tr><th>Билет</th><th>ФИО</th></tr></thead>
          <tbody>
            <tr v-for="r in oldAssignmentsReaders" :key="r.id">
              <td>{{ r.ticket_number }}</td>
              <td>{{ r.full_name }}</td>
            </tr>
          </tbody>
        </v-table>
        <p v-if="!loading.old && oldAssignmentsReaders.length === 0" class="text-medium-emphasis">Нет таких читателей</p>
      </v-card-text>
    </v-card>

    <v-card>
      <v-card-title>Читатели с редкими книгами (≤2 экз.)</v-card-title>
      <v-card-text>
        <v-progress-linear v-if="loading.rare" indeterminate />
        <v-table v-else density="compact">
          <thead><tr><th>Билет</th><th>ФИО</th></tr></thead>
          <tbody>
            <tr v-for="r in rareBooksReaders" :key="r.id">
              <td>{{ r.ticket_number }}</td>
              <td>{{ r.full_name }}</td>
            </tr>
          </tbody>
        </v-table>
        <p v-if="!loading.rare && rareBooksReaders.length === 0" class="text-medium-emphasis">Нет таких читателей</p>
      </v-card-text>
    </v-card>
  </div>
</template>
