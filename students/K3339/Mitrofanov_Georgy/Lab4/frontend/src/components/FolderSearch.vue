<template>
  <v-text-field
    v-model="query"
    label="Search in this folder"
    clearable
    append-icon="mdi-magnify"
    @input="onInput"
  />
</template>

<script>
import { ref, watch } from 'vue';

export default {
  props: {
    modelValue: { type: String, default: '' },
    currentFolderId: { type: [Number, null], default: null }
  },
  emits: ['update:modelValue', 'search'],
  setup(props, { emit }) {
    const query = ref(props.modelValue)

    watch(() => props.modelValue, val => query.value = val)

    const onInput = () => {
      emit('update:modelValue', query.value)
      emit('search', query.value)
    }

    return { query, onInput }
  }
}
</script>