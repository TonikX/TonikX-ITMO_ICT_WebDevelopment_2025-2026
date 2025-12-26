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

    <!-- Здесь будут диалоги для добавления/редактирования классов -->
    <!-- Аналогично TeachersView и StudentsView -->

  </v-container>
</template>

<script>
import ClassList from '../components/Classes/ClassList.vue'
import api from '../api/classes'

export default {
  name: 'ClassesView',
  components: {
    ClassList
  },
  data() {
    return {
      loading: false,
      classes: [],
      searchQuery: ''
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
    async loadData() {
      this.loading = true
      try {
        const response = await api.getClasses()
        this.classes = Array.isArray(response.data) ? response.data : response.data.results || []
      } catch (error) {
        this.$toast.error('Ошибка загрузки данных')
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
        this.$toast.error('Ошибка загрузки классов')
      } finally {
        this.loading = false
      }
    },

    editClass(classItem) {
      // Реализация редактирования
    },

    viewClass(classItem) {
      // Реализация просмотра
    },

    generateReport(classItem) {
      // Реализация генерации отчета
    },

    deleteClass(classItem) {
      // Реализация удаления
    }
  }
}
</script>