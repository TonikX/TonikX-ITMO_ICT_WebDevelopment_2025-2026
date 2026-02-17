<template>
  <div class="team-detail-page">
    <div v-if="loading" class="loading">Загрузка...</div>
    <div v-else-if="error" class="error-message">{{ error }}</div>
    <div v-else-if="team" class="team-detail">
      <div class="team-header">
        <h1>{{ team.name }}</h1>
        <router-link to="/teams" class="btn btn-secondary">← Назад к списку</router-link>
      </div>

      <div class="team-content">
        <div class="team-section">
          <h2>Информация о команде</h2>
          <div class="team-info">
            <p><strong>Капитан:</strong> {{ team.captain_username }} ({{ team.captain_email }})</p>
            <p v-if="team.motto"><strong>Девиз:</strong> {{ team.motto }}</p>
            <p v-if="team.selected_task_title">
              <strong>Выбранная задача:</strong> {{ team.selected_task_title }}
            </p>
            <p><strong>Участников:</strong> {{ team.members_count || 0 }}</p>
            <p><strong>Создана:</strong> {{ formatDate(team.created_at) }}</p>
          </div>
        </div>

        <div v-if="isMyTeam" class="team-section">
          <h2>Управление командой</h2>
          <div class="team-actions">
            <div class="action-form">
              <h3>Выбрать задачу</h3>
              <form @submit.prevent="handleSelectTask">
                <select v-model="selectedTaskId" class="input" required>
                  <option value="">Выберите задачу</option>
                  <option v-for="task in availableTasks" :key="task.id" :value="task.id">
                    {{ task.title }}
                  </option>
                </select>
                <button type="submit" class="btn" :disabled="loading">Выбрать</button>
              </form>
            </div>

            <div class="action-form">
              <h3>Добавить участника</h3>
              <form @submit.prevent="handleAddMember">
                <input
                  v-model="newMember.first_name"
                  type="text"
                  placeholder="Имя"
                  class="input"
                  required
                />
                <input
                  v-model="newMember.last_name"
                  type="text"
                  placeholder="Фамилия"
                  class="input"
                  required
                />
                <input
                  v-model="newMember.email"
                  type="email"
                  placeholder="Email"
                  class="input"
                  required
                />
                <button type="submit" class="btn" :disabled="loading">Добавить</button>
              </form>
            </div>
          </div>
        </div>

        <div v-if="team.members && team.members.length > 0" class="team-section">
          <h2>Участники</h2>
          <ul class="members-list">
            <li v-for="member in team.members" :key="member.id" class="member-item">
              <strong>{{ member.first_name }} {{ member.last_name }}</strong>
              <span>{{ member.email }}</span>
            </li>
          </ul>
        </div>

        <div v-if="team.solutions && team.solutions.length > 0" class="team-section">
          <h2>Решения команды</h2>
          <div class="solutions-list">
            <div v-for="solution in team.solutions" :key="solution.id" class="solution-item">
              <h3>{{ solution.task_title }}</h3>
              <p>{{ solution.description }}</p>
              <router-link :to="`/solutions/${solution.id}`" class="btn">Подробнее</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { teamsAPI, tasksAPI, apiErrorMessage } from '@/api'

export default {
  name: 'TeamDetail',
  data() {
    return {
      team: null,
      availableTasks: [],
      loading: false,
      error: '',
      selectedTaskId: '',
      newMember: {
        first_name: '',
        last_name: '',
        email: ''
      }
    }
  },
  computed: {
    isMyTeam() {
      if (!this.team) return false
      const userStr = localStorage.getItem('user')
      const user = userStr ? JSON.parse(userStr) : null
      return user?.role === 'captain' && this.team?.captain === user.id
    }
  },
  async mounted() {
    await this.loadTeam()
    if (this.isMyTeam) {
      await this.loadTasks()
    }
  },
  methods: {
    async loadTeam() {
      this.loading = true
      this.error = ''
      try {
        this.team = await teamsAPI.getDetail(this.$route.params.id)
        if (this.team.selected_task) {
          this.selectedTaskId = this.team.selected_task
        }
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
    async handleSelectTask() {
      this.loading = true
      this.error = ''
      try {
        await teamsAPI.selectTask(this.team.id, this.selectedTaskId)
        await this.loadTeam()
      } catch (e) {
        this.error = apiErrorMessage(e)
      } finally {
        this.loading = false
      }
    },
    async handleAddMember() {
      this.loading = true
      this.error = ''
      try {
        await teamsAPI.addMember(this.team.id, this.newMember)
        this.newMember = { first_name: '', last_name: '', email: '' }
        await this.loadTeam()
      } catch (e) {
        this.error = apiErrorMessage(e)
      } finally {
        this.loading = false
      }
    },
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString('ru-RU')
    }
  }
}
</script>

<style scoped>
.team-detail-page {
  max-width: 1000px;
  margin: 0 auto;
}

.team-detail {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.team-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #eee;
}

.team-header h1 {
  margin: 0;
  color: #2d7ef7;
}

.team-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.team-section h2 {
  margin: 0 0 1rem 0;
  color: #2d7ef7;
  font-size: 1.25rem;
}

.team-info p {
  margin: 0.5rem 0;
  color: #666;
}

.team-actions {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.action-form {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
}

.action-form h3 {
  margin: 0 0 0.75rem 0;
  font-size: 1rem;
  color: #2d7ef7;
}

.members-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.member-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 4px;
  margin-bottom: 0.5rem;
}

.solutions-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.solution-item {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
}

.solution-item h3 {
  margin: 0 0 0.5rem 0;
  color: #2d7ef7;
}

.solution-item p {
  margin: 0 0 0.75rem 0;
  color: #666;
}

.loading,
.error-message {
  text-align: center;
  padding: 2rem;
}

.error-message {
  background: #fee;
  color: #c33;
  border-radius: 4px;
}
</style>
