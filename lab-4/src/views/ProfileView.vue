<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-toolbar color="primary" dark>
            <v-toolbar-title>Профиль пользователя</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-tabs v-model="tab" class="mb-4">
              <v-tab value="profile">Личные данные</v-tab>
              <v-tab value="password">Смена пароля</v-tab>
            </v-tabs>

            <v-window v-model="tab">
              <v-window-item value="profile">
                <v-form @submit.prevent="handleUpdateProfile">
                  <v-text-field
                    v-model="profileForm.username"
                    label="Имя пользователя"
                    prepend-inner-icon="mdi-account"
                    variant="outlined"
                    :error-messages="profileErrors.username"
                    class="mb-4"
                  />
                  <v-text-field
                    v-model="profileForm.email"
                    label="Email"
                    prepend-inner-icon="mdi-email"
                    variant="outlined"
                    type="email"
                    :error-messages="profileErrors.email"
                    class="mb-4"
                  />
                  <v-alert
                    v-if="profileError"
                    type="error"
                    variant="tonal"
                    class="mb-4"
                    closable
                    @click:close="profileError = null"
                  >
                    {{ profileError }}
                  </v-alert>
                  <v-alert
                    v-if="profileSuccess"
                    type="success"
                    variant="tonal"
                    class="mb-4"
                    closable
                    @click:close="profileSuccess = false"
                  >
                    Профиль успешно обновлен
                  </v-alert>
                  <v-btn
                    type="submit"
                    color="primary"
                    :loading="authStore.loading"
                  >
                    Сохранить изменения
                  </v-btn>
                </v-form>
              </v-window-item>

              <v-window-item value="password">
                <v-form @submit.prevent="handleChangePassword">
                  <v-text-field
                    v-model="passwordForm.current_password"
                    label="Текущий пароль"
                    prepend-inner-icon="mdi-lock"
                    type="password"
                    variant="outlined"
                    :error-messages="passwordErrors.current_password"
                    class="mb-4"
                  />
                  <v-text-field
                    v-model="passwordForm.new_password"
                    label="Новый пароль"
                    prepend-inner-icon="mdi-lock-plus"
                    type="password"
                    variant="outlined"
                    :error-messages="passwordErrors.new_password"
                    class="mb-4"
                  />
                  <v-text-field
                    v-model="passwordForm.re_new_password"
                    label="Подтвердите новый пароль"
                    prepend-inner-icon="mdi-lock-check"
                    type="password"
                    variant="outlined"
                    :error-messages="passwordErrors.re_new_password"
                    class="mb-4"
                  />
                  <v-alert
                    v-if="passwordError"
                    type="error"
                    variant="tonal"
                    class="mb-4"
                    closable
                    @click:close="passwordError = null"
                  >
                    {{ passwordError }}
                  </v-alert>
                  <v-alert
                    v-if="passwordSuccess"
                    type="success"
                    variant="tonal"
                    class="mb-4"
                    closable
                    @click:close="passwordSuccess = false"
                  >
                    Пароль успешно изменен
                  </v-alert>
                  <v-btn
                    type="submit"
                    color="primary"
                    :loading="authStore.loading"
                  >
                    Изменить пароль
                  </v-btn>
                </v-form>
              </v-window-item>
            </v-window>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const tab = ref('profile')

const profileForm = reactive({
  username: '',
  email: '',
})

const profileErrors = reactive <{
  username: string[]
  email: string[]
}>({
  username: [],
  email: [],
})

const passwordForm = reactive({
  current_password: '',
  new_password: '',
  re_new_password: '',
})

const passwordErrors = reactive <{
  current_password: string[]
  new_password: string[]
  re_new_password: string[]
}>({
  current_password: [],
  new_password: [],
  re_new_password: [],
})

const profileError = ref<string | null>(null)
const profileSuccess = ref(false)
const passwordError = ref<string | null>(null)
const passwordSuccess = ref(false)

onMounted(() => {
  if (authStore.user) {
    profileForm.username = authStore.user.username || ''
    profileForm.email = authStore.user.email || ''
  }
})

async function handleUpdateProfile() {
  Object.keys(profileErrors).forEach(key => {
    profileErrors[key as keyof typeof profileErrors] = []
  })
  profileError.value = null
  profileSuccess.value = false

  const result = await authStore.updateProfile({
    username: profileForm.username || undefined,
    email: profileForm.email || undefined,
  })

  if (result.success) {
    profileSuccess.value = true
    setTimeout(() => {
      profileSuccess.value = false
    }, 3000)
  } else {
    profileError.value = result.error || 'Ошибка обновления профиля'
  }
}

async function handleChangePassword() {
  Object.keys(passwordErrors).forEach(key => {
    passwordErrors[key as keyof typeof passwordErrors] = []
  })
  passwordError.value = null
  passwordSuccess.value = false

  if (!passwordForm.current_password) {
    passwordErrors.current_password.push('Текущий пароль обязателен')
  }
  if (!passwordForm.new_password) {
    passwordErrors.new_password.push('Новый пароль обязателен')
  }
  if (!passwordForm.re_new_password) {
    passwordErrors.re_new_password.push('Подтверждение пароля обязательно')
  }
  if (passwordForm.new_password && passwordForm.re_new_password &&
      passwordForm.new_password !== passwordForm.re_new_password) {
    passwordErrors.re_new_password.push('Пароли не совпадают')
  }

  if (passwordErrors.current_password.length ||
      passwordErrors.new_password.length ||
      passwordErrors.re_new_password.length) {
    return
  }

  const result = await authStore.changePassword(
    passwordForm.current_password,
    passwordForm.new_password,
    passwordForm.re_new_password
  )

  if (result.success) {
    passwordSuccess.value = true
    passwordForm.current_password = ''
    passwordForm.new_password = ''
    passwordForm.re_new_password = ''
    setTimeout(() => {
      passwordSuccess.value = false
    }, 3000)
  } else {
    passwordError.value = result.error || 'Ошибка смены пароля'
  }
}
</script>

