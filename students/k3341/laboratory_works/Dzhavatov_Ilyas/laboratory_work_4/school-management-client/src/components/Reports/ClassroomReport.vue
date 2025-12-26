<template>
  <v-card>
    <v-toolbar color="primary" dark flat>
      <v-toolbar-title>
        <v-icon class="mr-2">mdi-door</v-icon>
        Статистика по кабинетам
      </v-toolbar-title>
      <v-spacer />
      <v-btn color="success" @click="loadData" :loading="loading">
        <v-icon left>mdi-refresh</v-icon>
        Обновить
      </v-btn>
    </v-toolbar>

    <v-card-text class="pa-6">
      <div v-if="loading" class="text-center py-8">
        <v-progress-circular indeterminate />
        <p class="mt-4">Загрузка статистики...</p>
      </div>

      <div v-else-if="statistics.length > 0">
        <v-row>
          <v-col cols="12" md="6">
            <v-table>
              <thead>
                <tr>
                  <th>Тип дисциплины</th>
                  <th>Количество кабинетов</th>
                  <th>Процент</th>
                  <th>Статус</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in statistics" :key="item.subject_type">
                  <td>{{ item.subject_type_display }}</td>
                  <td>
                    <v-chip :color="getCountColor(item.classroom_count)" variant="flat">
                      {{ item.classroom_count }}
                    </v-chip>
                  </td>
                  <td>
                    {{ ((item.classroom_count / totalClassrooms) * 100).toFixed(1) }}%
                  </td>
                  <td>
                    <v-progress-linear
                      :model-value="(item.classroom_count / totalClassrooms) * 100"
                      :color="getCountColor(item.classroom_count)"
                      height="10"
                      rounded
                    />
                  </td>
                </tr>
              </tbody>
            </v-table>

            <v-card class="mt-6" variant="outlined">
              <v-toolbar color="grey-lighten-3" density="compact">
                <v-toolbar-title>Сводная информация</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-list>
                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon color="primary">mdi-door</v-icon>
                    </template>
                    <v-list-item-title>Всего кабинетов</v-list-item-title>
                    <template v-slot:append>
                      <span class="text-h6">{{ totalClassrooms }}</span>
                    </template>
                  </v-list-item>

                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon color="info">mdi-book</v-icon>
                    </template>
                    <v-list-item-title>Для базовых дисциплин</v-list-item-title>
                    <template v-slot:append>
                      <span class="text-h6">{{ basicCount }}</span>
                    </template>
                  </v-list-item>

                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon color="success">mdi-book-education</v-icon>
                    </template>
                    <v-list-item-title>Для профильных дисциплин</v-list-item-title>
                    <template v-slot:append>
                      <span class="text-h6">{{ profileCount }}</span>
                    </template>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card variant="outlined" height="100%">
              <v-toolbar color="grey-lighten-3" density="compact">
                <v-toolbar-title>Визуализация распределения</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <div style="height: 300px;">
                  <canvas ref="chartCanvas"></canvas>
                </div>

                <v-divider class="my-4" />

                <h3 class="text-h6 mb-4">Анализ оснащенности</h3>

                <v-alert
                  v-if="basicCount < 10"
                  type="warning"
                  density="compact"
                  class="mb-2"
                >
                  <v-icon left>mdi-alert</v-icon>
                  Недостаточно кабинетов для базовых дисциплин
                </v-alert>

                <v-alert
                  v-if="profileCount < 5"
                  type="warning"
                  density="compact"
                  class="mb-2"
                >
                  <v-icon left>mdi-alert</v-icon>
                  Недостаточно кабинетов для профильных дисциплин
                </v-alert>

                <v-alert
                  v-if="basicCount >= 10 && profileCount >= 5"
                  type="success"
                  density="compact"
                >
                  <v-icon left>mdi-check-circle</v-icon>
                  Оснащенность кабинетами соответствует нормам
                </v-alert>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </div>

      <div v-else class="text-center py-8">
        <v-icon size="64" color="grey" class="mb-4">mdi-door</v-icon>
        <p class="text-h6 text-grey">Статистика не найдена</p>
        <p class="text-body-1 text-grey">Добавьте кабинеты в систему</p>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
import { Chart, registerables } from 'chart.js'

export default {
  name: 'ClassroomReport',
  data() {
    return {
      loading: false,
      statistics: [],
      chartInstance: null
    }
  },
  computed: {
    totalClassrooms() {
      return this.statistics.reduce((sum, item) => sum + item.classroom_count, 0)
    },
    basicCount() {
      const basic = this.statistics.find(item => item.subject_type === 'basic')
      return basic ? basic.classroom_count : 0
    },
    profileCount() {
      const profile = this.statistics.find(item => item.subject_type === 'profile')
      return profile ? profile.classroom_count : 0
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    getCountColor(count) {
      if (count >= 10) return 'success'
      if (count >= 5) return 'warning'
      return 'error'
    },

    async loadData() {
      this.loading = true
      try {
        const response = await this.$api.reports.getClassroomStatistics()
        this.statistics = response.data
        this.$toast.success('Статистика загружена')
        this.createChart()
      } catch (error) {
        this.$toast.error('Ошибка загрузки статистики')
      } finally {
        this.loading = false
      }
    },

    createChart() {
      if (!this.statistics.length) return

      const ctx = this.$refs.chartCanvas?.getContext('2d')
      if (!ctx) return

      if (this.chartInstance) {
        this.chartInstance.destroy()
      }

      const labels = this.statistics.map(item => item.subject_type_display)
      const data = this.statistics.map(item => item.classroom_count)
      const backgroundColors = ['rgba(54, 162, 235, 0.7)', 'rgba(75, 192, 192, 0.7)']

      Chart.register(...registerables)

      this.chartInstance = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            backgroundColor: backgroundColors,
            borderColor: ['rgba(54, 162, 235, 1)', 'rgba(75, 192, 192, 1)'],
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top'
            },
            title: {
              display: true,
              text: 'Распределение кабинетов по типам дисциплин'
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  const label = context.label || ''
                  const value = context.raw || 0
                  const total = context.dataset.data.reduce((a, b) => a + b, 0)
                  const percentage = Math.round((value / total) * 100)
                  return `${label}: ${value} кабинетов (${percentage}%)`
                }
              }
            }
          }
        }
      })
    }
  },
  beforeUnmount() {
    if (this.chartInstance) {
      this.chartInstance.destroy()
    }
  }
}
</script>