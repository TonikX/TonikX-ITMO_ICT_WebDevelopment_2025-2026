<template>
  <v-dialog v-model="dialog" max-width="800">
    <v-card>
      <v-toolbar color="info" dark>
        <v-toolbar-title>
          <v-icon class="mr-2">mdi-account-school</v-icon>
          Информация об ученике
        </v-toolbar-title>
        <v-spacer />
        <v-btn icon @click="close">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-toolbar>

      <v-card-text class="pa-6">
        <v-row v-if="student">
          <v-col cols="12" md="4">
            <v-card class="text-center" variant="flat">
              <v-card-text>
                <v-avatar size="120" color="primary" class="mb-4">
                  <span class="text-h3 text-white">
                    {{ student.first_name[0] }}{{ student.last_name[0] }}
                  </span>
                </v-avatar>
                <h2 class="text-h4">{{ student.last_name }} {{ student.first_name }}</h2>
                <p class="text-body-1 text-grey">ID: {{ student.id }}</p>
                <v-chip :color="student.gender === 'M' ? 'blue' : 'pink'" class="mt-2">
                  {{ student.gender === 'M' ? 'Мужской' : 'Женский' }}
                </v-chip>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="8">
            <v-list>
              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="primary">mdi-school</v-icon>
                </template>
                <v-list-item-title>
                  Класс: {{ student.class_name }}
                </v-list-item-title>
              </v-list-item>

              <v-divider class="my-2" />

              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="primary">mdi-chart-line</v-icon>
                </template>
                <v-list-item-title>
                  Средний балл:
                  <v-chip
                    :color="getGradeColor(student.average_grade)"
                    class="ml-2"
                  >
                    {{ student.average_grade ? student.average_grade.toFixed(2) : 'Нет оценок' }}
                  </v-chip>
                </v-list-item-title>
              </v-list-item>

              <v-divider class="my-2" />

              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="primary">mdi-calendar-text</v-icon>
                </template>
                <v-list-item-title class="font-weight-bold">
                  Оценки по предметам:
                </v-list-item-title>
              </v-list-item>
            </v-list>

            <v-table v-if="student.grades && student.grades.length" class="mt-2">
              <thead>
                <tr>
                  <th>Предмет</th>
                  <th>1 четверть</th>
                  <th>2 четверть</th>
                  <th>3 четверть</th>
                  <th>4 четверть</th>
                  <th>Среднее</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="subject in groupedGrades" :key="subject.name">
                  <td>{{ subject.name }}</td>
                  <td>
                    <v-chip v-if="subject.grades[1]" :color="getGradeColor(subject.grades[1])" size="small">
                      {{ subject.grades[1] }}
                    </v-chip>
                    <span v-else class="text-grey">-</span>
                  </td>
                  <td>
                    <v-chip v-if="subject.grades[2]" :color="getGradeColor(subject.grades[2])" size="small">
                      {{ subject.grades[2] }}
                    </v-chip>
                    <span v-else class="text-grey">-</span>
                  </td>
                  <td>
                    <v-chip v-if="subject.grades[3]" :color="getGradeColor(subject.grades[3])" size="small">
                      {{ subject.grades[3] }}
                    </v-chip>
                    <span v-else class="text-grey">-</span>
                  </td>
                  <td>
                    <v-chip v-if="subject.grades[4]" :color="getGradeColor(subject.grades[4])" size="small">
                      {{ subject.grades[4] }}
                    </v-chip>
                    <span v-else class="text-grey">-</span>
                  </td>
                  <td>
                    <v-chip v-if="subject.average" :color="getGradeColor(subject.average)" size="small">
                      {{ subject.average.toFixed(1) }}
                    </v-chip>
                    <span v-else class="text-grey">-</span>
                  </td>
                </tr>
              </tbody>
            </v-table>
            <div v-else class="text-center py-8 text-grey">
              Оценки не добавлены
            </div>
          </v-col>
        </v-row>

        <div v-else class="text-center py-8">
          <v-progress-circular indeterminate />
        </div>
      </v-card-text>

      <v-card-actions class="pa-4">
        <v-spacer />
        <v-btn color="warning" @click="$emit('edit', student)">
          <v-icon left>mdi-pencil</v-icon>
          Редактировать
        </v-btn>
        <v-btn color="success" @click="$emit('grades', student)">
          <v-icon left>mdi-chart-bar</v-icon>
          Управление оценками
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'StudentDetail',
  props: {
    value: {
      type: Boolean,
      default: false
    },
    student: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      groupedGrades: []
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
    }
  },
  watch: {
    student: {
      immediate: true,
      handler(newStudent) {
        if (newStudent && newStudent.grades) {
          this.groupGrades(newStudent.grades)
        }
      }
    }
  },
  methods: {
    getGradeColor(grade) {
      if (!grade) return 'grey'
      if (grade >= 4.5) return 'success'
      if (grade >= 3.5) return 'warning'
      return 'error'
    },
    groupGrades(grades) {
      const subjects = {}

      grades.forEach(grade => {
        if (!subjects[grade.subject_name]) {
          subjects[grade.subject_name] = {
            name: grade.subject_name,
            grades: {},
            total: 0,
            count: 0
          }
        }

        subjects[grade.subject_name].grades[grade.quarter] = grade.grade
        subjects[grade.subject_name].total += grade.grade
        subjects[grade.subject_name].count += 1
      })

      // Вычисляем среднее для каждого предмета
      this.groupedGrades = Object.values(subjects).map(subject => ({
        ...subject,
        average: subject.total / subject.count
      }))
    },
    close() {
      this.dialog = false
    }
  }
}
</script>