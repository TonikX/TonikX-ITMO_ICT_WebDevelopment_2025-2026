<template>
  <v-container>
    <v-breadcrumbs :items="breadcrumbs" class="pl-0">
      <template v-slot:divider>
        <v-icon>mdi-chevron-right</v-icon>
      </template>
    </v-breadcrumbs>

    <h1 class="text-h3 mb-4">Управление учителями</h1>

    <TeacherList
      :teachers="teachers"
      :loading="loading"
      @add="showAddDialog = true"
      @edit="editTeacher"
      @view="viewTeacher"
      @delete="deleteTeacher"
      @search="handleSearch"
      @filter="handleFilter"
    />

    <!-- Диалог добавления/редактирования -->
    <TeacherForm
      v-model="showFormDialog"
      :teacher="selectedTeacher"
      :classes="classes"
      :classrooms="classrooms"
      :subjects="subjects"
      :loading="formLoading"
      @save="saveTeacher"
    />

    <!-- Диалог просмотра -->
    <TeacherDetail
      v-model="showDetailDialog"
      :teacher="selectedTeacher"
      @edit="editSelectedTeacher"
    />

    <!-- Уведомление об удалении -->
    <v-dialog v-model="showDeleteDialog" max-width="400">
      <v-card>
        <v-toolbar color="error" dark>
          <v-toolbar-title>Подтверждение удаления</v-toolbar-title>
        </v-toolbar>
        <v-card-text class="pa-6">
          <p class="text-h6 mb-4">Вы уверены, что хотите удалить учителя?</p>
          <p class="text-body-1">
            {{ selectedTeacher?.last_name }} {{ selectedTeacher?.first_name }}
          </p>
          <p class="text-caption text-grey mt-2">
            Это действие нельзя отменить. Все связанные данные будут удалены.
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
import TeacherList from '../components/Teachers/TeacherList.vue'
import TeacherForm from '../components/Teachers/TeacherForm.vue'
import TeacherDetail from '../components/Teachers/TeacherDetail.vue'
import api from '../api/teachers'
import classesApi from '../api/classes'
import classroomsApi from '../api/classrooms'
import subjectsApi from '../api/subjects'

export default {
  name: 'TeachersView',
  components: {
    TeacherList,
    TeacherForm,
    TeacherDetail
  },
  data() {
    return {
      loading: false,
      teachers: [],
      classes: [],
      classrooms: [],
      subjects: [],
      searchQuery: '',
      filters: {},

      // Диалоги
      showFormDialog: false,
      showDetailDialog: false,
      showDeleteDialog: false,
      showAddDialog: false,

      // Загрузка
      formLoading: false,
      deleteLoading: false,

      // Выбранный учитель
      selectedTeacher: null
    }
  },
  computed: {
    breadcrumbs() {
      return [
        { title: 'Главная', to: '/dashboard' },
        { title: 'Учителя', disabled: true }
      ]
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      this.loading = true
      try {
        const [teachersRes, classesRes, classroomsRes, subjectsRes] = await Promise.all([
          api.getTeachers(),
          classesApi.getClasses(),
          classroomsApi.getClassrooms(),
          subjectsApi.getSubjects()
        ])

        this.teachers = Array.isArray(teachersRes.data) ? teachersRes.data : teachersRes.data.results || []
        this.classes = Array.isArray(classesRes.data) ? classesRes.data : classesRes.data.results || []
        this.classrooms = Array.isArray(classroomsRes.data) ? classroomsRes.data : classroomsRes.data.results || []
        this.subjects = Array.isArray(subjectsRes.data) ? subjectsRes.data : subjectsRes.data.results || []

      } catch (error) {
        console.error('Error loading data:', error)
        this.$toast.error('Ошибка загрузки данных')
      } finally {
        this.loading = false
      }
    },

    async handleSearch(query) {
      this.searchQuery = query
      await this.loadTeachers()
    },

    async handleFilter(filters) {
      this.filters = filters
      await this.loadTeachers()
    },

    async loadTeachers() {
      this.loading = true
      try {
        const params = {
          search: this.searchQuery,
          ...this.filters
        }

        const response = await api.getTeachers(params)
        this.teachers = Array.isArray(response.data) ? response.data : response.data.results || []
      } catch (error) {
        this.$toast.error('Ошибка загрузки учителей')
      } finally {
        this.loading = false
      }
    },

    editTeacher(teacher) {
      this.selectedTeacher = teacher
      this.showFormDialog = true
    },

    editSelectedTeacher() {
      this.showDetailDialog = false
      this.editTeacher(this.selectedTeacher)
    },

    viewTeacher(teacher) {
      this.selectedTeacher = teacher
      this.showDetailDialog = true
    },

    deleteTeacher(teacher) {
      this.selectedTeacher = teacher
      this.showDeleteDialog = true
    },

    async saveTeacher(teacherData) {
      this.formLoading = true
      try {
        if (this.selectedTeacher) {
          // Редактирование
          await api.updateTeacher(this.selectedTeacher.id, teacherData)
          this.$toast.success('Учитель обновлен')
        } else {
          // Добавление
          await api.createTeacher(teacherData)
          this.$toast.success('Учитель добавлен')
        }

        this.showFormDialog = false
        this.selectedTeacher = null
        await this.loadData()

      } catch (error) {
        console.error('Error saving teacher:', error)
        this.$toast.error('Ошибка сохранения')
      } finally {
        this.formLoading = false
      }
    },

    async confirmDelete() {
      this.deleteLoading = true
      try {
        await api.deleteTeacher(this.selectedTeacher.id)
        this.$toast.success('Учитель удален')
        this.showDeleteDialog = false
        this.selectedTeacher = null
        await this.loadData()
      } catch (error) {
        console.error('Error deleting teacher:', error)
        this.$toast.error('Ошибка удаления')
      } finally {
        this.deleteLoading = false
      }
    }
  },
  watch: {
    showAddDialog: {
      handler(newVal) {
        if (newVal) {
          this.selectedTeacher = null
          this.showFormDialog = true
        }
      }
    }
  }
}
</script>