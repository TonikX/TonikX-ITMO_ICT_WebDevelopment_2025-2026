<template>
  <div class="thumbnail-wrapper" @click="$emit('open', file)">

    <!-- PREVIEW BLOCK -->
    <div v-if="file.preview_url" class="preview-container">
      <v-img
        :src="file.preview_url"
        :height="size"
        :width="size"
        contain
        class="thumbnail-img"
      />

      <!-- Play overlay for video -->
      <div v-if="isVideo" class="play-overlay">
        <v-icon size="64" color="white">mdi-play-circle</v-icon>
      </div>
    </div>

    <!-- FALLBACK BLOCK -->
    <div v-else class="no-preview">
      <v-icon size="64">mdi-file</v-icon>
      <div class="filename">{{ file.name }}</div>
    </div>

  </div>
</template>

<script>
export default {
  name: "FileThumbnail",

  props: {
    file: { type: Object, required: true },
    size: { type: Number, default: 180 }
  },
  emits: ['open'],
  // Вычисляемые свойства
  computed: {
    // true, если файл — видео (для отображения плей-оверлея)
    isVideo() {
      return this.file?.mime_type?.startsWith("video/");
    }
  }
};
</script>

<style scoped>
.thumbnail-wrapper {
  width: 100%;
  height: 160px;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f6f6f6;
  position: relative;
}

.thumbnail-img {
  object-fit: contain;
  width: 100%;
  height: 100%;
}

.no-preview {
  text-align: center;
  color: #999;
}

.filename {
  font-size: 12px;
  margin-top: 4px;
  color: #666;
}

.play-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>