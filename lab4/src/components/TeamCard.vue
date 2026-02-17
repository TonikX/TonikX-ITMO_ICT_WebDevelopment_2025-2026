<template>
  <div class="team-card">
    <h3 class="team-name">{{ team.name }}</h3>
    <p v-if="team.motto" class="team-motto">{{ team.motto }}</p>
    <div class="team-info">
      <span class="team-captain">Капитан: {{ team.captain_username }}</span>
      <span v-if="team.selected_task_title" class="team-task">
        Задача: {{ team.selected_task_title }}
      </span>
      <span class="team-members">Участников: {{ team.members_count || 0 }}</span>
    </div>
    <div class="team-actions">
      <router-link :to="`/teams/${team.id}`" class="btn">Подробнее</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TeamCard',
  props: {
    team: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.team-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.team-name {
  margin: 0 0 0.5rem 0;
  color: #2d7ef7;
  font-size: 1.25rem;
}

.team-motto {
  margin: 0 0 1rem 0;
  color: #666;
  font-style: italic;
}

.team-info {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #888;
}

.team-actions {
  display: flex;
  gap: 0.5rem;
}
</style>
