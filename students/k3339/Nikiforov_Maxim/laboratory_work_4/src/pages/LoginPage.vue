<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

async function onSubmit() {
  error.value = ''
  if (!username.value || !password.value) {
    error.value = 'Заполните имя пользователя и пароль'
    return
  }
  loading.value = true
  try {
    await auth.login(username.value, password.value)
    const redirect = (route.query.redirect as string) || '/'
    router.push(redirect)
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Ошибка входа'
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
              <v-card-title class="text-h5">Вход</v-card-title>
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
                    autocomplete="current-password"
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
                    Войти
                  </v-btn>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer />
                <v-btn :to="{ name: 'register' }" variant="text">
                  Регистрация
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>
