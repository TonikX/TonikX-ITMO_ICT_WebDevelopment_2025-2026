<template>
  <v-row justify="center">
    <v-col cols="12" md="8" lg="6">
      <v-card>
        <v-card-title class="text-h4 mb-4">
          Настройки
        </v-card-title>

        <v-card-text>
          <v-tabs v-model="tab" color="primary">
            <v-tab value="account">Аккаунт</v-tab>
            <v-tab value="password">Пароль</v-tab>
          </v-tabs>

          <v-window v-model="tab">
            <!-- Настройки аккаунта -->
            <v-window-item value="account">
              <v-card-text>
                <v-form ref="accountFormRef" v-model="accountValid">
                  <v-text-field
                    v-model="email"
                    label="Email"
                    type="email"
                    prepend-inner-icon="mdi-email"
                    :rules="emailRules"
                    variant="outlined"
                    class="mb-2"
                  ></v-text-field>

                  <v-text-field
                    v-model="username"
                    label="Имя пользователя"
                    prepend-inner-icon="mdi-at"
                    :rules="usernameRules"
                    variant="outlined"
                    class="mb-4"
                  ></v-text-field>

                  <v-btn
                    color="primary"
                    :loading="savingAccount"
                    :disabled="!accountValid || savingAccount"
                    @click="saveAccount"
                  >
                    Сохранить изменения
                  </v-btn>
                </v-form>
              </v-card-text>
            </v-window-item>

            <!-- Изменение пароля -->
            <v-window-item value="password">
              <v-card-text>
                <v-form ref="passwordFormRef" v-model="passwordValid">
                  <v-text-field
                    v-model="currentPassword"
                    label="Текущий пароль"
                    type="password"
                    prepend-inner-icon="mdi-lock"
                    :rules="currentPasswordRules"
                    variant="outlined"
                    class="mb-2"
                  ></v-text-field>

                  <v-text-field
                    v-model="newPassword"
                    label="Новый пароль"
                    type="password"
                    prepend-inner-icon="mdi-lock-plus"
                    :rules="newPasswordRules"
                    variant="outlined"
                    class="mb-2"
                  ></v-text-field>

                  <v-text-field
                    v-model="reNewPassword"
                    label="Подтверждение нового пароля"
                    type="password"
                    prepend-inner-icon="mdi-lock-check"
                    :rules="reNewPasswordRules"
                    variant="outlined"
                    class="mb-4"
                  ></v-text-field>

                  <v-btn
                    color="primary"
                    :loading="changingPassword"
                    :disabled="!passwordValid || changingPassword"
                    @click="changePassword"
                  >
                    Изменить пароль
                  </v-btn>
                </v-form>
              </v-card-text>
            </v-window-item>
          </v-window>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { ref, computed, onMounted, inject } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import * as authAPI from '@/api/auth'

const authStore = useAuthStore()
const showSnackbar = inject('showSnackbar')

const tab = ref('account')
const accountFormRef = ref(null)
const passwordFormRef = ref(null)
const accountValid = ref(false)
const passwordValid = ref(false)

const savingAccount = ref(false)
const changingPassword = ref(false)

const user = computed(() => authStore.user)

const email = ref('')
const username = ref('')
const currentPassword = ref('')
const newPassword = ref('')
const reNewPassword = ref('')

const emailRules = [
  (v) => !!v || 'Email обязателен',
  (v) => /.+@.+\..+/.test(v) || 'Email должен быть валидным',
]

const usernameRules = [
  (v) => !!v || 'Имя пользователя обязательно',
  (v) => (v && v.length >= 3) || 'Имя пользователя должно содержать минимум 3 символа',
]

const currentPasswordRules = [
  (v) => !!v || 'Текущий пароль обязателен',
]

const newPasswordRules = [
  (v) => !!v || 'Новый пароль обязателен',
  (v) => (v && v.length >= 8) || 'Пароль должен содержать минимум 8 символов',
]

const reNewPasswordRules = [
  (v) => !!v || 'Подтверждение пароля обязательно',
  (v) => v === newPassword.value || 'Пароли не совпадают',
]

const saveAccount = async () => {
  const { valid: isValid } = await accountFormRef.value.validate()
  if (!isValid) return

  savingAccount.value = true
  try {
    const userData = {}
    if (email.value !== user.value?.email) {
      userData.email = email.value
    }
    if (username.value !== user.value?.username) {
      userData.username = username.value
    }

    if (Object.keys(userData).length === 0) {
      showSnackbar('Нет изменений для сохранения', 'info')
      return
    }

    const result = await authStore.updateUser(userData)
    if (result.success) {
      showSnackbar('Данные аккаунта успешно обновлены', 'success')
    } else {
      showSnackbar(result.error || 'Ошибка обновления данных', 'error')
    }
  } catch (error) {
    const message = error.response?.data?.detail ||
                   Object.values(error.response?.data || {})[0]?.[0] ||
                   'Ошибка обновления данных'
    showSnackbar(message, 'error')
  } finally {
    savingAccount.value = false
  }
}

const changePassword = async () => {
  const { valid: isValid } = await passwordFormRef.value.validate()
  if (!isValid) return

  changingPassword.value = true
  try {
    await authAPI.changePassword(
      currentPassword.value,
      newPassword.value,
      reNewPassword.value
    )
    showSnackbar('Пароль успешно изменен', 'success')

    // Очищаем поля формы
    currentPassword.value = ''
    newPassword.value = ''
    reNewPassword.value = ''
    passwordFormRef.value.resetValidation()
  } catch (error) {
    const message = error.response?.data?.detail ||
                   error.response?.data?.current_password?.[0] ||
                   error.response?.data?.new_password?.[0] ||
                   error.response?.data?.non_field_errors?.[0] ||
                   'Ошибка изменения пароля'
    showSnackbar(message, 'error')
  } finally {
    changingPassword.value = false
  }
}

onMounted(() => {
  if (user.value) {
    email.value = user.value.email || ''
    username.value = user.value.username || ''
  }
})
</script>
