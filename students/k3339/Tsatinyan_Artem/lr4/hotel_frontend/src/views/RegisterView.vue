<template>
  <v-container class="fill-height bg-deep-purple-lighten-5" fluid>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-5" rounded="lg">
          <div class="text-center pt-6 pb-2">
            <h2 class="text-h5 font-weight-bold text-primary">Регистрация</h2>
            <div class="text-subtitle-2 text-grey">Создание нового администратора</div>
          </div>

          <v-card-text class="px-6 pb-6">
            <v-form @submit.prevent="onSubmit">
              <v-text-field
                v-model="username"
                label="Логин *"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                density="comfortable"
                required
              />

              <v-row dense class="mt-1">
                <v-col cols="6">
                  <v-text-field
                    v-model="first_name"
                    label="Имя *"
                    variant="outlined"
                    density="comfortable"
                    required
                  />
                </v-col>
                <v-col cols="6">
                  <v-text-field
                    v-model="last_name"
                    label="Фамилия *"
                    variant="outlined"
                    density="comfortable"
                    required
                  />
                </v-col>
              </v-row>

              <v-text-field
                v-model="email"
                label="Email"
                prepend-inner-icon="mdi-email"
                variant="outlined"
                density="comfortable"
                class="mt-2"
              />

              <v-text-field
                v-model="password"
                label="Пароль *"
                prepend-inner-icon="mdi-lock"
                type="password"
                variant="outlined"
                density="comfortable"
                class="mt-2"
                required
              />

              <v-btn
                :loading="loading"
                type="submit"
                color="primary"
                block
                size="large"
                class="mt-6"
              >
                Создать аккаунт
              </v-btn>
            </v-form>

            <v-alert v-if="message" type="success" variant="tonal" class="mt-4">
              {{ message }}
            </v-alert>
            <v-alert v-if="error" type="error" variant="tonal" class="mt-4">
              {{ error }}
            </v-alert>
          </v-card-text>

          <v-divider></v-divider>

          <div class="pa-4 text-center bg-grey-lighten-5">
            <span class="text-body-2 text-grey">Уже есть доступ?</span>
            <router-link to="/login" class="text-primary font-weight-bold ml-2 text-decoration-none">
              Войти
            </router-link>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api/api'

const username = ref('')
const first_name = ref('')
const last_name = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)
const message = ref('')
const error = ref('')

const onSubmit = async () => {
  loading.value = true
  message.value = ''
  error.value = ''
  try {
    await api.post('/auth/users/', {
      username: username.value,
      first_name: first_name.value,
      last_name: last_name.value,
      email: email.value || undefined,
      password: password.value,
    })

    message.value = 'Успешно! Теперь войдите.'
    username.value = ''
    first_name.value = ''
    last_name.value = ''
    email.value = ''
    password.value = ''
  } catch (e) {
    if (e.response && e.response.data) {
      const keys = Object.keys(e.response.data)
      if (keys.length > 0) {
        error.value = `${keys[0]}: ${e.response.data[keys[0]]}`
      } else {
        error.value = 'Ошибка регистрации'
      }
    } else {
      error.value = 'Ошибка соединения'
    }
  } finally {
    loading.value = false
  }
}
</script>
