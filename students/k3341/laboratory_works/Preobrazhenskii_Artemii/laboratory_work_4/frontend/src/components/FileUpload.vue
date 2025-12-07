<template>
  <v-form @submit.prevent="submit">
    <v-file-input v-model="file" label="Choose file" required></v-file-input>
    <v-btn type="submit" color="primary">Upload</v-btn>
  </v-form>
</template>

<script>
import { ref } from 'vue';
import api from '../utils/api';

export default {
  emits: ['uploaded'],
  setup (_, { emit }) {
    const file = ref(null)
    const submit = async () => {
      if (!file.value) return
      const fd = new FormData()
      fd.append('file', file.value)
      const res = await api.post('/files/', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
      emit('uploaded')
      file.value = null
    }
    return { file, submit }
  }
}
</script>