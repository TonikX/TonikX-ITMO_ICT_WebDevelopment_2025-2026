<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <h2>Управление гостями</h2>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="showDialog = true">
              <v-icon left>mdi-plus</v-icon>Добавить гостя
            </v-btn>
          </v-card-title>

          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="guests"
              :loading="loading"
              class="elevation-1"
            >
              <template v-slot:item.actions="{ item }">
                <v-icon small class="mr-2" @click="editGuest(item)">
                  mdi-pencil
                </v-icon>
                <v-icon small @click="deleteGuest(item.id)">
                  mdi-delete
                </v-icon>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Диалог добавления/редактирования -->
    <v-dialog v-model="showDialog" max-width="600">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ editMode ? 'Редактировать' : 'Добавить' }} гостя</span>
        </v-card-title>

        <v-card-text>
          <v-form @submit.prevent="saveGuest" ref="guestForm">
            <v-text-field
              v-model="currentGuest.passport_number"
              label="Номер паспорта"
              required
            />

            <v-text-field
              v-model="currentGuest.last_name"
              label="Фамилия"
              required
            />

            <v-text-field
              v-model="currentGuest.first_name"
              label="Имя"
              required
            />

            <v-text-field
              v-model="currentGuest.patronymic"
              label="Отчество"
            />

            <v-text-field
              v-model="currentGuest.city"
              label="Город"
              required
            />
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="showDialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="saveGuest">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'

const guests = ref([])
const loading = ref(false)
const showDialog = ref(false)
const editMode = ref(false)
const guestForm = ref(null)

const headers = [
  { title: 'ID', value: 'id' },
  { title: 'Паспорт', value: 'passport_number' },
  { title: 'ФИО', value: 'full_name' },
  { title: 'Город', value: 'city' },
  { title: 'Дата регистрации', value: 'registration_date' },
  { title: 'Действия', value: 'actions', sortable: false }
]

const currentGuest = reactive({
  passport_number: '',
  last_name: '',
  first_name: '',
  patronymic: '',
  city: ''
})

onMounted(() => {
  fetchGuests()
})

const fetchGuests = async () => {
  loading.value = true
  try {
    const response = await axios.get('guests/')
    guests.value = response.data.map(guest => ({
      ...guest,
      full_name: `${guest.last_name} ${guest.first_name} ${guest.patronymic || ''}`
    }))
  } catch (error) {
    console.error('Ошибка загрузки гостей:', error)
  } finally {
    loading.value = false
  }
}

const editGuest = (guest) => {
  Object.assign(currentGuest, guest)
  editMode.value = true
  showDialog.value = true
}

const saveGuest = async () => {
  try {
    if (editMode.value) {
      await axios.put(`guests/${currentGuest.id}/`, currentGuest)
    } else {
      await axios.post('guests/', currentGuest)
    }

    showDialog.value = false
    resetForm()
    fetchGuests()
  } catch (error) {
    console.error('Ошибка сохранения гостя:', error)
  }
}

const deleteGuest = async (id) => {
  if (!confirm('Вы уверены, что хотите удалить гостя?')) return

  try {
    await axios.delete(`guests/${id}/`)
    fetchGuests()
  } catch (error) {
    console.error('Ошибка удаления гостя:', error)
  }
}

const resetForm = () => {
  Object.keys(currentGuest).forEach(key => {
    currentGuest[key] = ''
  })
  editMode.value = false
}
</script>