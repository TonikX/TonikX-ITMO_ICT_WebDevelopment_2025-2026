<template>
  <v-container>
    <v-breadcrumbs :items="breadcrumbs" class="pl-0">
      <template v-slot:divider>
        <v-icon>mdi-chevron-right</v-icon>
      </template>
    </v-breadcrumbs>

    <h1 class="text-h3 mb-4">Управление учениками</h1>

    <StudentList
      :students="students"
      :classes="classes"
      :loading="loading"
      @add="showAddDialog = true"
      @edit="editStudent"
      @view="viewStudent"
      @delete="deleteStudent"
      @search="handleSearch"
      @filter="handleFilter"
    />

    <!-- Диалог добавления/редактирования -->
    <StudentForm
      v-model="showFormDialog"
      :student="selectedStudent"
      :classes="classes"
      :loading="formLoading"
      @save="saveStudent"
    />

    <!-- Диалог просмотра -->
    <StudentDetail
      v-model="showDetailDialog"
      :student="selectedStudent"
      @edit="editSelectedStudent"
    />

    <!-- Уведомление об удалении -->
    <v-dialog v-model="showDeleteDialog" max-width="400">
      <v-card>
        <v-toolbar color="error" dark>
          <v-toolbar-title>Подтверждение удаления</v-toolbar-title>
        </v-toolbar>
        <v-card-text class="pa-6">
          <p class="text-h6 mb-4">Вы уверены, что хотите удалить ученика?</p>
          <p class="text-body-1">
            {{ selectedStudent?.last_name }} {{ selectedStudent?.first_name }}
          </p>
          <p class="text-caption text-grey mt-2">
            Это действие нельзя отменить. Все оценки ученика будут удалены.
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
import StudentList from '../components/Students/StudentList.vue'
import StudentForm from '../components/Students/StudentForm.vue'
import StudentDetail from '../components/Students/StudentDetail.vue'
import api from '../api/students'
import classesApi from '../api/classes'

export default {
  name: 'StudentsView',
  components: {
    StudentList,
    StudentForm,
    StudentDetail
  },
  data() {
    return {
      loading: false,
      students: [],
      classes: [],
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

      // Выбранный ученик
      selectedStudent: null
    }
  },
  computed: {
    breadcrumbs() {
      return [
        { title: 'Главная', to: '/dashboard' },
        { title: 'Ученики', disabled: true }
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
        const [studentsRes, classesRes] = await Promise.all([
          api.getStudents(),
          classesApi.getClasses()
        ])

        this.students = Array.isArray(studentsRes.data) ? studentsRes.data : studentsRes.data.results || []
        this.classes = Array.isArray(classesRes.data) ? classesRes.data : classesRes.data.results || []

      } catch (error) {
        console.error('Error loading data:', error)
        this.notify('error', 'Ошибка загрузки данных')
      } finally {
        this.loading = false
      }
    },

    async handleSearch(query) {
      this.searchQuery = query
      await this.loadStudents()
    },

    async handleFilter(filters) {
      this.filters = filters
      await this.loadStudents()
    },

    async loadStudents() {
      this.loading = true
      try {
        const params = {
          search: this.searchQuery,
          ...this.filters
        }

        const response = await api.getStudents(params)
        const data = Array.isArray(response.data) ? response.data : response.data.results || []
        this.students = data.filter(student => {
          if (this.filters.gender && student.gender !== this.filters.gender) {
            return false
          }
          if (this.filters.school_class && student.school_class !== this.filters.school_class) {
            return false
          }
          return true
        })
      } catch (error) {
        this.notify('error', 'Ошибка загрузки учеников')
      } finally {
        this.loading = false
      }
    },

    editStudent(student) {
      this.selectedStudent = student
      this.showFormDialog = true
    },

    editSelectedStudent() {
      this.showDetailDialog = false
      this.editStudent(this.selectedStudent)
    },

    viewStudent(student) {
      this.selectedStudent = student
      this.showDetailDialog = true
    },


    deleteStudent(student) {
      this.selectedStudent = student
      this.showDeleteDialog = true
    },

    async saveStudent(studentData) {
      this.formLoading = true
      try {
        if (this.selectedStudent) {
          // Редактирование
          await api.updateStudent(this.selectedStudent.id, studentData)
          this.notify('success', 'Ученик обновлен')
        } else {
          // Добавление
          await api.createStudent(studentData)
          this.notify('success', 'Ученик добавлен')
        }

        this.showFormDialog = false
        this.selectedStudent = null
        await this.loadData()

      } catch (error) {
        console.error('Error saving student:', error)
        this.notify('error', 'Ошибка сохранения')
      } finally {
        this.formLoading = false
      }
    },

    async confirmDelete() {
      this.deleteLoading = true
      try {
        await api.deleteStudent(this.selectedStudent.id)
        this.notify('success', 'Ученик удален')
        this.showDeleteDialog = false
        this.selectedStudent = null
        await this.loadData()
      } catch (error) {
        console.error('Error deleting student:', error)
        this.notify('error', 'Ошибка удаления')
      } finally {
        this.deleteLoading = false
      }
    },

  },
  watch: {
    showAddDialog: {
      handler(newVal) {
        if (newVal) {
          this.selectedStudent = null
          this.showFormDialog = true
        }
      }
    }
  }
}
</script>