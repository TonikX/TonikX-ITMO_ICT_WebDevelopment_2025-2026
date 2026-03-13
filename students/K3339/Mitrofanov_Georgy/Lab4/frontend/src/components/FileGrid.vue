<template>
  <v-container fluid class="file-grid-container">
    <v-row class="file-grid-row">
      <v-col v-for="file in files" :key="file.id" cols="12" sm="6" md="4" lg="3" xl="2" class="file-grid-col">
        <v-card
          class="file-card"
          draggable
          @dragstart="startDrag($event, file)"
          @dragover.prevent
          @drop="handleDrop($event, file)"
        >
          <!-- CLICK -> emit preview(file) -->
              <FileThumbnail :file="file" @open="$emit('preview', file)" />

          <v-card-title class="text-truncate">{{ file.name }}</v-card-title>
          <v-card-subtitle class="text-truncate">{{ formatSize(file.size) }}</v-card-subtitle>

          <v-card-actions>
            <v-btn icon small @click.stop="$emit('download', file)"><v-icon>mdi-download</v-icon></v-btn>
            <v-btn icon small @click.stop="$emit('delete', file)"><v-icon>mdi-delete</v-icon></v-btn>
            <v-btn icon small @click.stop="$emit('rename', file)"><v-icon>mdi-pencil</v-icon></v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import FileThumbnail from './FileThumbnail.vue';

export default {
  name: "FileGrid",
  // Компонент отображает сетку файлов в виде карточек.
  // Проп `files` — массив объектов файлов.
  props: { files: Array },
  components: { FileThumbnail },
  emits: ['preview', 'download', 'delete', 'rename', 'move'],
  methods: {
    startDrag(e, file) {
      e.dataTransfer.effectAllowed = 'move'
      e.dataTransfer.setData('application/json', JSON.stringify({ type: 'file', id: file.id }))
    },
    handleDrop(e, file) {
      e.stopPropagation()
      const data = e.dataTransfer.getData('application/json')
      if (data) {
        const item = JSON.parse(data)
        if (item.type === 'file' && item.id !== file.id) this.$emit('move', { sourceId: item.id, targetId: file.id })
      }
    },
    formatSize(bytes) {
      if (!bytes) return '0 B'
      const k = 1024
      const sizes = ['B','KB','MB','GB']
      const i = Math.floor(Math.log(bytes)/Math.log(k))
      return Math.round(bytes / Math.pow(k,i)*100)/100 + ' ' + sizes[i]
    }
  }
}
</script>

<style scoped>
.file-card {
  cursor: pointer;
  transition: box-shadow 0.2s, transform 0.2s;
  border-radius: 8px;
}
.file-card:hover {
  box-shadow: 0 4px 24px rgba(0,0,0,0.12);
  transform: translateY(-2px);
}
.file-card {
  display: flex;
  flex-direction: column;
  height: 320px;
}
.file-card .v-card-title,
.file-card .v-card-subtitle {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* robust single-line clamp for long/nospace filenames */
.file-card .v-card-title {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.file-card .v-card-subtitle {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  color: rgba(0,0,0,0.6);
  font-size: 0.85rem;
}

/* allow grid to use full width and control gutter */
.file-grid-container {
  max-width: 100%;
}
.file-grid-row {
  margin: 0;
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr)); /* max 5 columns */
  gap: 16px;
}

.file-grid-row > .file-grid-col { padding: 0; }
.file-grid-row > .file-grid-col { display: block; width: 100%; max-width: 100%; }

/* ensure grid children are true grid items and not affected by Vuetify flex rules */
.file-grid-row > .file-grid-col .file-card { box-sizing: border-box; }

/* Responsive: reduce columns on smaller screens */
@media (max-width: 1200px) {
  .file-grid-row { grid-template-columns: repeat(4, 1fr); }
}
@media (max-width: 960px) {
  .file-grid-row { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 640px) {
  .file-grid-row { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 420px) {
  .file-grid-row { grid-template-columns: repeat(1, 1fr); }
}

.file-card { display: flex; flex-direction: column; height: 300px; box-sizing: border-box; }
.file-card .thumbnail-wrapper { height: 160px; }
</style>