<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1>Проживания</h1>
        <v-btn color="primary" @click="openDialog" class="mb-4">Добавить проживание</v-btn>
      </v-col>
      <v-col cols="12">
        <v-data-table
          :headers="headers"
          :items="stays"
          :loading="loading"
        >
          <template v-slot:item.guest="{ item }">
            {{ item.guest.full_name || `${item.guest.last_name} ${item.guest.first_name}` }}
          </template>
          <template v-slot:item.room="{ item }">
            {{ item.room.number }}
          </template>
          <template v-slot:item.actions="{ item }">
            <v-btn icon @click="editStay(item)">
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <v-btn icon @click="deleteStay(item.id)">
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </v-col>
    </v-row>

    <v-dialog v-model="showDialog" max-width="500">
      <v-card>
        <v-card-title>{{ editingStay ? 'Редактировать' : 'Добавить' }} проживание</v-card-title>
        <v-card-text>
          <v-form>
            <v-select
              v-model="form.guest_id"
              :items="guests"
              item-title="full_name"
              item-value="id"
              label="Клиент"
            ></v-select>
            <v-select
              v-model="form.room_id"
              :items="rooms"
              item-title="number"
              item-value="id"
              label="Номер"
            ></v-select>
            <v-text-field
              v-model="form.check_in_date"
              label="Дата заселения"
              type="date"
            ></v-text-field>
            <v-text-field
              v-model="form.check_out_date"
              label="Дата выселения"
              type="date"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" @click="saveStay">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { ref, onMounted } from 'vue'
import { hotelAPI } from '../api/hotel'

export default {
  name: 'Stays',
  setup() {
    const stays = ref([])
    const guests = ref([])
    const rooms = ref([])
    const loading = ref(false)
    const showDialog = ref(false)
    const editingStay = ref(null)
    const form = ref({
      guest_id: null,
      room_id: null,
      check_in_date: '',
      check_out_date: ''
    })

    const headers = [
      { title: 'Клиент', key: 'guest' },
      { title: 'Номер', key: 'room' },
      { title: 'Заселение', key: 'check_in_date' },
      { title: 'Выселение', key: 'check_out_date' },
      { title: 'Действия', key: 'actions' }
    ]

    const resetForm = () => {
      form.value = {
        guest_id: null,
        room_id: null,
        check_in_date: '',
        check_out_date: ''
      }
      editingStay.value = null
    }

    const openDialog = () => {
      resetForm()
      showDialog.value = true
    }

    const closeDialog = () => {
      showDialog.value = false
      resetForm()
    }

    const loadStays = async () => {
      loading.value = true
      try {
        const response = await hotelAPI.stays.list()
        stays.value = response.data.results || response.data
      } catch (error) {
        console.error('Error loading stays:', error)
      } finally {
        loading.value = false
      }
    }

    const loadGuests = async () => {
      try {
        const response = await hotelAPI.guests.list()
        guests.value = (response.data.results || response.data).map(g => ({
          ...g,
          full_name: g.full_name || `${g.last_name} ${g.first_name}`
        }))
      } catch (error) {
        console.error('Error loading guests:', error)
      }
    }

    const loadRooms = async () => {
      try {
        const response = await hotelAPI.rooms.list()
        rooms.value = response.data.results || response.data
      } catch (error) {
        console.error('Error loading rooms:', error)
      }
    }

    const saveStay = async () => {
      try {
        if (editingStay.value) {
          await hotelAPI.stays.update(editingStay.value.id, form.value)
        } else {
          await hotelAPI.stays.create(form.value)
        }
        closeDialog()
        loadStays()
      } catch (error) {
        console.error('Error saving stay:', error)
      }
    }

    const editStay = (stay) => {
      editingStay.value = stay
      form.value = {
        guest_id: stay.guest.id,
        room_id: stay.room.id,
        check_in_date: stay.check_in_date,
        check_out_date: stay.check_out_date || ''
      }
      showDialog.value = true
    }

    const deleteStay = async (id) => {
      if (confirm('Удалить проживание?')) {
        try {
          await hotelAPI.stays.delete(id)
          loadStays()
        } catch (error) {
          console.error('Error deleting stay:', error)
        }
      }
    }

    onMounted(() => {
      loadStays()
      loadGuests()
      loadRooms()
    })

    return {
      stays,
      guests,
      rooms,
      loading,
      headers,
      showDialog,
      editingStay,
      form,
      saveStay,
      editStay,
      deleteStay,
      openDialog,
      closeDialog
    }
  }
}
</script>
