<template>
  <v-dialog v-model="show" persistent max-width="600px">
    <v-card>
      <v-card-title>Upload Files</v-card-title>
      <v-card-text>
        <v-container>
          <v-row
            @dragover.prevent="dragOver = true"
            @dragleave="dragOver = false"
            @drop.prevent="handleDrop"
            :class="{ 'drag-over': dragOver }"
            class="drop-zone pa-6 mb-4 border-2 rounded-lg text-center"
          >
            <v-col cols="12">
              <v-icon size="64" color="primary">mdi-cloud-upload-outline</v-icon>
              <p class="text-h6 mt-2">Drag files here or click below</p>
              <v-file-input
                v-model="uploadFiles"
                multiple
                label="Select files"
                show-size
              />
            </v-col>
          </v-row>

          <v-row v-if="uploadQueue.length">
            <v-col cols="12">
              <v-list dense>
                <v-list-item v-for="(item, idx) in uploadQueue" :key="idx">
                  <v-list-item-content>
                    <v-list-item-title>{{ item.file.name }}</v-list-item-title>
                    <v-progress-linear
                      :value="item.progress"
                      :color="item.status === 'success' ? 'green' : item.status === 'error' ? 'red' : 'primary'"
                      class="mt-2"
                    />
                    <v-list-item-subtitle>{{ item.progress }}%</v-list-item-subtitle>
                  </v-list-item-content>
                  <v-list-item-action v-if="item.status === 'error'">
                    <v-icon color="red">mdi-alert-circle</v-icon>
                  </v-list-item-action>
                  <v-list-item-action v-else-if="item.status === 'success'">
                    <v-icon color="green">mdi-check-circle</v-icon>
                  </v-list-item-action>
                </v-list-item>
              </v-list>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn text @click="show = false">Cancel</v-btn>
        <v-btn color="primary" @click="uploadAll" :disabled="!uploadFiles.length || uploading">
          <v-icon left>mdi-upload</v-icon>Upload
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { ref, watch } from 'vue';
import api from '../utils/api';

export default {
  props: {
    modelValue: { type: Boolean, default: false },
    currentFolderId: { type: [Number, String], default: null }
  },
  emits: ['update:modelValue', 'uploaded'],
  setup(props, { emit }) {
    const show = ref(props.modelValue);
    const uploadFiles = ref([]);
    const uploadQueue = ref([]);
    const uploading = ref(false);
    const dragOver = ref(false);
    // Комментарии:
    // show - локальная реактивная переменная для контроля диалога (v-model)
    // uploadFiles - выбранные файлы для загрузки
    // uploadQueue - очередь загрузки с прогрессом и статусом
    // uploading - индикатор активной загрузки
    // dragOver - состояние drag&drop области

    watch(show, val => emit('update:modelValue', val));
    watch(() => props.modelValue, val => show.value = val);

    const handleDrop = (e) => {
      dragOver.value = false;
      uploadFiles.value = Array.from(e.dataTransfer.files);
    };

    const uploadAll = async () => {
  if (!uploadFiles.value.length) return;
  console.log('uploadAll: currentFolderId =', props.currentFolderId, 'type:', typeof props.currentFolderId);
  uploading.value = true;
  uploadQueue.value = uploadFiles.value.map(f => ({ file: f, progress: 0, status: 'pending' }));

  for (let item of uploadQueue.value) {
    try {
      const fd = new FormData();
      fd.append('file', item.file);
      if (props.currentFolderId) {
        fd.append('folder', props.currentFolderId);
        console.log('Added folder to FormData:', props.currentFolderId);
      }

      // 👇 ВАЖНО: берём токен прямо из localStorage
      const token = localStorage.getItem('token')
      
      // 👇 Используем fetch вместо api, чтобы точно передать токен
      const response = await fetch('/api/files/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`  // ← токен ПРЯМО ЗДЕСЬ
        },
        body: fd
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      item.status = 'success';
      item.progress = 100;
    } catch (err) {
      item.status = 'error';
      console.error('Upload failed:', item.file.name, err);
    }
  }

  uploading.value = false;
  emit('uploaded');

  const allSuccess = uploadQueue.value.every(i => i.status === 'success');
  if (allSuccess) {
    setTimeout(() => {
      show.value = false;
      uploadFiles.value = [];
      uploadQueue.value = [];
    }, 1500);
  }
};

    return { show, uploadFiles, uploadQueue, uploading, dragOver, handleDrop, uploadAll };
  }
};
</script>

<style scoped>
.drop-zone {
  border: 2px dashed #ccc;
  border-radius: 8px;
  transition: all 0.3s;
}
.drop-zone.drag-over {
  border-color: #1976d2;
  background-color: rgba(25, 118, 210, 0.1);
}
</style>