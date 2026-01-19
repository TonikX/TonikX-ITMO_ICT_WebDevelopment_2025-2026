<template>
  <v-card>
    <v-card-title class="text-h6">Профиль</v-card-title>

    <v-card-text>
      <v-alert v-if="error" type="error" variant="tonal" class="mb-4">
        {{ error }}
      </v-alert>

      <v-alert v-if="success" type="success" variant="tonal" class="mb-4">
        Сохранено
      </v-alert>

      <div v-if="!auth.user" class="text-medium-emphasis">Нет данных пользователя.</div>

      <div v-else class="d-flex flex-wrap" style="gap: 12px">
        <v-text-field
          :model-value="auth.user.username"
          label="Логин"
          variant="outlined"
          density="compact"
          disabled
          style="flex:1 0 260px"
        />

        <v-text-field
          v-model="form.email"
          label="Email"
          variant="outlined"
          density="compact"
          :disabled="!editing"
          :rules="[emailRule]"
          style="flex:1 0 260px"
        />

        <v-text-field
          v-model="form.first_name"
          label="Имя"
          variant="outlined"
          density="compact"
          :disabled="!editing"
          style="flex:1 0 260px"
        />

        <v-text-field
          v-model="form.last_name"
          label="Фамилия"
          variant="outlined"
          density="compact"
          :disabled="!editing"
          style="flex:1 0 260px"
        />

        <template v-if="canSeeAdminFlags">
          <v-text-field
            :model-value="String(auth.user.is_staff)"
            label="staff"
            variant="outlined"
            density="compact"
            disabled
            style="flex:1 0 260px"
          />
          <v-text-field
            :model-value="String(auth.user.is_superuser)"
            label="superuser"
            variant="outlined"
            density="compact"
            disabled
            style="flex:1 0 260px"
          />
        </template>
      </div>

      <div class="mt-4 d-flex" style="gap: 12px">
        <v-btn v-if="!editing" variant="tonal" @click="startEdit">Редактировать</v-btn>

        <template v-else>
          <v-btn color="primary" :loading="saving" @click="save">Сохранить</v-btn>
          <v-btn variant="text" @click="cancel">Отмена</v-btn>
        </template>

        <v-spacer />

        <v-btn variant="tonal" @click="refresh" :loading="refreshing">Обновить</v-btn>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { computed, reactive, ref, watch, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'

const auth = useAuthStore()
auth.hydrate()

const error = ref('')
const success = ref(false)

const editing = ref(false)
const saving = ref(false)
const refreshing = ref(false)

const form = reactive({
  email: '',
  first_name: '',
  last_name: '',
})

const canSeeAdminFlags = computed(() => !!(auth.user?.is_staff || auth.user?.is_superuser))

function fillFormFromUser() {
  form.email = auth.user?.email || ''
  form.first_name = auth.user?.first_name || ''
  form.last_name = auth.user?.last_name || ''
}

onMounted(async () => {
  if (!auth.user && auth.token) {
    try { await auth.fetchCurrentUser() } catch {}
  }
})

// когда пользователь в store обновился — синхронизируем форму (если НЕ редактируем)
watch(
  () => auth.user,
  () => {
    if (!editing.value) fillFormFromUser()
  },
  { immediate: true }
)

const emailRule = (v) => {
  if (!v) return true // email можно оставить пустым
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || 'Некорректный email'
}

function startEdit() {
  success.value = false
  error.value = ''
  fillFormFromUser()
  editing.value = true
}

function cancel() {
  error.value = ''
  success.value = false
  editing.value = false
  fillFormFromUser()
}

async function refresh() {
  refreshing.value = true
  error.value = ''
  success.value = false
  try {
    await auth.fetchCurrentUser()
  } catch {
    error.value = 'Не удалось обновить профиль'
  } finally {
    refreshing.value = false
  }
}

async function save() {
  saving.value = true
  error.value = ''
  success.value = false

  try {
    // отправляем только изменяемые поля
    await auth.updateProfile({
      email: form.email,
      first_name: form.first_name,
      last_name: form.last_name,
    })
    success.value = true
    editing.value = false
  } catch (e) {
    const data = e?.response?.data
    if (data && typeof data === 'object') {
      const parts = []
      for (const [k, v] of Object.entries(data)) {
        parts.push(`${k}: ${Array.isArray(v) ? v.join(', ') : String(v)}`)
      }
      error.value = parts.join(' | ')
    } else {
      error.value = 'Не удалось сохранить профиль'
    }
  } finally {
    saving.value = false
  }
}
</script>
