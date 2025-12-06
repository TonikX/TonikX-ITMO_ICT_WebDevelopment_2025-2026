<template>
  <v-row justify="center">
    <v-col cols="12" md="8" lg="6">
      <v-card>
        <v-card-title class="text-h4 mb-4">
          Профиль
        </v-card-title>

        <v-card-text v-if="loading">
          <v-progress-circular
            indeterminate
            color="primary"
            class="d-block mx-auto"
          ></v-progress-circular>
        </v-card-text>

        <v-card-text v-else>
          <v-row>
            <v-col cols="12" class="text-center">
              <v-avatar size="120" class="mb-4">
                <v-img
                  v-if="profile?.avatar"
                  :src="getAvatarUrl(profile.avatar)"
                  cover
                ></v-img>
                <v-icon
                  v-else
                  size="64"
                  color="primary"
                >
                  mdi-account-circle
                </v-icon>
              </v-avatar>
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                v-model="displayName"
                label="Отображаемое имя"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                readonly
              ></v-text-field>
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                :model-value="user?.username || 'Не указано'"
                label="Имя пользователя"
                prepend-inner-icon="mdi-at"
                variant="outlined"
                readonly
              ></v-text-field>
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                :model-value="user?.email || 'Не указано'"
                label="Email"
                prepend-inner-icon="mdi-email"
                variant="outlined"
                readonly
              ></v-text-field>
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                :model-value="formatDate(profile?.created_at)"
                label="Дата регистрации"
                prepend-inner-icon="mdi-calendar"
                variant="outlined"
                readonly
              ></v-text-field>
            </v-col>

            <v-col cols="12">
              <v-textarea
                v-model="bio"
                label="О себе"
                prepend-inner-icon="mdi-text"
                variant="outlined"
                rows="4"
                readonly
              ></v-textarea>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <v-row>
            <v-col cols="12">
              <v-btn
                color="primary"
                prepend-icon="mdi-pencil"
                @click="editMode = true"
              >
                Редактировать профиль
              </v-btn>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Диалог редактирования -->
      <v-dialog v-model="editMode" max-width="600" persistent>
        <v-card>
          <v-card-title>
            Редактирование профиля
          </v-card-title>

          <v-card-text>
            <v-form ref="editFormRef" v-model="editValid">
              <v-text-field
                v-model="editDisplayName"
                label="Отображаемое имя"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                class="mb-2"
              ></v-text-field>

              <v-textarea
                v-model="editBio"
                label="О себе"
                prepend-inner-icon="mdi-text"
                variant="outlined"
                rows="4"
                class="mb-2"
              ></v-textarea>

              <v-file-input
                v-model="avatarFile"
                label="Аватар"
                prepend-inner-icon="mdi-image"
                accept="image/*"
                variant="outlined"
                show-size
                @update:model-value="handleAvatarSelect"
              ></v-file-input>

              <v-img
                v-if="avatarPreview"
                :src="avatarPreview"
                max-height="200"
                class="mt-2"
                cover
              ></v-img>
            </v-form>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              variant="text"
              @click="cancelEdit"
            >
              Отмена
            </v-btn>
            <v-btn
              color="primary"
              :loading="saving"
              :disabled="!editValid || saving"
              @click="saveProfile"
            >
              Сохранить
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-col>
  </v-row>
</template>

<script setup>
import { ref, computed, onMounted, inject } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import * as profileAPI from '@/api/profile'

const authStore = useAuthStore()
const showSnackbar = inject('showSnackbar')

const loading = ref(true)
const saving = ref(false)
const editMode = ref(false)
const editFormRef = ref(null)
const editValid = ref(false)

const user = computed(() => authStore.user)
const profile = computed(() => authStore.profile)

const displayName = ref('')
const bio = ref('')
const editDisplayName = ref('')
const editBio = ref('')
const avatarFile = ref(null)
const avatarPreview = ref(null)

// Функция для получения полного URL аватара
const getAvatarUrl = (avatarPath) => {
  if (!avatarPath) return null
  // Если уже полный URL (начинается с http:// или https://)
  if (avatarPath.startsWith('http://') || avatarPath.startsWith('https://')) {
    return avatarPath
  }
  // Если относительный URL, добавляем базовый URL бэкенда
  const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
  // Убираем начальный слеш если есть, чтобы избежать двойного слеша
  const cleanPath = avatarPath.startsWith('/') ? avatarPath : `/${avatarPath}`
  return `${baseURL}${cleanPath}`
}

const loadProfile = async () => {
  loading.value = true
  try {
    await authStore.loadProfile()
    const profileData = authStore.profile || {}
    displayName.value = profileData.display_name || authStore.displayName
    bio.value = profileData.bio || ''
    editDisplayName.value = profileData.display_name || ''
    editBio.value = profileData.bio || ''

    if (profileData.avatar) {
      avatarPreview.value = getAvatarUrl(profileData.avatar)
    }
  } catch (error) {
    showSnackbar('Ошибка загрузки профиля', 'error')
  } finally {
    loading.value = false
  }
}

const handleAvatarSelect = (file) => {
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      avatarPreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  } else {
    avatarPreview.value = profile.value?.avatar ? getAvatarUrl(profile.value.avatar) : null
  }
}

const cancelEdit = () => {
  editMode.value = false
  editDisplayName.value = profile.value?.display_name || ''
  editBio.value = profile.value?.bio || ''
  avatarFile.value = null
  avatarPreview.value = profile.value?.avatar ? getAvatarUrl(profile.value.avatar) : null
}

const saveProfile = async () => {
  const { valid: isValid } = await editFormRef.value.validate()
  if (!isValid) return

  saving.value = true
  try {
    const formData = new FormData()
    formData.append('display_name', editDisplayName.value)
    formData.append('bio', editBio.value)
    if (avatarFile.value) {
      formData.append('avatar', avatarFile.value)
    }

    const updatedProfile = await profileAPI.updateProfile(formData)
    await authStore.loadProfile()

    displayName.value = updatedProfile.display_name || authStore.displayName
    bio.value = updatedProfile.bio || ''

    editMode.value = false
    showSnackbar('Профиль успешно обновлен', 'success')
  } catch (error) {
    const message = error.response?.data?.detail ||
                   Object.values(error.response?.data || {})[0]?.[0] ||
                   'Ошибка обновления профиля'
    showSnackbar(message, 'error')
  } finally {
    saving.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'Не указано'
  return new Date(dateString).toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

onMounted(() => {
  loadProfile()
})
</script>
