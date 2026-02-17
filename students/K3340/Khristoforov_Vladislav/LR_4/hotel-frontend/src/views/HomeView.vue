<script setup>
/**
 * HomeView.vue - Главная страница (Дашборд).
 * Отображает статистику по отелю и предоставляет кнопки для быстрых действий.
 */
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

// Состояние для статистики
const stats = ref({
  freeRooms: 0,
  activeGuests: 0,
  occupiedRooms: 0
})

const loading = ref(true)

// Функция загрузки статистики с сервера
async function fetchHomeStats() {
  try {
    // Используем эндпоинт для получения кол-ва свободных номеров
    const freeRes = await api.get('/api/analytics/', { params: { type: 'free_rooms' } })
    stats.value.freeRooms = freeRes.data.free_rooms_count

    const bookingsRes = await api.get('/api/bookings/?is_active=true')
    stats.value.activeGuests = bookingsRes.data.filter(b => b.is_active).length

    // 3. Получаем количество занятых номеров
    const occupiedRoomsRes = await api.get('/api/rooms/?status=occupied')
    stats.value.occupiedRooms = occupiedRoomsRes.data.length
  } catch (e) { console.error(e) } finally { loading.value = false }
}

// Функция для перехода на страницы создания с параметром ?new=true
function quickAction(path) {
  router.push({ path: path, query: { new: 'true' } })
}

// Загружаем данные при монтировании, если пользователь авторизован
onMounted(fetchHomeStats)
</script>

<template>
  <v-container>
    <h1 class="text-h4 mb-6">Панель администратора</h1>

    <!-- Карточки статистики -->
    <v-row v-if="!loading" class="mb-6">
      <v-col cols="12" md="4">
        <v-card color="success" class="text-white" elevation="4">
          <v-card-title class="text-h6">Свободные номера</v-card-title>
          <v-card-text class="text-h2 font-weight-bold">{{ stats.freeRooms }}</v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card color="info" class="text-white" elevation="4">
          <v-card-title class="text-h6">Гостей сейчас</v-card-title>
          <v-card-text class="text-h2 font-weight-bold">{{ stats.activeGuests }}</v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card color="warning" class="text-white" elevation="4">
          <v-card-title class="text-h6">Занято номеров</v-card-title>
          <v-card-text class="text-h2 font-weight-bold">{{ stats.occupiedRooms }}</v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-alert v-else type="info" variant="tonal" class="mt-4">
      Загрузка данных...
    </v-alert>

    <!-- Блок быстрых действий -->
    <h2 class="text-h5 mb-4">Быстрые действия</h2>
    <v-row>
      <v-col cols="12" sm="6" md="4" lg="3">
        <v-card hover @click="quickAction('/bookings')" color="indigo-lighten-5" class="text-center pa-4 cursor-pointer"
          elevation="2">
          <v-icon icon="mdi-key-plus" size="48" color="indigo" class="mb-2"></v-icon>
          <div class="text-h6 font-weight-medium">Заселить гостя</div>
          <div class="text-caption text-grey-darken-1">Создать новую бронь</div>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="4" lg="3">
        <v-card hover @click="quickAction('/guests')" color="blue-lighten-5" class="text-center pa-4 cursor-pointer"
          elevation="2">
          <v-icon icon="mdi-account-plus" size="48" color="blue" class="mb-2"></v-icon>
          <div class="text-h6 font-weight-medium">Новый гость</div>
          <div class="text-caption text-grey-darken-1">Добавить в базу</div>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="4" lg="3">
        <v-card hover @click="quickAction('/schedules')" color="orange-lighten-5"
          class="text-center pa-4 cursor-pointer" elevation="2">
          <v-icon icon="mdi-calendar-clock" size="48" color="orange-darken-2" class="mb-2"></v-icon>
          <div class="text-h6 font-weight-medium">Назначить смену</div>
          <div class="text-caption text-grey-darken-1">График уборки</div>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="4" lg="3">
        <v-card hover @click="quickAction('/employees')" color="teal-lighten-5" class="text-center pa-4 cursor-pointer"
          elevation="2">
          <v-icon icon="mdi-badge-account" size="48" color="teal" class="mb-2"></v-icon>
          <div class="text-h6 font-weight-medium">Сотрудник</div>
          <div class="text-caption text-grey-darken-1">Принять на работу</div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.cursor-pointer {
  cursor: pointer;
  transition: transform 0.2s;
}

.cursor-pointer:active {
  transform: scale(0.98);
}
</style>