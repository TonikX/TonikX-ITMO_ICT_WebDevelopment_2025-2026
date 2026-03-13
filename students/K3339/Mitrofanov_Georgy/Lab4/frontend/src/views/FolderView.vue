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

    watch(() => route.params.id, async (newId) => {
      console.log('route.params.id changed:', newId)
      await load()
    }, { immediate: true })
        onMounted(load)

        // Создание папки
    const createFolder = async () => {
      const name = prompt('Folder name')
      if (!name) return
      
      const token = localStorage.getItem('token')
      console.log('Token:', token) // проверь в консоли браузера
      
      try {
        const response = await fetch('/api/folders/', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ 
            name: name, 
            parent: currentFolderId.value || null 
          })
        })
        
        const data = await response.json()
        console.log('Response:', data)
        
        if (response.ok) {
          await load()
        } else {
          alert('Failed to create folder: ' + (data.error || 'Unknown error'))
        }
      } catch (e) {
        console.error('Error:', e)
        alert('Failed to create folder')
      }
    }

    // Открыть папку
    const openFolder = async (f) => {
      await load()
    }

    // Переименовать папку
    const renameFolder = async (folder) => {
      const name = prompt('New name', folder.name)
      if (!name) return
      try {
        const token = localStorage.getItem('token')
        await fetch(`/api/folders/${folder.id}/`, {
          method: 'PATCH',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ name })
        })
        await load()
      } catch (e) {
        alert('Failed to rename folder')
      }
    }

    // Удалить папку
    const deleteFolder = async (folder) => {
      if (!confirm('Delete this folder?')) return
      try {
        const token = localStorage.getItem('token')
        await fetch(`/api/folders/${folder.id}/`, {
          method: 'DELETE',
          headers: { 'Authorization': `Bearer ${token}` }
        })
        await load()
      } catch (e) {
        alert('Failed to delete folder')
      }
    }

    // Переместить папку
    const moveFolder = async ({ sourceId, targetId }) => {
      try {
        const token = localStorage.getItem('token')
        await fetch(`/api/folders/${sourceId}/`, {
          method: 'PATCH',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ parent: targetId })
        })
        await load()
      } catch (e) {
        alert('Failed to move folder')
      }
    }

    // Переименовать файл
    const renameFile = async (file) => {
      const name = prompt('New name', file.name)
      if (!name) return
      try {
        const token = localStorage.getItem('token')
        await fetch(`/api/files/${file.id}/`, {
          method: 'PATCH',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ name })
        })
        await load()
      } catch (e) {
        alert('Failed to rename file')
      }
    }

    // Переместить файл
    const moveFile = async ({ sourceId, targetId }) => {
      try {
        const token = localStorage.getItem('token')
        await fetch(`/api/files/${sourceId}/move/`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ folder_id: targetId })
        })
        await load()
      } catch (e) {
        alert('Failed to move file')
      }
    }

    // Удалить файл
    const deleteFile = async (file) => {
      if (!confirm('Delete this file?')) return
      try {
        const token = localStorage.getItem('token')
        await fetch(`/api/files/${file.id}/`, {
          method: 'DELETE',
          headers: { 'Authorization': `Bearer ${token}` }
        })
        await load()
      } catch (e) {
        alert('Failed to delete file')
      }
    }

    // Скачать файл
    const download = async (f) => {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch(`/api/files/${f.id}/download/`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = f.name
        document.body.appendChild(a)
        a.click()
        a.remove()
        window.URL.revokeObjectURL(url)
      } catch (e) {
        alert('Failed to download file')
      }
    }
    const openPreview = f => { preview.value = { show: true, file: f } }
    const closePreview = () => { preview.value = { show: false, file: null } }

    return { folder, files, folders, preview, createFolder, openFolder, renameFolder, deleteFolder, moveFolder, renameFile, moveFile, deleteFile, download, openPreview, closePreview }
  }
}
</script>