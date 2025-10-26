<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-4">Панель управления</h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="4">
        <v-card color="primary" dark>
          <v-card-title>
            <v-icon left>mdi-account-group</v-icon>
            Сотрудники
          </v-card-title>
          <v-card-text>
            <div class="text-h3">{{ employeesCount }}</div>
            <div>Всего сотрудников</div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card color="warning" dark>
          <v-card-title>
            <v-icon left>mdi-wrench</v-icon>
            Самолеты в ремонте
          </v-card-title>
          <v-card-text>
            <div class="text-h3">{{ planesInRepair }}</div>
            <div>Самолетов на обслуживании</div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card color="success" dark>
          <v-card-title>
            <v-icon left>mdi-trophy</v-icon>
            Популярная марка
          </v-card-title>
          <v-card-text>
            <div class="text-h3">{{ topMark }}</div>
            <div>Самая популярная марка</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title>Быстрый доступ</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" sm="6" md="3">
                <v-btn block color="primary" to="/fleet" size="large">
                  <v-icon left>mdi-airplane</v-icon>
                  Флот
                </v-btn>
              </v-col>
              <v-col cols="12" sm="6" md="3">
                <v-btn block color="primary" to="/flights" size="large">
                  <v-icon left>mdi-airplane-search</v-icon>
                  Рейсы
                </v-btn>
              </v-col>
              <v-col cols="12" sm="6" md="3">
                <v-btn block color="primary" to="/employees" size="large">
                  <v-icon left>mdi-account-group</v-icon>
                  Сотрудники
                </v-btn>
              </v-col>
              <v-col cols="12" sm="6" md="3">
                <v-btn block color="primary" to="/profile" size="large">
                  <v-icon left>mdi-account</v-icon>
                  Профиль
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { dataAPI } from '@/services/api'

const employeesCount = ref(0)
const planesInRepair = ref(0)
const topMark = ref('-')

onMounted(async () => {
  try {
    const [employeesRes, planesRes, topMarkRes] = await Promise.all([
      dataAPI.getEmployeesCount(),
      dataAPI.getPlanesInRepair(),
      dataAPI.getTopMark()
    ])

    employeesCount.value = employeesRes.data.employees_count
    planesInRepair.value = planesRes.data.planes.length
    topMark.value = topMarkRes.data.top_mark
  } catch (error) {
    console.error('Error loading dashboard data:', error)
  }
})
</script>