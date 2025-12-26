<template>
  <v-dialog v-model="dialog" max-width="600" persistent>
    <v-card :loading="loading">
      <v-toolbar :color="isEdit ? 'warning' : 'success'" dark>
        <v-toolbar-title>
          <v-icon class="mr-2">{{ isEdit ? 'mdi-pencil' : 'mdi-plus' }}</v-icon>
          {{ isEdit ? 'Редактирование ученика' : 'Добавление ученика' }}
        </v-toolbar-title>
        <v-spacer />
        <v-btn icon @click="close">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-toolbar>

      <v-card-text class="pa-6">
        <v-form ref="form" v-model="valid" @submit.prevent="save">
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.last_name"
                label="Фамилия*"
                :rules="[rules.required]"
                variant="outlined"
                :disabled="loading"
              />
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.first_name"
                label="Имя*"
                :rules="[rules.required]"
                variant="outlined"
                :disabled="loading"
              />
            </v-col>

            <v-col cols="12" md="6">
              <v-select
                v-model="formData.gender"
                :items="genderOptions"
                label="Пол*"
                :rules="[rules.required]"
                variant="outlined"
                :disabled="loading"
              />
            </v-col>

            <v-col cols="12" md="6">
              <v-select
                v-model="formData.school_class"
                :items="classes"
                item-title="class_name"
                item-value="id"
                label="Класс*"
                :rules="[rules.required]"
                variant="outlined"
                :disabled="loading"
              />
            </v-col>
          </v-row>

          <v-divider class="my-4" />

          <h3 class="text-h6 mb-4">Начальные оценки</h3>

          <div v-for="(grade, index) in formData.grades" :key="index" class="mb-4">
            <v-row>
              <v-col cols="12" md="5">
                <v-select
                  v-model="grade.subject_id"
                  :items="subjects"
                  item-title="subject_name"
                  item-value="id"
                  label="Предмет"
                  variant="outlined"
                  :disabled="loading"
                  clearable
                />
              </v-col>

              <v-col cols="12" md="3">
                <v-select
                  v-model="grade.quarter"
                  :items="quarterOptions"
                  label="Четверть"
                  variant="outlined"
                  :disabled="loading"
                />
              </v-col>

              <v-col cols="12" md="3">
                <v-select
                  v-model="grade.grade"
                  :items="gradeOptions"
                  label="Оценка"
                  variant="outlined"
                  :disabled="loading"
                />
              </v-col>

              <v-col cols="12" md="1" class="d-flex align-center">
                <v-btn
                  icon
                  color="error"
                  @click="removeGrade(index)"
                  :disabled="loading || formData.grades.length === 1"
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </div>

          <v-btn
            color="secondary"
            variant="outlined"
            @click="addGrade"
            :disabled="loading"
            class="mb-4"
          >
            <v-icon left>mdi-plus</v-icon>
            Добавить оценку
          </v-btn>

          <v-alert
            v-if="error"
            type="error"
            density="compact"
            class="mb-4"
          >
            {{ error }}
          </v-alert>
        </v-form>
      </v-card-text>

      <v-card-actions class="pa-4">
        <v-spacer />
        <v-btn color="grey" @click="close" :disabled="loading">
          Отмена
        </v-btn>
        <v-btn
          :color="isEdit ? 'warning' : 'success'"
          @click="save"
          :loading="loading"
          :disabled="!valid || loading"
        >
          {{ isEdit ? 'Обновить' : 'Сохранить' }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'StudentForm',
  props: {
    value: {
      type: Boolean,
      default: false
    },
    student: {
      type: Object,
      default: null
    },
    classes: {
      type: Array,
      default: () => []
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
      valid: false,
      error: null,
      formData: {
        last_name: '',
        first_name: '',
        gender: '',
        school_class: null,
        grades: [
          { subject_id: null, quarter: 1, grade: 5 }
        ]
      },
      genderOptions: [
        { title: 'Мужской', value: 'M' },
        { title: 'Женский', value: 'F' }
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
        required: value => !!value || 'Обязательное поле'
      }
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
    isEdit() {
      return !!this.student
    }
  },
  watch: {
    student: {
      immediate: true,
      handler(newStudent) {
        if (newStudent) {
          this.formData = {
            last_name: newStudent.last_name,
            first_name: newStudent.first_name,
            gender: newStudent.gender,
            school_class: newStudent.school_class,
            grades: newStudent.grades?.map(g => ({
              subject_id: g.subject,
              quarter: g.quarter,
              grade: g.grade
            })) || [{ subject_id: null, quarter: 1, grade: 5 }]
          }
        } else {
          this.resetForm()
        }
      }
    }
  },
  methods: {
    resetForm() {
      this.formData = {
        last_name: '',
        first_name: '',
        gender: '',
        school_class: null,
        grades: [
          { subject_id: null, quarter: 1, grade: 5 }
        ]
      }
      this.error = null
      if (this.$refs.form) {
        this.$refs.form.resetValidation()
      }
    },
    addGrade() {
      this.formData.grades.push({ subject_id: null, quarter: 1, grade: 5 })
    },
    removeGrade(index) {
      this.formData.grades.splice(index, 1)
    },
    save() {
      if (!this.$refs.form.validate()) return

      const studentData = {
        ...this.formData,
        grades: this.formData.grades.filter(g => g.subject_id)
      }

      this.$emit('save', studentData)
    },
    close() {
      this.dialog = false
      this.resetForm()
    }
  }
}
</script>