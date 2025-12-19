<template>
  <div>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>Отчеты</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-select
                  v-model.number="classId"
                  label="Выберите класс"
                  :items="classItems"
                  item-title="text"
                  item-value="value"
                  variant="outlined"
                  clearable
                ></v-select>
                <v-btn 
                  color="primary" 
                  @click="loadReport" 
                  :loading="loading"
                  :disabled="!classId"
                  class="mt-2"
                >
                  Загрузить отчет об успеваемости
                </v-btn>
              </v-col>
            </v-row>
            
            <v-divider class="my-4"></v-divider>
            
            <v-card v-if="report" class="mt-4">
              <v-card-title>
                Отчет об успеваемости класса {{ report.class_name || selectedClassName }}
              </v-card-title>
              <v-card-text>
                <v-row class="mb-4">
                  <v-col cols="12" md="4">
                    <v-card variant="outlined">
                      <v-card-text>
                        <div class="text-subtitle-2 text-grey">Количество учеников</div>
                        <div class="text-h6">{{ report.students_count || 0 }}</div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="12" md="4">
                    <v-card variant="outlined">
                      <v-card-text>
                        <div class="text-subtitle-2 text-grey">Общий средний балл</div>
                        <div class="text-h6">{{ report.overall_average_grade ? report.overall_average_grade.toFixed(2) : '-' }}</div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="12" md="4">
                    <v-card variant="outlined">
                      <v-card-text>
                        <div class="text-subtitle-2 text-grey">Классный руководитель</div>
                        <div class="text-h6">
                          {{ report.homeroom_teacher 
                            ? `${report.homeroom_teacher.last_name} ${report.homeroom_teacher.first_name} ${report.homeroom_teacher.middle_name || ''}`.trim()
                            : '-' }}
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
                
                <v-divider class="my-4"></v-divider>
                
                <div class="text-h6 mb-3">Успеваемость по предметам</div>
                <v-data-table
                  :headers="reportHeaders"
                  :items="reportData"
                  :loading="loading"
                ></v-data-table>
              </v-card-text>
            </v-card>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/api/client'
import { useReferenceStore } from '@/stores/reference'

const referenceStore = useReferenceStore()
const loading = ref(false)
const classId = ref(null)
const report = ref(null)
const reportData = ref([])

const classItems = computed(() => {
  return referenceStore.classes.map(c => ({
    text: `${c.grade}${c.letter}`,
    value: c.id
  }))
})

const selectedClassName = computed(() => {
  if (!classId.value) return ''
  return referenceStore.getClassLabel(classId.value)
})

const reportHeaders = [
  { title: 'Предмет', key: 'subject_name' },
  { title: 'Средняя оценка', key: 'average_grade' },
  { title: 'Количество оценок', key: 'grades_count' }
]

const loadReport = async () => {
  if (!classId.value) {
    alert('Выберите класс')
    return
  }
  
  loading.value = true
  try {
    const response = await api.get(`/reports/class-performance`, {
      params: { classId: classId.value }
    })
    report.value = response.data
    // Преобразуем subject_performance для таблицы
    if (response.data && response.data.subject_performance && Array.isArray(response.data.subject_performance)) {
      reportData.value = response.data.subject_performance.map(item => ({
        subject_name: item.subject_name,
        average_grade: item.average_grade ? item.average_grade.toFixed(2) : '-',
        grades_count: item.grades_count || 0
      }))
    } else {
      reportData.value = []
    }
  } catch (error) {
    console.error('Ошибка загрузки отчета:', error)
    alert(error.response?.data?.error || 'Ошибка загрузки отчета')
    report.value = null
    reportData.value = []
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  // Загружаем классы при монтировании компонента
  if (!referenceStore.classes || referenceStore.classes.length === 0) {
    await referenceStore.loadClasses()
  }
})
</script>

