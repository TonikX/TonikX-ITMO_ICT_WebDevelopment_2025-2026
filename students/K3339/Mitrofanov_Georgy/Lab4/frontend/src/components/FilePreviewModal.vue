<template>
  <v-dialog :model-value="show" @update:model-value="$emit('update:show', $event)" max-width="800px">
    <v-card>
      <v-card-title>{{ file?.name }}</v-card-title>
      <v-card-text>
        <v-img v-if="isImage(file)" :src="file.full_url" max-height="600" contain />
        <video v-else-if="isVideo(file)" :src="file.full_url" controls style="max-width:100%; max-height:600px;" />
        <div v-else class="pa-4 text-center">
          <v-icon size="96">mdi-file</v-icon>
          <div class="mt-2">No preview available</div>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="$emit('update:show', false)">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "FilePreviewModal",
  props: {
    show: Boolean,
    file: Object
  },
  methods: {
    // Возвращает true для изображений (и проверяет, что есть URL превью)
    isImage(f) { return f?.mime_type?.startsWith('image/') && f.full_url },
    // Возвращает true для видеофайлов
    isVideo(f) { return f?.mime_type?.startsWith('video/') }
  }
}
</script>