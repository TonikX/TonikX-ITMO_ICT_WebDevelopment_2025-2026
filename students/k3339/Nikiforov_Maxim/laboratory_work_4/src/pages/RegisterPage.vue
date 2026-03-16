<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const username = ref('')
const password = ref('')
const rePassword = ref('')
const error = ref('')
const loading = ref(false)

const auth = useAuthStore()
const router = useRouter()

async function onSubmit() {
  error.value = ''
  if (!username.value || !password.value || !rePassword.value) {
    error.value = 'Заполните все поля'
    return
  }
  if (password.value !== rePassword.value) {
    error.value = 'Пароли не совпадают'
    return
  }
  if (password.value.length < 8) {
    error.value = 'Пароль не менее 8 символов'
    return
  }
  loading.value = true
  try {
    await auth.register(username.value, password.value, rePassword.value)
    router.push({ name: 'login' })
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e)
    error.value = msg
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <v-app>
    <v-main>
      <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
          <v-col cols="12" sm="8" md="4">
            <v-card>
              <v-card-title class="text-h5">Регистрация</v-card-title>
              <v-card-text>
                <v-form @submit.prevent="onSubmit">
                  <v-text-field
                    v-model="username"
                    label="Имя пользователя"
                    type="text"
                    required
                    autocomplete="username"
                  />
                  <v-text-field
                    v-model="password"
                    label="Пароль"
                    type="password"
                    required
                    autocomplete="new-password"
                  />
                  <v-text-field
                    v-model="rePassword"
                    label="Повтор пароля"
                    type="password"
                    required
                    autocomplete="new-password"
                  />
                  <v-alert v-if="error" type="error" density="compact" class="mt-2">
                    {{ error }}
                  </v-alert>
                  <v-btn
                    type="submit"
                    color="primary"
                    block
                    class="mt-4"
                    :loading="loading"
                  >
                    Зарегистрироваться
                  </v-btn>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer />
                <v-btn :to="{ name: 'login' }" variant="text">
                  Вход
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>
