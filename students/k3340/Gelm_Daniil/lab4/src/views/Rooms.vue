<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1>Номера</h1>
        <v-btn color="primary" @click="openDialog" class="mb-4">Добавить номер</v-btn>
      </v-col>
      <v-col cols="12">
        <v-data-table
          :headers="headers"
          :items="rooms"
          :loading="loading"
        >
          <template v-slot:item.room_type_display="{ item }">
            {{ getRoomType(item.room_type) }}
          </template>
          <template v-slot:item.is_occupied="{ item }">
            <v-chip :color="item.is_occupied ? 'error' : 'success'">
              {{ item.is_occupied ? 'Занят' : 'Свободен' }}
            </v-chip>
          </template>
          <template v-slot:item.actions="{ item }">
            <v-btn icon @click="editRoom(item)">
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <v-btn icon @click="deleteRoom(item.id)">
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </v-col>
    </v-row>

    <v-dialog v-model="showDialog" max-width="500">
      <v-card>
        <v-card-title>{{ editingRoom ? 'Редактировать' : 'Добавить' }} номер</v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field v-model="form.number" label="Номер"></v-text-field>
            <v-select v-model="form.room_type" :items="roomTypes" item-title="title" item-value="value" label="Тип"></v-select>
            <v-text-field v-model.number="form.floor" label="Этаж" type="number"></v-text-field>
            <v-text-field v-model="form.price_per_night" label="Цена за сутки"></v-text-field>
            <v-text-field v-model="form.phone" label="Телефон"></v-text-field>
            <v-checkbox v-model="form.is_occupied" label="Занят"></v-checkbox>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" @click="saveRoom">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { ref, onMounted } from 'vue'
import { hotelAPI } from '../api/hotel'

export default {
  name: 'Rooms',
  setup() {
    const rooms = ref([])
    const loading = ref(false)
    const showDialog = ref(false)
    const editingRoom = ref(null)
    const form = ref({
      number: '',
      room_type: 'single',
      floor: 1,
      price_per_night: '',
      phone: '',
      is_occupied: false
    })

    const headers = [
      { title: 'Номер', key: 'number' },
      { title: 'Тип', key: 'room_type_display' },
      { title: 'Этаж', key: 'floor' },
      { title: 'Цена', key: 'price_per_night' },
      { title: 'Телефон', key: 'phone' },
      { title: 'Статус', key: 'is_occupied' },
      { title: 'Действия', key: 'actions' }
    ]

    const roomTypes = [
      { title: 'Одноместный', value: 'single' },
      { title: 'Двухместный', value: 'double' },
      { title: 'Трехместный', value: 'triple' }
    ]

    const getRoomType = (type) => {
      const found = roomTypes.find(t => t.value === type)
      return found ? found.title : type
    }

    const resetForm = () => {
      form.value = {
        number: '',
        room_type: 'single',
        floor: 1,
        price_per_night: '',
        phone: '',
        is_occupied: false
      }
      editingRoom.value = null
    }

    const openDialog = () => {
      resetForm()
      showDialog.value = true
    }

    const closeDialog = () => {
      showDialog.value = false
      resetForm()
    }

    const loadRooms = async () => {
      loading.value = true
      try {
        const response = await hotelAPI.rooms.list()
        rooms.value = response.data.results || response.data
      } catch (error) {
        console.error('Error loading rooms:', error)
      } finally {
        loading.value = false
      }
    }

    const saveRoom = async () => {
      try {
        if (editingRoom.value) {
          await hotelAPI.rooms.update(editingRoom.value.id, form.value)
        } else {
          await hotelAPI.rooms.create(form.value)
        }
        closeDialog()
        loadRooms()
      } catch (error) {
        console.error('Error saving room:', error)
      }
    }

    const editRoom = (room) => {
      editingRoom.value = room
      form.value = { ...room }
      showDialog.value = true
    }

    const deleteRoom = async (id) => {
      if (confirm('Удалить номер?')) {
        try {
          await hotelAPI.rooms.delete(id)
          loadRooms()
        } catch (error) {
          console.error('Error deleting room:', error)
        }
      }
    }

    onMounted(() => {
      loadRooms()
    })

    return {
      rooms,
      loading,
      headers,
      roomTypes,
      showDialog,
      editingRoom,
      form,
      getRoomType,
      saveRoom,
      editRoom,
      deleteRoom,
      openDialog,
      closeDialog
    }
  }
}
</script>
