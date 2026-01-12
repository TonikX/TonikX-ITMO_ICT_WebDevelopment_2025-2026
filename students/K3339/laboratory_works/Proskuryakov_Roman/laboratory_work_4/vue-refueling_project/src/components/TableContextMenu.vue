<template>
  <div 
    v-if="visible" 
    class="context-menu" 
    :style="{ left: `${position.x}px`, top: `${position.y}px` }"
    @click.stop
  >
    <div class="menu-item" @click="hideColumn">
      <span>Скрыть колонку</span>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  visible: Boolean,
  position: {
    type: Object,
    default: () => ({ x: 0, y: 0 })
  },
  columnKey: String,
  canHide: Boolean
})

const emit = defineEmits(['hide'])

const hideColumn = () => {
  if (props.canHide) {
    emit('hide', props.columnKey)
  }
}
</script>

<style scoped>
.context-menu {
  position: fixed;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  min-width: 150px;
}

.menu-item {
  padding: 8px 12px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.menu-item:hover {
  background-color: #f5f5f5;
}

.menu-item span {
  font-size: 0.9rem;
  color: #333;
}
</style>