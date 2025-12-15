<template>
  <v-card class="mx-auto pa-12 pb-8" elevation="8" max-width="500" rounded="lg">
    <div class="text-subtitle-1 text-medium-emphasis">Присоединяйтесь к нам</div>
    <div class="text-h4 font-weight-bold mb-4">Регистрация</div>

    <v-form @submit.prevent="handleRegister" v-model="isValid">
      <v-text-field
        v-model="form.username"
        label="Имя пользователя*"
        variant="outlined"
        density="compact"
        :rules="[rules.required]"
      ></v-text-field>

      <v-text-field
        v-model="form.email"
        label="Email"
        variant="outlined"
        density="compact"
        :rules="[rules.email]"
      ></v-text-field>

      <v-row>
        <v-col cols="6">
            <v-text-field
                v-model="form.first_name"
                label="Имя"
                variant="outlined"
                density="compact"
            ></v-text-field>
        </v-col>
        <v-col cols="6">
            <v-text-field
                v-model="form.last_name"
                label="Фамилия"
                variant="outlined"
                density="compact"
            ></v-text-field>
        </v-col>
      </v-row>

      <v-select
        v-model="form.role"
        label="Роль"
        :items="['editor', 'manager']"
        variant="outlined"
        density="compact"
      ></v-select>

      <v-text-field
        v-model="form.password"
        :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
        :type="visible ? 'text' : 'password'"
        label="Пароль*"
        variant="outlined"
        density="compact"
        @click:append-inner="visible = !visible"
        :rules="[rules.required, rules.password]"
      ></v-text-field>



      <v-btn
        block
        class="mb-8"
        color="blue"
        size="large"
        variant="tonal"
        type="submit"
        :loading="loading"
        :disabled="!isValid"
      >
        Зарегистрироваться
      </v-btn>

      <v-card-text class="text-center">
        <router-link class="text-blue text-decoration-none" to="/login">
          Уже есть аккаунт? Войти <v-icon icon="mdi-chevron-right"></v-icon>
        </router-link>
      </v-card-text>
    </v-form>
  </v-card>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useAlertStore } from '@/stores/alert'

const router = useRouter()
const authStore = useAuthStore()
const alertStore = useAlertStore()

const visible = ref(false)
const isValid = ref(false)
const loading = ref(false)

const form = reactive({
  username: '',
  password: '',
  email: '',
  first_name: '',
  last_name: '',
  role: 'editor' // по умолчанию
})

const rules = {
  required: value => !!value || 'Required.',
  email: value => {
      if (!value) return true // необязательно
      const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      return pattern.test(value) || 'Invalid e-mail.'
  },
  password: value => value.length >= 8 || 'Min 8 characters',
}

const handleRegister = async () => {
  if (!isValid.value) return
  
  loading.value = true
  
  try {
    await authStore.register(form)
    router.push('/login')
  } catch (err) {
      console.error(err)
      alertStore.showError(err)
  } finally {
    loading.value = false
  }
}
</script>
