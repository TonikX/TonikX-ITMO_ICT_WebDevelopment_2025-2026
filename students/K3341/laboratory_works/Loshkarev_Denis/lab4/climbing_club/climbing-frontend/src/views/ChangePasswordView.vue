<template>
  <div class="page--center">
    <v-card class="panel-card" rounded="xl" elevation="8">
      <v-card-title class="py-3">
        <div class="text-h5 font-weight-medium">Смена пароля</div>
        <div class="panel-subtitle">Учетные данные</div>
      </v-card-title>

      <v-card-text class="pt-2">
        <v-alert v-if="error" type="error" variant="tonal" class="mb-4" :text="error" />
        <v-alert v-if="ok" type="success" variant="tonal" class="mb-4" :text="ok" />

        <v-form @submit.prevent="submit">
          <v-text-field
            v-model="current_password"
            label="Текущий пароль"
            :type="showCurrent ? 'text' : 'password'"
            variant="outlined"
            density="comfortable"
            :append-inner-icon="showCurrent ? 'mdi-eye-off' : 'mdi-eye'"
            @click:append-inner="showCurrent = !showCurrent"
            :disabled="loading"
            class="mb-3"
          />

          <v-text-field
            v-model="new_password"
            label="Новый пароль"
            :type="showNew ? 'text' : 'password'"
            variant="outlined"
            density="comfortable"
            :append-inner-icon="showNew ? 'mdi-eye-off' : 'mdi-eye'"
            @click:append-inner="showNew = !showNew"
            :disabled="loading"
            class="mb-3"
          />

          <v-text-field
            v-model="re_new_password"
            label="Повторите новый пароль"
            :type="showReNew ? 'text' : 'password'"
            variant="outlined"
            density="comfortable"
            :append-inner-icon="showReNew ? 'mdi-eye-off' : 'mdi-eye'"
            @click:append-inner="showReNew = !showReNew"
            :disabled="loading"
          />

          <v-btn
            type="submit"
            block
            color="black"
            class="mt-5 text-none"
            size="large"
            :loading="loading"
            :disabled="!canSubmit"
          >
            Сменить пароль
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import api from '../api'

const loading = ref(false)
const error = ref('')
const ok = ref('')

const current_password = ref('')
const new_password = ref('')
const re_new_password = ref('')

const showCurrent = ref(false)
const showNew = ref(false)
const showReNew = ref(false)

const canSubmit = computed(() =>
  current_password.value &&
  new_password.value &&
  re_new_password.value &&
  new_password.value === re_new_password.value
)

function formatErr(e) {
  const d = e?.response?.data
  if (!d) return 'Ошибка запроса'
  if (typeof d === 'string') return d
  if (typeof d === 'object') {
    return Object.entries(d)
      .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : String(v)}`)
      .join(' | ')
  }
  return 'Ошибка'
}

async function submit() {
  error.value = ''
  ok.value = ''
  loading.value = true
  try {
    await api.post('auth/users/set_password/', {
      current_password: current_password.value,
      new_password: new_password.value,
      re_new_password: re_new_password.value,
    })
    ok.value = 'Пароль успешно изменён'
    current_password.value = ''
    new_password.value = ''
    re_new_password.value = ''
  } catch (e) {
    error.value = formatErr(e)
  } finally {
    loading.value = false
  }
}
</script>