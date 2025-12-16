<template>
  <v-container>
    <div class="d-flex justify-space-between align-center mb-6">
      <h1 class="text-h4 font-weight-bold">Бронирования</h1>
      <v-btn to="/booking" color="primary" prepend-icon="mdi-plus">Новая бронь</v-btn>
    </div>

    <v-card elevation="2" rounded="lg">
      <v-data-table
        :headers="headers"
        :items="stays"
        :loading="loading"
        :search="search"
        hover
        @click:row="openDetails"
        class="row-pointer"
      >
        <template v-slot:top>
          <v-text-field
            v-model="search"
            class="pa-4"
            density="compact"
            label="Поиск (фамилия, город, номер...)"
            prepend-inner-icon="mdi-magnify"
            variant="outlined"
            hide-details
            single-line
            style="max-width: 400px;"
          ></v-text-field>
        </template>

        <template v-slot:item.status="{ item }">
          <v-chip :color="getStatusColor(item)" size="small" variant="flat" class="font-weight-bold">
            {{ getStatusText(item) }}
          </v-chip>
        </template>

        <template v-slot:item.client="{ item }">
          <div class="py-2">
            <div class="font-weight-bold">{{ item.client?.last_name }} {{ item.client?.first_name }}</div>
            <div class="text-caption text-grey">{{ item.client?.city }}</div>
          </div>
        </template>

        <template v-slot:item.room="{ item }">
          <div class="font-weight-medium">№ {{ item.room?.number }}</div>
          <div class="text-caption text-grey">{{ item.room?.room_type }}</div>
        </template>

        <template v-slot:item.check_in="{ item }">
          {{ formatDate(item.check_in) }}
        </template>
        <template v-slot:item.check_out="{ item }">
          {{ item.check_out ? formatDate(item.check_out) : '...' }}
        </template>
      </v-data-table>
    </v-card>

    <v-dialog v-model="showDialog" max-width="700">
      <v-card rounded="lg" v-if="selectedStay">
        <v-toolbar color="primary" dark>
          <v-toolbar-title>Детали проживания</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn icon="mdi-close" @click="showDialog = false"></v-btn>
        </v-toolbar>

        <v-card-text class="pa-6">
          <v-row>
            <v-col cols="12" md="6">
              <v-card variant="outlined" class="h-100">
                <v-card-title class="d-flex align-center text-subtitle-2 text-uppercase text-grey">
                  <v-icon start size="small">mdi-account</v-icon> Клиент
                </v-card-title>
                <v-card-text>
                  <div class="text-h6 font-weight-bold">
                    {{ selectedStay.client?.last_name }} {{ selectedStay.client?.first_name }} {{ selectedStay.client?.patronymic }}
                  </div>
                  <div class="mt-2">
                    <div><strong>Паспорт:</strong> {{ selectedStay.client?.passport_number }}</div>
                    <div><strong>Город:</strong> {{ selectedStay.client?.city }}</div>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>

            <v-col cols="12" md="6">
              <v-card variant="outlined" class="h-100">
                <v-card-title class="d-flex align-center text-subtitle-2 text-uppercase text-grey">
                  <v-icon start size="small">mdi-door</v-icon> Номер
                </v-card-title>
                <v-card-text>
                  <div class="text-h4 font-weight-bold text-primary">№ {{ selectedStay.room?.number }}</div>
                  <div class="mt-2">
                    <v-chip size="small" class="mr-2">{{ selectedStay.room?.room_type }}</v-chip>
                    <v-chip size="small">{{ selectedStay.room?.floor }} этаж</v-chip>
                  </div>
                  <div class="mt-2 text-grey-darken-1">
                    Цена: <strong>{{ selectedStay.room?.daily_price }} ₽</strong> / сутки
                  </div>
                </v-card-text>
              </v-card>
            </v-col>

            <v-col cols="12">
              <v-divider class="my-4"></v-divider>
              <h3 class="text-h6 mb-3">Управление бронированием</h3>

              <v-form @submit.prevent="saveDates">
                <v-row align="center">
                  <v-col cols="12" md="5">
                    <v-text-field
                      v-model="editForm.check_in"
                      label="Дата заезда"
                      type="date"
                      variant="outlined"
                      density="comfortable"
                    />
                  </v-col>
                  <v-col cols="12" md="5">
                    <v-text-field
                      v-model="editForm.check_out"
                      label="Дата выезда"
                      type="date"
                      variant="outlined"
                      density="comfortable"
                      hint="Оставьте пустым для бессрочного проживания"
                      persistent-hint
                    />
                  </v-col>
                  <v-col cols="12" md="2">
                    <v-btn
                      color="primary"
                      block
                      height="48"
                      type="submit"
                      :loading="saving"
                      variant="tonal"
                    >
                      Сохранить
                    </v-btn>
                  </v-col>
                </v-row>
              </v-form>

              <v-alert v-if="errorMsg" type="error" variant="tonal" class="mt-3" density="compact">
                {{ errorMsg }}
              </v-alert>
            </v-col>
          </v-row>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions class="pa-4 bg-grey-lighten-5">
          <v-spacer></v-spacer>

          <v-btn
            v-if="canCheckOut(selectedStay)"
            color="orange-darken-2"
            variant="elevated"
            prepend-icon="mdi-logout"
            @click="checkOut"
          >
            Выселить сейчас
          </v-btn>

          <v-btn
            color="error"
            variant="text"
            prepend-icon="mdi-delete"
            @click="deleteStay"
          >
            {{ isFuture(selectedStay) ? 'Отменить бронь' : 'Удалить запись' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import api from '../api/api'

const stays = ref([])
const loading = ref(false)
const search = ref('')
const showDialog = ref(false)
const selectedStay = ref(null)
const saving = ref(false)
const errorMsg = ref('')

const editForm = reactive({
  check_in: '',
  check_out: ''
})

const headers = [
  { title: 'Статус', key: 'status', align: 'center', sortable: false },
  { title: 'Клиент', key: 'client', align: 'start' },
  { title: 'Номер', key: 'room', align: 'start' },
  { title: 'Заезд', key: 'check_in' },
  { title: 'Выезд', key: 'check_out' },
]

const fetchStays = async () => {
  loading.value = true
  try {
    const { data } = await api.get('/api/stays/?status=current_and_future')
    stays.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const openDetails = (event, { item }) => {
  selectedStay.value = item
  editForm.check_in = item.check_in
  editForm.check_out = item.check_out
  errorMsg.value = ''
  showDialog.value = true
}

const saveDates = async () => {
  saving.value = true
  errorMsg.value = ''
  try {
    await api.patch(`/api/stays/${selectedStay.value.id}/`, {
      check_in: editForm.check_in,
      check_out: editForm.check_out || null
    })
    await fetchStays()
    showDialog.value = false
  } catch (e) {
    errorMsg.value = e.response?.data?.detail || 'Не удалось изменить даты. Возможно пересечение.'
  } finally {
    saving.value = false
  }
}

const checkOut = async () => {
  if (!confirm('Оформить выезд клиента сегодня?')) return
  try {
    const today = new Date().toISOString().substr(0, 10)

    await api.patch(`/api/stays/${selectedStay.value.id}/`, {
      check_out: today
    })

    showDialog.value = false

    stays.value = stays.value.filter(s => s.id !== selectedStay.value.id)

  } catch (e) {
    alert('Ошибка при выселении')
  }
}

const deleteStay = async () => {
  if (!confirm('Полностью удалить эту запись из базы?')) return
  try {
    await api.delete(`/api/stays/${selectedStay.value.id}/`)

    showDialog.value = false
    stays.value = stays.value.filter(s => s.id !== selectedStay.value.id)

  } catch (e) {
    alert('Ошибка удаления')
  }
}

const canCheckOut = (item) => {
  if (!item) return false
  const today = new Date().toISOString().substr(0, 10)

  const isLiving = item.check_in <= today

  const notCheckingOutToday = !item.check_out || item.check_out > today

  return isLiving && notCheckingOutToday
}

const isFuture = (item) => {
  if (!item) return false
  const today = new Date().toISOString().substr(0, 10)
  return item.check_in > today
}

const getStatusText = (item) => {
  const today = new Date().toISOString().substr(0, 10)
  if (item.check_in > today) return 'Бронь'
  if (item.check_out === today) return 'Выезд сегодня'
  return 'Живёт'
}

const getStatusColor = (item) => {
  const today = new Date().toISOString().substr(0, 10)
  if (item.check_in > today) return 'blue-lighten-4'
  if (item.check_out === today) return 'orange-lighten-4'
  return 'green-lighten-4'
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const [y, m, d] = dateStr.split('-')
  return `${d}.${m}.${y}`
}

onMounted(fetchStays)
</script>

<style scoped>
.row-pointer :deep(tbody tr) {
  cursor: pointer;
}
</style>
