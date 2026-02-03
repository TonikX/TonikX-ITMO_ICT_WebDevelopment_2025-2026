<template>
  <div>
    <v-row justify="center" class="mt-8">
      <v-col cols="12" md="10" lg="8">
        <v-card class="text-center pa-8" elevation="8">
          <v-icon size="80" color="primary" class="mb-4">mdi-domain</v-icon>
          <h1 class="text-h3 mb-4">Система управления гостиницей</h1>
          <p class="text-body-1 text-grey mb-6">
            Добро пожаловать в систему управления гостиницей. 
            Здесь вы можете просматривать информацию о номерах, гостях, служащих и расписании уборки.
          </p>
          
          <v-row justify="center" class="mt-6">
            <v-col cols="12" sm="6" md="3" v-for="stat in stats" :key="stat.title">
              <v-card :color="stat.color" class="pa-4" variant="tonal">
                <v-icon size="40" class="mb-2">{{ stat.icon }}</v-icon>
                <div class="text-h4 font-weight-bold">{{ stat.value }}</div>
                <div class="text-body-2">{{ stat.title }}</div>
              </v-card>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>

    <v-row justify="center" class="mt-8">
      <v-col cols="12" md="10" lg="8">
        <v-row>
          <v-col cols="12" sm="6" md="3" v-for="card in navigationCards" :key="card.title">
            <v-card 
              :to="card.to" 
              class="pa-6 text-center h-100" 
              hover
              elevation="4"
            >
              <v-icon size="48" :color="card.color" class="mb-3">{{ card.icon }}</v-icon>
              <h3 class="text-h6 mb-2">{{ card.title }}</h3>
              <p class="text-body-2 text-grey">{{ card.description }}</p>
            </v-card>
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <v-row justify="center" class="mt-8" v-if="availableRooms.length > 0">
      <v-col cols="12" md="10" lg="8">
        <v-card>
          <v-card-title class="d-flex align-center">
            <v-icon class="mr-2">mdi-door-open</v-icon>
            Свободные номера
          </v-card-title>
          <v-card-text>
            <v-chip-group>
              <v-chip 
                v-for="room in availableRooms" 
                :key="room.id"
                :to="`/rooms/${room.id}`"
                color="success"
                variant="elevated"
              >
                {{ room.number }} ({{ room.room_type_display }})
              </v-chip>
            </v-chip-group>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { roomsAPI, guestsAPI, staffAPI, schedulesAPI } from '@/api'

const stats = ref([
  { title: 'Номеров', value: 0, icon: 'mdi-door', color: 'primary' },
  { title: 'Гостей', value: 0, icon: 'mdi-account-group', color: 'success' },
  { title: 'Служащих', value: 0, icon: 'mdi-account-hard-hat', color: 'warning' },
  { title: 'Расписаний', value: 0, icon: 'mdi-calendar-clock', color: 'info' },
])

const navigationCards = [
  {
    title: 'Номера',
    description: 'Управление номерами гостиницы',
    icon: 'mdi-door',
    color: 'primary',
    to: '/rooms',
  },
  {
    title: 'Гости',
    description: 'Информация о гостях и бронированиях',
    icon: 'mdi-account-group',
    color: 'success',
    to: '/guests',
  },
  {
    title: 'Служащие',
    description: 'Управление персоналом',
    icon: 'mdi-account-hard-hat',
    color: 'warning',
    to: '/staff',
  },
  {
    title: 'Расписания',
    description: 'График уборки номеров',
    icon: 'mdi-calendar-clock',
    color: 'info',
    to: '/schedules',
  },
]

const availableRooms = ref([])

onMounted(async () => {
  try {
    const [roomsRes, guestsRes, staffRes, schedulesRes, availableRes] = await Promise.all([
      roomsAPI.getAll(),
      guestsAPI.getCurrent(),
      staffAPI.getActive(),
      schedulesAPI.getAll(),
      roomsAPI.getAvailable(),
    ])

    stats.value[0].value = roomsRes.data.count || roomsRes.data.results?.length || 0
    stats.value[1].value = guestsRes.data.count || 0
    stats.value[2].value = staffRes.data.count || 0
    stats.value[3].value = schedulesRes.data.count || schedulesRes.data.results?.length || 0
    
    availableRooms.value = availableRes.data.rooms || []
  } catch (error) {
    console.error('Error loading stats:', error)
  }
})
</script>
