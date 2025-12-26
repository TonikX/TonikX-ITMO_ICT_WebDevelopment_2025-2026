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
      @grades="manageGrades"
      @delete="deleteStudent"
      @search="handleSearch"
      @filter="handleFilter"
    />

    <!-- Диалог добавления/редактирования -->
    <StudentForm
      v-model="showFormDialog"
      :student="selectedStudent"
      :classes="classes"
      :subjects="subjects"
      :loading="formLoading"
      @save="saveStudent"
    />

    <!-- Диалог просмотра -->
    <StudentDetail
      v-model="showDetailDialog"
      :student="selectedStudent"
      @edit="editSelectedStudent"
      @grades="manageGrades"
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

    <!-- Диалог управления оценками -->
    <v-dialog v-model="showGradesDialog" max-width="800" persistent>
      <v-card :loading="gradesLoading">
        <v-toolbar color="success" dark>
          <v-toolbar-title>
            <v-icon left>mdi-chart-bar</v-icon>
            Оценки ученика: {{ selectedStudent?.last_name }} {{ selectedStudent?.first_name }}
          </v-toolbar-title>
          <v-spacer />
          <v-btn icon @click="showGradesDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>

        <v-card-text class="pa-6">
          <GradesManager
            v-if="selectedStudent"
            :student="selectedStudent"
            :subjects="subjects"
            @save="handleGradesSave"
          />
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import StudentList from '../components/Students/StudentList.vue'
import StudentForm from '../components/Students/StudentForm.vue'
import StudentDetail from '../components/Students/StudentDetail.vue'
import GradesManager from '../components/Students/GradesManager.vue'
import api from '../api/students'
import classesApi from '../api/classes'
import subjectsApi from '../api/subjects'

export default {
  name: 'StudentsView',
  components: {
    StudentList,
    StudentForm,
    StudentDetail,
    GradesManager
  },
  data() {
    return {
      loading: false,
      students: [],
      classes: [],
      subjects: [],
      searchQuery: '',
      filters: {},

      // Диалоги
      showFormDialog: false,
      showDetailDialog: false,
      showDeleteDialog: false,
      showAddDialog: false,
      showGradesDialog: false,

      // Загрузка
      formLoading: false,
      deleteLoading: false,
      gradesLoading: false,

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
    async loadData() {
      this.loading = true
      try {
        const [studentsRes, classesRes, subjectsRes] = await Promise.all([
          api.getStudents(),
          classesApi.getClasses(),
          subjectsApi.getSubjects()
        ])

        this.students = Array.isArray(studentsRes.data) ? studentsRes.data : studentsRes.data.results || []
        this.classes = Array.isArray(classesRes.data) ? classesRes.data : classesRes.data.results || []
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
        this.students = Array.isArray(response.data) ? response.data : response.data.results || []
      } catch (error) {
        this.$toast.error('Ошибка загрузки учеников')
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

    manageGrades(student) {
      this.selectedStudent = student
      this.showGradesDialog = true
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
          this.$toast.success('Ученик обновлен')
        } else {
          // Добавление
          await api.createStudent(studentData)
          this.$toast.success('Ученик добавлен')
        }

        this.showFormDialog = false
        this.selectedStudent = null
        await this.loadData()

      } catch (error) {
        console.error('Error saving student:', error)
        this.$toast.error('Ошибка сохранения')
      } finally {
        this.formLoading = false
      }
    },

    async confirmDelete() {
      this.deleteLoading = true
      try {
        await api.deleteStudent(this.selectedStudent.id)
        this.$toast.success('Ученик удален')
        this.showDeleteDialog = false
        this.selectedStudent = null
        await this.loadData()
      } catch (error) {
        console.error('Error deleting student:', error)
        this.$toast.error('Ошибка удаления')
      } finally {
        this.deleteLoading = false
      }
    },

    async handleGradesSave() {
      this.gradesLoading = true
      try {
        this.$toast.success('Оценки сохранены')
        this.showGradesDialog = false
        await this.loadData()
      } catch (error) {
        this.$toast.error('Ошибка сохранения оценок')
      } finally {
        this.gradesLoading = false
      }
    }
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