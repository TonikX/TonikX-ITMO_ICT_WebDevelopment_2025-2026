<template>
  <v-card>
    <v-toolbar color="success" dark flat>
      <v-toolbar-title>
        <v-icon class="mr-2">mdi-chart-bar</v-icon>
        Отчет об успеваемости класса
      </v-toolbar-title>
      <v-spacer />
      <v-btn color="info" @click="exportToPdf" :loading="exporting">
        <v-icon left>mdi-file-pdf</v-icon>
        Экспорт в PDF
      </v-btn>
    </v-toolbar>

    <v-card-text class="pa-6">
      <v-row class="mb-6">
        <v-col cols="12" md="6">
          <v-select
            v-model="selectedClass"
            :items="classes"
            item-title="class_name"
            item-value="id"
            label="Выберите класс*"
            :rules="[rules.required]"
            variant="outlined"
            @update:model-value="loadReport"
          />
        </v-col>
        <v-col cols="12" md="6" class="d-flex align-center">
          <v-btn
            color="primary"
            @click="loadReport"
            :loading="loading"
            :disabled="!selectedClass"
            class="mt-3"
          >
            <v-icon left>mdi-refresh</v-icon>
            Обновить отчет
          </v-btn>
        </v-col>
      </v-row>

      <div v-if="loading" class="text-center py-8">
        <v-progress-circular indeterminate />
        <p class="mt-4">Загрузка отчета...</p>
      </div>

      <div v-else-if="reportData">
        <v-card variant="outlined" class="mb-6">
          <v-card-text>
            <v-row>
              <v-col cols="12" md="4" class="text-center">
                <div class="text-h4 mb-2">{{ reportData.class_name }}</div>
                <v-chip color="primary" variant="flat">
                  Класс
                </v-chip>
              </v-col>

              <v-col cols="12" md="4" class="text-center">
                <div class="text-h6 mb-2">Классный руководитель</div>
                <div class="text-h5">{{ reportData.class_teacher || 'Не назначен' }}</div>
              </v-col>

              <v-col cols="12" md="4" class="text-center">
                <div class="text-h6 mb-2">Количество учеников</div>
                <div class="text-h5">{{ reportData.total_students }}</div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <v-card variant="outlined" class="mb-6">
          <v-toolbar color="grey-lighten-3" density="compact">
            <v-toolbar-title>Успеваемость по предметам</v-toolbar-title>
            <v-spacer />
            <v-chip color="primary" variant="flat">
              Средний балл класса: {{ reportData.class_average.toFixed(2) }}
            </v-chip>
          </v-toolbar>

          <v-card-text>
            <v-table v-if="reportData.subjects_data && Object.keys(reportData.subjects_data).length">
              <thead>
                <tr>
                  <th>Предмет</th>
                  <th>Средний балл</th>
                  <th>Количество оценок</th>
                  <th>Оценка успеваемости</th>
                  <th>График</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="[subject, data] in Object.entries(reportData.subjects_data)" :key="subject">
                  <td>{{ subject }}</td>
                  <td>
                    <v-chip :color="getGradeColor(data.average_grade)" variant="flat">
                      {{ data.average_grade.toFixed(2) }}
                    </v-chip>
                  </td>
                  <td>{{ data.grades_count }}</td>
                  <td>
                    <v-progress-linear
                      :model-value="data.average_grade * 20"
                      :color="getGradeColor(data.average_grade)"
                      height="10"
                      rounded
                    />
                  </td>
                  <td>
                    <div style="width: 100px; height: 30px;">
                      <canvas ref="chartCanvas" style="display: none;"></canvas>
                    </div>
                  </td>
                </tr>
              </tbody>
            </v-table>
            <div v-else class="text-center py-8 text-grey">
              Нет данных по успеваемости
            </div>
          </v-card-text>
        </v-card>

        <v-row>
          <v-col cols="12" md="6">
            <v-card variant="outlined">
              <v-toolbar color="grey-lighten-3" density="compact">
                <v-toolbar-title>Статистика оценок</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <div class="text-center">
                  <v-progress-circular
                    :model-value="(reportData.class_average / 5) * 100"
                    :color="getGradeColor(reportData.class_average)"
                    size="120"
                    width="12"
                  >
                    <span class="text-h5">{{ reportData.class_average.toFixed(1) }}</span>
                  </v-progress-circular>
                  <p class="mt-4 text-body-1">Общий средний балл</p>
                </div>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card variant="outlined">
              <v-toolbar color="grey-lighten-3" density="compact">
                <v-toolbar-title>Рекомендации</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-list>
                  <v-list-item v-for="(rec, index) in recommendations" :key="index">
                    <template v-slot:prepend>
                      <v-icon :color="rec.color">{{ rec.icon }}</v-icon>
                    </template>
                    <v-list-item-title>{{ rec.text }}</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </div>

      <div v-else-if="!selectedClass" class="text-center py-8">
        <v-icon size="64" color="grey" class="mb-4">mdi-chart-bar</v-icon>
        <p class="text-h6 text-grey">Выберите класс для просмотра отчета</p>
      </div>

      <div v-else class="text-center py-8">
        <v-icon size="64" color="grey" class="mb-4">mdi-chart-bar</v-icon>
        <p class="text-h6 text-grey">Данные не найдены</p>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
import { Chart, registerables } from 'chart.js'

export default {
  name: 'ClassReport',
  props: {
    classes: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      loading: false,
      exporting: false,
      selectedClass: null,
      reportData: null,
      chart: null,
      rules: {
        required: value => !!value || 'Обязательное поле'
      }
    }
  },
  computed: {
    recommendations() {
      if (!this.reportData) return []

      const recs = []
      const avg = this.reportData.class_average

      if (avg >= 4.5) {
        recs.push({
          icon: 'mdi-emoticon-excited',
          color: 'success',
          text: 'Отличная успеваемость!'
        })
        recs.push({
          icon: 'mdi-star',
          color: 'success',
          text: 'Рекомендуется участие в олимпиадах'
        })
      } else if (avg >= 4.0) {
        recs.push({
          icon: 'mdi-emoticon-happy',
          color: 'success',
          text: 'Хорошая успеваемость'
        })
        recs.push({
          icon: 'mdi-school',
          color: 'info',
          text: 'Рекомендуется уделить внимание слабым предметам'
        })
      } else if (avg >= 3.5) {
        recs.push({
          icon: 'mdi-emoticon-neutral',
          color: 'warning',
          text: 'Средняя успеваемость'
        })
        recs.push({
          icon: 'mdi-book',
          color: 'warning',
          text: 'Требуется дополнительная работа'
        })
      } else {
        recs.push({
          icon: 'mdi-emoticon-sad',
          color: 'error',
          text: 'Низкая успеваемость'
        })
        recs.push({
          icon: 'mdi-alert',
          color: 'error',
          text: 'Требуется срочное вмешательство'
        })
      }

      return recs
    }
  },
  methods: {
    async loadReport() {
      if (!this.selectedClass) return

      this.loading = true
      try {
        const response = await this.$api.reports.getClassPerformanceReport(this.selectedClass)
        this.reportData = response.data
        this.$toast.success('Отчет загружен')
      } catch (error) {
        this.$toast.error('Ошибка загрузки отчета')
      } finally {
        this.loading = false
      }
    },

    getGradeColor(grade) {
      if (!grade) return 'grey'
      if (grade >= 4.5) return 'success'
      if (grade >= 4.0) return 'info'
      if (grade >= 3.5) return 'warning'
      return 'error'
    },

    async exportToPdf() {
      if (!this.selectedClass) {
        this.$toast.warning('Выберите класс для экспорта')
        return
      }

      this.exporting = true
      try {
        const response = await this.$api.reports.exportReportToPdf(this.selectedClass)

        // Создаем ссылку для скачивания
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `report_${this.reportData.class_name}.pdf`)
        document.body.appendChild(link)
        link.click()
        link.remove()

        this.$toast.success('PDF отчет скачан')
      } catch (error) {
        this.$toast.error('Ошибка экспорта в PDF')
      } finally {
        this.exporting = false
      }
    }
  }
}
</script>