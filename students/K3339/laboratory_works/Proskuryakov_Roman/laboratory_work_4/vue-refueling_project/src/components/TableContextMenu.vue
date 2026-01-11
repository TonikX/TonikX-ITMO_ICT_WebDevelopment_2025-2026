<template>
  <div 
    v-if="visible" 
    class="context-menu" 
    :style="{ left: `${position.x}px`, top: `${position.y}px` }"
    @click.stop
  >
    <v-list density="compact" class="pa-0">
      <v-list-item 
        @click="hideColumn" 
        :disabled="!canHide"
        class="px-3 py-2"
      >
        <template v-slot:prepend>
          <v-icon icon="mdi-eye-off" size="small"></v-icon>
        </template>
        <v-list-item-title class="text-caption">
          Скрыть колонку
        </v-list-item-title>
      </v-list-item>
    </v-list>
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
  z-index: 1000;
  box-shadow: 0 5px 5px -3px var(--v-shadow-key-umbra-opacity, rgba(0, 0, 0, 0.2)), 
              0 8px 10px 1px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.14)), 
              0 3px 14px 2px var(--v-shadow-key-ambient-opacity, rgba(0, 0, 0, 0.12));
  border-radius: 4px;
  background: white;
  min-width: 160px;
}
</style>