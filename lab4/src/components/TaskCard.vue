<template>
  <div class="task-card">
    <h3 class="task-title">{{ task.title }}</h3>
    <p class="task-description">{{ task.description }}</p>
    <div class="task-info">
      <span v-if="task.curator_username" class="task-curator">
        Куратор: {{ task.curator_username }}
      </span>
      <span class="task-teams">Команд: {{ task.teams_count || 0 }}</span>
    </div>
    <div class="task-actions">
      <router-link :to="`/tasks/${task.id}`" class="btn">Подробнее</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TaskCard',
  props: {
    task: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.task-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.task-title {
  margin: 0 0 0.5rem 0;
  color: #2d7ef7;
  font-size: 1.25rem;
}

.task-description {
  margin: 0 0 1rem 0;
  color: #666;
  line-height: 1.5;
}

.task-info {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #888;
}

.task-actions {
  display: flex;
  gap: 0.5rem;
}
</style>
