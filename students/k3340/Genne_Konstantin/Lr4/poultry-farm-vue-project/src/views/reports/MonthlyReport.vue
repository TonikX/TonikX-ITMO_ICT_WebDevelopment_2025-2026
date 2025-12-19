<template>
  <v-container>
    <v-card>
      <v-card-title>Ежемесячный отчёт</v-card-title>
      <v-card-text>
        <p><strong>Период:</strong> {{ report.period }}</p>
        <p><strong>Всего кур:</strong> {{ report.total_hens }}</p>
        <p><strong>Всего яиц:</strong> {{ report.total_eggs }}</p>

        <v-expansion-panels>
          <v-expansion-panel v-for="ws in report.workshops" :key="ws.workshop_number">
            <v-expansion-panel-title>
              Цех {{ ws.workshop_number }} — {{ ws.total_hens }} кур, {{ ws.total_eggs }} яиц
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-table>
                <thead>
                  <tr>
                    <th>Порода</th>
                    <th>Кур</th>
                    <th>Яиц</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="b in ws.breeds" :key="b.breed_name">
                    <td>{{ b.breed_name }}</td>
                    <td>{{ b.count }}</td>
                    <td>{{ b.eggs }}</td>
                  </tr>
                </tbody>
              </v-table>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getMonthlyReport } from '@/api/reports'

const report = ref({
  period: '',
  workshops: [],
  total_hens: 0,
  total_eggs: 0
})

onMounted(async () => {
  report.value = await getMonthlyReport()
})
</script>