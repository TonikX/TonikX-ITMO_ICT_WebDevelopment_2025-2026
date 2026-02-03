<template>
  <div>
    <v-btn variant="text" to="/guests" class="mb-4">
      <v-icon left>mdi-arrow-left</v-icon>
      Назад к списку
    </v-btn>

    <v-progress-linear v-if="loading" indeterminate color="primary"></v-progress-linear>

    <template v-if="guest">
      <v-row>
        <v-col cols="12" md="6">
          <v-card>
            <v-card-title class="d-flex justify-space-between align-center">
              <span>{{ guest.full_name }}</span>
              <v-chip :color="guest.is_current ? 'success' : 'grey'">
                {{ guest.is_current ? 'Проживает' : 'Выехал' }}
              </v-chip>
            </v-card-title>
            <v-card-text>
              <v-list>
                <v-list-item>
                  <template v-slot:prepend><v-icon>mdi-passport</v-icon></template>
                  <v-list-item-title>Паспорт</v-list-item-title>
                  <v-list-item-subtitle>{{ guest.passport_number }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <template v-slot:prepend><v-icon>mdi-city</v-icon></template>
                  <v-list-item-title>Город</v-list-item-title>
                  <v-list-item-subtitle>{{ guest.city }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item :to="`/rooms/${guest.room}`">
                  <template v-slot:prepend><v-icon>mdi-door</v-icon></template>
                  <v-list-item-title>Номер</v-list-item-title>
                  <v-list-item-subtitle>{{ guest.room_number }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <template v-slot:prepend><v-icon>mdi-calendar-arrow-right</v-icon></template>
                  <v-list-item-title>Дата заселения</v-list-item-title>
                  <v-list-item-subtitle>{{ guest.check_in_date }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <template v-slot:prepend><v-icon>mdi-calendar-arrow-left</v-icon></template>
                  <v-list-item-title>Дата выселения</v-list-item-title>
                  <v-list-item-subtitle>{{ guest.check_out_date || 'Проживает' }}</v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="6">
          <!-- Кто убирает номер -->
          <v-card class="mb-4">
            <v-card-title>
              <v-icon class="mr-2">mdi-broom</v-icon>
              Уборка номера
            </v-card-title>
            <v-card-text>
              <v-select
                v-model="selectedWeekday"
                label="День недели"
                :items="weekdays"
                item-title="text"
                item-value="value"
              ></v-select>
              <v-btn color="primary" @click="loadCleaningStaff" :loading="loadingCleaning" block>
                Показать
              </v-btn>

              <v-list v-if="cleaningStaff.length > 0" class="mt-4">
                <v-list-item v-for="schedule in cleaningStaff" :key="schedule.id">
                  <template v-slot:prepend>
                    <v-avatar color="warning">
                      <v-icon>mdi-account-hard-hat</v-icon>
                    </v-avatar>
                  </template>
                  <v-list-item-title>{{ schedule.staff_name }}</v-list-item-title>
                </v-list-item>
              </v-list>
              <v-alert v-else-if="cleaningStaffLoaded" type="info" class="mt-4">
                Уборщик не назначен
              </v-alert>
            </v-card-text>
          </v-card>

          <!-- Одновременно проживающие гости -->
          <v-card>
            <v-card-title>
              <v-icon class="mr-2">mdi-account-multiple</v-icon>
              Одновременные гости
            </v-card-title>
            <v-card-text>
              <v-btn color="primary" @click="loadConcurrentGuests" :loading="loadingConcurrent" block>
                Показать
              </v-btn>

              <v-list v-if="concurrentGuests.length > 0" class="mt-4">
                <v-list-item 
                  v-for="g in concurrentGuests" 
                  :key="g.id"
                  :to="`/guests/${g.id}`"
                >
                  <template v-slot:prepend>
                    <v-avatar color="primary">
                      <v-icon>mdi-account</v-icon>
                    </v-avatar>
                  </template>
                  <v-list-item-title>{{ g.full_name }}</v-list-item-title>
                  <v-list-item-subtitle>
                    Номер {{ g.room_number }}, {{ g.city }}
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
              <v-alert v-else-if="concurrentGuestsLoaded" type="info" class="mt-4">
                Нет одновременно проживающих гостей
              </v-alert>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { guestsAPI } from '@/api'

const route = useRoute()

const guest = ref(null)
const loading = ref(false)
const loadingCleaning = ref(false)
const loadingConcurrent = ref(false)
const cleaningStaff = ref([])
const cleaningStaffLoaded = ref(false)
const concurrentGuests = ref([])
const concurrentGuestsLoaded = ref(false)
const selectedWeekday = ref(1)

const weekdays = [
  { value: 1, text: 'Понедельник' },
  { value: 2, text: 'Вторник' },
  { value: 3, text: 'Среда' },
  { value: 4, text: 'Четверг' },
  { value: 5, text: 'Пятница' },
  { value: 6, text: 'Суббота' },
  { value: 7, text: 'Воскресенье' },
]

const loadGuest = async () => {
  loading.value = true
  try {
    const response = await guestsAPI.getById(route.params.id)
    guest.value = response.data
  } catch (error) {
    console.error('Error loading guest:', error)
  } finally {
    loading.value = false
  }
}

const loadCleaningStaff = async () => {
  loadingCleaning.value = true
  cleaningStaffLoaded.value = false
  try {
    const response = await guestsAPI.getCleaningStaff(route.params.id, selectedWeekday.value)
    cleaningStaff.value = response.data.cleaning_staff || []
    cleaningStaffLoaded.value = true
  } catch (error) {
    console.error('Error loading cleaning staff:', error)
  } finally {
    loadingCleaning.value = false
  }
}

const loadConcurrentGuests = async () => {
  loadingConcurrent.value = true
  concurrentGuestsLoaded.value = false
  try {
    const response = await guestsAPI.getConcurrentGuests(route.params.id, {})
    concurrentGuests.value = response.data.concurrent_guests || []
    concurrentGuestsLoaded.value = true
  } catch (error) {
    console.error('Error loading concurrent guests:', error)
  } finally {
    loadingConcurrent.value = false
  }
}

onMounted(loadGuest)
</script>
