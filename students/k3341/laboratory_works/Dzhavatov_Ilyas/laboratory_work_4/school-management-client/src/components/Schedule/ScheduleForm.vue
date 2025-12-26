<template>
  <v-dialog v-model="dialog" max-width="600" persistent>
    <v-card :loading="loading">
      <v-toolbar :color="isEdit ? 'warning' : 'success'" dark>
        <v-toolbar-title>
          <v-icon class="mr-2">{{ isEdit ? 'mdi-pencil' : 'mdi-plus' }}</v-icon>
          {{ isEdit ? 'Редактирование занятия' : 'Добавление занятия' }}
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

            <v-col cols="12" md="6">
              <v-select
                v-model="formData.subject"
                :items="subjects"
                item-title="subject_name"
                item-value="id"
                label="Предмет*"
                :rules="[rules.required]"
                variant="outlined"
                :disabled="loading"
              />
            </v-col>

            <v-col cols="12" md="6">
              <v-select
                v-model="formData.teacher"
                :items="filteredTeachers"
                item-title="full_name"
                item-value="id"
                label="Учитель*"
                :rules="[rules.required]"
                variant="outlined"
                :disabled="loading"
              />
            </v-col>

            <v-col cols="12" md="6">
              <v-select
                v-model="formData.classroom"
                :items="classrooms"
                item-title="room_number"
                item-value="id"
                label="Кабинет*"
                :rules="[rules.required]"
                variant="outlined"
                :disabled="loading"
              />
            </v-col>

            <v-col cols="12" md="6">
              <v-select
                v-model="formData.day_of_week"
                :items="dayOptions"
                label="День недели*"
                :rules="[rules.required]"
                variant="outlined"
                :disabled="loading"
              />
            </v-col>

            <v-col cols="12" md="6">
              <v-select
                v-model="formData.lesson_number"
                :items="lessonOptions"
                label="Номер урока*"
                :rules="[rules.required]"
                variant="outlined"
                :disabled="loading"
              />
            </v-col>
          </v-row>

          <v-alert
            v-if="error"
            type="error"
            density="compact"
            class="mb-4"
          >
            {{ error }}
          </v-alert>

          <v-alert
            v-if="conflict"
            type="warning"
            density="compact"
            class="mb-4"
          >
            Внимание: Уже есть занятие в это время у выбранного класса/учителя/кабинета
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
  name: 'ScheduleForm',
  props: {
    value: {
      type: Boolean,
      default: false
    },
    schedule: {
      type: Object,
      default: null
    },
    classes: {
      type: Array,
      default: () => []
    },
    teachers: {
      type: Array,
      default: () => []
    },
    subjects: {
      type: Array,
      default: () => []
    },
    classrooms: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    },
    conflict: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      valid: false,
      error: null,
      formData: {
        school_class: null,
        subject: null,
        teacher: null,
        classroom: null,
        day_of_week: null,
        lesson_number: null
      },
      dayOptions: [
        { title: 'Понедельник', value: 1 },
        { title: 'Вторник', value: 2 },
        { title: 'Среда', value: 3 },
        { title: 'Четверг', value: 4 },
        { title: 'Пятница', value: 5 },
        { title: 'Суббота', value: 6 }
      ],
      lessonOptions: [
        { title: '1 урок', value: 1 },
        { title: '2 урок', value: 2 },
        { title: '3 урок', value: 3 },
        { title: '4 урок', value: 4 },
        { title: '5 урок', value: 5 },
        { title: '6 урок', value: 6 },
        { title: '7 урок', value: 7 },
        { title: '8 урок', value: 8 }
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
      return !!this.schedule
    },
    filteredTeachers() {
      if (!this.formData.subject) return this.teachers

      // Фильтруем учителей по выбранному предмету
      return this.teachers.filter(teacher =>
        teacher.subjects?.includes(this.formData.subject)
      )
    }
  },
  watch: {
    schedule: {
      immediate: true,
      handler(newSchedule) {
        if (newSchedule) {
          this.formData = {
            school_class: newSchedule.school_class,
            subject: newSchedule.subject,
            teacher: newSchedule.teacher,
            classroom: newSchedule.classroom,
            day_of_week: newSchedule.day_of_week,
            lesson_number: newSchedule.lesson_number
          }
        } else {
          this.resetForm()
        }
      }
    },
    'formData.subject': {
      handler(newSubject) {
        if (newSubject && this.formData.teacher) {
          // Проверяем, преподает ли выбранный учитель этот предмет
          const teacher = this.teachers.find(t => t.id === this.formData.teacher)
          if (teacher && !teacher.subjects?.includes(newSubject)) {
            this.formData.teacher = null
          }
        }
      }
    }
  },
  methods: {
    resetForm() {
      this.formData = {
        school_class: null,
        subject: null,
        teacher: null,
        classroom: null,
        day_of_week: null,
        lesson_number: null
      }
      this.error = null
      if (this.$refs.form) {
        this.$refs.form.resetValidation()
      }
    },
    save() {
      if (!this.$refs.form.validate()) return

      this.$emit('save', this.formData)
    },
    close() {
      this.dialog = false
      this.resetForm()
    }
  }
}
</script>