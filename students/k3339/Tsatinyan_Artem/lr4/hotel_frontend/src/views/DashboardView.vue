<template>
  <v-container>
    <v-card class="mb-6 bg-primary" theme="dark" elevation="4" rounded="lg">
      <v-card-text class="d-flex align-center py-6">
        <div>
          <h2 class="text-h4 font-weight-bold mb-2">
            Привет, {{ user?.first_name || 'Администратор' }}!
          </h2>
          <div class="text-subtitle-1 opacity-90">
            Добро пожаловать в панель управления отелем. Удачной работы!
          </div>
        </div>
        <v-spacer></v-spacer>
        <v-icon size="64" class="opacity-50">mdi-office-building</v-icon>
      </v-card-text>
    </v-card>

    <h2 class="text-h5 mb-4 text-grey-darken-1 font-weight-medium">Сводка за сегодня</h2>

    <v-row>
      <v-col cols="12" md="4">
        <v-card elevation="2" class="h-100" rounded="lg">
          <v-card-item>
            <template v-slot:prepend>
              <v-avatar color="green-lighten-5" size="large">
                <v-icon color="green" size="large">mdi-door-open</v-icon>
              </v-avatar>
            </template>
            <v-card-title class="text-h4 font-weight-bold">{{ stats.free_rooms }}</v-card-title>
            <v-card-subtitle>Свободных номеров</v-card-subtitle>
          </v-card-item>
          <v-card-actions>
            <v-btn to="/rooms" variant="text" color="primary" append-icon="mdi-arrow-right">Посмотреть</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card elevation="2" class="h-100" rounded="lg">
          <v-card-item>
            <template v-slot:prepend>
              <v-avatar color="blue-lighten-5" size="large">
                <v-icon color="blue" size="large">mdi-account-group</v-icon>
              </v-avatar>
            </template>
            <v-card-title class="text-h4 font-weight-bold">{{ stats.guests_today }}</v-card-title>
            <v-card-subtitle>Гостей проживает</v-card-subtitle>
          </v-card-item>
          <v-card-actions>
            <v-btn to="/stays" variant="text" color="primary" append-icon="mdi-arrow-right">Список</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card elevation="2" class="h-100 d-flex flex-column" color="grey-lighten-4" rounded="lg">
          <v-card-item>
            <template v-slot:prepend>
              <v-avatar color="white" size="large">
                <v-icon color="orange-darken-2" size="large">mdi-lightning-bolt</v-icon>
              </v-avatar>
            </template>
            <v-card-title class="text-h6">Быстрые действия</v-card-title>
          </v-card-item>
          <v-card-text class="d-flex flex-column gap-2 mt-auto">
            <v-btn to="/booking" color="white" block class="mb-2 text-primary" prepend-icon="mdi-key-plus">Заселить</v-btn>
            <v-btn to="/stays" variant="outlined" block color="grey-darken-2" prepend-icon="mdi-logout">Выселить</v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12" md="6">
        <v-card elevation="3" rounded="lg">
          <v-toolbar color="transparent" density="compact">
            <v-toolbar-title class="text-subtitle-1 font-weight-bold">
              <v-icon start color="grey">mdi-broom</v-icon>
              Проверка уборки
            </v-toolbar-title>
          </v-toolbar>
          <v-divider></v-divider>
          <v-card-text>
            <v-form @submit.prevent="findCleaner">
              <v-row dense>
                <v-col cols="6">
                  <v-text-field
                    v-model="cleanerSearch.room"
                    label="Номер"
                    variant="outlined"
                    density="compact"
                    prepend-inner-icon="mdi-door"
                    hide-details
                  />
                </v-col>
                <v-col cols="6">
                  <v-text-field
                    v-model="cleanerSearch.date"
                    type="date"
                    variant="outlined"
                    density="compact"
                    hide-details
                  />
                </v-col>
              </v-row>
              <v-btn
                type="submit"
                class="mt-4"
                color="primary"
                variant="flat"
                :loading="cleanerLoading"
                block
              >
                Найти ответственного
              </v-btn>
            </v-form>

            <v-expand-transition>
              <div v-if="cleanerResult" class="mt-4">
                <v-alert type="success" variant="tonal" border="start" density="compact">
                  <div class="text-caption text-grey">Уборщик назначен:</div>
                  <div class="text-h6">{{ cleanerResult.last_name }} {{ cleanerResult.first_name }}</div>
                </v-alert>
              </div>
            </v-expand-transition>

            <v-expand-transition>
              <div v-if="cleanerError" class="mt-4">
                <v-alert type="warning" variant="tonal" density="compact" icon="mdi-alert-circle-outline">
                  {{ cleanerError }}
                </v-alert>
              </div>
            </v-expand-transition>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import api from '../api/api'

const stats = ref({
  free_rooms: 0,
  guests_today: 0
})
const user = ref(null)

onMounted(async () => {
  try {
    const u = await api.get('/auth/users/me/')
    user.value = u.data
  } catch {}

  try {
    const today = new Date()
    const tomorrow = new Date(today)
    tomorrow.setDate(tomorrow.getDate() + 1)

    const todayStr = today.toISOString().substr(0, 10)
    const tomorrowStr = tomorrow.toISOString().substr(0, 10)

    const freeRes = await api.get('/api/reports/free-rooms/', {
      params: {
        check_in: todayStr,
        check_out: tomorrowStr
      }
    })
    stats.value.free_rooms = freeRes.data.length || 0

    const staysRes = await api.get('/api/stays/?status=active')
    stats.value.guests_today = staysRes.data.length
  } catch (e) {
    console.error('Ошибка загрузки статистики:', e)
  }
})

const cleanerSearch = reactive({
  room: '',
  date: new Date().toISOString().substr(0, 10)
})
const cleanerResult = ref(null)
const cleanerError = ref('')
const cleanerLoading = ref(false)

const findCleaner = async () => {
  cleanerLoading.value = true
  cleanerResult.value = null
  cleanerError.value = ''
  try {
    const { data } = await api.get('/api/reports/who-cleaned/', {
      params: {
        room_number: cleanerSearch.room,
        date: cleanerSearch.date
      }
    })
    cleanerResult.value = data
  } catch (e) {
    cleanerError.value = e.response?.data?.detail || 'Не найдено'
  } finally {
    cleanerLoading.value = false
  }
}
</script>
