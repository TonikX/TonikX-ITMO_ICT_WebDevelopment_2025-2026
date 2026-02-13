<template>
  <button class="app-button" @click="$emit('click')">
    <slot />
  </button>
</template>

<script setup>
</script>

<style scoped>
.app-button {
  padding: 10px 16px;
  border-radius: 10px;
  border: none;

  background: linear-gradient(135deg, #6d5dfc, #c850c0);
  color: white;
  font-weight: 500;

  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.app-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
}

.app-button:active {
  transform: translateY(0);
}
</style>
