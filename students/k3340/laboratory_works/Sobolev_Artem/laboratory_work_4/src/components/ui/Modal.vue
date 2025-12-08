<template>
  <div class="modal-overlay" @click.self="close">
    <div class="modal">
      <h2 class="modal-title">{{ title }}</h2>

      <Button
          class="modal-close"
          @click="close"
          icon-name="close"
          icon-width="32"
          icon-height="32"
      />

      <component :is="formComponent" @close="close" @submit="onFormSubmit" />
    </div>
  </div>
</template>

<script setup>
import Button from "@/components/ui/Button.vue";

defineProps({
  title: {
    type: String,
    required: true
  },
  formComponent: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(["close", "submit"]);

const close = () => emit("close");
const onFormSubmit = (payload) => emit("submit", payload);
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: var(--section-bg);
  padding: 36px;
  border-radius: 8px;
  max-width: 800px;
  width: 100%;
  position: relative;
  display: flex;
  align-items: center;
  flex-direction: column;
}

.modal-title {
  font-size: 24px;
  padding-bottom: 24px;
}

.modal-close {
  position: absolute;
  top: 12px;
  right: 12px;
  background: transparent;
  border: none;
  font-size: 24px;
  cursor: pointer;
}
</style>
