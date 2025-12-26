<template>
  <v-dialog v-model="dialog" max-width="900">
    <v-card>
      <v-toolbar color="info" dark>
        <v-toolbar-title>
          <v-icon class="mr-2">mdi-google-classroom</v-icon>
          Информация о классе {{ schoolClass?.class_name }}
        </v-toolbar-title>
        <v-spacer />
        <v-btn icon @click="close">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-toolbar>

      <v-card-text class="pa-6">
        <v-row v-if="schoolClass">
          <v-col cols="12" md="4">
            <v-card variant="flat" class="text-center">
              <v-card-text>
                <v-icon size="64" color="primary" class="mb-4">mdi-google-classroom</v-icon>
                <h2 class="text-h3">{{ schoolClass.class_name }}</h2>
                <p class="text-body-1 text-grey mb-4">ID: {{ schoolClass.id }}</p>

                <v-chip color="info" class="mb-2">
                  <v-icon left>mdi-account</v-icon>
                  {{ schoolClass.students_count }} учеников
                </v-chip>

                <div v-if="schoolClass.class_teacher_name" class="mt-4">
                  <p class="text-body-2 text-grey mb-1">Классный руководитель:</p>
                  <v-chip color="success">
                    {{ schoolClass.class_teacher_name }}
                  </v-chip>
                </div>
                <div v-else class="mt-4">
                  <p class="text-body-2 text-grey">Классный руководитель не назначен</p>
                </div>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="8">
            <v-tabs v-model="tab" color="primary">
              <v-tab value="students">
                <v-icon left>mdi-school</v-icon>
                Ученики
              </v-tab>
              <v-tab value="schedule">
                <v-icon left>mdi-calendar</v-icon>
                Расписание
              </v-tab>
              <v-tab value="statistics">
                <v-icon left>mdi-chart-bar</v-icon>
                Статистика
              </v-tab>
            </v-tabs>

            <v-window v-model="tab" class="mt-4">
              <v-window-item value="students">
                <v-card variant="flat">
                  <v-card-text>
                    <v-table v-if="schoolClass.students && schoolClass.students.length">
                      <thead>
                        <tr>
                          <th>Фамилия</th>
                          <th>Имя</th>
                          <th>Пол</th>
                          <th>Средний балл</th>
                          <th>Действия</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="student in schoolClass.students" :key="student.id">
                          <td>{{ student.last_name }}</td>
                          <td>{{ student.first_name }}</td>
                          <td>
                            <v-chip :color="student.gender === 'M' ? 'blue' : 'pink'" size="small">
                              {{ student.gender === 'M' ? 'М' : 'Ж' }}
                            </v-chip>
                          </td>
                          <td>
                            <v-chip
                              :color="getGradeColor(student.average_grade)"
                              size="small"
                            >
                              {{ student.average_grade ? student.average_grade.toFixed(1) : 'Нет' }}
                            </v-chip>
                          </td>
                          <td>
                            <v-btn icon size="small" @click="$emit('view-student', student)">
                              <v-icon color="info" size="small">mdi-eye</v-icon>
                            </v-btn>
                            <v-btn icon size="small" @click="$emit('edit-student', student)">
                              <v-icon color="primary" size="small">mdi-pencil</v-icon>
                            </v-btn>
                          </td>
                        </tr>
                      </tbody>
                    </v-table>
                    <div v-else class="text-center py-8 text-grey">
                      Нет учеников в классе
                    </div>
                  </v-card-text>
                </v-card>
              </v-window-item>

              <v-window-item value="schedule">
                <v-card variant="flat">
                  <v-card-text>
                    <v-table v-if="schoolClass.schedule && schoolClass.schedule.length">
                      <thead>
                        <tr>
                          <th>День недели</th>
                          <th>Урок</th>
                          <th>Предмет</th>
                          <th>Учитель</th>
                          <th>Кабинет</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="lesson in sortedSchedule" :key="lesson.id">
                          <td>{{ lesson.day_of_week_display }}</td>
                          <td>{{ lesson.lesson_number }}</td>
                          <td>{{ lesson.subject_name }}</td>
                          <td>{{ lesson.teacher_name }}</td>
                          <td>{{ lesson.classroom_number }}</td>
                        </tr>
                      </tbody>
                    </v-table>
                    <div v-else class="text-center py-8 text-grey">
                      Расписание не составлено
                    </div>
                  </v-card-text>
                </v-card>
              </v-window-item>

              <v-window-item value="statistics">
                <v-card variant="flat">
                  <v-card-text>
                    <v-row>
                      <v-col cols="12" md="6">
                        <v-card class="pa-4" variant="outlined">
                          <div class="text-center">
                            <v-icon size="48" color="primary" class="mb-2">mdi-gender-male-female</v-icon>
                            <h3 class="text-h5">Распределение по полу</h3>
                            <div class="d-flex justify-center mt-4">
                              <div class="text-center mr-6">
                                <v-icon size="32" color="blue">mdi-gender-male</v-icon>
                                <p class="text-h4">{{ boysCount }}</p>
                                <p class="text-caption">Мальчиков</p>
                              </div>
                              <div class="text-center">
                                <v-icon size="32" color="pink">mdi-gender-female</v-icon>
                                <p class="text-h4">{{ girlsCount }}</p>
                                <p class="text-caption">Девочек</p>
                              </div>
                            </div>
                          </div>
                        </v-card>
                      </v-col>

                      <v-col cols="12" md="6">
                        <v-card class="pa-4" variant="outlined">
                          <div class="text-center">
                            <v-icon size="48" color="success" class="mb-2">mdi-chart-line</v-icon>
                            <h3 class="text-h5">Успеваемость</h3>
                            <div class="mt-4">
                              <p class="text-h4">{{ classAverage.toFixed(2) }}</p>
                              <p class="text-caption">Средний балл класса</p>
                            </div>
                          </div>
                        </v-card>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
              </v-window-item>
            </v-window>
          </v-col>
        </v-row>

        <div v-else class="text-center py-8">
          <v-progress-circular indeterminate />
        </div>
      </v-card-text>

      <v-card-actions class="pa-4">
        <v-spacer />
        <v-btn color="warning" @click="$emit('edit', schoolClass)">
          <v-icon left>mdi-pencil</v-icon>
          Редактировать
        </v-btn>
        <v-btn color="success" @click="$emit('report', schoolClass)">
          <v-icon left>mdi-file-pdf</v-icon>
          Отчет в PDF
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'ClassDetail',
  props: {
    value: {
      type: Boolean,
      default: false
    },
    schoolClass: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      tab: 'students'
    }
  },
  computed: {
    dialog: {
      get() {
        return this.value
      },
      set(value) {
        this.$emit('input', value)
      }
    },
    boysCount() {
      if (!this.schoolClass?.students) return 0
      return this.schoolClass.students.filter(s => s.gender === 'M').length
    },
    girlsCount() {
      if (!this.schoolClass?.students) return 0
      return this.schoolClass.students.filter(s => s.gender === 'F').length
    },
    classAverage() {
      if (!this.schoolClass?.students) return 0
      const studentsWithGrades = this.schoolClass.students.filter(s => s.average_grade)
      if (studentsWithGrades.length === 0) return 0

      const total = studentsWithGrades.reduce((sum, student) => sum + student.average_grade, 0)
      return total / studentsWithGrades.length
    },
    sortedSchedule() {
      if (!this.schoolClass?.schedule) return []
      return [...this.schoolClass.schedule].sort((a, b) => {
        if (a.day_of_week === b.day_of_week) {
          return a.lesson_number - b.lesson_number
        }
        return a.day_of_week - b.day_of_week
      })
    }
  },
  methods: {
    getGradeColor(grade) {
      if (!grade) return 'grey'
      if (grade >= 4.5) return 'success'
      if (grade >= 3.5) return 'warning'
      return 'error'
    },
    close() {
      this.dialog = false
      this.tab = 'students'
    }
  }
}
</script>