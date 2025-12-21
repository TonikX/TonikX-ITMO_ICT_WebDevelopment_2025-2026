<template>
  <v-form @submit.prevent="handleRegister" class="mt-4">
    <v-text-field
      v-model="form.username"
      label="Username"
      type="username"
      required
      variant="outlined"
      prepend-inner-icon="mdi-account"
      :rules="[rules.required]"
      class="mb-4"
    ></v-text-field>
    
    <v-text-field
      v-model="form.first_name"
      label="Имя"
      type="first_name"
      required
      variant="outlined"
      prepend-inner-icon="mdi-pen"
      :rules="[rules.required]"
      class="mb-4"
    ></v-text-field>

    <v-text-field
      v-model="form.last_name"
      label="Фамилия"
      type="last_name"
      required
      variant="outlined"
      prepend-inner-icon="mdi-pen"
      :rules="[rules.required]"
      class="mb-4"
    ></v-text-field>

    <v-text-field
      v-model="form.phone"
      label="Телефон"
      type="phone"
      required
      variant="outlined"
      prepend-inner-icon="mdi-phone"
      :rules="[rules.required]"
      class="mb-4"
    ></v-text-field>

    <v-text-field
      v-model="form.passport"
      label="Паспортные данные"
      type="passport"
      required
      variant="outlined"
      prepend-inner-icon="mdi-passport"
      :rules="[rules.required]"
      class="mb-4"
    ></v-text-field>

    <v-text-field
      v-model="form.password"
      label="Пароль"
      type="password"
      required
      variant="outlined"
      prepend-inner-icon="mdi-lock"
      :rules="[rules.required]"
      class="mb-2"
    ></v-text-field>

    <v-text-field
      v-model="form.password_confirm"
      label="Подтверждение пароля"
      type="password"
      required
      variant="outlined"
      prepend-inner-icon="mdi-lock"
      :rules="[rules.required, rules.password_confirm]"
      class="mb-2"
    ></v-text-field>

    <v-btn
      type="submit"
      color="primary"
      size="large"
      block
      :loading="loading"
      class="mb-4"
    >
      <v-icon start icon="mdi-login"></v-icon>
      Зарегистрироваться
    </v-btn>

    <v-alert
      v-if="error"
      type="error"
      variant="tonal"
      density="compact"
      class="mt-4"
    >
      {{ error }}
    </v-alert>
  </v-form>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const form = ref({
  username: '',
  first_name: '',
  last_name: '',
  phone: '',
  passport: '',
  password: '',
  password_confirm: '',
})

const loading = ref(false)
const error = ref('')


const rules = {
  required: value => !!value || 'Обязательное поле',
  password_confirm: value => form.value.password === value || 'Пароли не совпадают'
}

const handleRegister = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const userData = {
      username: form.value.username,
      first_name: form.value.first_name,
      last_name: form.value.last_name,
      phone: form.value.phone,
      passport: form.value.passport,
      password: form.value.password,
    }
    
    await authStore.register(userData)
    await authStore.login(userData);
    router.push('/')
  } catch (err) {
    console.log(err);
    error.value = err
  } finally {
    loading.value = false
  }
}
</script>