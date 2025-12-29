<template>
  <v-snackbar
      v-model="internalShow"
      :color="color"
      :timeout="3000"
      location="top"
      :elevation="24"
      style="z-index: 9999;"
  >
    <div class="d-flex align-center">
      <v-icon :color="color === 'success' ? 'white' : 'white'" class="mr-3">
        {{ icon }}
      </v-icon>
      <span class="text-body-1" style="color: white;">{{ text }}</span>
    </div>
    <template v-slot:actions>
      <v-btn
          variant="text"
          color="white"
          @click="internalShow = false"
      >
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  text: {
    type: String,
    required: true
  },
  color: {
    type: String,
    default: 'success'
  },
  icon: {
    type: String,
    default: 'mdi-check-circle'
  }
})

const emit = defineEmits(['close'])

const internalShow = ref(props.show)

watch(() => props.show, (newValue) => {
  internalShow.value = newValue
})

watch(internalShow, (newValue) => {
  if (!newValue) {
    emit('close')
  }
})
</script>