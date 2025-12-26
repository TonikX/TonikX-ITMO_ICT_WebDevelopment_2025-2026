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

              <v-divider class="my-2" />

              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="primary">mdi-gender-male-female</v-icon>
                </template>
                <v-list-item-title>
                  Пол: {{ teacher.gender === 'M' ? 'Мужской' : 'Женский' }}
                </v-list-item-title>
              </v-list-item>

              <v-list-item v-if="teacher.class_name">
                <template v-slot:prepend>
                  <v-icon color="primary">mdi-school</v-icon>
                </template>
                <v-list-item-title>
                  Классное руководство: {{ teacher.class_name }}
                </v-list-item-title>
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
                v-for="subject in teacher.subjects"
                :key="subject"
                class="pl-8"
              >
                <template v-slot:prepend>
                  <v-icon color="secondary" size="small">mdi-circle-small</v-icon>
                </template>
                <v-list-item-title>{{ subject }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-col>

          <v-col cols="12" class="mt-4">
            <v-card>
              <v-toolbar color="grey-lighten-3" flat>
                <v-toolbar-title>Расписание учителя</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-table v-if="teacher.schedules && teacher.schedules.length">
                  <thead>
                    <tr>
                      <th>День</th>
                      <th>Урок</th>
                      <th>Класс</th>
                      <th>Предмет</th>
                      <th>Кабинет</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="schedule in teacher.schedules" :key="schedule.id">
                      <td>{{ schedule.day_of_week_display }}</td>
                      <td>{{ schedule.lesson_number }}</td>
                      <td>{{ schedule.class_name }}</td>
                      <td>{{ schedule.subject_name }}</td>
                      <td>{{ schedule.classroom_number }}</td>
                    </tr>
                  </tbody>
                </v-table>
                <div v-else class="text-center py-4 text-grey">
                  Расписание не назначено
                </div>
              </v-card-text>
            </v-card>
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
        <v-btn color="primary" @click="getSameSubjectTeachers">
          <v-icon left>mdi-account-group</v-icon>
          Коллеги по предметам
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'TeacherDetail',
  props: {
    value: {
      type: Boolean,
      default: false
    },
    teacher: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      sameSubjectTeachers: [],
      loadingColleagues: false
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
    }
  },
  methods: {
    async getSameSubjectTeachers() {
      if (!this.teacher) return

      this.loadingColleagues = true
      try {
        // Здесь будет запрос к API
        const response = await this.$api.teachers.getSameSubjectTeachers(this.teacher.id)
        this.sameSubjectTeachers = response.data

        if (this.sameSubjectTeachers.length > 0) {
          this.$emit('show-colleagues', this.sameSubjectTeachers)
        } else {
          this.$toast.info('Учителя с такими же предметами не найдены')
        }
      } catch (error) {
        this.$toast.error('Ошибка получения данных')
      } finally {
        this.loadingColleagues = false
      }
    },
    close() {
      this.dialog = false
    }
  }
}
</script>