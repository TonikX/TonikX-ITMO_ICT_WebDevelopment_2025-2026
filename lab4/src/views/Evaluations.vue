<template>
  <div class="evaluations-page">
    <h1>Оценки</h1>

    <div class="evaluations-tabs">
      <button
        @click="activeTab = 'solutions'"
        :class="['tab-btn', { active: activeTab === 'solutions' }]"
      >
        Решения для оценки
      </button>
      <button
        @click="activeTab = 'my'"
        :class="['tab-btn', { active: activeTab === 'my' }]"
      >
        Мои оценки
      </button>
    </div>

    <div v-if="activeTab === 'solutions'" class="solutions-tab">
      <div v-if="loadingSolutions" class="loading">Загрузка...</div>
      <div v-else-if="solutionsError" class="error-message">{{ solutionsError }}</div>
      <div v-else-if="solutions.length === 0" class="empty">Решений для оценки нет</div>
      <div v-else class="solutions-list">
        <div v-for="solution in solutions" :key="solution.id" class="solution-item">
          <h3>{{ solution.team_name }} - {{ solution.task_title }}</h3>
          <p>{{ solution.description }}</p>
          <div class="solution-meta">
            <span>Опубликовано: {{ formatDate(solution.published_at) }}</span>
            <span v-if="solution.evaluations_count > 0">
              Оценок: {{ solution.evaluations_count }}
            </span>
            <span v-if="solution.average_score !== null">
              Средний балл: {{ solution.average_score }}
            </span>
          </div>
          <router-link :to="`/solutions/${solution.id}`" class="btn">Оценить</router-link>
        </div>
      </div>
    </div>

    <div v-if="activeTab === 'my'" class="my-evaluations-tab">
      <div v-if="loadingEvaluations" class="loading">Загрузка...</div>
      <div v-else-if="evaluationsError" class="error-message">{{ evaluationsError }}</div>
      <div v-else-if="evaluations.length === 0" class="empty">Вы еще не оценили ни одного решения</div>
      <div v-else class="evaluations-list">
        <div v-for="evaluation in evaluations" :key="evaluation.id" class="evaluation-item">
          <h3>{{ evaluation.solution_team_name }} - {{ evaluation.solution_task_title }}</h3>
          <div class="evaluation-info">
            <span class="evaluation-score">Балл: {{ evaluation.score }}</span>
            <span class="evaluation-date">{{ formatDate(evaluation.created_at) }}</span>
          </div>
          <p v-if="evaluation.comment" class="evaluation-comment">{{ evaluation.comment }}</p>
          <router-link :to="`/solutions/${evaluation.solution}`" class="btn">Посмотреть решение</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { evaluationsAPI, apiErrorMessage } from '@/api'

export default {
  name: 'Evaluations',
  data() {
    return {
      activeTab: 'solutions',
      solutions: [],
      evaluations: [],
      loadingSolutions: false,
      loadingEvaluations: false,
      solutionsError: '',
      evaluationsError: ''
    }
  },
  mounted() {
    this.loadSolutions()
    this.loadMyEvaluations()
  },
  methods: {
    async loadSolutions() {
      this.loadingSolutions = true
      this.solutionsError = ''
      try {
        this.solutions = await evaluationsAPI.getSolutionsByDate()
      } catch (e) {
        this.solutionsError = apiErrorMessage(e)
      } finally {
        this.loadingSolutions = false
      }
    },
    async loadMyEvaluations() {
      this.loadingEvaluations = true
      this.evaluationsError = ''
      try {
        this.evaluations = await evaluationsAPI.getMyEvaluations()
      } catch (e) {
        this.evaluationsError = apiErrorMessage(e)
      } finally {
        this.loadingEvaluations = false
      }
    },
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString('ru-RU')
    }
  },
  watch: {
    activeTab() {
      if (this.activeTab === 'solutions') {
        this.loadSolutions()
      } else {
        this.loadMyEvaluations()
      }
    }
  }
}
</script>

<style scoped>
.evaluations-page {
  max-width: 1000px;
  margin: 0 auto;
}

.evaluations-page h1 {
  margin: 0 0 2rem 0;
  color: #2d7ef7;
}

.evaluations-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  border-bottom: 2px solid #eee;
}

.tab-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  background: transparent;
  color: #666;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
  transition: color 0.2s;
}

.tab-btn:hover {
  color: #2d7ef7;
}

.tab-btn.active {
  color: #2d7ef7;
  border-bottom-color: #2d7ef7;
}

.solutions-list,
.evaluations-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.solution-item,
.evaluation-item {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.solution-item h3,
.evaluation-item h3 {
  margin: 0 0 0.5rem 0;
  color: #2d7ef7;
}

.solution-item p,
.evaluation-comment {
  margin: 0.5rem 0;
  color: #666;
  line-height: 1.5;
}

.solution-meta,
.evaluation-info {
  display: flex;
  gap: 1rem;
  margin: 1rem 0;
  font-size: 0.9rem;
  color: #888;
}

.evaluation-score {
  color: #2d7ef7;
  font-weight: bold;
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
</style>
