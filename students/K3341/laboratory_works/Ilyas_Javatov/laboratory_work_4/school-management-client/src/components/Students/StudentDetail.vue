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
                  Класс: {{ student.school_class_name || student.class_name }}
                </v-list-item-title>
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
        <v-btn color="warning" @click="$emit('edit', student)">
          <v-icon left>mdi-pencil</v-icon>
          Редактировать
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'StudentDetail',
  props: {
    modelValue: {
      type: Boolean,
      default: false
    },
    student: {
      type: Object,
      default: null
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
    }
  },
  methods: {
    close() {
      this.dialog = false
    }
  }
}
</script>