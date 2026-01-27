<template>
  <v-dialog v-model="dialog" max-width="600" persistent>
    <v-card :loading="loading">
      <v-toolbar :color="isEdit ? 'warning' : 'success'" dark>
        <v-toolbar-title>
          <v-icon class="mr-2">{{ isEdit ? 'mdi-pencil' : 'mdi-plus' }}</v-icon>
          {{ isEdit ? 'Редактирование кабинета' : 'Добавление кабинета' }}
        </v-toolbar-title>
        <v-spacer />
        <v-btn icon @click="close">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-toolbar>

      <v-card-text class="pa-6">
        <v-form ref="form" v-model="valid" @submit.prevent="save">
          <v-text-field
            v-model="formData.room_number"
            label="Номер кабинета*"
            :rules="[rules.required]"
            variant="outlined"
            :disabled="loading"
          />

          <v-select
            v-model="formData.subject_type"
            :items="subjectTypes"
            item-title="title"
            item-value="value"
            label="Тип дисциплин*"
            :rules="[rules.required]"
            variant="outlined"
            :disabled="loading"
          />
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
  name: 'ClassroomForm',
  props: {
    modelValue: {
      type: Boolean,
      default: false
    },
    classroom: {
      type: Object,
      default: null
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      valid: false,
      formData: {
        room_number: '',
        subject_type: 'base'
      },
      subjectTypes: [
        { title: 'Базовые', value: 'base' },
        { title: 'Профильные', value: 'profile' }
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
      return !!this.classroom
    }
  },
  watch: {
    classroom: {
      immediate: true,
      handler(newValue) {
        if (newValue) {
          this.formData = {
            room_number: newValue.room_number,
            subject_type: newValue.subject_type || 'base'
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
        room_number: '',
        subject_type: 'base'
      }
      if (this.$refs.form) {
        this.$refs.form.resetValidation()
      }
    },
    save() {
      if (!this.$refs.form.validate()) return
      this.$emit('save', {
        room_number: this.formData.room_number,
        subject_type: this.formData.subject_type
      })
    },
    close() {
      this.dialog = false
      this.resetForm()
    }
  }
}
</script>
