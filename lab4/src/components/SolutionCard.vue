<template>
  <div class="solution-card">
    <h3 class="solution-title">{{ solution.team_name }} - {{ solution.task_title }}</h3>
    <p class="solution-description">{{ solution.description }}</p>
    <div class="solution-info">
      <span class="solution-date">
        Опубликовано: {{ formatDate(solution.published_at) }}
      </span>
      <span v-if="solution.evaluations_count > 0" class="solution-evaluations">
        Оценок: {{ solution.evaluations_count }}
      </span>
      <span v-if="solution.average_score !== null" class="solution-score">
        Средний балл: {{ solution.average_score }}
      </span>
    </div>
    <div v-if="solution.file_url" class="solution-file">
      <a :href="solution.file_url" target="_blank" class="btn btn-secondary">Скачать файл</a>
    </div>
    <div class="solution-actions">
      <router-link :to="`/solutions/${solution.id}`" class="btn">Подробнее</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SolutionCard',
  props: {
    solution: {
      type: Object,
      required: true
    }
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString('ru-RU')
    }
  }
}
</script>

<style scoped>
.solution-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.solution-title {
  margin: 0 0 0.5rem 0;
  color: #2d7ef7;
  font-size: 1.25rem;
}

.solution-description {
  margin: 0 0 1rem 0;
  color: #666;
  line-height: 1.5;
}

.solution-info {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #888;
}

.solution-file {
  margin-bottom: 1rem;
}

.solution-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-secondary {
  background: #6c757d;
}

.btn-secondary:hover {
  background: #5a6268;
}
</style>
