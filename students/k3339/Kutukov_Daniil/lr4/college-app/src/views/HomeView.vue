<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h3 mb-4">
          <v-icon icon="mdi-home" class="mr-2"></v-icon>
          Главная
        </h1>
        <p class="text-h6">Добро пожаловать, {{ authStore.user?.username }}!</p>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="3">
        <v-card @click="router.push('/groups')" class="hover-card">
          <v-card-text class="text-center">
            <v-icon icon="mdi-account-group" size="64" color="primary"></v-icon>
            <h3 class="mt-2">Группы</h3>
            <p>Управление учебными группами</p>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="3">
        <v-card @click="router.push('/students')" class="hover-card">
          <v-card-text class="text-center">
            <v-icon icon="mdi-account-school" size="64" color="success"></v-icon>
            <h3 class="mt-2">Студенты</h3>
            <p>База данных студентов</p>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="3">
        <v-card @click="router.push('/teachers')" class="hover-card">
          <v-card-text class="text-center">
            <v-icon icon="mdi-account-tie" size="64" color="warning"></v-icon>
            <h3 class="mt-2">Преподаватели</h3>
            <p>Информация о преподавателях</p>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="3">
        <v-card @click="router.push('/schedule')" class="hover-card">
          <v-card-text class="text-center">
            <v-icon icon="mdi-calendar-clock" size="64" color="info"></v-icon>
            <h3 class="mt-2">Расписание</h3>
            <p>Расписание занятий</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-if="stats">
      <v-col cols="12">
        <h2 class="text-h4 mt-4 mb-2">Статистика</h2>
      </v-col>
      <v-col v-for="stat in stats" :key="stat.course" cols="12" md="3">
        <v-card color="primary" dark>
          <v-card-text>
            <div class="text-h2">{{ stat.students_count }}</div>
            <div>Студентов на {{ stat.course }} курсе</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { collegeService } from '@/services/college'

const router = useRouter()
const authStore = useAuthStore()
const stats = ref<any[] | null>(null)

onMounted(async () => {
  try {
    stats.value = await collegeService.getStudentsPerCourse()
  } catch (error) {
    console.error('Failed to load stats:', error)
  }
})
</script>

<style scoped>
.hover-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.hover-card:hover {
  transform: translateY(-4px);
}
</style>
