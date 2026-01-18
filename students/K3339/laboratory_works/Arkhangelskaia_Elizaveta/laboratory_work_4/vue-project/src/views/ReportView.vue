<template>
  <v-container>
    <v-card>
      <v-card-title>Отчёт по отелю</v-card-title>

      <v-card-text>
        <v-row dense>
          <v-col cols="12" md="4">
            <v-text-field
              v-model="year"
              label="Год"
              type="number"
              outlined
              dense
            />
          </v-col>

          <v-col cols="12" md="4">
            <v-select
              v-model="quarter"
              :items="[1, 2, 3, 4]"
              label="Квартал"
              outlined
              dense
            />
          </v-col>
        </v-row>

        <v-btn color="#1B5E20" class="mt-2" @click="loadReport">
          Сформировать отчёт
        </v-btn>

        <div v-if="error" class="mt-2" style="color:red">
          {{ error }}
        </div>

        <div v-if="report" class="mt-6">
          <h3>
            Отчёт за {{ report.year }} год, {{ report.quarter }} квартал
          </h3>

          <v-card class="mt-4" variant="outlined">
            <v-card-title>Клиенты по номерам</v-card-title>
            <v-card-text>
              <v-list>
                <v-list-item
                  v-for="item in report.clients_per_room"
                  :key="item.room_number"
                >
                  Номер {{ item.room_number }} — {{ item.clients_count }} клиент(ов)
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
          <v-card class="mt-4" variant="outlined">
            <v-card-title>Номера по этажам</v-card-title>
            <v-card-text>
              <v-list>
                <v-list-item
                  v-for="item in report.rooms_per_floor"
                  :key="item.floor"
                >
                  Этаж {{ item.floor }} — {{ item.rooms_count }} номер(ов)
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>

          <v-card class="mt-4" variant="outlined">
            <v-card-title>Доход по номерам</v-card-title>
            <v-card-text>
              <v-list>
                <v-list-item
                  v-for="item in report.income_per_room"
                  :key="item.room_number"
                >
                  Номер {{ item.room_number }} — {{ item.total_income }} ₽
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>

          <v-card class="mt-4" color="green-lighten-4">
            <v-card-title>
              Общий доход отеля: {{ report.total_hotel_income }} ₽
            </v-card-title>
          </v-card>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/api'

const year = ref('')
const quarter = ref(null)
const report = ref(null)
const error = ref('')

const loadReport = async () => {
  error.value = ''
  report.value = null

  if (!year.value || !quarter.value) {
    error.value = 'Введите год и квартал'
    return
  }

  try {
    const res = await api.get(
      `req/report/?year=${year.value}&quarter=${quarter.value}`
    )
    report.value = res.data
  } catch (e) {
    console.error(e)
    error.value = 'Ошибка получения отчёта'
  }
}
</script>
