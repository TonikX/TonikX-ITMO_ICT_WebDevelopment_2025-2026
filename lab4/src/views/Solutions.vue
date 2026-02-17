<template>
  <div class="solutions-page">
    <div class="page-header">
      <h1>Решения</h1>
      <button v-if="isCaptain" @click="showCreateForm = true" class="btn">Отправить решение</button>
    </div>

    <div v-if="showCreateForm" class="create-form">
      <h2>Отправить решение</h2>
      <form @submit.prevent="handleCreateSolution">
        <div v-if="error" class="error-message">{{ error }}</div>
        <select v-model="newSolution.task" class="input" required>
          <option value="">Выберите задачу</option>
          <option v-for="task in availableTasks" :key="task.id" :value="task.id">
            {{ task.title }}
          </option>
        </select>
        <textarea
          v-model="newSolution.description"
          placeholder="Описание решения"
          class="input"
          rows="5"
          required
        ></textarea>
        <input
          ref="fileInput"
          type="file"
          @change="handleFileChange"
          class="input"
        />
        <div class="form-actions">
          <button type="submit" class="btn" :disabled="loading">Отправить</button>
          <button type="button" @click="cancelCreate" class="btn btn-secondary">Отмена</button>
        </div>
      </form>
    </div>

    <div v-if="loading && !solutions.length" class="loading">Загрузка...</div>
    <div v-else-if="error && !solutions.length" class="error-message">{{ error }}</div>
    <div v-else-if="solutions.length === 0" class="empty">Решений пока нет</div>
    <div v-else class="solutions-list">
      <SolutionCard v-for="solution in solutions" :key="solution.id" :solution="solution" />
    </div>
  </div>
</template>

<script>
import SolutionCard from '@/components/SolutionCard.vue'
import { solutionsAPI, tasksAPI, teamsAPI, apiErrorMessage } from '@/api'

export default {
  name: 'Solutions',
  components: {
    SolutionCard
  },
  data() {
    return {
      solutions: [],
      availableTasks: [],
      myTeamId: null,
      loading: false,
      error: '',
      showCreateForm: false,
      newSolution: {
        task: '',
        description: ''
      },
      selectedFile: null
    }
  },
  computed: {
    isCaptain() {
      const userStr = localStorage.getItem('user')
      const user = userStr ? JSON.parse(userStr) : null
      return user?.role === 'captain'
    }
  },
  async mounted() {
    await this.loadSolutions()
    if (this.isCaptain) {
      await this.loadMyTeam()
      await this.loadTasks()
    }
  },
  methods: {
    async loadSolutions() {
      this.loading = true
      this.error = ''
      try {
        this.solutions = await solutionsAPI.getList()
      } catch (e) {
        this.error = apiErrorMessage(e)
      } finally {
        this.loading = false
      }
    },
    async loadTasks() {
      try {
        this.availableTasks = await tasksAPI.getList()
      } catch (e) {
        console.error('Ошибка загрузки задач:', e)
      }
    },
    async loadMyTeam() {
      try {
        const teams = await teamsAPI.getList()
        this.myTeamId = teams.length ? teams[0].id : null
      } catch (e) {
        console.error('Ошибка загрузки команды:', e)
      }
    },
    handleFileChange(event) {
      this.selectedFile = event.target.files[0]
    },
    async handleCreateSolution() {
      if (!this.myTeamId) {
        this.error = 'Сначала создайте команду в разделе "Команды"'
        return
      }

      this.error = ''
      this.loading = true
      try {
        const formData = new FormData()
        formData.append('team', this.myTeamId)
        formData.append('task', this.newSolution.task)
        formData.append('description', this.newSolution.description)
        if (this.selectedFile) {
          formData.append('file', this.selectedFile)
        }
        await solutionsAPI.create(formData)
        this.newSolution = { task: '', description: '' }
        this.selectedFile = null
        if (this.$refs.fileInput) {
          this.$refs.fileInput.value = ''
        }
        this.showCreateForm = false
        await this.loadSolutions()
      } catch (e) {
        this.error = apiErrorMessage(e)
      } finally {
        this.loading = false
      }
    },
    cancelCreate() {
      this.showCreateForm = false
      this.newSolution = { task: '', description: '' }
      this.selectedFile = null
      this.error = ''
    }
  }
}
</script>

<style scoped>
.solutions-page {
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

.solutions-list {
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
