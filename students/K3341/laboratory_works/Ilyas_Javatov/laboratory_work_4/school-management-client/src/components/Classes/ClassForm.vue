<template>
  <v-dialog v-model="dialog" max-width="600" persistent>
    <v-card :loading="loading">
      <v-toolbar :color="isEdit ? 'warning' : 'success'" dark>
        <v-toolbar-title>
          <v-icon class="mr-2">{{ isEdit ? 'mdi-pencil' : 'mdi-plus' }}</v-icon>
          {{ isEdit ? 'Редактирование класса' : 'Добавление класса' }}
        </v-toolbar-title>
        <v-spacer />
        <v-btn icon @click="close">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-toolbar>

      <v-card-text class="pa-6">
        <v-form ref="form" v-model="valid" @submit.prevent="save">
          <v-text-field
            v-model="formData.name"
            label="Название класса*"
            :rules="[rules.required]"
            variant="outlined"
            :disabled="loading"
          />

          <v-select
            v-model="formData.class_teacher"
            :items="teachers"
            item-title="full_name"
            item-value="id"
            label="Классный руководитель"
            variant="outlined"
            :disabled="loading"
            clearable
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
  name: 'ClassForm',
  props: {
    modelValue: {
      type: Boolean,
      default: false
    },
    classItem: {
      type: Object,
      default: null
    },
    teachers: {
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
      formData: {
        name: '',
        class_teacher: null
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
      return !!this.classItem
    }
  },
  watch: {
    classItem: {
      immediate: true,
      handler(newValue) {
        if (newValue) {
          this.formData = {
            name: newValue.class_name || newValue.name,
            class_teacher: newValue.class_teacher || null
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
        name: '',
        class_teacher: null
      }
      if (this.$refs.form) {
        this.$refs.form.resetValidation()
      }
    },
    save() {
      if (!this.$refs.form.validate()) return
      this.$emit('save', {
        name: this.formData.name,
        class_teacher: this.formData.class_teacher || null
      })
    },
    close() {
      this.dialog = false
      this.resetForm()
    }
  }
}
</script>
