<template>
  <div>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="text-h4 pa-4">
            Добро пожаловать, {{ authStore.user?.username }}!
          </v-card-title>
          <v-card-text>
            <p class="text-h6 mb-4">Вы вошли как: <strong>{{ getRoleName(authStore.user?.role) }}</strong></p>
            <v-divider class="my-4"></v-divider>
            <v-row>
              <v-col cols="12" md="4">
                <v-card color="primary" dark>
                  <v-card-title>Учителя</v-card-title>
                  <v-card-text>
                    <div class="text-h3">{{ stats.teachers }}</div>
                    <div>всего учителей</div>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" md="4">
                <v-card color="success" dark>
                  <v-card-title>Ученики</v-card-title>
                  <v-card-text>
                    <div class="text-h3">{{ stats.students }}</div>
                    <div>всего учеников</div>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" md="4">
                <v-card color="info" dark>
                  <v-card-title>Классы</v-card-title>
                  <v-card-text>
                    <div class="text-h3">{{ stats.classes }}</div>
                    <div>всего классов</div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/client'

const authStore = useAuthStore()
const stats = ref({
  teachers: 0,
  students: 0,
  classes: 0
})

const getRoleName = (role) => {
  const roles = {
    admin: 'Администратор',
    head_teacher: 'Завуч',
    teacher: 'Учитель'
  }
  return roles[role] || role
}

onMounted(async () => {
  try {
    const [teachersRes, studentsRes, classesRes] = await Promise.all([
      api.get('/teachers'),
      api.get('/students'),
      api.get('/classes')
    ])
    stats.value.teachers = teachersRes.data?.length || 0
    stats.value.students = studentsRes.data?.length || 0
    stats.value.classes = classesRes.data?.length || 0
  } catch (error) {
    console.error('Ошибка загрузки статистики:', error)
  }
})
</script>

