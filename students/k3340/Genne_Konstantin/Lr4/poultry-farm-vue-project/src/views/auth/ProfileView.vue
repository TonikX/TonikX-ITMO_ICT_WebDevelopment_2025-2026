<template>
  <v-container>
    <v-card max-width="600" class="mx-auto">
      <v-card-title class="text-h5">Мой профиль</v-card-title>
      
      <v-card-text>
        <v-text-field
          v-model="profileForm.username"
          label="Имя пользователя *"
          :rules="[rules.required]"
          required
        />
        <v-text-field
          v-model="profileForm.email"
          label="Email *"
          type="email"
          :rules="[rules.required, rules.email]"
          required
        />

        <v-btn 
          color="primary" 
          @click="updateProfile"
          :loading="loading"
          class="mt-4"
        >
          Сохранить изменения
        </v-btn>

        <!-- Смена пароля -->
        <v-divider class="my-6" />

        <h3 class="text-h6 mb-3">Сменить пароль</h3>
        <v-text-field
          v-model="passwordForm.current_password"
          label="Текущий пароль *"
          type="password"
          :rules="[rules.required]"
          required
        />
        <v-text-field
          v-model="passwordForm.new_password"
          label="Новый пароль *"
          type="password"
          :rules="[rules.required, rules.min8]"
          required
        />
        <v-text-field
          v-model="passwordForm.re_new_password"
          label="Подтвердите новый пароль *"
          type="password"
          :rules="[rules.required, rules.passwordMatch]"
          required
        />

        <v-btn 
          color="primary" 
          variant="outlined"
          @click="changePassword"
          :loading="loading"
          class="mt-4"
        >
          Сменить пароль
        </v-btn>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/store/auth'
import { updateUser, setPassword } from '@/api/auth'

const authStore = useAuthStore()
const loading = ref(false)

// Инициализируем формы пустыми
const profileForm = ref({
  username: '',
  email: ''
})

const passwordForm = ref({
  current_password: '',
  new_password: '',
  re_new_password: ''
})

const rules = {
  required: value => !!value || 'Обязательное поле',
  email: value => {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return pattern.test(value) || 'Неверный email'
  },
  min8: value => (value && value.length >= 8) || 'Минимум 8 символов',
  passwordMatch: value => value === passwordForm.value.new_password || 'Пароли не совпадают'
}

// Загружаем профиль и устанавливаем текущие значения
onMounted(async () => {
  try {
    // Убедимся, что профиль загружен
    if (!authStore.user) {
      await authStore.fetchProfile()
    }
    // Устанавливаем текущие значения
    profileForm.value.username = authStore.user.username
    profileForm.value.email = authStore.user.email
  } catch (err) {
    console.error('Ошибка загрузки профиля:', err)
    alert('Не удалось загрузить профиль')
  }
})

const updateProfile = async () => {
  if (!profileForm.value.username || !profileForm.value.email) return

  loading.value = true
  try {
    const updated = await updateUser(profileForm.value)
    // Обновляем профиль в store
    authStore.user = updated
    alert('Профиль успешно обновлён!')
  } catch (err) {
    const errors = err.response?.data
    let msg = 'Ошибка обновления профиля'
    if (errors?.username) msg = errors.username[0]
    else if (errors?.email) msg = errors.email[0]
    alert(msg)
  } finally {
    loading.value = false
  }
}

const changePassword = async () => {
  const { current_password, new_password, re_new_password } = passwordForm.value
  if (!current_password || !new_password || !re_new_password) {
    alert('Заполните все поля пароля')
    return
  }
  if (new_password !== re_new_password) {
    alert('Новые пароли не совпадают')
    return
  }

  loading.value = true
  try {
    await setPassword({
      current_password,
      new_password,
      re_new_password
    })
    alert('Пароль успешно изменён!')
    // Очищаем поля пароля после успешной смены
    passwordForm.value = { current_password: '', new_password: '', re_new_password: '' }
  } catch (err) {
    const errors = err.response?.data
    let msg = 'Ошибка смены пароля'
    if (errors?.current_password) msg = errors.current_password[0]
    else if (errors?.new_password) msg = errors.new_password[0]
    alert(msg)
  } finally {
    loading.value = false
  }
}
</script>