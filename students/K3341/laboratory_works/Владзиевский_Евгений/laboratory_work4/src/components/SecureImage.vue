<template>
  <div>
    <v-skeleton-loader v-if="loading" type="image"></v-skeleton-loader>
    <v-img
      v-else-if="src"
      :src="src"
      :aspect-ratio="aspectRatio"
      :cover="cover"
      :class="imgClass"
    ></v-img>
    <div v-else class="image-placeholder"></div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { resolveImageSrc } from '../utils/images'

const props = defineProps({
  image: {
    type: [String, Object],
    default: '',
  },
  aspectRatio: {
    type: [Number, String],
    default: 1,
  },
  cover: {
    type: Boolean,
    default: true,
  },
  imgClass: {
    type: [String, Array, Object],
    default: '',
  },
})

const src = ref('')
const loading = ref(false)

const load = async () => {
  if (!props.image) {
    src.value = ''
    return
  }
  loading.value = true
  try {
    src.value = await resolveImageSrc(props.image)
  } catch (e) {
    src.value = ''
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(
  () => props.image,
  () => load(),
)
</script>

<style scoped>
.image-placeholder {
  width: 100%;
  padding-top: 56%;
  background: repeating-linear-gradient(45deg, #f2f2f7, #f2f2f7 10px, #e6e6ec 10px, #e6e6ec 20px);
  border-radius: 12px;
}
</style>
