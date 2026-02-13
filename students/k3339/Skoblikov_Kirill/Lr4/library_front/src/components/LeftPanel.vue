<template>
  <aside class="side-bar">
    <AppButton @click="$emit('add')">Добавить</AppButton>
    <AppButton @click="$emit('update')">Изменить</AppButton>
    <AppButton @click="$emit('delete')">Удалить</AppButton>
  </aside>
</template>

<script setup>
import AppButton from '@/components/UI/AppButton.vue'
</script>


<style scoped>
.side-bar {
  height: calc(100vh - 80px);
  width: 180px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;

  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(8px);
}
</style>
