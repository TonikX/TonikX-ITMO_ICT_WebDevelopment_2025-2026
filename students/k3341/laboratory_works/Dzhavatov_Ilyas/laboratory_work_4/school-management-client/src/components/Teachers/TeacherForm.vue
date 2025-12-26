<template>
  <v-dialog v-model="dialog" max-width="800" persistent>
    <v-card :loading="loading">
      <v-toolbar :color="isEdit ? 'warning' : 'success'" dark>
        <v-toolbar-title>
          <v-icon class="mr-2">{{ isEdit ? 'mdi-pencil' : 'mdi-plus' }}</v-icon>
          {{ isEdit ? 'Редактирование учителя' : 'Добавление учителя' }}
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
                label="Классное руководство"
                variant="outlined"
                :disabled="loading"
                clearable
              />
            </v-col>

            <v-col cols="12" md="6">
              <v-select
                v-model="formData.classroom"
                :items="classrooms"
                item-title="room_number"
                item-value="id"
                label="Закрепленный кабинет"
                variant="outlined"
                :disabled="loading"
                clearable
              />
            </v-col>

            <v-col cols="12">
              <v-divider class="my-4" />
              <h3 class="text-h6 mb-4">Предметы преподавания</h3>

              <div v-for="(subject, index) in formData.subjects" :key="index" class="mb-4">
                <v-row>
                  <v-col cols="12" md="5">
                    <v-select
                      v-model="subject.subject_id"
                      :items="availableSubjects"
                      item-title="subject_name"
                      item-value="id"
                      label="Предмет*"
                      :rules="[rules.required]"
                      variant="outlined"
                      :disabled="loading"
                    />
                  </v-col>

                  <v-col cols="12" md="5">
                    <v-select
                      v-model="subject.class_ids"
                      :items="classes"
                      item-title="class_name"
                      item-value="id"
                      label="Классы*"
                      :rules="[rules.required]"
                      variant="outlined"
                      :disabled="loading"
                      multiple
                      chips
                    />
                  </v-col>

                  <v-col cols="12" md="2" class="d-flex align-center">
                    <v-btn
                      icon
                      color="error"
                      @click="removeSubject(index)"
                      :disabled="loading || formData.subjects.length === 1"
                    >
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>
              </div>

              <v-btn
                color="secondary"
                variant="outlined"
                @click="addSubject"
                :disabled="loading"
                class="mb-4"
              >
                <v-icon left>mdi-plus</v-icon>
                Добавить предмет
              </v-btn>
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
  name: 'TeacherForm',
  props: {
    value: {
      type: Boolean,
      default: false
    },
    teacher: {
      type: Object,
      default: null
    },
    classes: {
      type: Array,
      default: () => []
    },
    classrooms: {
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
        classroom: null,
        subjects: [
          { subject_id: null, class_ids: [] }
        ]
      },
      genderOptions: [
        { title: 'Мужской', value: 'M' },
        { title: 'Женский', value: 'F' }
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
      return !!this.teacher
    },
    availableSubjects() {
      return this.subjects.filter(subject => {
        return !this.formData.subjects.some(s => s.subject_id === subject.id)
      })
    }
  },
  watch: {
    teacher: {
      immediate: true,
      handler(newTeacher) {
        if (newTeacher) {
          this.formData = {
            last_name: newTeacher.last_name,
            first_name: newTeacher.first_name,
            gender: newTeacher.gender,
            school_class: newTeacher.school_class,
            classroom: newTeacher.classroom,
            subjects: newTeacher.subjects?.map(s => ({
              subject_id: s.id,
              class_ids: s.classes || []
            })) || [{ subject_id: null, class_ids: [] }]
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
        classroom: null,
        subjects: [
          { subject_id: null, class_ids: [] }
        ]
      }
      this.error = null
      if (this.$refs.form) {
        this.$refs.form.resetValidation()
      }
    },
    addSubject() {
      this.formData.subjects.push({ subject_id: null, class_ids: [] })
    },
    removeSubject(index) {
      this.formData.subjects.splice(index, 1)
    },
    save() {
      if (!this.$refs.form.validate()) return

      const teacherData = {
        ...this.formData,
        subjects: this.formData.subjects.filter(s => s.subject_id)
      }

      this.$emit('save', teacherData)
    },
    close() {
      this.dialog = false
      this.resetForm()
    }
  }
}
</script>