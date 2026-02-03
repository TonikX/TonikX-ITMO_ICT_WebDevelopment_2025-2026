<template>
  <v-row justify="center" class="mt-4">
    <v-col cols="12" md="8" lg="6">
      <v-card class="pa-6" elevation="4">
        <v-card-title class="d-flex align-center mb-4">
          <v-icon size="32" color="primary" class="mr-2">mdi-account-circle</v-icon>
          Профиль пользователя
        </v-card-title>

        <v-tabs v-model="tab" color="primary">
          <v-tab value="info">Информация</v-tab>
          <v-tab value="password">Смена пароля</v-tab>
        </v-tabs>

        <v-window v-model="tab" class="mt-4">
          <!-- Информация о пользователе -->
          <v-window-item value="info">
            <v-form @submit.prevent="handleUpdateUser" ref="userFormRef">
              <v-text-field
                v-model="userForm.username"
                label="Имя пользователя"
                prepend-inner-icon="mdi-account"
                :rules="[rules.required]"
                class="mb-2"
              ></v-text-field>

              <v-text-field
                v-model="userForm.email"
                label="Email"
                type="email"
                prepend-inner-icon="mdi-email"
                :rules="[rules.required, rules.email]"
                class="mb-2"
              ></v-text-field>

              <v-text-field
                v-model="userForm.first_name"
                label="Имя"
                prepend-inner-icon="mdi-account-outline"
                class="mb-2"
              ></v-text-field>

              <v-text-field
                v-model="userForm.last_name"
                label="Фамилия"
                prepend-inner-icon="mdi-account-outline"
                class="mb-4"
              ></v-text-field>

              <v-btn
                type="submit"
                color="primary"
                :loading="authStore.loading"
              >
                Сохранить изменения
              </v-btn>
            </v-form>
          </v-window-item>

          <!-- Смена пароля -->
          <v-window-item value="password">
            <v-form @submit.prevent="handleChangePassword" ref="passwordFormRef">
              <v-text-field
                v-model="passwordForm.current_password"
                label="Текущий пароль"
                prepend-inner-icon="mdi-lock"
                :type="showCurrentPassword ? 'text' : 'password'"
                :append-inner-icon="showCurrentPassword ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append-inner="showCurrentPassword = !showCurrentPassword"
                :rules="[rules.required]"
                class="mb-2"
              ></v-text-field>

              <v-text-field
                v-model="passwordForm.new_password"
                label="Новый пароль"
                prepend-inner-icon="mdi-lock-plus"
                :type="showNewPassword ? 'text' : 'password'"
                :append-inner-icon="showNewPassword ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append-inner="showNewPassword = !showNewPassword"
                :rules="[rules.required, rules.minLength(8)]"
                class="mb-2"
              ></v-text-field>

              <v-text-field
                v-model="passwordForm.re_new_password"
                label="Подтверждение нового пароля"
                prepend-inner-icon="mdi-lock-check"
                :type="showNewPassword ? 'text' : 'password'"
                :rules="[rules.required, rules.passwordMatch]"
                class="mb-4"
              ></v-text-field>

              <v-btn
                type="submit"
                color="primary"
                :loading="authStore.loading"
              >
                Сменить пароль
              </v-btn>
            </v-form>
          </v-window-item>
        </v-window>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { ref, reactive, inject, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const showSnackbar = inject('showSnackbar')

const tab = ref('info')
const userFormRef = ref(null)
const passwordFormRef = ref(null)
const showCurrentPassword = ref(false)
const showNewPassword = ref(false)

const userForm = reactive({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
})

const passwordForm = reactive({
  current_password: '',
  new_password: '',
  re_new_password: '',
})

const rules = {
  required: (v) => !!v || 'Обязательное поле',
  minLength: (min) => (v) => (v && v.length >= min) || `Минимум ${min} символов`,
  email: (v) => /.+@.+\..+/.test(v) || 'Некорректный email',
  passwordMatch: (v) => v === passwordForm.new_password || 'Пароли не совпадают',
}

onMounted(() => {
  if (authStore.user) {
    userForm.username = authStore.user.username || ''
    userForm.email = authStore.user.email || ''
    userForm.first_name = authStore.user.first_name || ''
    userForm.last_name = authStore.user.last_name || ''
  }
})

const handleUpdateUser = async () => {
  const { valid } = await userFormRef.value.validate()
  if (!valid) return

  const success = await authStore.updateUser(userForm)
  if (success) {
    showSnackbar('Данные обновлены', 'success')
  } else {
    showSnackbar('Ошибка обновления данных', 'error')
  }
}

const handleChangePassword = async () => {
  const { valid } = await passwordFormRef.value.validate()
  if (!valid) return

  const success = await authStore.changePassword(passwordForm)
  if (success) {
    showSnackbar('Пароль изменен', 'success')
    passwordForm.current_password = ''
    passwordForm.new_password = ''
    passwordForm.re_new_password = ''
    passwordFormRef.value.resetValidation()
  } else {
    showSnackbar('Ошибка смены пароля', 'error')
  }
}
</script>
