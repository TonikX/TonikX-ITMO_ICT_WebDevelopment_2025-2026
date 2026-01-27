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

              <v-select
                v-model="formData.subjects"
                :items="subjects"
                item-title="subject_name"
                item-value="id"
                label="Предметы*"
                :rules="[rules.required]"
                variant="outlined"
                :disabled="loading"
                multiple
                chips
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
    modelValue: {
      type: Boolean,
      default: false
    },
    teacher: {
      type: Object,
      default: null
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
        classroom: null,
        subjects: []
      },
      rules: {
        required: value => !!value || 'Обязательное поле'
      }
    }
  },
  computed: {
    dialog: {
      get() {
        return this.modelValue
      },
      set(value) {
        this.$emit('update:modelValue', value)
      }
    },
    isEdit() {
      return !!this.teacher
    },
  },
  watch: {
    teacher: {
      immediate: true,
      handler(newTeacher) {
        if (newTeacher) {
          this.formData = {
            last_name: newTeacher.last_name,
            first_name: newTeacher.first_name,
            classroom: newTeacher.classroom,
            subjects: newTeacher.subjects || []
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
        classroom: null,
        subjects: []
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