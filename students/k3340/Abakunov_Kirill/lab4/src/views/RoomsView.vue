<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4">
          <v-icon class="mr-2">mdi-door</v-icon>
          Номера гостиницы
        </h1>
      </v-col>
      <v-col cols="auto" v-if="authStore.isAuthenticated">
        <v-btn color="primary" @click="openCreateDialog">
          <v-icon left>mdi-plus</v-icon>
          Добавить номер
        </v-btn>
      </v-col>
    </v-row>

    <!-- Фильтры -->
    <v-card class="mb-4 pa-4">
      <v-row>
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
          <v-select
            v-model="filterType"
            label="Тип номера"
            :items="roomTypes"
            item-title="text"
            item-value="value"
            clearable
            hide-details
          ></v-select>
        </v-col>
        <v-col cols="12" sm="4">
          <v-btn color="success" @click="showOnlyAvailable = !showOnlyAvailable" variant="tonal" block>
            <v-icon left>{{ showOnlyAvailable ? 'mdi-check-circle' : 'mdi-circle-outline' }}</v-icon>
            Только свободные
          </v-btn>
        </v-col>
      </v-row>
    </v-card>

    <!-- Загрузка -->
    <v-progress-linear v-if="loading" indeterminate color="primary"></v-progress-linear>

    <!-- Список номеров -->
    <v-row>
      <v-col 
        v-for="room in filteredRooms" 
        :key="room.id" 
        cols="12" 
        sm="6" 
        md="4" 
        lg="3"
      >
        <v-card class="h-100" hover>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>Номер {{ room.number }}</span>
            <v-chip 
              :color="room.is_available ? 'success' : 'error'" 
              size="small"
            >
              {{ room.is_available ? 'Свободен' : 'Занят' }}
            </v-chip>
          </v-card-title>
          
          <v-card-text>
            <v-list density="compact">
              <v-list-item>
                <template v-slot:prepend>
                  <v-icon>mdi-bed</v-icon>
                </template>
                <v-list-item-title>{{ room.room_type_display }}</v-list-item-title>
              </v-list-item>
              <v-list-item>
                <template v-slot:prepend>
                  <v-icon>mdi-stairs</v-icon>
                </template>
                <v-list-item-title>{{ room.floor }} этаж</v-list-item-title>
              </v-list-item>
              <v-list-item>
                <template v-slot:prepend>
                  <v-icon>mdi-phone</v-icon>
                </template>
                <v-list-item-title>{{ room.phone }}</v-list-item-title>
              </v-list-item>
              <v-list-item>
                <template v-slot:prepend>
                  <v-icon>mdi-currency-rub</v-icon>
                </template>
                <v-list-item-title class="font-weight-bold">
                  {{ room.price_per_day }} руб/сутки
                </v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>

          <v-card-actions>
            <v-btn variant="text" color="primary" :to="`/rooms/${room.id}`">
              Подробнее
            </v-btn>
            <v-spacer></v-spacer>
            <template v-if="authStore.isAuthenticated">
              <v-btn icon size="small" @click="editRoom(room)">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn icon size="small" color="error" @click="confirmDelete(room)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-alert v-if="!loading && filteredRooms.length === 0" type="info" class="mt-4">
      Номера не найдены
    </v-alert>

    <!-- Диалог создания/редактирования -->
    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title>
          {{ isEditing ? 'Редактировать номер' : 'Добавить номер' }}
        </v-card-title>
        <v-card-text>
          <v-form ref="formRef">
            <v-text-field
              v-model="form.number"
              label="Номер"
              :rules="[rules.required]"
            ></v-text-field>
            <v-select
              v-model="form.room_type"
              label="Тип номера"
              :items="roomTypes"
              item-title="text"
              item-value="value"
              :rules="[rules.required]"
            ></v-select>
            <v-text-field
              v-model.number="form.floor"
              label="Этаж"
              type="number"
              :rules="[rules.required, rules.minValue(1)]"
            ></v-text-field>
            <v-text-field
              v-model="form.phone"
              label="Телефон"
              :rules="[rules.required]"
            ></v-text-field>
            <v-text-field
              v-model.number="form.price_per_day"
              label="Стоимость за сутки"
              type="number"
              :rules="[rules.required, rules.minValue(0)]"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="dialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="saveRoom" :loading="saving">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог подтверждения удаления -->
    <v-dialog v-model="deleteDialog" max-width="600">
      <v-card>
        <v-card-title>Подтверждение удаления</v-card-title>
        <v-card-text>
          <p class="mb-4">Вы уверены, что хотите удалить номер <strong>{{ roomToDelete?.number }}</strong>?</p>
          
          <v-alert 
            v-if="currentGuests.length > 0" 
            type="warning" 
            class="mb-4"
          >
            <div class="mb-2">
              <strong>Внимание!</strong> В этом номере проживают {{ currentGuests.length }} {{ currentGuests.length === 1 ? 'гость' : 'гостей' }}:
            </div>
            <v-list density="compact" class="bg-transparent">
              <v-list-item 
                v-for="guest in currentGuests" 
                :key="guest.id"
                class="px-0"
              >
                <template v-slot:prepend>
                  <v-icon size="small">mdi-account</v-icon>
                </template>
                <v-list-item-title>{{ guest.full_name }}</v-list-item-title>
                <v-list-item-subtitle>
                  Заселение: {{ guest.check_in_date }}
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
            <div class="mt-3">
              <v-select
                v-model="moveToRoom"
                label="Переместить гостей в номер"
                :items="otherRooms"
                item-title="display"
                item-value="id"
                hide-details
                density="compact"
                required
              ></v-select>
              <div class="text-caption text-grey mt-2">
                Необходимо выбрать номер для перемещения гостей перед удалением
              </div>
            </div>
          </v-alert>
          
          <v-alert 
            v-else-if="roomGuests.length > 0" 
            type="info" 
            class="mb-4"
          >
            У номера есть {{ roomGuests.length }} {{ roomGuests.length === 1 ? 'историческая запись' : 'исторических записей' }} о гостях, но все гости уже выселены. Удаление безопасно.
          </v-alert>
          
          <v-alert v-else type="success">
            У номера нет связанных гостей. Удаление безопасно.
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="deleteDialog = false">Отмена</v-btn>
          <v-btn 
            color="error" 
            @click="deleteRoom" 
            :loading="saving"
            :disabled="currentGuests.length > 0 && !moveToRoom"
          >
            {{ currentGuests.length > 0 && !moveToRoom ? 'Выберите номер' : 'Удалить' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, inject } from 'vue'
import { roomsAPI, guestsAPI } from '@/api'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const showSnackbar = inject('showSnackbar')

const rooms = ref([])
const loading = ref(false)
const saving = ref(false)
const dialog = ref(false)
const deleteDialog = ref(false)
const isEditing = ref(false)
const editingId = ref(null)
const roomToDelete = ref(null)
const roomGuests = ref([])
const moveToRoom = ref(null)
const formRef = ref(null)
const search = ref('')
const filterType = ref(null)
const showOnlyAvailable = ref(false)

const roomTypes = [
  { value: 'single', text: 'Одноместный' },
  { value: 'double', text: 'Двухместный' },
  { value: 'triple', text: 'Трехместный' },
]

const form = reactive({
  number: '',
  room_type: '',
  floor: 1,
  phone: '',
  price_per_day: 0,
})

const rules = {
  required: (v) => !!v || 'Обязательное поле',
  minValue: (min) => (v) => v >= min || `Минимум ${min}`,
}

const filteredRooms = computed(() => {
  let result = rooms.value

  if (search.value) {
    const s = search.value.toLowerCase()
    result = result.filter(r => 
      r.number.toLowerCase().includes(s) || 
      r.phone.toLowerCase().includes(s)
    )
  }

  if (filterType.value) {
    result = result.filter(r => r.room_type === filterType.value)
  }

  if (showOnlyAvailable.value) {
    result = result.filter(r => r.is_available)
  }

  return result
})

const otherRooms = computed(() => {
  if (!roomToDelete.value) return []
  return rooms.value
    .filter(r => r.id !== roomToDelete.value.id)
    .map(r => ({
      id: r.id,
      display: `${r.number} (${r.room_type_display})`
    }))
})

const currentGuests = computed(() => {
  return roomGuests.value.filter(g => !g.check_out_date)
})

const loadRooms = async () => {
  loading.value = true
  try {
    const response = await roomsAPI.getAll()
    rooms.value = response.data.results || response.data
  } catch (error) {
    showSnackbar('Ошибка загрузки номеров', 'error')
  } finally {
    loading.value = false
  }
}

const openCreateDialog = () => {
  isEditing.value = false
  editingId.value = null
  Object.assign(form, { number: '', room_type: '', floor: 1, phone: '', price_per_day: 0 })
  dialog.value = true
}

const editRoom = (room) => {
  isEditing.value = true
  editingId.value = room.id
  Object.assign(form, {
    number: room.number,
    room_type: room.room_type,
    floor: room.floor,
    phone: room.phone,
    price_per_day: room.price_per_day,
  })
  dialog.value = true
}

const saveRoom = async () => {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  saving.value = true
  try {
    if (isEditing.value) {
      await roomsAPI.update(editingId.value, form)
      showSnackbar('Номер обновлен', 'success')
    } else {
      await roomsAPI.create(form)
      showSnackbar('Номер добавлен', 'success')
    }
    dialog.value = false
    loadRooms()
  } catch (error) {
    const errorMessage = error.response?.data?.error || error.response?.data?.detail || 'Ошибка сохранения'
    showSnackbar(errorMessage, 'error')
  } finally {
    saving.value = false
  }
}

const confirmDelete = async (room) => {
  roomToDelete.value = room
  moveToRoom.value = null
  roomGuests.value = []
  
  // Загружаем гостей этого номера
  try {
    const response = await roomsAPI.getGuestsHistory(room.id, {})
    roomGuests.value = response.data.guests || []
  } catch (error) {
    console.error('Error loading guests:', error)
  }
  
  deleteDialog.value = true
}

const deleteRoom = async () => {
  saving.value = true
  try {
    // Если есть текущие гости и выбран номер для перемещения
    if (currentGuests.value.length > 0 && moveToRoom.value) {
      // Перемещаем всех текущих гостей в новый номер
      for (const guest of currentGuests.value) {
        await guestsAPI.update(guest.id, {
          room: moveToRoom.value,
          passport_number: guest.passport_number,
          last_name: guest.last_name,
          first_name: guest.first_name,
          middle_name: guest.middle_name || '',
          city: guest.city,
          check_in_date: guest.check_in_date,
        })
      }
      showSnackbar(`${currentGuests.value.length} ${currentGuests.value.length === 1 ? 'гость перемещен' : 'гостей перемещено'} в другой номер`, 'info')
    }
    
    // Удаляем номер
    await roomsAPI.delete(roomToDelete.value.id)
    showSnackbar('Номер удален', 'success')
    deleteDialog.value = false
    loadRooms()
  } catch (error) {
    const errorMessage = error.response?.data?.error || error.response?.data?.detail || 'Ошибка удаления'
    showSnackbar(errorMessage, 'error')
  } finally {
    saving.value = false
  }
}

onMounted(loadRooms)
</script>
