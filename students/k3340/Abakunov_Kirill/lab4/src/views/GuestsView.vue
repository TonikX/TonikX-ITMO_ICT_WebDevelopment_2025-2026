<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4">
          <v-icon class="mr-2">mdi-account-group</v-icon>
          Гости
        </h1>
      </v-col>
      <v-col cols="auto" v-if="authStore.isAuthenticated">
        <v-btn color="primary" @click="openCheckInDialog">
          <v-icon left>mdi-account-plus</v-icon>
          Заселить гостя
        </v-btn>
      </v-col>
    </v-row>

    <!-- Фильтры -->
    <v-card class="mb-4 pa-4">
      <v-row align="center">
        <v-col cols="12" sm="4">
          <v-text-field
            v-model="search"
            label="Поиск"
            prepend-inner-icon="mdi-magnify"
            clearable
            hide-details
          ></v-text-field>
        </v-col>
        <v-col cols="12" sm="4">
          <v-text-field
            v-model="cityFilter"
            label="Город"
            prepend-inner-icon="mdi-city"
            clearable
            hide-details
          ></v-text-field>
        </v-col>
        <v-col cols="12" sm="4">
          <v-btn-toggle v-model="guestFilter" mandatory color="primary">
            <v-btn value="all">Все</v-btn>
            <v-btn value="current">Проживают</v-btn>
            <v-btn value="past">Выехали</v-btn>
          </v-btn-toggle>
        </v-col>
      </v-row>
    </v-card>

    <v-progress-linear v-if="loading" indeterminate color="primary"></v-progress-linear>

    <!-- Таблица гостей -->
    <v-card>
      <v-data-table
        :headers="headers"
        :items="filteredGuests"
        :search="search"
        :loading="loading"
        class="elevation-1"
      >
        <template v-slot:item.full_name="{ item }">
          <router-link :to="`/guests/${item.id}`" class="text-decoration-none">
            {{ item.full_name }}
          </router-link>
        </template>

        <template v-slot:item.room="{ item }">
          <v-chip size="small" :to="`/rooms/${item.room}`">
            {{ item.room_number }}
          </v-chip>
        </template>

        <template v-slot:item.status="{ item }">
          <v-chip :color="item.is_current ? 'success' : 'grey'" size="small">
            {{ item.is_current ? 'Проживает' : 'Выехал' }}
          </v-chip>
        </template>

        <template v-slot:item.actions="{ item }" v-if="authStore.isAuthenticated">
          <v-btn 
            v-if="item.is_current" 
            icon 
            size="small" 
            color="warning"
            @click="openCheckOutDialog(item)"
          >
            <v-icon>mdi-logout</v-icon>
            <v-tooltip activator="parent">Выселить</v-tooltip>
          </v-btn>
          <v-btn icon size="small" @click="editGuest(item)">
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-btn icon size="small" color="error" @click="confirmDelete(item)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>
      </v-data-table>
    </v-card>

    <!-- Диалог заселения -->
    <v-dialog v-model="checkInDialog" max-width="600">
      <v-card>
        <v-card-title>{{ isEditing ? 'Редактировать гостя' : 'Заселение гостя' }}</v-card-title>
        <v-card-text>
          <v-form ref="checkInFormRef">
            <v-row>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="guestForm.last_name"
                  label="Фамилия"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="guestForm.first_name"
                  label="Имя"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="guestForm.middle_name"
                  label="Отчество"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="guestForm.passport_number"
                  label="Номер паспорта"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="guestForm.city"
                  label="Город"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-select
                  v-model="guestForm.room"
                  label="Номер"
                  :items="availableRooms"
                  item-title="display"
                  item-value="id"
                  :rules="[rules.required]"
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="guestForm.check_in_date"
                  label="Дата заселения"
                  type="date"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" v-if="isEditing">
                <v-text-field
                  v-model="guestForm.check_out_date"
                  label="Дата выселения"
                  type="date"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="checkInDialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="saveGuest" :loading="saving">
            {{ isEditing ? 'Сохранить' : 'Заселить' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

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

    <!-- Диалог удаления -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>Подтверждение удаления</v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить запись о госте {{ guestToDelete?.full_name }}?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="deleteDialog = false">Отмена</v-btn>
          <v-btn color="error" @click="deleteGuest" :loading="saving">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, inject } from 'vue'
import { guestsAPI, roomsAPI } from '@/api'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const showSnackbar = inject('showSnackbar')

const guests = ref([])
const availableRooms = ref([])
const loading = ref(false)
const saving = ref(false)
const search = ref('')
const cityFilter = ref('')
const guestFilter = ref('all')

const checkInDialog = ref(false)
const checkOutDialog = ref(false)
const deleteDialog = ref(false)
const isEditing = ref(false)
const editingId = ref(null)
const guestToCheckOut = ref(null)
const guestToDelete = ref(null)
const checkOutDate = ref('')
const checkInFormRef = ref(null)

const headers = [
  { title: 'ФИО', key: 'full_name' },
  { title: 'Паспорт', key: 'passport_number' },
  { title: 'Город', key: 'city' },
  { title: 'Номер', key: 'room' },
  { title: 'Заселение', key: 'check_in_date' },
  { title: 'Выселение', key: 'check_out_date' },
  { title: 'Статус', key: 'status' },
  { title: 'Действия', key: 'actions', sortable: false },
]

const guestForm = reactive({
  passport_number: '',
  last_name: '',
  first_name: '',
  middle_name: '',
  city: '',
  room: null,
  check_in_date: '',
  check_out_date: '',
})

const rules = {
  required: (v) => !!v || 'Обязательное поле',
}

const filteredGuests = computed(() => {
  let result = guests.value

  if (cityFilter.value) {
    result = result.filter(g => 
      g.city.toLowerCase().includes(cityFilter.value.toLowerCase())
    )
  }

  if (guestFilter.value === 'current') {
    result = result.filter(g => g.is_current)
  } else if (guestFilter.value === 'past') {
    result = result.filter(g => !g.is_current)
  }

  return result
})

const loadGuests = async () => {
  loading.value = true
  try {
    const response = await guestsAPI.getAll()
    guests.value = response.data.results || response.data
  } catch (error) {
    showSnackbar('Ошибка загрузки гостей', 'error')
  } finally {
    loading.value = false
  }
}

const loadRooms = async () => {
  try {
    const response = await roomsAPI.getAll()
    const rooms = response.data.results || response.data
    availableRooms.value = rooms.map(r => ({
      id: r.id,
      display: `${r.number} (${r.room_type_display})`
    }))
  } catch (error) {
    console.error('Error loading rooms:', error)
  }
}

const openCheckInDialog = () => {
  isEditing.value = false
  editingId.value = null
  Object.assign(guestForm, {
    passport_number: '',
    last_name: '',
    first_name: '',
    middle_name: '',
    city: '',
    room: null,
    check_in_date: new Date().toISOString().split('T')[0],
    check_out_date: '',
  })
  checkInDialog.value = true
}

const editGuest = (guest) => {
  isEditing.value = true
  editingId.value = guest.id
  Object.assign(guestForm, {
    passport_number: guest.passport_number,
    last_name: guest.last_name,
    first_name: guest.first_name,
    middle_name: guest.middle_name,
    city: guest.city,
    room: guest.room,
    check_in_date: guest.check_in_date,
    check_out_date: guest.check_out_date || '',
  })
  checkInDialog.value = true
}

const saveGuest = async () => {
  const { valid } = await checkInFormRef.value.validate()
  if (!valid) return

  saving.value = true
  try {
    const data = { ...guestForm }
    if (!data.check_out_date) delete data.check_out_date

    if (isEditing.value) {
      await guestsAPI.update(editingId.value, data)
      showSnackbar('Данные гостя обновлены', 'success')
    } else {
      await guestsAPI.checkIn(data)
      showSnackbar('Гость заселен', 'success')
    }
    checkInDialog.value = false
    loadGuests()
  } catch (error) {
    showSnackbar('Ошибка сохранения', 'error')
  } finally {
    saving.value = false
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
    loadGuests()
  } catch (error) {
    const errorMessage = error.response?.data?.error || error.response?.data?.detail || 'Ошибка выселения'
    showSnackbar(errorMessage, 'error')
  } finally {
    saving.value = false
  }
}

const confirmDelete = (guest) => {
  guestToDelete.value = guest
  deleteDialog.value = true
}

const deleteGuest = async () => {
  saving.value = true
  try {
    await guestsAPI.delete(guestToDelete.value.id)
    showSnackbar('Запись удалена', 'success')
    deleteDialog.value = false
    loadGuests()
  } catch (error) {
    showSnackbar('Ошибка удаления', 'error')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  loadGuests()
  loadRooms()
})
</script>
