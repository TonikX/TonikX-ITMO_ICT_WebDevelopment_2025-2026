<template>
  <div>
    <v-btn variant="text" to="/rooms" class="mb-4">
      <v-icon left>mdi-arrow-left</v-icon>
      Назад к списку
    </v-btn>

    <v-progress-linear v-if="loading" indeterminate color="primary"></v-progress-linear>

    <template v-if="room">
      <v-row>
        <v-col cols="12" md="6">
          <v-card>
            <v-card-title class="d-flex justify-space-between align-center">
              <span>Номер {{ room.number }}</span>
              <v-chip :color="room.is_available ? 'success' : 'error'">
                {{ room.is_available ? 'Свободен' : 'Занят' }}
              </v-chip>
            </v-card-title>
            <v-card-text>
              <v-list>
                <v-list-item>
                  <template v-slot:prepend><v-icon>mdi-bed</v-icon></template>
                  <v-list-item-title>Тип номера</v-list-item-title>
                  <v-list-item-subtitle>{{ room.room_type_display }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <template v-slot:prepend><v-icon>mdi-stairs</v-icon></template>
                  <v-list-item-title>Этаж</v-list-item-title>
                  <v-list-item-subtitle>{{ room.floor }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <template v-slot:prepend><v-icon>mdi-phone</v-icon></template>
                  <v-list-item-title>Телефон</v-list-item-title>
                  <v-list-item-subtitle>{{ room.phone }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <template v-slot:prepend><v-icon>mdi-currency-rub</v-icon></template>
                  <v-list-item-title>Стоимость</v-list-item-title>
                  <v-list-item-subtitle class="font-weight-bold">
                    {{ room.price_per_day }} руб/сутки
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="6">
          <v-card>
            <v-card-title>
              <v-icon class="mr-2">mdi-history</v-icon>
              История гостей
            </v-card-title>
            <v-card-text>
              <v-row class="mb-4">
                <v-col cols="6">
                  <v-text-field
                    v-model="historyStartDate"
                    label="Дата начала"
                    type="date"
                    hide-details
                  ></v-text-field>
                </v-col>
                <v-col cols="6">
                  <v-text-field
                    v-model="historyEndDate"
                    label="Дата конца"
                    type="date"
                    hide-details
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-btn color="primary" @click="loadGuestsHistory" :loading="loadingHistory" block>
                Загрузить историю
              </v-btn>

              <v-divider class="my-4"></v-divider>

              <v-alert v-if="guestsHistory.length === 0" type="info">
                История гостей пуста
              </v-alert>

              <v-list v-else>
                <v-list-item v-for="guest in guestsHistory" :key="guest.id">
                  <template v-slot:prepend>
                    <v-avatar :color="guest.is_current ? 'success' : 'primary'">
                      <v-icon>mdi-account</v-icon>
                    </v-avatar>
                  </template>
                  <v-list-item-title>{{ guest.full_name }}</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ guest.check_in_date }} — {{ guest.check_out_date || 'проживает' }}
                    <v-chip 
                      v-if="guest.is_current" 
                      size="x-small" 
                      color="success" 
                      class="ml-2"
                    >
                      Проживает
                    </v-chip>
                  </v-list-item-subtitle>
                  <template v-slot:append>
                    <v-btn 
                      v-if="guest.is_current && authStore.isAuthenticated"
                      icon 
                      size="small" 
                      color="warning"
                      @click="openCheckOutDialog(guest)"
                    >
                      <v-icon>mdi-logout</v-icon>
                      <v-tooltip activator="parent">Выселить</v-tooltip>
                    </v-btn>
                    <v-btn icon size="small" :to="`/guests/${guest.id}`">
                      <v-icon>mdi-eye</v-icon>
                      <v-tooltip activator="parent">Подробнее</v-tooltip>
                    </v-btn>
                  </template>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </template>

    <!-- Диалог выселения -->
    <v-dialog v-model="checkOutDialog" max-width="500">
      <v-card>
        <v-card-title class="d-flex align-center">
          <v-icon class="mr-2">mdi-logout</v-icon>
          Выселение гостя
        </v-card-title>
        <v-card-text>
          <div class="mb-4">
            <p class="text-h6 mb-2">{{ guestToCheckOut?.full_name }}</p>
            <v-list density="compact" class="bg-grey-lighten-5 rounded pa-2">
              <v-list-item>
                <template v-slot:prepend>
                  <v-icon size="small">mdi-calendar-arrow-right</v-icon>
                </template>
                <v-list-item-title class="text-caption">Дата заселения</v-list-item-title>
                <v-list-item-subtitle>{{ guestToCheckOut?.check_in_date }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </div>

          <v-alert 
            v-if="isEarlyCheckOut" 
            type="info" 
            density="compact"
            class="mb-4"
          >
            <v-icon size="small" class="mr-2">mdi-information</v-icon>
            Выселение до запланированной даты (досрочное выселение)
          </v-alert>

          <v-text-field
            v-model="checkOutDate"
            label="Дата выселения"
            type="date"
            :min="guestToCheckOut?.check_in_date"
            hint="Выберите дату выселения или нажмите 'Выселить сейчас'"
            persistent-hint
          ></v-text-field>

          <v-btn
            color="primary"
            variant="outlined"
            block
            class="mt-2"
            @click="setCheckOutToday"
          >
            <v-icon left>mdi-calendar-today</v-icon>
            Выселить сейчас (сегодня)
          </v-btn>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="checkOutDialog = false">Отмена</v-btn>
          <v-btn 
            color="warning" 
            @click="checkOutGuest" 
            :loading="saving"
            :disabled="!checkOutDate"
          >
            Выселить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject } from 'vue'
import { useRoute } from 'vue-router'
import { roomsAPI, guestsAPI } from '@/api'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const authStore = useAuthStore()
const showSnackbar = inject('showSnackbar')

const room = ref(null)
const loading = ref(false)
const loadingHistory = ref(false)
const guestsHistory = ref([])
const historyStartDate = ref('')
const historyEndDate = ref('')
const checkOutDialog = ref(false)
const guestToCheckOut = ref(null)
const checkOutDate = ref('')
const saving = ref(false)

const loadRoom = async () => {
  loading.value = true
  try {
    const response = await roomsAPI.getById(route.params.id)
    room.value = response.data
  } catch (error) {
    console.error('Error loading room:', error)
  } finally {
    loading.value = false
  }
}

const loadGuestsHistory = async () => {
  loadingHistory.value = true
  try {
    const params = {}
    if (historyStartDate.value) params.start_date = historyStartDate.value
    if (historyEndDate.value) params.end_date = historyEndDate.value
    
    const response = await roomsAPI.getGuestsHistory(route.params.id, params)
    guestsHistory.value = response.data.guests || []
  } catch (error) {
    console.error('Error loading history:', error)
  } finally {
    loadingHistory.value = false
  }
}

const openCheckOutDialog = (guest) => {
  guestToCheckOut.value = guest
  // Устанавливаем сегодняшнюю дату по умолчанию, но не меньше даты заселения
  const today = new Date().toISOString().split('T')[0]
  const checkInDate = guest.check_in_date
  checkOutDate.value = today >= checkInDate ? today : checkInDate
  checkOutDialog.value = true
}

const setCheckOutToday = () => {
  const today = new Date().toISOString().split('T')[0]
  const checkInDate = guestToCheckOut.value?.check_in_date
  checkOutDate.value = today >= checkInDate ? today : checkInDate
}

const isEarlyCheckOut = computed(() => {
  // Проверяем, выселяем ли мы раньше, чем сегодня (если сегодня не дата заселения)
  if (!guestToCheckOut.value || !checkOutDate.value) return false
  const today = new Date().toISOString().split('T')[0]
  const checkInDate = guestToCheckOut.value.check_in_date
  // Если выселяем сегодня, но заселение было раньше - это нормально
  // Если выселяем в будущем - это тоже нормально
  // Досрочное выселение - это когда выселяем в прошлом (раньше сегодня), но после заселения
  return checkOutDate.value < today && checkOutDate.value > checkInDate
})

const checkOutGuest = async () => {
  if (!checkOutDate.value) {
    showSnackbar('Выберите дату выселения', 'warning')
    return
  }

  // Проверка, что дата выселения не раньше даты заселения
  if (checkOutDate.value < guestToCheckOut.value.check_in_date) {
    showSnackbar('Дата выселения не может быть раньше даты заселения', 'error')
    return
  }

  saving.value = true
  try {
    await guestsAPI.checkOut(guestToCheckOut.value.id, { check_out_date: checkOutDate.value })
    const today = new Date().toISOString().split('T')[0]
    const message = checkOutDate.value < today
      ? `Гость выселен досрочно (${checkOutDate.value})`
      : checkOutDate.value === today
      ? 'Гость выселен сегодня'
      : `Гость будет выселен ${checkOutDate.value}`
    showSnackbar(message, 'success')
    checkOutDialog.value = false
    // Перезагружаем историю и информацию о номере
    loadGuestsHistory()
    loadRoom()
  } catch (error) {
    const errorMessage = error.response?.data?.error || error.response?.data?.detail || 'Ошибка выселения'
    showSnackbar(errorMessage, 'error')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  loadRoom()
  loadGuestsHistory()
})
</script>
