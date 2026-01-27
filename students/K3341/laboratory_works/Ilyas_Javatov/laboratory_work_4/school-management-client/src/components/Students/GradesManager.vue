<template>
  <div>
    <h3 class="text-h5 mb-4">Управление оценками</h3>

    <v-form @submit.prevent="saveGrades">
      <div v-for="(grade, index) in grades" :key="index" class="mb-6">
        <v-card variant="outlined">
          <v-toolbar color="grey-lighten-3" density="compact">
            <v-toolbar-title>Оценка {{ index + 1 }}</v-toolbar-title>
            <v-spacer />
            <v-btn
              icon
              size="small"
              @click="removeGrade(index)"
              :disabled="grades.length === 1"
            >
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </v-toolbar>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-select
                  v-model="grade.subject_id"
                  :items="subjects"
                  item-title="subject_name"
                  item-value="id"
                  label="Предмет"
                  :rules="[rules.required]"
                  variant="outlined"
                  required
                />
              </v-col>

              <v-col cols="12" md="3">
                <v-select
                  v-model="grade.quarter"
                  :items="quarterOptions"
                  label="Четверть"
                  :rules="[rules.required]"
                  variant="outlined"
                  required
                />
              </v-col>

              <v-col cols="12" md="3">
                <v-select
                  v-model="grade.grade"
                  :items="gradeOptions"
                  label="Оценка"
                  :rules="[rules.required, rules.grade]"
                  variant="outlined"
                  required
                />
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </div>

      <div class="d-flex gap-2 mb-6">
        <v-btn color="secondary" @click="addGrade" variant="outlined">
          <v-icon left>mdi-plus</v-icon>
          Добавить оценку
        </v-btn>

        <v-btn color="primary" type="submit" :loading="loading">
          <v-icon left>mdi-content-save</v-icon>
          Сохранить все оценки
        </v-btn>
      </div>
    </v-form>
  </div>
</template>

<script>
export default {
  name: 'GradesManager',
  props: {
    student: {
      type: Object,
      required: true
    },
    subjects: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      grades: [
        {
          subject_id: null,
          quarter: 1,
          grade: 5
        }
      ],
      quarterOptions: [
        { title: '1 четверть', value: 1 },
        { title: '2 четверть', value: 2 },
        { title: '3 четверть', value: 3 },
        { title: '4 четверть', value: 4 }
      ],
      gradeOptions: [
        { title: '5 (Отлично)', value: 5 },
        { title: '4 (Хорошо)', value: 4 },
        { title: '3 (Удовлетворительно)', value: 3 },
        { title: '2 (Неудовлетворительно)', value: 2 }
      ],
      rules: {
        required: value => !!value || 'Обязательное поле',
        grade: value => value >= 2 && value <= 5 || 'Оценка должна быть от 2 до 5'
      }
    }
  },
  watch: {
    student: {
      immediate: true,
      handler(newStudent) {
        if (newStudent && newStudent.grades) {
          this.grades = newStudent.grades.map(g => ({
            subject_id: g.subject,
            quarter: g.quarter,
            grade: g.grade
          }))
        }
      }
    }
  },
  methods: {
    addGrade() {
      this.grades.push({
        subject_id: null,
        quarter: 1,
        grade: 5
      })
    },
    removeGrade(index) {
      this.grades.splice(index, 1)
    },
    async saveGrades() {
      const gradesData = this.grades.filter(g => g.subject_id)
      this.$emit('save', gradesData)
    }
  }
}
</script>