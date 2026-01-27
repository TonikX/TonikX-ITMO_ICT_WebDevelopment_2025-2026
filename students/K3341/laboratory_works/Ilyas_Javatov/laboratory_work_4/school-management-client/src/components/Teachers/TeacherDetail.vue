<template>
  <v-dialog v-model="dialog" max-width="800">
    <v-card>
      <v-toolbar color="info" dark>
        <v-toolbar-title>
          <v-icon class="mr-2">mdi-account-details</v-icon>
          Информация об учителе
        </v-toolbar-title>
        <v-spacer />
        <v-btn icon @click="close">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-toolbar>

      <v-card-text class="pa-6">
        <v-row v-if="teacher">
          <v-col cols="12">
            <v-list>
              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="primary">mdi-account</v-icon>
                </template>
                <v-list-item-title class="text-h6">
                  {{ teacher.last_name }} {{ teacher.first_name }}
                </v-list-item-title>
              <v-list-item-subtitle>
                ID: {{ teacher.id }}
              </v-list-item-subtitle>
            </v-list-item>

              <v-list-item v-if="teacher.classroom_number">
                <template v-slot:prepend>
                  <v-icon color="primary">mdi-door</v-icon>
                </template>
                <v-list-item-title>
                  Кабинет: {{ teacher.classroom_number }}
                </v-list-item-title>
              </v-list-item>

              <v-divider class="my-2" />

              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="primary">mdi-book-open-variant</v-icon>
                </template>
                <v-list-item-title class="font-weight-bold">
                  Преподаваемые предметы:
                </v-list-item-title>
              </v-list-item>

              <v-list-item
                v-for="subject in subjectNames"
                :key="subject"
                class="pl-8"
              >
                <template v-slot:prepend>
                  <v-icon color="secondary" size="small">mdi-circle-small</v-icon>
                </template>
                <v-list-item-title>{{ subject }}</v-list-item-title>
              </v-list-item>
              <v-list-item v-if="!subjectNames.length" class="pl-8 text-grey">
                <v-list-item-title>Предметы не назначены</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-col>

        </v-row>

        <div v-else class="text-center py-8">
          <v-progress-circular indeterminate />
        </div>
      </v-card-text>

      <v-card-actions class="pa-4">
        <v-spacer />
        <v-btn color="secondary" @click="$emit('edit', teacher)">
          <v-icon left>mdi-pencil</v-icon>
          Редактировать
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'TeacherDetail',
  props: {
    modelValue: {
      type: Boolean,
      default: false
    },
    teacher: {
      type: Object,
      default: null
    },
    subjects: {
      type: Array,
      default: () => []
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
    subjectNames() {
      if (!this.teacher) return []
      if (Array.isArray(this.teacher.subjects_names) && this.teacher.subjects_names.length) {
        return this.teacher.subjects_names
      }
      if (Array.isArray(this.teacher.subjects) && this.teacher.subjects.length) {
        return this.teacher.subjects
          .map(id => this.subjects.find(subject => subject.id === id)?.subject_name)
          .filter(Boolean)
      }
      return []
    }
  },
  methods: {
    close() {
      this.dialog = false
    }
  }
}
</script>