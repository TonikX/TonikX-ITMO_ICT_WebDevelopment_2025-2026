<template>
  <div>
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card color="primary" dark>
          <v-card-title class="text-h4">
            <v-icon icon="mdi-bus-multiple" size="large" class="mr-3"></v-icon>
            Панель управления автобусным парком
          </v-card-title>
          <v-card-subtitle class="text-h6">
            Обзор состояния и статистика
          </v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>

    <!-- Статистические карточки -->
    <v-row>
      <v-col cols="12" sm="6" md="3">
        <v-card hover @click="$router.push('/drivers')" style="cursor: pointer;">
          <v-card-title class="text-h6">
            <v-icon icon="mdi-account-group" color="primary" class="mr-2"></v-icon>
            Водители
          </v-card-title>
          <v-card-text>
            <div class="text-h3">{{ driversCount || 0 }}</div>
            <v-progress-linear
              v-if="loading"
              indeterminate
              color="primary"
              class="mt-2"
            ></v-progress-linear>
          </v-card-text>
          <v-card-actions>
            <v-btn
              color="primary"
              variant="text"
              prepend-icon="mdi-arrow-right"
            >
              Перейти
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card hover @click="$router.push('/buses')" style="cursor: pointer;">
          <v-card-title class="text-h6">
            <v-icon icon="mdi-bus" color="green" class="mr-2"></v-icon>
            Автобусы
          </v-card-title>
          <v-card-text>
            <div class="text-h3">{{ busesCount || 0 }}</div>
            <v-progress-linear
              v-if="loading"
              indeterminate
              color="green"
              class="mt-2"
            ></v-progress-linear>
          </v-card-text>
          <v-card-actions>
            <v-btn
              color="green"
              variant="text"
              prepend-icon="mdi-arrow-right"
            >
              Перейти
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card hover @click="$router.push('/routes')" style="cursor: pointer;">
          <v-card-title class="text-h6">
            <v-icon icon="mdi-map-marker-path" color="orange" class="mr-2"></v-icon>
            Маршруты
          </v-card-title>
          <v-card-text>
            <div class="text-h3">{{ routesCount || 0 }}</div>
            <v-progress-linear
              v-if="loading"
              indeterminate
              color="orange"
              class="mt-2"
            ></v-progress-linear>
          </v-card-text>
          <v-card-actions>
            <v-btn
              color="orange"
              variant="text"
              prepend-icon="mdi-arrow-right"
            >
              Перейти
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card hover @click="$router.push('/workshifts')" style="cursor: pointer;">
          <v-card-title class="text-h6">
            <v-icon icon="mdi-calendar-clock" color="red" class="mr-2"></v-icon>
            Активные смены
          </v-card-title>
          <v-card-text>
            <div class="text-h3">{{ workshiftsCount || 0 }}</div>
            <v-progress-linear
              v-if="loading"
              indeterminate
              color="red"
              class="mt-2"
            ></v-progress-linear>
          </v-card-text>
          <v-card-actions>
            <v-btn
              color="red"
              variant="text"
              prepend-icon="mdi-arrow-right"
            >
              Перейти
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Дополнительные модули в два ряда -->
    <v-row>
      <v-col cols="12" sm="6" md="3">
        <v-card hover @click="$router.push('/bus-types')" style="cursor: pointer;">
          <v-card-title class="text-h6">
            <v-icon icon="mdi-bus-double-decker" color="teal" class="mr-2"></v-icon>
            Типы автобусов
          </v-card-title>
          <v-card-text>
            <div class="text-h3">{{ busTypesCount || 0 }}</div>
            <v-progress-linear
              v-if="loading"
              indeterminate
              color="teal"
              class="mt-2"
            ></v-progress-linear>
          </v-card-text>
          <v-card-actions>
            <v-btn
              color="teal"
              variant="text"
              prepend-icon="mdi-arrow-right"
            >
              Перейти
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card hover @click="$router.push('/depots')" style="cursor: pointer;">
          <v-card-title class="text-h6">
            <v-icon icon="mdi-garage" color="purple" class="mr-2"></v-icon>
            Депо
          </v-card-title>
          <v-card-text>
            <div class="text-h3">{{ depotsCount || 0 }}</div>
            <v-progress-linear
              v-if="loading"
              indeterminate
              color="purple"
              class="mt-2"
            ></v-progress-linear>
          </v-card-text>
          <v-card-actions>
            <v-btn
              color="purple"
              variant="text"
              prepend-icon="mdi-arrow-right"
            >
              Перейти
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card hover @click="$router.push('/driver-classes')" style="cursor: pointer;">
          <v-card-title class="text-h6">
            <v-icon icon="mdi-license" color="indigo" class="mr-2"></v-icon>
            Классы водителей
          </v-card-title>
          <v-card-text>
            <div class="text-h3">{{ driverClassesCount || 0 }}</div>
            <v-progress-linear
              v-if="loading"
              indeterminate
              color="indigo"
              class="mt-2"
            ></v-progress-linear>
          </v-card-text>
          <v-card-actions>
            <v-btn
              color="indigo"
              variant="text"
              prepend-icon="mdi-arrow-right"
            >
              Перейти
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card hover @click="$router.push('/reports')" style="cursor: pointer;">
          <v-card-title class="text-h6">
            <v-icon icon="mdi-chart-box" color="blue-grey" class="mr-2"></v-icon>
            Отчеты
          </v-card-title>
          <v-card-text>
            <div class="text-caption mt-2">Аналитика и статистика</div>
          </v-card-text>
          <v-card-actions>
            <v-btn
              color="blue-grey"
              variant="text"
              prepend-icon="mdi-arrow-right"
            >
              Перейти
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import {ref, onMounted} from 'vue'
import {useRouter} from 'vue-router'
import apiClient from '@/api/axios'

export default {
  setup() {
    const router = useRouter()

    // Основная статистика
    const driversCount = ref(0)
    const busesCount = ref(0)
    const routesCount = ref(0)
    const workshiftsCount = ref(0)
    const busTypesCount = ref(0)
    const depotsCount = ref(0)
    const driverClassesCount = ref(0)

    // Дополнительная статистика
    const activeBusesCount = ref(0)
    const todayShiftsCount = ref(0)
    const totalRoutesDuration = ref(0)
    const avgDriverExperience = ref(0)
    const depotOccupancy = ref(0)
    const missedTripsToday = ref(0)

    // Последние действия
    const recentActivities = ref([])
    const loading = ref(false)

    const formatDuration = (minutes) => {
      if (!minutes) return '0 мин'
      const hours = Math.floor(minutes / 60)
      const mins = minutes % 60

      if (hours === 0) return `${mins} мин`
      if (mins === 0) return `${hours} ч`
      return `${hours} ч ${mins} мин`
    }

    const getActivityColor = (type) => {
      const colors = {
        'driver': 'primary',
        'bus': 'green',
        'route': 'orange',
        'shift': 'red',
        'type': 'teal',
        'depot': 'purple',
        'class': 'indigo'
      }
      return colors[type] || 'blue'
    }

    const getActivityIcon = (type) => {
      const icons = {
        'driver': 'mdi-account',
        'bus': 'mdi-bus',
        'route': 'mdi-map-marker-path',
        'shift': 'mdi-calendar-clock',
        'type': 'mdi-bus-double-decker',
        'depot': 'mdi-garage',
        'class': 'mdi-license'
      }
      return icons[type] || 'mdi-information'
    }

    const fetchData = async () => {
      loading.value = true
      try {
        // Основные данные
        const [driversRes, busesRes, routesRes, workshiftsRes, busTypesRes, depotsRes, driverClassesRes] = await Promise.all([
          apiClient.get('drivers/'),
          apiClient.get('buses/'),
          apiClient.get('routes/'),
          apiClient.get('workshifts/'),
          apiClient.get('bus-types/'),
          apiClient.get('depots/'),
          apiClient.get('driverclasses/')
        ])

        driversCount.value = driversRes.data.length
        busesCount.value = busesRes.data.length
        routesCount.value = routesRes.data.length
        workshiftsCount.value = workshiftsRes.data.length
        busTypesCount.value = busTypesRes.data.length
        depotsCount.value = depotsRes.data.length
        driverClassesCount.value = driverClassesRes.data.length

        // Дополнительная статистика
        activeBusesCount.value = busesRes.data.filter(b => b.is_active).length

        // Смены сегодня
        const today = new Date().toISOString().split('T')[0]
        todayShiftsCount.value = workshiftsRes.data.filter(shift => shift.date === today).length

        // Общая протяженность маршрутов
        totalRoutesDuration.value = routesRes.data.reduce((sum, route) => sum + (route.duration_minutes || 0), 0)

        // Средний опыт водителей
        const totalExperience = driversRes.data.reduce((sum, driver) => sum + (driver.experience_years || 0), 0)
        avgDriverExperience.value = driversRes.data.length > 0 ? totalExperience / driversRes.data.length : 0

        // Загруженность депо (примерная)
        const totalCapacity = depotsRes.data.reduce((sum, depot) => sum + (depot.capacity || 0), 0)
        const totalOccupancy = depotsRes.data.reduce((sum, depot) => sum + (depot.current_occupancy || 0), 0)
        depotOccupancy.value = totalCapacity > 0 ? (totalOccupancy / totalCapacity) * 100 : 0

        // Пропущенные рейсы сегодня
        const todayShifts = workshiftsRes.data.filter(shift => shift.date === today)
        missedTripsToday.value = todayShifts.filter(shift => shift.absence_reason).length

        // Последние действия (имитация)
        recentActivities.value = [
          {
            type: 'shift',
            title: 'Новая рабочая смена',
            description: 'Водитель Иванов И.И. назначен на маршрут 101',
            time: '10:30'
          },
          {
            type: 'bus',
            title: 'Добавлен автобус',
            description: 'Новый автобус A123BC поступил в депо №3',
            time: '09:15'
          },
          {
            type: 'driver',
            title: 'Новый водитель',
            description: 'Петров П.П. принят на работу',
            time: 'Вчера, 14:20'
          },
          {
            type: 'route',
            title: 'Изменен маршрут',
            description: 'Маршрут 22А продлен до аэропорта',
            time: 'Вчера, 11:45'
          }
        ]

      } catch (error) {
        console.error('Ошибка загрузки:', error)
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      fetchData()
    })

    return {
      // Основная статистика
      driversCount,
      busesCount,
      routesCount,
      workshiftsCount,
      busTypesCount,
      depotsCount,
      driverClassesCount,

      // Дополнительная статистика
      activeBusesCount,
      todayShiftsCount,
      totalRoutesDuration,
      avgDriverExperience,
      depotOccupancy,
      missedTripsToday,

      // Последние действия
      recentActivities,
      loading,

      // Вспомогательные функции
      formatDuration,
      getActivityColor,
      getActivityIcon
    }
  }
}
</script>

<style scoped>
.v-card {
  transition: transform 0.3s ease;
}

.v-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.v-list-item {
  cursor: default;
}

.v-list-item:hover {
  background-color: rgba(0, 0, 0, 0.02);
}

/* Анимация для карточек при наведении */
@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.02);
  }
  100% {
    transform: scale(1);
  }
}

.v-card:hover {
  animation: pulse 0.5s ease;
}
</style>
