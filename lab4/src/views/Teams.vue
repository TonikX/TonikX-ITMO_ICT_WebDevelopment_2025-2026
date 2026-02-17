<template>
  <div class="teams-page">
    <div class="page-header">
      <h1>Команды</h1>
      <button v-if="isCaptain" @click="showCreateForm = true" class="btn">Создать команду</button>
    </div>

    <div v-if="showCreateForm" class="create-form">
      <h2>Создать команду</h2>
      <form @submit.prevent="handleCreateTeam">
        <div v-if="error" class="error-message">{{ error }}</div>
        <input
          v-model="newTeam.name"
          type="text"
          placeholder="Название команды"
          class="input"
          required
        />
        <textarea
          v-model="newTeam.motto"
          placeholder="Девиз/Описание команды"
          class="input"
          rows="3"
        ></textarea>
        <div class="form-actions">
          <button type="submit" class="btn" :disabled="loading">Создать</button>
          <button type="button" @click="cancelCreate" class="btn btn-secondary">Отмена</button>
        </div>
      </form>
    </div>

    <div v-if="loading && !teams.length" class="loading">Загрузка...</div>
    <div v-else-if="error && !teams.length" class="error-message">{{ error }}</div>
    <div v-else-if="teams.length === 0" class="empty">Команд пока нет</div>
    <div v-else class="teams-list">
      <TeamCard v-for="team in teams" :key="team.id" :team="team" />
    </div>
  </div>
</template>

<script>
import TeamCard from '@/components/TeamCard.vue'
import { teamsAPI, apiErrorMessage } from '@/api'

export default {
  name: 'Teams',
  components: {
    TeamCard
  },
  data() {
    return {
      teams: [],
      loading: false,
      error: '',
      showCreateForm: false,
      newTeam: {
        name: '',
        motto: ''
      }
    }
  },
  computed: {
    currentUser() {
      const userStr = localStorage.getItem('user')
      return userStr ? JSON.parse(userStr) : null
    },
    isCaptain() {
      return this.currentUser?.role === 'captain'
    }
  },
  mounted() {
    this.loadTeams()
  },
  methods: {
    async loadTeams() {
      this.loading = true
      this.error = ''
      try {
        this.teams = await teamsAPI.getList()
      } catch (e) {
        this.error = apiErrorMessage(e)
      } finally {
        this.loading = false
      }
    },
    async handleCreateTeam() {
      if (!this.currentUser?.id) {
        this.error = 'Не удалось определить текущего пользователя'
        return
      }

      this.error = ''
      this.loading = true
      try {
        await teamsAPI.create({
          ...this.newTeam,
          captain: this.currentUser.id
        })
        this.newTeam = { name: '', motto: '' }
        this.showCreateForm = false
        await this.loadTeams()
      } catch (e) {
        this.error = apiErrorMessage(e)
      } finally {
        this.loading = false
      }
    },
    cancelCreate() {
      this.showCreateForm = false
      this.newTeam = { name: '', motto: '' }
      this.error = ''
    }
  }
}
</script>

<style scoped>
.teams-page {
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

.teams-list {
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
