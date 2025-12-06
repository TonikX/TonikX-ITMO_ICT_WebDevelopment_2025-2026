<template>
  <v-row justify="center">
    <v-col cols="12" md="8">
      <v-card elevation="2" class="pa-6">
        <v-card-title class="text-h5 font-weight-bold">Новый пост</v-card-title>
        <v-card-subtitle class="mb-4">Расскажите о важном: добавьте заголовок, текст и иллюстрации.</v-card-subtitle>

        <v-alert v-if="error" type="error" variant="tonal" class="mb-4">{{ error }}</v-alert>
        <v-alert v-if="success" type="success" variant="tonal" class="mb-4">{{ success }}</v-alert>

        <v-form @submit.prevent="submit">
          <v-text-field v-model="form.title" label="Заголовок" required></v-text-field>
          <v-textarea v-model="form.text" label="Текст" rows="4" required auto-grow></v-textarea>

          <div class="d-flex align-center justify-space-between mt-2 mb-2">
            <div class="text-subtitle-2">Изображения</div>
            <v-btn color="primary" variant="tonal" @click="pickFiles" prepend-icon="mdi-image-plus">
              Загрузить
            </v-btn>
            <input ref="fileInput" type="file" class="d-none" multiple accept="image/*" @change="handleFiles" />
          </div>
          <v-chip-group column class="mb-4">
            <v-chip v-for="img in uploaded" :key="img.hash" color="primary" variant="tonal">
              {{ img.name }}
            </v-chip>
          </v-chip-group>
          <v-row v-if="uploaded.length" dense>
            <v-col v-for="img in uploaded" :key="img.hash" cols="12" sm="6" md="4">
              <SecureImage :image="img.hash" aspect-ratio="1.6" img-class="rounded-lg border" />
            </v-col>
          </v-row>

          <v-btn :loading="loading" color="primary" type="submit" block class="mt-4">Опубликовать</v-btn>
        </v-form>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { addPost, uploadImage } from '../api/client'
import SecureImage from '../components/SecureImage.vue'

const router = useRouter()
const form = reactive({ title: '', text: '', images: [] })
const uploaded = ref([])
const loading = ref(false)
const error = ref('')
const success = ref('')
const fileInput = ref(null)

const pickFiles = () => fileInput.value?.click()

const handleFiles = async (event) => {
  const files = Array.from(event.target.files)
  if (!files.length) return
  loading.value = true
  error.value = ''
  try {
    for (const file of files) {
      const data = await uploadImage(file)
      form.images.push(data.hash)
      uploaded.value.push({ hash: data.hash, name: file.name })
    }
  } catch (e) {
    error.value = e.response?.data?.detail || 'Не удалось загрузить изображения'
  } finally {
    loading.value = false
    event.target.value = ''
  }
}

const submit = async () => {
  loading.value = true
  error.value = ''
  success.value = ''
  try {
    const post = await addPost(form)
    success.value = 'Пост опубликован'
    router.push({ name: 'post', params: { id: post.id } })
  } catch (e) {
    error.value = e.response?.data?.detail || 'Не удалось создать пост'
  } finally {
    loading.value = false
  }
}
</script>
