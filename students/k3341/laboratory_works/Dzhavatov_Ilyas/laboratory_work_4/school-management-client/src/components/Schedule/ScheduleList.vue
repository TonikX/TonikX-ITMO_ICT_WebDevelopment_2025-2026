<template>
  <v-card>
    <v-toolbar color="primary" dark flat>
      <v-toolbar-title>
        <v-icon class="mr-2">mdi-calendar</v-icon>
        Расписание занятий
      </v-toolbar-title>
      <v-spacer />
      <v-btn color="success" @click="$emit('add')">
        <v-icon left>mdi-plus</v-icon>
        Добавить
      </v-btn>
      <v-btn color="info" @click="$emit('find-lesson')" class="ml-2">
        <v-icon left>mdi-magnify</v-icon>
        Найти урок
      </v-btn>
    </v-toolbar>

    <v-card-text>
      <v-row class="mb-4">
        <v-col cols="12" md="3">
          <v-select
            v-model="filters.day_of_week"
            :items="dayOptions"
            label="День недели"
            variant="outlined"
            clearable
            @update:model-value="applyFilters"
          />
        </v-col>
        <v-col cols="12" md="3">
          <v-select
            v-model="filters.school_class"
            :items="classes"
            item-title="class_name"
            item-value="id"
            label="Класс"
            variant="outlined"
            clearable
            @update:model-value="applyFilters"
          />
        </v-col>
        <v-col cols="12" md="3">
          <v-select
            v-model="filters.teacher"
            :items="teachers"
            item-title="full_name"
            item-value="id"
            label="Учитель"
            variant="outlined"
            clearable
            @update:model-value="applyFilters"
          />
        </v-col>
        <v-col cols="12" md="3">
          <v-select
            v-model="filters.subject"
            :items="subjects"
            item-title="subject_name"
            item-value="id"
            label="Предмет"
            variant="outlined"
            clearable
            @update:model-value="applyFilters"
          />
        </v-col>
      </v-row>

      <div v-if="groupedSchedules.length === 0" class="text-center py-8">
        <v-icon size="64" color="grey" class="mb-4">mdi-calendar-blank</v-icon>
        <p class="text-h6 text-grey">Расписание не найдено</p>
        <p class="text-body-1 text-grey">Добавьте первое занятие</p>
      </div>

      <div v-else>
        <v-card
          v-for="(dayGroup, dayIndex) in groupedSchedules"
          :key="dayIndex"
          class="mb-4"
          variant="outlined"
        >
          <v-toolbar color="grey-lighten-3" density="compact">
            <v-toolbar-title class="font-weight-bold">
              {{ dayGroup.day_name }}
            </v-toolbar-title>
          </v-toolbar>

          <v-table>
            <thead>
              <tr>
                <th>Класс</th>
                <th>Урок</th>
                <th>Предмет</th>
                <th>Учитель</th>
                <th>Кабинет</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="lesson in dayGroup.lessons.sort((a, b) => a.lesson_number - b.lesson_number)"
                :key="lesson.id"
              >
                <td>{{ lesson.class_name }}</td>
                <td>{{ lesson.lesson_number }}</td>
                <td>{{ lesson.subject_name }}</td>
                <td>{{ lesson.teacher_name }}</td>
                <td>{{ lesson.classroom_number }}</td>
                <td>
                  <v-btn icon size="small" @click="$emit('edit', lesson)">
                    <v-icon color="primary">mdi-pencil</v-icon>
                  </v-btn>
                  <v-btn icon size="small" @click="$emit('delete', lesson)">
                    <v-icon color="error">mdi-delete</v-icon>
                  </v-btn>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-card>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'ScheduleList',
  props: {
    schedules: {
      type: Array,
      default: () => []
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
    loading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      filters: {
        day_of_week: null,
        school_class: null,
        teacher: null,
        subject: null
      },
      dayOptions: [
        { title: 'Понедельник', value: 1 },
        { title: 'Вторник', value: 2 },
        { title: 'Среда', value: 3 },
        { title: 'Четверг', value: 4 },
        { title: 'Пятница', value: 5 },
        { title: 'Суббота', value: 6 }
      ]
    }
  },
  computed: {
    groupedSchedules() {
      const groups = {}

      this.schedules.forEach(lesson => {
        const dayName = lesson.day_of_week_display
        if (!groups[dayName]) {
          groups[dayName] = {
            day_name: dayName,
            day_number: lesson.day_of_week,
            lessons: []
          }
        }
        groups[dayName].lessons.push(lesson)
      })

      // Сортируем по дням недели
      return Object.values(groups).sort((a, b) => a.day_number - b.day_number)
    }
  },
  methods: {
    applyFilters() {
      this.$emit('filter', this.filters)
    }
  }
}
</script>