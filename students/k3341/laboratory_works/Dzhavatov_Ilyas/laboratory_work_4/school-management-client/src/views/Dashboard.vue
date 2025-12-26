<template>
  <v-container>
    <v-breadcrumbs :items="breadcrumbs" class="pl-0">
      <template v-slot:divider>
        <v-icon>mdi-chevron-right</v-icon>
      </template>
    </v-breadcrumbs>

    <v-row>
      <v-col cols="12">
        <h1 class="text-h3 mb-2">Панель управления</h1>
        <p class="text-body-1 text-grey mb-6">Обзор системы и быстрый доступ</p>
      </v-col>
    </v-row>

    <v-row class="mb-6">
      <v-col v-for="stat in stats" :key="stat.title" cols="12" sm="6" md="3">
        <v-card :color="stat.color" dark class="h-100">
          <v-card-text class="pa-4">
            <div class="d-flex align-center">
              <v-icon size="48" class="mr-4">{{ stat.icon }}</v-icon>
              <div>
                <div class="text-h4">{{ stat.value }}</div>
                <div class="text-body-1">{{ stat.title }}</div>
              </div>
            </div>
            <v-divider class="my-3" />
            <div class="text-caption">{{ stat.description }}</div>
          </v-card-text>
          <v-card-actions class="pa-3">
            <v-btn :to="stat.to" variant="text" size="small">
              Подробнее
              <v-icon right>mdi-arrow-right</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>
              <v-icon left>mdi-account-multiple</v-icon>
              Недавние учителя
            </v-toolbar-title>
            <v-spacer />
            <v-btn :to="{ name: 'Teachers' }" variant="text">
              Все учителя
            </v-btn>
          </v-toolbar>
          <v-card-text>
            <v-list v-if="recentTeachers.length">
              <v-list-item
                v-for="teacher in recentTeachers"
                :key="teacher.id"
                :to="`/teachers/${teacher.id}`"
              >
                <template v-slot:prepend>
                  <v-avatar color="primary" size="40">
                    <span class="text-white">{{ teacher.first_name[0] }}{{ teacher.last_name[0] }}</span>
                  </v-avatar>
                </template>
                <v-list-item-title>
                  {{ teacher.last_name }} {{ teacher.first_name }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  <v-chip size="small" v-if="teacher.class_name" color="info">
                    {{ teacher.class_name }}
                  </v-chip>
                  <span v-else class="text-grey">Без класса</span>
                </v-list-item-subtitle>
                <template v-slot:append>
                  <v-chip :color="teacher.gender === 'M' ? 'blue' : 'pink'" size="small">
                    {{ teacher.gender === 'M' ? 'М' : 'Ж' }}
                  </v-chip>
                </template>
              </v-list-item>
            </v-list>
            <div v-else class="text-center py-8">
              <v-icon size="64" color="grey" class="mb-4">mdi-account-off</v-icon>
              <p class="text-grey">Учителя не найдены</p>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card>
          <v-toolbar color="success" dark flat>
            <v-toolbar-title>
              <v-icon left>mdi-calendar</v-icon>
              Ближайшие уроки
            </v-toolbar-title>
            <v-spacer />
            <v-btn :to="{ name: 'Schedule' }" variant="text">
              Все расписание
            </v-btn>
          </v-toolbar>
          <v-card-text>
            <v-timeline v-if="upcomingLessons.length" side="end" align="start">
              <v-timeline-item
                v-for="lesson in upcomingLessons"
                :key="lesson.id"
                :dot-color="getLessonColor(lesson)"
                size="small"
              >
                <template v-slot:opposite>
                  <span class="text-caption text-grey">
                    {{ lesson.day_of_week_display }}
                    <br>
                    {{ lesson.lesson_number }} урок
                  </span>
                </template>
                <v-card variant="outlined">
                  <v-card-text class="pa-3">
                    <div class="d-flex justify-space-between align-center">
                      <div>
                        <strong>{{ lesson.subject_name }}</strong>
                        <div class="text-caption text-grey">
                          {{ lesson.class_name }}, {{ lesson.teacher_name }}
                        </div>
                      </div>
                      <v-chip size="small" color="grey-lighten-3">
                        {{ lesson.classroom_number }}
                      </v-chip>
                    </div>
                  </v-card-text>
                </v-card>
              </v-timeline-item>
            </v-timeline>
            <div v-else class="text-center py-8">
              <v-icon size="64" color="grey" class="mb-4">mdi-calendar-blank</v-icon>
              <p class="text-grey">Уроки не найдены</p>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-6">
      <v-col cols="12">
        <v-card>
          <v-toolbar color="info" dark flat>
            <v-toolbar-title>
              <v-icon left>mdi-chart-bar</v-icon>
              Быстрые действия
            </v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-row>
              <v-col v-for="action in quickActions" :key="action.title" cols="12" sm="6" md="3">
                <v-card
                  :to="action.to"
                  variant="outlined"
                  class="text-center pa-4 action-card"
                  hover
                >
                  <v-icon size="48" :color="action.color" class="mb-3">{{ action.icon }}</v-icon>
                  <h3 class="text-h6 mb-2">{{ action.title }}</h3>
                  <p class="text-caption text-grey">{{ action.description }}</p>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import api from '../api/teachers'
import scheduleApi from '../api/schedules'
import studentApi from '../api/students'

export default {
  name: 'Dashboard',
  data() {
    return {
      loading: false,
      stats: [
        {
          title: 'Учителя',
          value: 0,
          icon: 'mdi-account-multiple',
          color: 'blue',
          description: 'Преподавательский состав',
          to: { name: 'Teachers' }
        },
        {
          title: 'Ученики',
          value: 0,
          icon: 'mdi-school',
          color: 'green',
          description: 'Всего учащихся',
          to: { name: 'Students' }
        },
        {
          title: 'Классы',
          value: 0,
          icon: 'mdi-google-classroom',
          color: 'orange',
          description: 'Учебные классы',
          to: { name: 'Classes' }
        },
        {
          title: 'Кабинеты',
          value: 0,
          icon: 'mdi-door',
          color: 'red',
          description: 'Учебные помещения',
          to: { name: 'Classrooms' }
        }
      ],
      recentTeachers: [],
      upcomingLessons: [],
      quickActions: [
        {
          title: 'Добавить учителя',
          icon: 'mdi-account-plus',
          color: 'blue',
          description: 'Новый преподаватель',
          to: { name: 'Teachers', query: { action: 'add' } }
        },
        {
          title: 'Добавить ученика',
          icon: 'mdi-account-plus',
          color: 'green',
          description: 'Новый учащийся',
          to: { name: 'Students', query: { action: 'add' } }
        },
        {
          title: 'Составить расписание',
          icon: 'mdi-calendar-plus',
          color: 'orange',
          description: 'Новое занятие',
          to: { name: 'Schedule', query: { action: 'add' } }
        },
        {
          title: 'Создать отчет',
          icon: 'mdi-file-chart',
          color: 'purple',
          description: 'Успеваемость класса',
          to: { name: 'Reports' }
        }
      ]
    }
  },
  computed: {
    breadcrumbs() {
      return [
        { title: 'Главная', disabled: false, to: '/' },
        { title: 'Панель управления', disabled: true }
      ]
    }
  },
  async mounted() {
    await this.loadDashboardData()
  },
  methods: {
    getLessonColor(lesson) {
      const colors = ['blue', 'green', 'orange', 'red', 'purple', 'cyan']
      const index = lesson.lesson_number % colors.length
      return colors[index]
    },

    async loadDashboardData() {
      this.loading = true
      try {
        // Загружаем данные параллельно
        const [teachersRes, studentsRes, schedulesRes] = await Promise.all([
          api.getTeachers({ limit: 5 }),
          studentApi.getStudents({ limit: 1 }),
          scheduleApi.getSchedules({ limit: 5 })
        ])

        // Обновляем статистику
        this.stats[0].value = teachersRes.data.count || teachersRes.data.length || 0
        this.stats[1].value = studentsRes.data.count || studentsRes.data.length || 0

        // Ближайшие учителя
        this.recentTeachers = Array.isArray(teachersRes.data)
          ? teachersRes.data.slice(0, 5)
          : teachersRes.data.results?.slice(0, 5) || []

        // Ближайшие уроки
        this.upcomingLessons = Array.isArray(schedulesRes.data)
          ? schedulesRes.data.slice(0, 5)
          : schedulesRes.data.results?.slice(0, 5) || []

      } catch (error) {
        console.error('Error loading dashboard data:', error)
        this.$toast.error('Ошибка загрузки данных')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.action-card {
  transition: transform 0.2s;
  cursor: pointer;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.h-100 {
  height: 100%;
}
</style>