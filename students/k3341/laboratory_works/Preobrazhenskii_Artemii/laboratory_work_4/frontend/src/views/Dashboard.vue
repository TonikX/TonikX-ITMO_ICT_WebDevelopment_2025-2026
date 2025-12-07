<template>
  <v-container>
    <h2>Welcome to brvjeo Cloud</h2>

    <v-row class="mb-4">
      <v-col cols="12" sm="8">
        <v-text-field
          v-model="searchQuery"
          label="Search files and folders"
          clearable
          append-icon="mdi-magnify"
          @input="onSearch"
        />
      </v-col>
      <v-col cols="12" sm="4" class="text-right">
        <v-btn color="primary" @click="$router.push({ name: 'files' })">Go to Files</v-btn>
        <v-btn color="primary" class="ml-2" @click="showUpload = true"><v-icon left>mdi-cloud-upload</v-icon>Upload</v-btn>
        <v-btn color="primary" class="ml-2" @click="createFolder"><v-icon left>mdi-folder-plus</v-icon>New Folder</v-btn>
        <FileUploadDialog v-model="showUpload" @uploaded="onUploaded" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { ref } from 'vue';
import FileUploadDialog from '../components/FileUploadDialog.vue';
import api from '../utils/api';

export default {
  components: { FileUploadDialog },
  setup() {
    const searchQuery = ref('')
    const showUpload = ref(false)
    const onSearch = () => {}
    const createFolder = async () => {
      const name = prompt('Folder name')
      if (!name) return
      try { await api.post('/folders/', { name, parent: null }); alert('Folder created') }
      catch (e) { alert('Failed to create folder') }
    }
    const onUploaded = () => { alert('Upload finished'); }
    return { searchQuery, onSearch, showUpload, createFolder, onUploaded }
  }
}
</script>