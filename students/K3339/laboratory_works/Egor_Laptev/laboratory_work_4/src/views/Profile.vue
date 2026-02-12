<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title class="bg-primary text-white">
            Профиль пользователя
          </v-card-title>
          <v-card-text>
            <v-tabs v-model="tab" class="mb-4">
              <v-tab value="profile">Профиль</v-tab>
              <v-tab value="password">Изменение пароля</v-tab>
            </v-tabs>

            <v-window v-model="tab" class="mt-4">
              <!-- Вкладка профиля -->
              <v-window-item value="profile">
                <v-form ref="profileForm" v-model="profileValid" lazy-validation>
                  <v-text-field
                    v-model="userData.username"
                    label="Имя пользователя"
                    prepend-icon="mdi-account"
                    :rules="usernameRules"
                    required
                    variant="outlined"
                  />
                  <v-text-field
                    v-model="userData.email"
                    label="Email"
                    prepend-icon="mdi-email"
                    type="email"
                    :rules="emailRules"
                    required
                    variant="outlined"
                  />
                  <div v-if="profileError" class="mt-3">
                    <v-alert type="error" dense>{{ profileError }}</v-alert>
                  </div>
                  <div v-if="profileSuccess" class="mt-3">
                    <v-alert type="success" dense>Профиль успешно обновлен!</v-alert>
                  </div>
                  <v-btn
                    color="primary"
                    :disabled="!profileValid || profileLoading"
                    @click="updateProfile"
                    class="mt-4"
                  >
                    Сохранить изменения
                  </v-btn>
                </v-form>
              </v-window-item>

              <!-- Вкладка изменения пароля -->
              <v-window-item value="password">
                <v-form ref="passwordForm" v-model="passwordValid" lazy-validation>
                  <v-text-field
                    v-model="passwordData.currentPassword"
                    label="Текущий пароль"
                    prepend-icon="mdi-lock"
                    type="password"
                    :rules="currentPasswordRules"
                    required
                    variant="outlined"
                  />
                  <v-text-field
                    v-model="passwordData.newPassword"
                    label="Новый пароль"
                    prepend-icon="mdi-lock-plus"
                    type="password"
                    :rules="newPasswordRules"
                    required
                    variant="outlined"
                  />
                  <v-text-field
                    v-model="passwordData.confirmPassword"
                    label="Подтвердите новый пароль"
                    prepend-icon="mdi-lock-check"
                    type="password"
                    :rules="confirmPasswordRules"
                    required
                    variant="outlined"
                  />
                  <div v-if="passwordError" class="mt-3">
                    <v-alert type="error" dense>{{ passwordError }}</v-alert>
                  </div>
                  <div v-if="passwordSuccess" class="mt-3">
                    <v-alert type="success" dense>Пароль успешно изменен!</v-alert>
                  </div>
                  <v-btn
                    color="primary"
                    :disabled="!passwordValid || passwordLoading"
                    @click="changePassword"
                    class="mt-4"
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

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '../services/api'

const router = useRouter()

const tab = ref('profile')
const profileValid = ref(false)
const passwordValid = ref(false)
const profileLoading = ref(false)
const passwordLoading = ref(false)
const profileError = ref('')
const passwordError = ref('')
const profileSuccess = ref(false)
const passwordSuccess = ref(false)

const userData = ref({
  username: '',
  email: '',
})

const passwordData = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
})

const usernameRules = [
  (v) => !!v || 'Имя пользователя обязательно',
  (v) => (v && v.length >= 3) || 'Имя пользователя должно содержать минимум 3 символа',
]

const emailRules = [
  (v) => !!v || 'Email обязателен',
  (v) => /.+@.+\..+/.test(v) || 'Email должен быть валидным',
]

const currentPasswordRules = [
  (v) => !!v || 'Текущий пароль обязателен',
]

const newPasswordRules = [
  (v) => !!v || 'Новый пароль обязателен',
  (v) => (v && v.length >= 8) || 'Пароль должен содержать минимум 8 символов',
]

const confirmPasswordRules = [
  (v) => !!v || 'Подтверждение пароля обязательно',
  (v) => v === passwordData.value.newPassword || 'Пароли не совпадают',
]

const loadUserData = async () => {
  try {
    const response = await authAPI.getCurrentUser()
    userData.value = {
      username: response.data.username,
      email: response.data.email,
    }
  } catch (err) {
    profileError.value = 'Ошибка при загрузке данных пользователя'
  }
}

const updateProfile = async () => {
  profileError.value = ''
  profileSuccess.value = false

  if (!profileValid.value) {
    return
  }

  profileLoading.value = true

  try {
    await authAPI.updateUser({
      username: userData.value.username,
      email: userData.value.email,
    })
    profileSuccess.value = true
    setTimeout(() => {
      profileSuccess.value = false
    }, 3000)
  } catch (err) {
    if (err.response?.data) {
      const data = err.response.data
      if (data.username) {
        profileError.value = `Имя пользователя: ${data.username[0]}`
      } else if (data.email) {
        profileError.value = `Email: ${data.email[0]}`
      } else {
        profileError.value = 'Ошибка при обновлении профиля'
      }
    } else {
      profileError.value = 'Ошибка при обновлении профиля'
    }
  } finally {
    profileLoading.value = false
  }
}

const changePassword = async () => {
  passwordError.value = ''
  passwordSuccess.value = false

  if (!passwordValid.value) {
    return
  }

  if (passwordData.value.newPassword !== passwordData.value.confirmPassword) {
    passwordError.value = 'Пароли не совпадают'
    return
  }

  passwordLoading.value = true

  try {
    await authAPI.changePassword(
      passwordData.value.currentPassword,
      passwordData.value.newPassword
    )
    passwordSuccess.value = true
    passwordData.value = {
      currentPassword: '',
      newPassword: '',
      confirmPassword: '',
    }
    setTimeout(() => {
      passwordSuccess.value = false
    }, 3000)
  } catch (err) {
    if (err.response?.data?.current_password) {
      passwordError.value = err.response.data.current_password[0]
    } else if (err.response?.data?.new_password) {
      passwordError.value = err.response.data.new_password[0]
    } else {
      passwordError.value = 'Ошибка при изменении пароля'
    }
  } finally {
    passwordLoading.value = false
  }
}

onMounted(() => {
  loadUserData()
})
</script>

