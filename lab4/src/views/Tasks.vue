<template>
  <div class="tasks-page">
    <div class="page-header">
      <h1>Задачи</h1>
      <button v-if="isAdmin" @click="showCreateForm = true" class="btn">Создать задачу</button>
    </div>

    <div v-if="showCreateForm" class="create-form">
      <h2>Создать задачу</h2>
      <form @submit.prevent="handleCreateTask">
        <div v-if="error" class="error-message">{{ error }}</div>
        <input
          v-model="newTask.title"
          type="text"
          placeholder="Название задачи"
          class="input"
          required
        />
        <textarea
          v-model="newTask.description"
          placeholder="Описание задачи"
          class="input"
          rows="5"
          required
        ></textarea>
        <div class="form-actions">
          <button type="submit" class="btn" :disabled="loading">Создать</button>
          <button type="button" @click="cancelCreate" class="btn btn-secondary">Отмена</button>
        </div>
      </form>
    </div>

    <div v-if="loading && !tasks.length" class="loading">Загрузка...</div>
    <div v-else-if="error && !tasks.length" class="error-message">{{ error }}</div>
    <div v-else-if="tasks.length === 0" class="empty">Задач пока нет</div>
    <div v-else class="tasks-list">
      <TaskCard v-for="task in tasks" :key="task.id" :task="task" />
    </div>
  </div>
</template>

<script>
import TaskCard from '@/components/TaskCard.vue'
import { tasksAPI, apiErrorMessage } from '@/api'

export default {
  name: 'Tasks',
  components: {
    TaskCard
  },
  data() {
    return {
      tasks: [],
      loading: false,
      error: '',
      showCreateForm: false,
      newTask: {
        title: '',
        description: ''
      }
    }
  },
  computed: {
    currentUser() {
      const userStr = localStorage.getItem('user')
      return userStr ? JSON.parse(userStr) : null
    },
    isAdmin() {
      return this.currentUser?.role === 'admin'
    }
  },
  mounted() {
    this.loadTasks()
  },
  methods: {
    async loadTasks() {
      this.loading = true
      this.error = ''
      try {
        this.tasks = await tasksAPI.getList()
      } catch (e) {
        this.error = apiErrorMessage(e)
      } finally {
        this.loading = false
      }
    },
    async handleCreateTask() {
      if (!this.currentUser?.id) {
        this.error = 'Не удалось определить текущего пользователя'
        return
      }

      this.error = ''
      this.loading = true
      try {
        await tasksAPI.create({
          ...this.newTask,
          created_by: this.currentUser.id
        })
        this.newTask = { title: '', description: '' }
        this.showCreateForm = false
        await this.loadTasks()
      } catch (e) {
        this.error = apiErrorMessage(e)
      } finally {
        this.loading = false
      }
    },
    cancelCreate() {
      this.showCreateForm = false
      this.newTask = { title: '', description: '' }
      this.error = ''
    }
  }
}
</script>

<style scoped>
.tasks-page {
  max-width: 1000px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  margin: 0;
  color: #2d7ef7;
}

.create-form {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.create-form h2 {
  margin: 0 0 1rem 0;
  color: #2d7ef7;
}

.form-actions {
  display: flex;
  gap: 0.5rem;
}

.tasks-list {
  display: flex;
  flex-direction: column;
}

.loading,
.empty {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

textarea.input {
  resize: vertical;
  font-family: inherit;
}
</style>
