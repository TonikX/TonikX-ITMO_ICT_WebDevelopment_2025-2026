<template>
  <div class="cells">
    <div class="cells__actions">
      <Button
          label="Добавить ячейку"
          mode="violet"
          location="page-action"
      />
      <!-- <Button
          label="Удалить ячейку"
          mode="violet"
          location="page-action"
      /> -->
    </div>

  </div>
</template>

<script setup>
import Button from "@/components/ui/Button.vue";
</script>

<style lang="scss" scoped>
.cells {
  &__header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }

  &__title {
    margin-bottom: 16px;
  }

  &__actions {
    margin-bottom: 16px;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    gap: 32px;
  }
}

.worker-info {
  padding: 16px;
  border: 1px solid #d0d0d0;
  border-radius: 8px;
  max-width: 300px;
  background: #f9f9f9;
}

.loading {
  color: gray;
  font-style: italic;
}
</style>
