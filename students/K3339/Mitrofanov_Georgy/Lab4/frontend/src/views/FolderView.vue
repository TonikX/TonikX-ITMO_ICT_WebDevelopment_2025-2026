<template>
  <v-container>
    <h3>Folder: {{ folder?.name }}</h3>

    <FolderGrid
      :folders="folders"
      @open="openFolder"
      @rename="renameFolder"
      @delete="deleteFolder"
      @move="moveFolder"
    />

    <FileGrid
      :files="files"
      @preview="openPreview"
      @download="download"
      @delete="deleteFile"
      @rename="renameFile"
      @move="moveFile"
    />

    <FilePreviewModal :show="preview.show" :file="preview.file" @close="closePreview" />
  </v-container>
</template>

<script>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import FileGrid from '../components/FileGrid.vue'
import FilePreviewModal from '../components/FilePreviewModal.vue'
import FolderGrid from '../components/FolderGrid.vue'
import api from '../utils/api'

export default {
  components: { FileGrid, FolderGrid, FilePreviewModal },
  setup() {
    const route = useRoute()
    const folder = ref(null)
    const files = ref([])
    const folders = ref([])
    const preview = ref({ show: false, file: null })

    const load = async () => {
      const res = await api.get(`/folders/${route.params.id}/content/`)
      folder.value = { id: route.params.id, name: res.data.name || 'Folder' }
      files.value = res.data.files
      folders.value = res.data.folders
    }
    onMounted(load)

    const openFolder = f => load()
    const renameFolder = f => {}
    const deleteFolder = f => {}
    const moveFolder = f => {}
    const renameFile = f => {}
    const moveFile = f => {}
    const deleteFile = f => {}
    const download = f => {}
    const openPreview = f => { preview.value = { show: true, file: f } }
    const closePreview = () => { preview.value = { show: false, file: null } }

    return { folder, files, folders, preview, openFolder, renameFolder, deleteFolder, moveFolder, renameFile, moveFile, deleteFile, download, openPreview, closePreview }
  }
}
</script>