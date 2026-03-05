<template>
  <v-app-bar app color="primary" dark dense>
    <v-toolbar-title>brvjeo Cloud</v-toolbar-title>
    <v-spacer />
      <div class="left-search" v-if="auth.isAuthenticated">
      <v-text-field
        v-model="searchQuery"
        placeholder="Search files..."
        dense
        clearable
        rounded
        hide-details
        outlined
          class="search-input"
          style="width: 380px;"
        @input="onSearch"
        @keyup.enter="() => onSearch(true)"
      >
        <template #append-inner>
          <v-icon color="primary">mdi-magnify</v-icon>
        </template>
      </v-text-field>
    </div>
    <v-spacer />

    <div v-if="auth.isAuthenticated" class="d-flex align-center gap-2">
      <v-btn
        icon
        small
        @click="onUpload"
        title="Upload"
      >
        <v-icon>mdi-cloud-upload</v-icon>
      </v-btn>
      <v-btn
        icon
        small
        @click="onCreateFolder"
        title="New folder"
      >
        <v-icon>mdi-folder-plus</v-icon>
      </v-btn>

      <v-divider vertical class="mx-2" />

      <v-btn text @click="goto('files')">Files</v-btn>
      <v-btn text @click="goto('account')">Account</v-btn>
      <v-btn text @click="logout">Logout</v-btn>
    </div>
    <div v-else>
      <v-btn text @click="goto('login')">Login</v-btn>
      <v-btn text @click="goto('register')">Register</v-btn>
    </div>
  </v-app-bar>
</template>

<script>
import { computed, onUnmounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';


export default {
  emits: ['search', 'upload', 'create-folder'],
  setup(_, { emit }) {
    const auth = useAuthStore()
    const router = useRouter()
    const route = useRoute()
    const searchQuery = ref('')
    const isFileArea = computed(() => ['files', 'home', 'folder'].includes(route.name))

    // Debounce поиска: уменьшаем количество событий при быстром вводе
    let searchTimer = null
    const onSearch = (immediate = false) => {
      if (searchTimer) clearTimeout(searchTimer)
      const dispatch = () => {
        emit('search', searchQuery.value)
        window.dispatchEvent(new CustomEvent('brvjeo:search', { detail: searchQuery.value }))
      }
      if (immediate) dispatch()
      else searchTimer = setTimeout(dispatch, 300)
    }

    onUnmounted(() => {
      if (searchTimer) clearTimeout(searchTimer)
    })

    // Генерация глобальных событий для взаимодействия с view (FileList и т.д.)
    const onUpload = () => {
      emit('upload')
      window.dispatchEvent(new CustomEvent('brvjeo:upload'))
    }

    const onCreateFolder = () => {
      emit('create-folder')
      window.dispatchEvent(new CustomEvent('brvjeo:create-folder'))
    }

    return {
      auth,
      searchQuery,
      isFileArea,
      onSearch,
      onUpload,
      onCreateFolder,
      goto: (name) => router.push({ name }),
      logout: () => auth.logout().then(() => router.push({ name: 'login' }))
    }
  }
}
</script>

<style scoped>
.gap-2 {
  gap: 8px;
}
.search-input .v-field__input {
  color: #111 !important;
}
.search-input .v-input__control input::placeholder {
  color: rgba(0,0,0,0.55) !important;
}
.left-search { margin-left: 12px; }
</style>