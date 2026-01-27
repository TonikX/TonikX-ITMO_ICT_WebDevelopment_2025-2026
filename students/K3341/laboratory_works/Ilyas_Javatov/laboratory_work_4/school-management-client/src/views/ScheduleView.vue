<template>
  <v-container>
    <v-breadcrumbs :items="breadcrumbs" class="pl-0">
      <template v-slot:divider>
        <v-icon>mdi-chevron-right</v-icon>
      </template>
    </v-breadcrumbs>

    <h1 class="text-h3 mb-4">Расписание занятий</h1>

    <ScheduleList
      :schedules="schedules"
      :classes="classes"
      :teachers="teachers"
      :subjects="subjects"
      :loading="loading"
      @add="showAddDialog = true"
      @edit="editSchedule"
      @delete="deleteSchedule"
      @find-lesson="showFindLessonDialog = true"
      @filter="handleFilter"
    />

    <!-- Диалог добавления/редактирования -->
    <ScheduleForm
      v-model="showFormDialog"
      :schedule="selectedSchedule"
      :classes="classes"
      :teachers="teachers"
      :subjects="subjects"
      :loading="formLoading"
      :conflict="hasConflict"
      @save="saveSchedule"
    />

    <!-- Диалог поиска урока -->
    <ScheduleLookup
      v-model="showFindLessonDialog"
      :classes="classes"
    />

    <!-- Уведомление об удалении -->
    <v-dialog v-model="showDeleteDialog" max-width="400">
      <v-card>
        <v-toolbar color="error" dark>
          <v-toolbar-title>Подтверждение удаления</v-toolbar-title>
        </v-toolbar>
        <v-card-text class="pa-6">
          <p class="text-h6 mb-4">Вы уверены, что хотите удалить занятие?</p>
          <p class="text-body-1" v-if="selectedSchedule">
            {{ selectedSchedule.class_name }} - {{ selectedSchedule.subject_name }}
            <br>
            {{ selectedSchedule.day_of_week_display }}, {{ selectedSchedule.lesson_number }} урок
          </p>
          <p class="text-caption text-grey mt-2">
            Это действие нельзя отменить.
          </p>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer />
          <v-btn color="grey" @click="showDeleteDialog = false">
            Отмена
          </v-btn>
          <v-btn color="error" @click="confirmDelete" :loading="deleteLoading">
            Удалить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import ScheduleList from '../components/Schedule/ScheduleList.vue'
import ScheduleForm from '../components/Schedule/ScheduleForm.vue'
import ScheduleLookup from '../components/Schedule/ScheduleView.vue'
import api from '../api/schedules'
import classesApi from '../api/classes'
import teachersApi from '../api/teachers'
import subjectsApi from '../api/subjects'

export default {
  name: 'ScheduleView',
  components: {
    ScheduleList,
    ScheduleForm,
    ScheduleLookup
  },
  data() {
    return {
      loading: false,
      schedules: [],
      classes: [],
      teachers: [],
      subjects: [],
      filters: {},
      hasConflict: false,

      // Диалоги
      showFormDialog: false,
      showDeleteDialog: false,
      showFindLessonDialog: false,
      showAddDialog: false,

      // Загрузка
      formLoading: false,
      deleteLoading: false,

      // Выбранное расписание
      selectedSchedule: null
    }
  },
  computed: {
    breadcrumbs() {
      return [
        { title: 'Главная', to: '/dashboard' },
        { title: 'Расписание', disabled: true }
      ]
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    notify(type, message) {
      if (this.$toast && typeof this.$toast[type] === 'function') {
        this.$toast[type](message)
      }
    },
    async loadData() {
      this.loading = true
      try {
        const [schedulesRes, classesRes, teachersRes, subjectsRes] = await Promise.all([
          api.getSchedules(),
          classesApi.getClasses(),
          teachersApi.getTeachers(),
          subjectsApi.getSubjects()
        ])

        const schedulesRaw = Array.isArray(schedulesRes.data) ? schedulesRes.data : schedulesRes.data.results || []
        this.classes = Array.isArray(classesRes.data) ? classesRes.data : classesRes.data.results || []
        this.teachers = Array.isArray(teachersRes.data) ? teachersRes.data : teachersRes.data.results || []
        this.subjects = Array.isArray(subjectsRes.data) ? subjectsRes.data : subjectsRes.data.results || []

        // Добавляем full_name для учителей
        this.teachers = this.teachers.map(teacher => ({
          ...teacher,
          full_name: `${teacher.last_name} ${teacher.first_name}`
        }))

        this.schedules = this.normalizeSchedules(schedulesRaw)

      } catch (error) {
        console.error('Error loading data:', error)
        this.notify('error', 'Ошибка загрузки данных')
      } finally {
        this.loading = false
      }
    },

    async handleFilter(filters) {
      this.filters = filters
      await this.loadSchedules()
    },

    async loadSchedules() {
      this.loading = true
      try {
        const response = await api.getSchedules(this.filters)
        const schedulesRaw = Array.isArray(response.data) ? response.data : response.data.results || []
        this.schedules = this.normalizeSchedules(schedulesRaw)
      } catch (error) {
        this.notify('error', 'Ошибка загрузки расписания')
      } finally {
        this.loading = false
      }
    },

    editSchedule(schedule) {
      this.selectedSchedule = schedule
      this.hasConflict = false
      this.showFormDialog = true
    },

    deleteSchedule(schedule) {
      this.selectedSchedule = schedule
      this.showDeleteDialog = true
    },

    async saveSchedule(scheduleData) {
      this.formLoading = true
      try {
        // Проверяем на конфликты
        const conflict = await this.checkConflict(scheduleData)
        if (conflict && !this.selectedSchedule) {
          this.hasConflict = true
          this.notify('warning', 'Обнаружен конфликт расписания')
          return
        }

        if (this.selectedSchedule) {
          // Редактирование
          await api.updateSchedule(this.selectedSchedule.id, scheduleData)
          this.notify('success', 'Занятие обновлено')
        } else {
          // Добавление
          await api.createSchedule(scheduleData)
          this.notify('success', 'Занятие добавлено')
        }

        this.showFormDialog = false
        this.selectedSchedule = null
        this.hasConflict = false
        await this.loadData()

      } catch (error) {
        console.error('Error saving schedule:', error)
        this.notify('error', 'Ошибка сохранения')
      } finally {
        this.formLoading = false
      }
    },

    checkConflict(scheduleData) {
      const conflicts = this.schedules.filter(schedule => {
        return (
          schedule.school_class === scheduleData.school_class &&
          schedule.day_of_week === scheduleData.day_of_week &&
          schedule.lesson_number === scheduleData.lesson_number
        )
      })

      if (this.selectedSchedule) {
        return conflicts.some(s => s.id !== this.selectedSchedule.id)
      }

      return conflicts.length > 0
    },

    async confirmDelete() {
      this.deleteLoading = true
      try {
        await api.deleteSchedule(this.selectedSchedule.id)
        this.notify('success', 'Занятие удалено')
        this.showDeleteDialog = false
        this.selectedSchedule = null
        await this.loadData()
      } catch (error) {
        console.error('Error deleting schedule:', error)
        this.notify('error', 'Ошибка удаления')
      } finally {
        this.deleteLoading = false
      }
    },
    normalizeSchedules(schedules) {
      return schedules.map(schedule => {
        const teacher = this.teachers.find(item => item.id === schedule.teacher)
        return {
          ...schedule,
          class_name: schedule.school_class_name || schedule.class_name,
          subject_name: schedule.subject_name,
          teacher_name: schedule.teacher_name || teacher?.full_name,
          classroom_number: teacher?.classroom_number || '-'
        }
      })
    }
  },
  watch: {
    showAddDialog: {
      handler(newVal) {
        if (newVal) {
          this.selectedSchedule = null
          this.hasConflict = false
          this.showFormDialog = true
        }
      }
    }
  }
}
</script>