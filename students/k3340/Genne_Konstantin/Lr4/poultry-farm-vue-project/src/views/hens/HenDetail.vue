<template>
  <v-container v-if="hen">
    <v-card>
      <v-card-title>Курица #{{ hen.id }}</v-card-title>
      <v-card-text>
        <p><strong>Порода:</strong> {{ hen.breed?.name }}</p>
        <p><strong>Вес:</strong> {{ hen.weight }} г</p>
        <p><strong>Дата рождения:</strong> {{ formatDate(hen.birth_date) }}</p>
        <p v-if="hen.death_date"><strong>Дата смерти:</strong> {{ formatDate(hen.death_date) }}</p>
        <p v-else><strong>Статус:</strong> Жива</p>

        <h4>Текущее размещение</h4>
        <div v-if="hen.current_cage">
          <p>
            Цех {{ hen.current_cage.workshop_number }},
            ряд {{ hen.current_cage.row_number }},
            клетка {{ hen.current_cage.in_row_number }}
          </p>
          <p>Заселена: {{ formatDate(hen.current_cage.date_start) }}</p>
        </div>
        <p v-else>Не размещена</p>

        <h4 class="mt-4">Яйценоскость (последние 30 дней)</h4>
        <v-table density="compact" v-if="recentEggs.length">
          <thead>
            <tr>
              <th>Дата</th>
              <th>Количество яиц</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="egg in recentEggs" :key="egg.id">
              <td>{{ formatDate(egg.date) }}</td>
              <td>{{ egg.count_eggs }}</td>
            </tr>
          </tbody>
        </v-table>
        <p v-else>Нет данных о яйценоскости за последние 30 дней.</p>
      </v-card-text>
      <v-card-actions>
        <v-btn to="/hens">Назад к списку</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>

  <v-container v-else>
    <v-row justify="center">
      <v-col cols="auto">
        <v-progress-circular indeterminate color="primary" />
        <div class="mt-2">Загрузка данных о курице...</div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getHenDetail } from '@/api/hens'
import { getEggRecords } from '@/api/eggs'

const route = useRoute()
const hen = ref(null)
const recentEggs = ref([])

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('ru-RU')
}

onMounted(async () => {
  try {
    // Загружаем детали курицы
    hen.value = await getHenDetail(route.params.id)

    // Загружаем яйценоскость
    const today = new Date()
    const lastMonth = new Date(today)
    lastMonth.setDate(today.getDate() - 30)
    recentEggs.value = await getEggRecords({
      hen_id: route.params.id,
      date_from: lastMonth.toISOString().split('T')[0],
      date_to: today.toISOString().split('T')[0]
    })
  } catch (err) {
    console.error('Ошибка загрузки:', err)
    // Можно показать snackbar об ошибке
  }
})
</script>