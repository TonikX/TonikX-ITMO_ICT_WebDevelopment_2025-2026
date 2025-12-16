<template>
  <v-container class="fill-height align-start">
    <v-card class="mx-auto mt-10 w-100" max-width="600" elevation="4" rounded="lg">
      <v-img
        height="150"
        src="https://cdn.vuetifyjs.com/images/cards/server-room.jpg"
        cover
        class="bg-grey-lighten-2"
      >
        <div class="d-flex fill-height align-end pl-4 pb-4 gradient-overlay">
          <v-avatar size="80" color="white" class="elevation-2">
             <span class="text-h4 font-weight-bold text-primary">
               {{ initials }}
             </span>
          </v-avatar>
        </div>
      </v-img>

      <v-card-text class="pt-4">
        <h2 class="text-h5 font-weight-bold mb-1">
          {{ displayName }}
        </h2>
        <div class="text-subtitle-2 text-grey mb-6">Администратор системы</div>

        <v-form @submit.prevent="onSave" v-if="user">
          <v-row dense>
            <v-col cols="12">
              <v-text-field
                v-model="user.username"
                label="Логин"
                disabled
                variant="outlined"
                prepend-inner-icon="mdi-account"
              />
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model="user.email"
                label="Email"
                variant="outlined"
                prepend-inner-icon="mdi-email"
              />
            </v-col>
            <v-col cols="6">
              <v-text-field
                v-model="user.first_name"
                label="Имя"
                variant="outlined"
              />
            </v-col>
            <v-col cols="6">
              <v-text-field
                v-model="user.last_name"
                label="Фамилия"
                variant="outlined"
              />
            </v-col>
          </v-row>

          <v-btn
            :loading="saving"
            type="submit"
            color="primary"
            block
            size="large"
            class="mt-4"
          >
            Сохранить изменения
          </v-btn>
        </v-form>

        <v-snackbar v-model="showSnack" color="success" timeout="3000">
          {{ message }}
          <template v-slot:actions>
            <v-btn variant="text" @click="showSnack = false">OK</v-btn>
          </template>
        </v-snackbar>

        <v-alert v-if="error" type="error" variant="tonal" class="mt-4">{{ error }}</v-alert>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../api/api'

const user = ref(null)
const saving = ref(false)
const message = ref('')
const error = ref('')
const showSnack = ref(false)

const initials = computed(() => {
  if (!user.value) return ''
  const f = user.value.first_name ? user.value.first_name[0] : ''
  const l = user.value.last_name ? user.value.last_name[0] : ''
  if (!f && !l && user.value.username) {
    return user.value.username.slice(0, 2).toUpperCase()
  }
  return (f + l).toUpperCase()
})

const displayName = computed(() => {
  if (!user.value) return '...'
  if (user.value.first_name || user.value.last_name) {
    return `${user.value.last_name} ${user.value.first_name}`.trim()
  }
  return user.value.username
})

onMounted(async () => {
  try {
    const { data } = await api.get('/auth/users/me/')
    user.value = data
  } catch (e) {
    error.value = 'Ошибка загрузки профиля'
  }
})

const onSave = async () => {
  saving.value = true
  message.value = ''
  error.value = ''
  try {
    const { data } = await api.patch('/auth/users/me/', {
      email: user.value.email,
      first_name: user.value.first_name,
      last_name: user.value.last_name
    })

    user.value = data

    message.value = 'Профиль успешно обновлен'
    showSnack.value = true
  } catch (e) {
    error.value = 'Ошибка при сохранении. Проверьте данные.'
    console.error(e)
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.gradient-overlay {
  background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
}
</style>
