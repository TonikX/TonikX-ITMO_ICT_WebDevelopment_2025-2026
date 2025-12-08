<template>
  <main class="content">
    <slot></slot>
  </main>
</template>

<style scoped>
.content {
  flex: 1;
  transition: margin-left 0.3s ease, width 0.3s ease;
  padding: 20px;
  overflow-y: auto;
  max-height: 100%;
}
</style>