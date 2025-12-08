<template>
  <component
      v-if="iconComponent"
      :is="iconComponent"
      :width="width"
      :height="height"
  />
</template>

<script setup>
import { ref, watchEffect, markRaw } from 'vue'

const props = defineProps({
  name: {
    type: String,
    required: true
  },
  class: {
    type: String,
    default: ''
  },
  width: {
    type: [String, Number],
    default: 24
  },
  height: {
    type: [String, Number],
    default: 24
  }
})

const iconComponent = ref(null)

watchEffect(async () => {
  try {
    const mod = await import(`@/assets/icons/${props.name}.svg`)
    iconComponent.value = markRaw(mod.default)
  } catch (e) {
    console.warn(`Icon "${props.name}" not found`)
    iconComponent.value = null
  }
})
</script>