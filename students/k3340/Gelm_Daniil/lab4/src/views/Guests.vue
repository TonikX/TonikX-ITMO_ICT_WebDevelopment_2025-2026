<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1>Клиенты</h1>
        <v-btn color="primary" @click="openDialog" class="mb-4">Добавить клиента</v-btn>
      </v-col>
      <v-col cols="12">
        <v-data-table
          :headers="headers"
          :items="guests"
          :loading="loading"
        >
          <template v-slot:item.actions="{ item }">
            <v-btn icon @click="editGuest(item)">
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <v-btn icon @click="deleteGuest(item.id)">
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </v-col>
    </v-row>

    <v-dialog v-model="showDialog" max-width="500">
      <v-card>
        <v-card-title>{{ editingGuest ? 'Редактировать' : 'Добавить' }} клиента</v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field v-model="form.passport_number" label="Номер паспорта"></v-text-field>
            <v-text-field v-model="form.last_name" label="Фамилия"></v-text-field>
            <v-text-field v-model="form.first_name" label="Имя"></v-text-field>
            <v-text-field v-model="form.middle_name" label="Отчество"></v-text-field>
            <v-text-field v-model="form.city" label="Город"></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" @click="saveGuest">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { ref, onMounted } from 'vue'
import { hotelAPI } from '../api/hotel'

export default {
  name: 'Guests',
  setup() {
    const guests = ref([])
    const loading = ref(false)
    const showDialog = ref(false)
    const editingGuest = ref(null)
    const form = ref({
      passport_number: '',
      last_name: '',
      first_name: '',
      middle_name: '',
      city: ''
    })

    const headers = [
      { title: 'Паспорт', key: 'passport_number' },
      { title: 'Фамилия', key: 'last_name' },
      { title: 'Имя', key: 'first_name' },
      { title: 'Отчество', key: 'middle_name' },
      { title: 'Город', key: 'city' },
      { title: 'Действия', key: 'actions' }
    ]

    const resetForm = () => {
      form.value = {
        passport_number: '',
        last_name: '',
        first_name: '',
        middle_name: '',
        city: ''
      }
      editingGuest.value = null
    }

    const openDialog = () => {
      resetForm()
      showDialog.value = true
    }

    const closeDialog = () => {
      showDialog.value = false
      resetForm()
    }

    const loadGuests = async () => {
      loading.value = true
      try {
        const response = await hotelAPI.guests.list()
        guests.value = response.data.results || response.data
      } catch (error) {
        console.error('Error loading guests:', error)
      } finally {
        loading.value = false
      }
    }

    const saveGuest = async () => {
      try {
        if (editingGuest.value) {
          await hotelAPI.guests.update(editingGuest.value.id, form.value)
        } else {
          await hotelAPI.guests.create(form.value)
        }
        closeDialog()
        loadGuests()
      } catch (error) {
        console.error('Error saving guest:', error)
      }
    }

    const editGuest = (guest) => {
      editingGuest.value = guest
      form.value = { ...guest }
      showDialog.value = true
    }

    const deleteGuest = async (id) => {
      if (confirm('Удалить клиента?')) {
        try {
          await hotelAPI.guests.delete(id)
          loadGuests()
        } catch (error) {
          console.error('Error deleting guest:', error)
        }
      }
    }

    onMounted(() => {
      loadGuests()
    })

    return {
      guests,
      loading,
      headers,
      showDialog,
      editingGuest,
      form,
      saveGuest,
      editGuest,
      deleteGuest,
      openDialog,
      closeDialog
    }
  }
}
</script>
