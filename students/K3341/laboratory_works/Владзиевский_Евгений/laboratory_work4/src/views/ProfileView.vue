<template>
  <v-row justify="center">
    <v-col cols="12" md="8">
      <v-card elevation="2" class="pa-6">
        <v-card-title class="text-h5 font-weight-bold">Профиль</v-card-title>
        <v-card-subtitle class="mb-4">Измените имя, описание и аватар.</v-card-subtitle>

        <v-alert v-if="error" type="error" variant="tonal" class="mb-4">{{ error }}</v-alert>
        <v-alert v-if="success" type="success" variant="tonal" class="mb-4">{{ success }}</v-alert>

        <div class="d-flex align-center mb-4">
          <v-avatar size="80" class="mr-4" color="primary" variant="tonal">
            <v-img v-if="avatar" :src="avatar"></v-img>
            <span v-else class="text-h5">{{ initials }}</span>
          </v-avatar>
          <div>
            <div class="text-body-2 text-medium-emphasis">ID: {{ user?.id }}</div>
            <v-btn color="primary" variant="tonal" @click="pickAvatar" prepend-icon="mdi-camera">
              Загрузить фото
            </v-btn>
            <input ref="fileInput" type="file" class="d-none" accept="image/*" @change="handleAvatar" />
          </div>
        </div>

        <v-form @submit.prevent="submit">
          <v-text-field v-model="form.name" label="Имя" required></v-text-field>
          <v-textarea v-model="form.about" label="О себе" rows="3" auto-grow></v-textarea>
          <v-btn :loading="loading" color="primary" type="submit" block class="mt-4">Сохранить</v-btn>
        </v-form>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { useAuthState, saveProfile } from '../stores/auth'
import { uploadImage } from '../api/client'
import { resolveImageSrc } from '../utils/images'

const state = useAuthState()
const user = computed(() => state.user)
const form = reactive({ name: state.user?.name || '', about: state.user?.about || '', img_hash: null })
const avatar = ref(null)
const fileInput = ref(null)
const loading = ref(false)
const error = ref('')
const success = ref('')

const initials = computed(() => (user.value?.name ? user.value.name[0] : '?'))

watch(
  () => state.user,
  async (val) => {
    form.name = val?.name || ''
    form.about = val?.about || ''
    avatar.value = val?.images?.[0] ? await resolveImageSrc(val.images[0]) : null
  },
  { immediate: true },
)

const pickAvatar = () => fileInput.value?.click()

const handleAvatar = async (event) => {
  const file = event.target.files?.[0]
  if (!file) return
  loading.value = true
  error.value = ''
  try {
    const data = await uploadImage(file)
    form.img_hash = data.hash
    avatar.value = await resolveImageSrc({ hash: data.hash })
  } catch (e) {
    error.value = e.response?.data?.detail || 'Не удалось загрузить изображение'
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
    await saveProfile(form)
    success.value = 'Профиль обновлен'
  } catch (e) {
    error.value = e.response?.data?.detail || 'Не удалось сохранить профиль'
  } finally {
    loading.value = false
  }
}
</script>
