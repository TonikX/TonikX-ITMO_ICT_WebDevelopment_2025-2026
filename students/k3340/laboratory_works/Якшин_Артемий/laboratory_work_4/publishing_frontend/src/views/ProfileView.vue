<template>
  <div class="profile-view">
    <v-row>
      <v-col cols="12">
        <h1 class="page-title mb-6">
          <v-icon class="mr-2">mdi-account-cog</v-icon>
          Настройки профиля
        </h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="6">
        <v-card class="mb-6">
          <v-card-title class="d-flex align-center">
            <v-icon class="mr-2">mdi-account-circle</v-icon>
            Информация профиля
          </v-card-title>
          <v-card-text>
            <v-form ref="profileForm" v-model="profileValid" @submit.prevent="updateProfile">
              <v-text-field
                v-model="profileData.username"
                label="Имя пользователя"
                prepend-inner-icon="mdi-account"
                :rules="[rules.required]"
                :disabled="profileLoading"
                class="mb-4"
              ></v-text-field>

              <v-text-field
                v-model="profileData.email"
                label="Email"
                type="email"
                prepend-inner-icon="mdi-email"
                :rules="[rules.required, rules.email]"
                :disabled="profileLoading"
                class="mb-4"
              ></v-text-field>

              <v-text-field
                v-model="profileData.first_name"
                label="Имя"
                prepend-inner-icon="mdi-badge-account-horizontal"
                :disabled="profileLoading"
                class="mb-4"
              ></v-text-field>

              <v-text-field
                v-model="profileData.last_name"
                label="Фамилия"
                prepend-inner-icon="mdi-badge-account"
                :disabled="profileLoading"
                class="mb-4"
              ></v-text-field>

              <v-btn
                type="submit"
                color="primary"
                :loading="profileLoading"
                :disabled="!profileValid"
              >
                <v-icon left>mdi-content-save</v-icon>
                Сохранить
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="d-flex align-center">
            <v-icon class="mr-2">mdi-lock-reset</v-icon>
            Смена пароля
          </v-card-title>
          <v-card-text>
            <v-form ref="passwordForm" v-model="passwordValid" @submit.prevent="changePassword">
              <v-text-field
                v-model="passwordData.current_password"
                label="Текущий пароль"
                prepend-inner-icon="mdi-lock"
                :append-inner-icon="showCurrentPassword ? 'mdi-eye-off' : 'mdi-eye'"
                :type="showCurrentPassword ? 'text' : 'password'"
                :rules="[rules.required]"
                :disabled="passwordLoading"
                @click:append-inner="showCurrentPassword = !showCurrentPassword"
                class="mb-4"
              ></v-text-field>

              <v-text-field
                v-model="passwordData.new_password"
                label="Новый пароль"
                prepend-inner-icon="mdi-lock-plus"
                :append-inner-icon="showNewPassword ? 'mdi-eye-off' : 'mdi-eye'"
                :type="showNewPassword ? 'text' : 'password'"
                :rules="[rules.required, rules.minLength]"
                :disabled="passwordLoading"
                @click:append-inner="showNewPassword = !showNewPassword"
                hint="Минимум 8 символов"
                class="mb-4"
              ></v-text-field>

              <v-text-field
                v-model="passwordData.re_new_password"
                label="Подтвердите новый пароль"
                prepend-inner-icon="mdi-lock-check"
                :append-inner-icon="showConfirmPassword ? 'mdi-eye-off' : 'mdi-eye'"
                :type="showConfirmPassword ? 'text' : 'password'"
                :rules="[rules.required, rules.passwordMatch]"
                :disabled="passwordLoading"
                @click:append-inner="showConfirmPassword = !showConfirmPassword"
                class="mb-4"
              ></v-text-field>

              <v-btn
                type="submit"
                color="warning"
                :loading="passwordLoading"
                :disabled="!passwordValid"
              >
                <v-icon left>mdi-lock-reset</v-icon>
                Сменить пароль
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, inject } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const showSnackbar = inject('showSnackbar')

const profileForm = ref(null)
const passwordForm = ref(null)
const profileValid = ref(false)
const passwordValid = ref(false)
const profileLoading = ref(false)
const passwordLoading = ref(false)

const showCurrentPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

const profileData = reactive({
  username: '',
  email: '',
  first_name: '',
  last_name: ''
})

const passwordData = reactive({
  current_password: '',
  new_password: '',
  re_new_password: ''
})

const rules = {
  required: (v) => !!v || 'Обязательное поле',
  email: (v) => /.+@.+\..+/.test(v) || 'Введите корректный email',
  minLength: (v) => v.length >= 8 || 'Минимум 8 символов',
  passwordMatch: (v) => v === passwordData.new_password || 'Пароли не совпадают'
}

onMounted(() => {
  if (authStore.user) {
    profileData.username = authStore.user.username || ''
    profileData.email = authStore.user.email || ''
    profileData.first_name = authStore.user.first_name || ''
    profileData.last_name = authStore.user.last_name || ''
  }
})

const updateProfile = async () => {
  const { valid } = await profileForm.value.validate()
  if (!valid) return

  profileLoading.value = true
  const result = await authStore.updateProfile(profileData)
  profileLoading.value = false

  if (result.success) {
    showSnackbar('Профиль успешно обновлён', 'success')
  } else {
    showSnackbar(result.error, 'error')
  }
}

const changePassword = async () => {
  const { valid } = await passwordForm.value.validate()
  if (!valid) return

  passwordLoading.value = true
  const result = await authStore.changePassword(passwordData)
  passwordLoading.value = false

  if (result.success) {
    showSnackbar('Пароль успешно изменён', 'success')
    passwordData.current_password = ''
    passwordData.new_password = ''
    passwordData.re_new_password = ''
    passwordForm.value.reset()
  } else {
    showSnackbar(result.error, 'error')
  }
}
</script>

<style scoped>
.profile-view {
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2rem;
  font-weight: 600;
  color: rgb(var(--v-theme-on-background));
}
</style>

