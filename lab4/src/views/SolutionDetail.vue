<template>
  <div class="solution-detail-page">
    <div v-if="loading" class="loading">Загрузка...</div>
    <div v-else-if="error" class="error-message">{{ error }}</div>
    <div v-else-if="solution" class="solution-detail">
      <div class="solution-header">
        <h1>{{ solution.team_name }} - {{ solution.task_title }}</h1>
        <router-link to="/solutions" class="btn btn-secondary">← Назад к списку</router-link>
      </div>

      <div class="solution-content">
        <div class="solution-section">
          <h2>Описание решения</h2>
          <p class="solution-description">{{ solution.description }}</p>
        </div>

        <div class="solution-section">
          <h2>Информация</h2>
          <div class="solution-info">
            <p><strong>Команда:</strong> {{ solution.team_name }}</p>
            <p><strong>Задача:</strong> {{ solution.task_title }}</p>
            <p><strong>Опубликовано:</strong> {{ formatDate(solution.published_at) }}</p>
            <p v-if="solution.file_url">
              <strong>Файл:</strong>
              <a :href="solution.file_url" target="_blank" class="btn btn-secondary">Скачать</a>
            </p>
          </div>
        </div>

        <div v-if="solution.evaluations && solution.evaluations.length > 0" class="solution-section">
          <h2>Оценки</h2>
          <div class="evaluations-list">
            <div v-for="evaluation in solution.evaluations" :key="evaluation.id" class="evaluation-item">
              <div class="evaluation-header">
                <strong>{{ evaluation.jury_username }}</strong>
                <span class="evaluation-score">Балл: {{ evaluation.score }}</span>
              </div>
              <p v-if="evaluation.comment" class="evaluation-comment">{{ evaluation.comment }}</p>
              <span class="evaluation-date">{{ formatDate(evaluation.created_at) }}</span>
            </div>
          </div>
          <div v-if="solution.average_score !== null" class="average-score">
            <strong>Средний балл: {{ solution.average_score }}</strong>
          </div>
        </div>

        <div v-if="isJury && !hasMyEvaluation" class="solution-section">
          <h2>Оценить решение</h2>
          <form @submit.prevent="handleCreateEvaluation" class="evaluation-form">
            <div v-if="evaluationError" class="error-message">{{ evaluationError }}</div>
            <label>
              Балл (1-10):
              <input
                v-model.number="newEvaluation.score"
                type="number"
                min="1"
                max="10"
                class="input"
                required
              />
            </label>
            <label>
              Комментарий:
              <textarea
                v-model="newEvaluation.comment"
                class="input"
                rows="4"
                placeholder="Ваш комментарий к решению"
              ></textarea>
            </label>
            <button type="submit" class="btn" :disabled="evaluationLoading">Отправить оценку</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { solutionsAPI, evaluationsAPI, apiErrorMessage } from '@/api'

export default {
  name: 'SolutionDetail',
  data() {
    return {
      solution: null,
      loading: false,
      error: '',
      evaluationError: '',
      evaluationLoading: false,
      newEvaluation: {
        score: '',
        comment: ''
      }
    }
  },
  computed: {
    isJury() {
      const userStr = localStorage.getItem('user')
      const user = userStr ? JSON.parse(userStr) : null
      return user?.role === 'jury'
    },
    hasMyEvaluation() {
      if (!this.solution || !this.solution.evaluations || !this.solution.evaluations.length) return false
      const userStr = localStorage.getItem('user')
      const user = userStr ? JSON.parse(userStr) : null
      if (!user) return false
      return this.solution.evaluations.some(e => e.jury === user.id)
    }
  },
  mounted() {
    this.loadSolution()
  },
  methods: {
    async loadSolution() {
      this.loading = true
      this.error = ''
      try {
        this.solution = await solutionsAPI.getDetail(this.$route.params.id)
      } catch (e) {
        this.error = apiErrorMessage(e)
      } finally {
        this.loading = false
      }
    },
    async handleCreateEvaluation() {
      const userStr = localStorage.getItem('user')
      const user = userStr ? JSON.parse(userStr) : null
      if (!user?.id) {
        this.evaluationError = 'Не удалось определить текущего пользователя'
        return
      }

      this.evaluationError = ''
      this.evaluationLoading = true
      try {
        await evaluationsAPI.create({
          solution: this.solution.id,
          jury: user.id,
          score: this.newEvaluation.score,
          comment: this.newEvaluation.comment
        })
        this.newEvaluation = { score: '', comment: '' }
        await this.loadSolution()
      } catch (e) {
        this.evaluationError = apiErrorMessage(e)
      } finally {
        this.evaluationLoading = false
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
.solution-detail-page {
  max-width: 1000px;
  margin: 0 auto;
}

.solution-detail {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.solution-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #eee;
}

.solution-header h1 {
  margin: 0;
  color: #2d7ef7;
}

.solution-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.solution-section h2 {
  margin: 0 0 1rem 0;
  color: #2d7ef7;
  font-size: 1.25rem;
}

.solution-description {
  line-height: 1.6;
  color: #333;
}

.solution-info p {
  margin: 0.5rem 0;
  color: #666;
}

.evaluations-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1rem;
}

.evaluation-item {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
}

.evaluation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.evaluation-score {
  color: #2d7ef7;
  font-weight: bold;
}

.evaluation-comment {
  margin: 0.5rem 0;
  color: #666;
  line-height: 1.5;
}

.evaluation-date {
  font-size: 0.9rem;
  color: #888;
}

.average-score {
  padding: 1rem;
  background: #e7f3ff;
  border-radius: 4px;
  text-align: center;
  color: #2d7ef7;
  font-size: 1.1rem;
}

.evaluation-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.evaluation-form label {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
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
