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
    modelValue: {
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
        school_class: null
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
        return this.modelValue
      },
      set(value) {
        this.$emit('update:modelValue', value)
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
            school_class: newStudent.school_class
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
        school_class: null
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