<template>
  <v-container>
    <v-breadcrumbs :items="breadcrumbs" class="pl-0">
      <template v-slot:divider>
        <v-icon>mdi-chevron-right</v-icon>
      </template>
    </v-breadcrumbs>

    <h1 class="text-h3 mb-4">Отчеты и статистика</h1>

    <v-tabs v-model="activeTab" color="primary" class="mb-6">
      <v-tab value="performance">
        <v-icon left>mdi-chart-line</v-icon>
        Успеваемость
      </v-tab>
      <v-tab value="gender">
        <v-icon left>mdi-gender-male-female</v-icon>
        Статистика по полу
      </v-tab>
      <v-tab value="classrooms">
        <v-icon left>mdi-door</v-icon>
        Кабинеты
      </v-tab>
      <v-tab value="teachers">
        <v-icon left>mdi-account-multiple</v-icon>
        Учителя по предметам
      </v-tab>
    </v-tabs>

    <v-window v-model="activeTab">
      <v-window-item value="performance">
        <ClassReport :classes="classes" />
      </v-window-item>

      <v-window-item value="gender">
        <GenderReport />
      </v-window-item>

      <v-window-item value="classrooms">
        <ClassroomReport />
      </v-window-item>

      <v-window-item value="teachers">
        <v-card>
          <v-toolbar color="info" dark flat>
            <v-toolbar-title>
              <v-icon left>mdi-account-multiple</v-icon>
              Учителя по предметам
            </v-toolbar-title>
            <v-spacer />
            <v-btn color="success" @click="loadTeachersBySubject" :loading="loading">
              <v-icon left>mdi-refresh</v-icon>
              Обновить
            </v-btn>
          </v-toolbar>

          <v-card-text class="pa-6">
            <div v-if="loading" class="text-center py-8">
              <v-progress-circular indeterminate />
              <p class="mt-4">Загрузка данных...</p>
            </div>

            <div v-else-if="teachersBySubject.length > 0">
              <v-table>
                <thead>
                  <tr>
                    <th>Предмет</th>
                    <th>Количество учителей</th>
                    <th>Процент от общего числа</th>
                    <th>Статус</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in teachersBySubject" :key="item.subject">
                    <td>{{ item.subject }}</td>
                    <td>
                      <v-chip :color="getTeacherCountColor(item.teachers_count)" variant="flat">
                        {{ item.teachers_count }}
                      </v-chip>
                    </td>
                    <td>
                      {{ ((item.teachers_count / totalTeachers) * 100).toFixed(1) }}%
                    </td>
                    <td>
                      <v-progress-linear
                        :model-value="(item.teachers_count / totalTeachers) * 100"
                        :color="getTeacherCountColor(item.teachers_count)"
                        height="10"
                        rounded
                      />
                    </td>
                  </tr>
                </tbody>
              </v-table>

              <v-card class="mt-6" variant="outlined">
                <v-toolbar color="grey-lighten-3" density="compact">
                  <v-toolbar-title>Анализ распределения</v-toolbar-title>
                </v-toolbar>
                <v-card-text>
                  <v-list>
                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon color="primary">mdi-account-group</v-icon>
                      </template>
                      <v-list-item-title>Всего учителей</v-list-item-title>
                      <template v-slot:append>
                        <span class="text-h6">{{ totalTeachers }}</span>
                      </template>
                    </v-list-item>

                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon color="info">mdi-book-multiple</v-icon>
                      </template>
                      <v-list-item-title>Количество предметов</v-list-item-title>
                      <template v-slot:append>
                        <span class="text-h6">{{ teachersBySubject.length }}</span>
                      </template>
                    </v-list-item>

                    <v-divider class="my-2" />

                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon color="success">mdi-star</v-icon>
                      </template>
                      <v-list-item-title>Самый популярный предмет</v-list-item-title>
                      <template v-slot:append>
                        <span class="text-h6">{{ mostPopularSubject?.subject || 'Нет данных' }}</span>
                      </template>
                    </v-list-item>

                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon color="warning">mdi-alert</v-icon>
                      </template>
                      <v-list-item-title>Предмет с нехваткой учителей</v-list-item-title>
                      <template v-slot:append>
                        <span class="text-h6">{{ leastPopularSubject?.subject || 'Нет данных' }}</span>
                      </template>
                    </v-list-item>
                  </v-list>
                </v-card-text>
              </v-card>
            </div>

            <div v-else class="text-center py-8">
              <v-icon size="64" color="grey" class="mb-4">mdi-book-off</v-icon>
              <p class="text-h6 text-grey">Данные не найдены</p>
              <p class="text-body-1 text-grey">Добавьте учителей и предметы</p>
            </div>
          </v-card-text>
        </v-card>
      </v-window-item>
    </v-window>
  </v-container>
</template>

<script>
import ClassReport from '../components/Reports/ClassReport.vue'
import GenderReport from '../components/Reports/GenderReport.vue'
import ClassroomReport from '../components/Reports/ClassroomReport.vue'
import classesApi from '../api/classes'
import reportsApi from '../api/reports'

export default {
  name: 'ReportsView',
  components: {
    ClassReport,
    GenderReport,
    ClassroomReport
  },
  data() {
    return {
      activeTab: 'performance',
      loading: false,
      classes: [],
      teachersBySubject: []
    }
  },
  computed: {
    breadcrumbs() {
      return [
        { title: 'Главная', to: '/dashboard' },
        { title: 'Отчеты', disabled: true }
      ]
    },
    totalTeachers() {
      return this.teachersBySubject.reduce((sum, item) => sum + item.teachers_count, 0)
    },
    mostPopularSubject() {
      if (!this.teachersBySubject.length) return null
      return this.teachersBySubject.reduce((prev, current) =>
        prev.teachers_count > current.teachers_count ? prev : current
      )
    },
    leastPopularSubject() {
      if (!this.teachersBySubject.length) return null
      return this.teachersBySubject.reduce((prev, current) =>
        prev.teachers_count < current.teachers_count ? prev : current
      )
    }
  },
  async mounted() {
    await this.loadClasses()
  },
  methods: {
    async loadClasses() {
      try {
        const response = await classesApi.getClasses()
        this.classes = Array.isArray(response.data) ? response.data : response.data.results || []
      } catch (error) {
        this.$toast.error('Ошибка загрузки классов')
      }
    },

    async loadTeachersBySubject() {
      this.loading = true
      try {
        const response = await reportsApi.getTeachersBySubject()
        this.teachersBySubject = Array.isArray(response.data) ? response.data : response.data.results || []
        this.$toast.success('Данные загружены')
      } catch (error) {
        this.$toast.error('Ошибка загрузки данных')
      } finally {
        this.loading = false
      }
    },

    getTeacherCountColor(count) {
      if (count >= 5) return 'success'
      if (count >= 3) return 'warning'
      return 'error'
    }
  }
}
</script>