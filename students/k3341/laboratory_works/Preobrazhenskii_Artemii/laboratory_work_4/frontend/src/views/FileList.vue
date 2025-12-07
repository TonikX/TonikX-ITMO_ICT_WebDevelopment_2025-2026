<template>
  <div>
    <!-- Breadcrumbs (left-aligned, styled) -->
    <div v-if="breadcrumbs.length" class="py-2 content-left-padding breadcrumbs-wrap">
      <div class="breadcrumbs-inline">
        <span v-for="(crumb, idx) in breadcrumbs" :key="idx">
          <a href="#" @click.prevent="navigateTo(crumb.folderId)" class="crumb-link">{{ crumb.text }}</a>
          <span v-if="idx < breadcrumbs.length - 1" class="crumb-sep">&nbsp;›&nbsp;</span>
        </span>
      </div>
    </div>

    <!-- File & Folder Grid -->
    <div class="file-area content-left-padding">
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
      <FilePreviewModal :show="preview.show" :file="preview.file" @update:show="val => { if(!val) closePreview() }" />
      <!-- Upload Dialog -->
      <FileUploadDialog
        :model-value="showUpload"
        :currentFolderId="currentFolderId"
        @update:model-value="showUpload = $event"
        @uploaded="load"
      />
    </div>

              <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      timeout="4000"
    >
      {{ snackbar.message }}
    </v-snackbar>
  </div>
</template>

<script>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import FileGrid from '../components/FileGrid.vue'
import FilePreviewModal from '../components/FilePreviewModal.vue'
import FileUploadDialog from '../components/FileUploadDialog.vue'
import FolderGrid from '../components/FolderGrid.vue'
// FolderSearch не используется в этом файле — убран
import api from '../utils/api'



export default {
  // Регистрируем компоненты, используемые во view
  components: { FileGrid, FolderGrid, FilePreviewModal, FileUploadDialog },

  setup() {
    // Основные реактивные состояния
    // files: список файлов, отображаемых на странице
    const files = ref([])
    // folders: список папок в текущем представлении (корень или внутри папки)
    const folders = ref([])
    const searchQuery = ref('')
    const snackbar = ref({ show: false, message: '', color: 'error' })
    const preview = ref({ show: false, file: null })
    // currentFolderId = null означает корень
    const currentFolderId = ref(null)
    const folderHistory = ref([])
    const showUpload = ref(false)

    const syncUrlWithFolder = () => {
      const folderId = currentFolderId.value ? `?folder=${currentFolderId.value}` : ''
      window.history.replaceState({}, '', `/file-list${folderId}`)
    }

    const loadFolderFromUrl = () => {
      const params = new URLSearchParams(window.location.search)
      const folderId = params.get('folder')
      if (folderId) currentFolderId.value = parseInt(folderId, 10)
    }

    const breadcrumbs = computed(() => {
      const crumbs = [{ text: 'Root', folderId: null }]
      folderHistory.value.forEach(f => crumbs.push({ text: f.name, folderId: f.id }))
      return crumbs
    })

    // Загрузка списка файлов/папок.
    // Если задана currentFolderId — запрашиваем содержимое папки,
    // иначе загружаем корневые файлы и папки.
    const load = async () => {
      try {
        const resFiles = currentFolderId.value
          ? await api.get(`/folders/${currentFolderId.value}/content/`)
          : {
              data: {
                files: (await api.get('/files/')).data.filter(f => !f.folder),
                folders: (await api.get('/folders/')).data.filter(f => !f.parent)
              }
            }

        files.value = resFiles.data?.files ?? resFiles.data ?? []
        folders.value = resFiles.data?.folders ?? folders.value
      } catch (e) {
        console.error(e)
        snackbar.value = { show: true, message: 'Failed to load files', color: 'error' }
      }
    }

    const headerUploadHandler = () => { showUpload.value = true }
    const headerCreateFolderHandler = () => { createFolder() }
    const headerSearchHandler = (e) => { search(e.detail) }

    onMounted(() => {
      loadFolderFromUrl()
      load()
      // Listen to header events dispatched as window CustomEvents
      window.addEventListener('brvjeo:upload', headerUploadHandler)
      window.addEventListener('brvjeo:create-folder', headerCreateFolderHandler)
      window.addEventListener('brvjeo:search', headerSearchHandler)
    })

    // cleanup
    onUnmounted(() => {
      window.removeEventListener('brvjeo:upload', headerUploadHandler)
      window.removeEventListener('brvjeo:create-folder', headerCreateFolderHandler)
      window.removeEventListener('brvjeo:search', headerSearchHandler)
    })

    watch(currentFolderId, syncUrlWithFolder)

    const search = async query => {
      if (!query?.trim()) return load()
      try {
        // fetch all files and filter client-side to avoid backend search inconsistencies
        const res = await api.get('/files/')
        const all = Array.isArray(res.data) ? res.data : res.data?.results ?? []
        const q = query.toLowerCase()
        files.value = all.filter(f => (f.name || '').toLowerCase().includes(q))
        folders.value = []
      } catch (e) {
        console.error('Search failed', e)
        snackbar.value = { show: true, message: 'Search failed', color: 'error' }
      }
    }

    const navigateTo = folderId => {
      currentFolderId.value = folderId || null
      folderHistory.value = folderId ? folderHistory.value.filter(f => f.id !== folderId) : []
      searchQuery.value = ''
      load()
    }

    const openFolder = async folder => {
      currentFolderId.value = folder.id
      folderHistory.value.push(folder)
      searchQuery.value = ''
      await load()
    }

    const createFolder = async () => {
      const name = prompt('Folder name')
      if (!name) return
      try {
        await api.post('/folders/', { name, parent: currentFolderId.value })
        await load()
      } catch (e) {
        snackbar.value = { show: true, message: 'Failed to create folder', color: 'error' }
      }
    }

    const renameFolder = async folder => {
      const name = prompt('New name', folder.name)
      if (!name) return
      try {
        await api.patch(`/folders/${folder.id}/`, { name })
        await load()
      } catch (e) {
        snackbar.value = { show: true, message: 'Failed to rename folder', color: 'error' }
      }
    }

    const deleteFolder = async folder => {
      if (!confirm(`Delete "${folder.name}"?`)) return
      try {
        await api.delete(`/folders/${folder.id}/`)
        await load()
      } catch (e) {
        snackbar.value = { show: true, message: 'Failed to delete folder', color: 'error' }
      }
    }

    const moveFolder = async ({ sourceId, targetId }) => {
      try {
        await api.patch(`/folders/${sourceId}/`, { parent: targetId })
        await load()
      } catch (e) {
        snackbar.value = { show: true, message: 'Failed to move folder', color: 'error' }
      }
    }

    const renameFile = async f => {
      const name = prompt('New file name', f.name)
      if (!name) return
      try {
        await api.patch(`/files/${f.id}/`, { name })
        await load()
      } catch (e) {
        snackbar.value = { show: true, message: 'Failed to rename file', color: 'error' }
      }
    }

    const moveFile = async ({ sourceId, targetId }) => {
      try {
        await api.post(`/files/${sourceId}/move/`, { folder_id: targetId })
        await load()
      } catch (e) {
        snackbar.value = { show: true, message: 'Failed to move file', color: 'error' }
      }
    }

    const deleteFile = async f => {
      if (!confirm(`Delete "${f.name}"?`)) return
      try {
        await api.delete(`/files/${f.id}/`)
        await load()
      } catch (e) {
        snackbar.value = { show: true, message: 'Failed to delete file', color: 'error' }
      }
    }

    const download = async f => {
      try {
        const res = await api.get(`/files/${f.id}/download/`, { responseType: 'blob' })
        const blob = new Blob([res.data], { type: res.headers['content-type'] })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = f.name
        document.body.appendChild(a)
        a.click()
        a.remove()
        URL.revokeObjectURL(url)
      } catch (e) {
        snackbar.value = { show: true, message: 'Failed to download file', color: 'error' }
      }
    }

    const openPreview = f => { preview.value = { show: true, file: f } }
    const closePreview = () => { preview.value = { show: false, file: null } }

    // Handle HeaderBar events
    const handleHeaderSearch = (query) => {
      searchQuery.value = query
      search(query)
    }

    const handleHeaderUpload = () => {
      showUpload.value = true
    }

    const handleHeaderCreateFolder = () => {
      createFolder()
    }

    return {
      files,
      folders,
      searchQuery,
      snackbar,
      preview,
      breadcrumbs,
      showUpload,
      currentFolderId,

      load,
      search,
      navigateTo,
      openFolder,
      createFolder,
      renameFolder,
      deleteFolder,
      moveFolder,

      renameFile,
      moveFile,
      deleteFile,
      download,

      openPreview,
      closePreview
    }
  }
}
</script>

<style scoped>
.breadcrumbs-inline { font-size: 0.95rem; color: rgba(0,0,0,0.8); }
.crumb-link { color: #1976d2; text-decoration: none; cursor: pointer; font-weight: 500 }
.crumb-link { color: #1976d2; text-decoration: none; cursor: pointer; font-weight: 700 }
.crumb-sep { color: rgba(0,0,0,0.45); }
.file-grid-container { max-width: 100%; }
.content-left-padding { padding-left: 24px; padding-right: 24px; }

@media (max-width: 600px) {
  .file-card { height: 220px !important; }
  .folder-card { height: 100px !important; }
}
</style>