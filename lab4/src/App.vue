<template>
  <div class="app">
    <Navigation />
    <div class="app-content">
      <router-view />
    </div>
  </div>
</template>

<script>
import Navigation from '@/components/Navigation.vue'

export default {
  name: 'App',
  components: {
    Navigation
  }
}
</script>

<style scoped>
.app {
  min-height: 100vh;
  background: #f5f5f5;
}

.app-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px 24px 24px;
}
</style>
