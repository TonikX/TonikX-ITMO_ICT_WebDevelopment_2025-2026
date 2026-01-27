<template>
  <v-container>
    <v-breadcrumbs :items="breadcrumbs" class="pl-0">
      <template v-slot:divider>
        <v-icon>mdi-chevron-right</v-icon>
      </template>
    </v-breadcrumbs>

    <h1 class="text-h3 mb-4">Управление кабинетами</h1>

    <ClassroomList
      :classrooms="classrooms"
      :loading="loading"
      @add="showAddDialog = true"
      @edit="editClassroom"
      @delete="deleteClassroom"
      @search="handleSearch"
    />

    <ClassroomForm
      v-model="showFormDialog"
      :classroom="selectedClassroom"
      :loading="formLoading"
      @save="saveClassroom"
    />

    <v-dialog v-model="showDeleteDialog" max-width="400">
      <v-card>
        <v-toolbar color="error" dark>
          <v-toolbar-title>Подтверждение удаления</v-toolbar-title>
        </v-toolbar>
        <v-card-text class="pa-6">
          <p class="text-h6 mb-4">Вы уверены, что хотите удалить кабинет?</p>
          <p class="text-body-1">
            {{ selectedClassroom?.room_number }}
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
import ClassroomList from '../components/Classrooms/ClassroomList.vue'
import ClassroomForm from '../components/Classrooms/ClassroomForm.vue'
import api from '../api/classrooms'

export default {
  name: 'ClassroomsView',
  components: {
    ClassroomList,
    ClassroomForm
  },
  data() {
    return {
      loading: false,
      classrooms: [],
      searchQuery: '',
      showFormDialog: false,
      showDeleteDialog: false,
      showAddDialog: false,
      formLoading: false,
      deleteLoading: false,
      selectedClassroom: null
    }
  },
  computed: {
    breadcrumbs() {
      return [
        { title: 'Главная', to: '/dashboard' },
        { title: 'Кабинеты', disabled: true }
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
        const response = await api.getClassrooms()
        this.classrooms = Array.isArray(response.data) ? response.data : response.data.results || []
      } catch (error) {
        this.notify('error', 'Ошибка загрузки данных')
      } finally {
        this.loading = false
      }
    },
    async handleSearch(query) {
      this.searchQuery = query
      await this.loadClassrooms()
    },
    async loadClassrooms() {
      this.loading = true
      try {
        const params = { search: this.searchQuery }
        const response = await api.getClassrooms(params)
        this.classrooms = Array.isArray(response.data) ? response.data : response.data.results || []
      } catch (error) {
        this.notify('error', 'Ошибка загрузки кабинетов')
      } finally {
        this.loading = false
      }
    },
    editClassroom(classroom) {
      this.selectedClassroom = classroom
      this.showFormDialog = true
    },
    deleteClassroom(classroom) {
      this.selectedClassroom = classroom
      this.showDeleteDialog = true
    },
    async saveClassroom(classroomData) {
      this.formLoading = true
      try {
        if (this.selectedClassroom) {
          await api.updateClassroom(this.selectedClassroom.id, classroomData)
          this.notify('success', 'Кабинет обновлен')
        } else {
          await api.createClassroom(classroomData)
          this.notify('success', 'Кабинет добавлен')
        }
        this.showFormDialog = false
        this.selectedClassroom = null
        await this.loadData()
      } catch (error) {
        console.error('Error saving classroom:', error)
        this.notify('error', 'Ошибка сохранения')
      } finally {
        this.formLoading = false
      }
    },
    async confirmDelete() {
      this.deleteLoading = true
      try {
        await api.deleteClassroom(this.selectedClassroom.id)
        this.notify('success', 'Кабинет удален')
        this.showDeleteDialog = false
        this.selectedClassroom = null
        await this.loadData()
      } catch (error) {
        console.error('Error deleting classroom:', error)
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
          this.selectedClassroom = null
          this.showFormDialog = true
        }
      }
    }
  }
}
</script>