<template>
  <v-row class="folder-row">
    <v-col v-for="folder in folders" :key="folder.id" cols="12" sm="6" md="4" lg="3" xl="2" class="folder-grid-col">
      <v-card
        class="folder-card"
        draggable
        @dragstart="startDrag($event, folder)"
        @dragover.prevent
        @drop="handleDrop($event, folder)"
        @click="$emit('open', folder)"
      >
        <v-card-title class="d-flex align-center">
          <v-icon left large color="amber">mdi-folder</v-icon>
          <span class="text-truncate">{{ folder.name }}</span>
        </v-card-title>
        <v-card-actions>
          <v-btn icon small @click.stop="$emit('rename', folder)"><v-icon>mdi-pencil</v-icon></v-btn>
          <v-btn icon small @click.stop="$emit('delete', folder)"><v-icon>mdi-delete</v-icon></v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  // Компонент отображает сетку папок (карточки) и обрабатывает drag/drop
  props: { folders: Array },
  methods: {
    startDrag(e, folder) {
      e.dataTransfer.effectAllowed = 'move'
      e.dataTransfer.setData('application/json', JSON.stringify({ type: 'folder', id: folder.id }))
    },
    handleDrop(e, folder) {
      e.stopPropagation()
      e.preventDefault()
      const data = e.dataTransfer.getData('application/json')
      if (data) {
        const item = JSON.parse(data)
        if (item.type === 'folder' && item.id !== folder.id) {
          this.$emit('move', { sourceId: item.id, targetId: folder.id })
        }
        if (item.type === 'file') {
          // moving a file into this folder
          this.$emit('move', { sourceId: item.id, targetId: folder.id })
        }
      }
    }
  }
}
</script>

<style scoped>
.folder-card {
  cursor: pointer;
  transition: box-shadow 0.2s, transform 0.2s;
  border-radius: 8px;
}
.folder-card:hover {
  box-shadow: 0 4px 24px rgba(0,0,0,0.12);
  transform: translateY(-2px);
}
.text-truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.folder-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 120px;
}
.folder-card .v-card-title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.folder-row { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 16px; margin: 0; }
.folder-row > .folder-grid-col { padding: 0; display: block; width: 100%; max-width: 100%; }
.folder-row > .folder-grid-col .folder-card { box-sizing: border-box; }

@media (max-width: 1200px) { .folder-row { grid-template-columns: repeat(4, 1fr); } }
@media (max-width: 960px) { .folder-row { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 640px) { .folder-row { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 420px) { .folder-row { grid-template-columns: repeat(1, 1fr); } }

.folder-card { height: 160px; display:flex; flex-direction:column; justify-content:center; align-items:flex-start; padding:12px; }
.folder-card .v-icon { font-size: 42px; }
.folder-card .v-card-title { display:flex; align-items:center; gap:8px; }

/* reduce size of edit/delete buttons in folder cards */
.folder-card .v-card-actions { padding: 6px 0 0 0; }
.folder-card .v-card-actions .v-btn { min-width: 32px; height: 32px; padding: 4px; }
.folder-card .v-card-actions .v-icon { font-size: 18px; }
</style>