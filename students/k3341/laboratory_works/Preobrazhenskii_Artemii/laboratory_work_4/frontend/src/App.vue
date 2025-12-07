<template>
  <v-app>
    <HeaderBar 
      @search="handleSearch"
      @upload="handleUpload"
      @create-folder="handleCreateFolder"
    />
    <v-main>
      <router-view 
        :key="fileListKey"
        :header-search="headerSearch"
        :show-upload="showUploadDialog"
        @upload-closed="showUploadDialog = false"
        @folder-created="handleFolderCreated"
      />
    </v-main>
  </v-app>
</template>

<script>
import { ref } from 'vue';
import HeaderBar from './components/HeaderBar.vue';

export default {
  components: { HeaderBar },
  setup() {
    const headerSearch = ref('')
    const showUploadDialog = ref(false)
    const fileListKey = ref(0)

    return {
      headerSearch,
      showUploadDialog,
      fileListKey,
      handleSearch: (query) => { headerSearch.value = query },
      handleUpload: () => { showUploadDialog.value = true },
      handleCreateFolder: () => { /* Handled in FileList */ },
      handleFolderCreated: () => { fileListKey.value++ }
    }
  }
}
</script>