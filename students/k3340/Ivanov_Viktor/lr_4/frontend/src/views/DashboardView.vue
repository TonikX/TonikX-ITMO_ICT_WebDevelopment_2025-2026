<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const loading = ref(false)
const teachers = ref([])
const error = ref(null)

const loadTeachers = async () => {
  loading.value = true
  error.value = null
  try {
    const { data } = await api.get('/api/teachers/?limit=5')
    teachers.value = Array.isArray(data?.results) ? data.results : data
  } catch (e) {
    error.value = 'Не удалось загрузить данные (нужна авторизация?)'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (auth.token) {
    loadTeachers()
  }
})
</script>

<template>
  <v-row>
    <v-col cols="12" md="4">
      <v-card color="primary" variant="tonal">
        <v-card-title class="text-h6">Быстрый старт</v-card-title>
        <v-card-text>
          <div>1. Зарегистрируйтесь или войдите.</div>
          <div>2. Получите токен через Djoser.</div>
          <div>3. Данные подтянутся в интерфейс.</div>
        </v-card-text>
      </v-card>
    </v-col>
    <v-col cols="12" md="4">
      <v-card color="success" variant="tonal">
        <v-card-title class="text-h6">Документация API</v-card-title>
        <v-card-text>
          <div>Swagger: <strong>/api/schema/swagger-ui/</strong></div>
          <div>Redoc: <strong>/api/schema/redoc/</strong></div>
          <div>Бэкенд: DRF + Djoser + Token Auth</div>
        </v-card-text>
      </v-card>
    </v-col>
    <v-col cols="12" md="4">
      <v-card color="info" variant="tonal">
        <v-card-title class="text-h6">Учётки</v-card-title>
        <v-card-text>
          <div>Суперпользователь создаётся через <strong>createsuperuser</strong>.</div>
          <div>Токен: <strong>/api/auth/token/login/</strong></div>
          <div>Профиль: <strong>/api/auth/users/me/</strong></div>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>

  <v-row class="mt-4">
    <v-col cols="12" md="8">
      <v-card>
        <v-card-title class="d-flex align-center">
          <span class="text-h6">Пример запроса: /api/teachers/</span>
          <v-spacer />
          <v-btn size="small" color="primary" variant="tonal" @click="loadTeachers" :loading="loading">Обновить</v-btn>
        </v-card-title>
        <v-card-text>
          <v-alert v-if="error" type="warning" class="mb-4" density="compact">{{ error }}</v-alert>
          <v-progress-linear v-if="loading" indeterminate color="primary" class="mb-4" />
          <v-list v-else-if="teachers.length">
            <v-list-item v-for="teacher in teachers" :key="teacher.id || teacher.username">
              <v-list-item-title>{{ teacher.full_name || teacher.username || teacher.name }}</v-list-item-title>
              <v-list-item-subtitle>{{ teacher.subjects || teacher.position || teacher.email || '...' }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
          <v-alert v-else type="info" density="compact">Нет данных или нужна авторизация.</v-alert>
        </v-card-text>
      </v-card>
    </v-col>

    <v-col cols="12" md="4">
      <v-card>
        <v-card-title class="text-h6">Профиль</v-card-title>
        <v-card-text>
          <div class="text-subtitle-1 font-weight-medium">{{ auth.user?.username || 'Неизвестно' }}</div>
          <div class="text-body-2">{{ auth.user?.email || 'email не указан' }}</div>
          <v-btn
            class="mt-3"
            block
            color="primary"
            variant="flat"
            :to="{ name: 'profile' }"
            :disabled="!auth.isAuthenticated"
          >
            Перейти в профиль
          </v-btn>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>


