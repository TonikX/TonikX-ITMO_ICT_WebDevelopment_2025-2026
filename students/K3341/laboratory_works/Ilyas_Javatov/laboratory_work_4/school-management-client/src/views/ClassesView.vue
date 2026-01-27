<template>
  <v-container>
    <v-breadcrumbs :items="breadcrumbs" class="pl-0">
      <template v-slot:divider>
        <v-icon>mdi-chevron-right</v-icon>
      </template>
    </v-breadcrumbs>

    <h1 class="text-h3 mb-4">Управление классами</h1>

    <ClassList
      :classes="classes"
      :loading="loading"
      @add="showAddDialog = true"
      @edit="editClass"
      @view="viewClass"
      @report="generateReport"
      @delete="deleteClass"
      @search="handleSearch"
    />

    <ClassForm
      v-model="showFormDialog"
      :class-item="selectedClass"
      :teachers="teachers"
      :loading="formLoading"
      @save="saveClass"
    />

    <ClassDetail
      v-model="showDetailDialog"
      :school-class="selectedClass"
      @edit="editSelectedClass"
      @report="generateReport"
    />

    <v-dialog v-model="showDeleteDialog" max-width="400">
      <v-card>
        <v-toolbar color="error" dark>
          <v-toolbar-title>Подтверждение удаления</v-toolbar-title>
        </v-toolbar>
        <v-card-text class="pa-6">
          <p class="text-h6 mb-4">Вы уверены, что хотите удалить класс?</p>
          <p class="text-body-1">
            {{ selectedClass?.class_name }}
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
import ClassList from '../components/Classes/ClassList.vue'
import ClassForm from '../components/Classes/ClassForm.vue'
import ClassDetail from '../components/Classes/ClassDetail.vue'
import api from '../api/classes'
import teachersApi from '../api/teachers'

export default {
  name: 'ClassesView',
  components: {
    ClassList,
    ClassForm,
    ClassDetail
  },
  data() {
    return {
      loading: false,
      classes: [],
      teachers: [],
      searchQuery: '',
      showFormDialog: false,
      showDetailDialog: false,
      showDeleteDialog: false,
      showAddDialog: false,
      formLoading: false,
      deleteLoading: false,
      selectedClass: null
    }
  },
  computed: {
    breadcrumbs() {
      return [
        { title: 'Главная', to: '/dashboard' },
        { title: 'Классы', disabled: true }
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
        const [classesRes, teachersRes] = await Promise.all([
          api.getClasses(),
          teachersApi.getTeachers()
        ])
        this.classes = Array.isArray(classesRes.data) ? classesRes.data : classesRes.data.results || []
        const teachers = Array.isArray(teachersRes.data)
          ? teachersRes.data
          : teachersRes.data.results || []
        this.teachers = teachers.map(teacher => ({
          ...teacher,
          full_name: `${teacher.last_name} ${teacher.first_name}`
        }))
      } catch (error) {
        this.notify('error', 'Ошибка загрузки данных')
      } finally {
        this.loading = false
      }
    },

    async handleSearch(query) {
      this.searchQuery = query
      await this.loadClasses()
    },

    async loadClasses() {
      this.loading = true
      try {
        const params = { search: this.searchQuery }
        const response = await api.getClasses(params)
        this.classes = Array.isArray(response.data) ? response.data : response.data.results || []
      } catch (error) {
        this.notify('error', 'Ошибка загрузки классов')
      } finally {
        this.loading = false
      }
    },

    editClass(classItem) {
      this.selectedClass = classItem
      this.showFormDialog = true
    },

    viewClass(classItem) {
      this.selectedClass = classItem
      this.showDetailDialog = true
    },

    generateReport(classItem) {
      this.$router.push({ name: 'Reports', query: { type: 'performance', classId: classItem.id } })
    },

    deleteClass(classItem) {
      this.selectedClass = classItem
      this.showDeleteDialog = true
    },

    editSelectedClass() {
      this.showDetailDialog = false
      this.editClass(this.selectedClass)
    },

    async saveClass(classData) {
      this.formLoading = true
      try {
        if (this.selectedClass) {
          await api.updateClass(this.selectedClass.id, classData)
          this.notify('success', 'Класс обновлен')
        } else {
          await api.createClass(classData)
          this.notify('success', 'Класс добавлен')
        }
        this.showFormDialog = false
        this.selectedClass = null
        await this.loadData()
      } catch (error) {
        console.error('Error saving class:', error)
        this.notify('error', 'Ошибка сохранения')
      } finally {
        this.formLoading = false
      }
    },

    async confirmDelete() {
      this.deleteLoading = true
      try {
        await api.deleteClass(this.selectedClass.id)
        this.notify('success', 'Класс удален')
        this.showDeleteDialog = false
        this.selectedClass = null
        await this.loadData()
      } catch (error) {
        console.error('Error deleting class:', error)
        this.notify('error', 'Ошибка удаления')
      } finally {
        this.deleteLoading = false
      }
    }
  },
  watch: {
    showAddDialog: {
      handler(newVal) {
        if (newVal) {
          this.selectedClass = null
          this.showFormDialog = true
        }
      }
    }
  }
}
</script>