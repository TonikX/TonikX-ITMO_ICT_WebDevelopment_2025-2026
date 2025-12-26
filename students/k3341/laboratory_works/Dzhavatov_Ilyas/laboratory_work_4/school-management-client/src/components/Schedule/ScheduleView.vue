<template>
  <v-card>
    <v-toolbar color="info" dark flat>
      <v-toolbar-title>
        <v-icon class="mr-2">mdi-calendar-search</v-icon>
        Поиск урока
      </v-toolbar-title>
      <v-spacer />
      <v-btn icon @click="close">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-toolbar>

    <v-card-text class="pa-6">
      <v-form ref="form" v-model="valid" @submit.prevent="findLesson">
        <v-row>
          <v-col cols="12" md="4">
            <v-select
              v-model="searchParams.class_id"
              :items="classes"
              item-title="class_name"
              item-value="id"
              label="Класс*"
              :rules="[rules.required]"
              variant="outlined"
            />
          </v-col>

          <v-col cols="12" md="4">
            <v-select
              v-model="searchParams.day_of_week"
              :items="dayOptions"
              label="День недели*"
              :rules="[rules.required]"
              variant="outlined"
            />
          </v-col>

          <v-col cols="12" md="4">
            <v-select
              v-model="searchParams.lesson_number"
              :items="lessonOptions"
              label="Номер урока*"
              :rules="[rules.required]"
              variant="outlined"
            />
          </v-col>
        </v-row>

        <div class="text-center mt-6">
          <v-btn
            color="primary"
            size="large"
            @click="findLesson"
            :loading="loading"
            :disabled="!valid || loading"
          >
            <v-icon left>mdi-magnify</v-icon>
            Найти урок
          </v-btn>
        </div>
      </v-form>

      <v-divider class="my-6" />

      <div v-if="loading" class="text-center py-8">
        <v-progress-circular indeterminate />
        <p class="mt-4">Поиск урока...</p>
      </div>

      <div v-else-if="foundLessons && foundLessons.length > 0">
        <h3 class="text-h5 mb-4">Найденные уроки:</h3>

        <v-card
          v-for="lesson in foundLessons"
          :key="lesson.id"
          class="mb-4"
          variant="outlined"
        >
          <v-card-text>
            <v-row>
              <v-col cols="12" md="3">
                <v-list>
                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon color="primary">mdi-google-classroom</v-icon>
                    </template>
                    <v-list-item-title>Класс</v-list-item-title>
                    <v-list-item-subtitle>{{ lesson.class_name }}</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-col>

              <v-col cols="12" md="3">
                <v-list>
                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon color="primary">mdi-book-open-variant</v-icon>
                    </template>
                    <v-list-item-title>Предмет</v-list-item-title>
                    <v-list-item-subtitle>{{ lesson.subject_name }}</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-col>

              <v-col cols="12" md="3">
                <v-list>
                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon color="primary">mdi-account</v-icon>
                    </template>
                    <v-list-item-title>Учитель</v-list-item-title>
                    <v-list-item-subtitle>{{ lesson.teacher_name }}</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-col>

              <v-col cols="12" md="3">
                <v-list>
                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon color="primary">mdi-door</v-icon>
                    </template>
                    <v-list-item-title>Кабинет</v-list-item-title>
                    <v-list-item-subtitle>{{ lesson.classroom_number }}</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </div>

      <div v-else-if="searched" class="text-center py-8">
        <v-icon size="64" color="grey" class="mb-4">mdi-calendar-remove</v-icon>
        <p class="text-h6 text-grey">Урок не найден</p>
        <p class="text-body-1 text-grey">В это время уроков нет</p>
      </div>
    </v-card-text>

    <v-card-actions class="pa-4">
      <v-spacer />
      <v-btn color="grey" @click="close">
        Закрыть
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'ScheduleView',
  props: {
    value: {
      type: Boolean,
      default: false
    },
    classes: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      valid: false,
      loading: false,
      searched: false,
      foundLessons: null,
      searchParams: {
        class_id: null,
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
    }
  },
  methods: {
    async findLesson() {
      if (!this.$refs.form.validate()) return

      this.loading = true
      this.searched = true

      try {
        const response = await this.$api.schedules.getLesson(this.searchParams)
        this.foundLessons = Array.isArray(response.data) ? response.data : [response.data]
        this.$toast.success('Урок найден')
      } catch (error) {
        if (error.response?.status === 404) {
          this.foundLessons = []
          this.$toast.info('В это время уроков нет')
        } else {
          this.$toast.error('Ошибка поиска')
        }
      } finally {
        this.loading = false
      }
    },
    close() {
      this.dialog = false
      this.searched = false
      this.foundLessons = null
      this.searchParams = {
        class_id: null,
        day_of_week: null,
        lesson_number: null
      }
      if (this.$refs.form) {
        this.$refs.form.resetValidation()
      }
    }
  }
}
</script>