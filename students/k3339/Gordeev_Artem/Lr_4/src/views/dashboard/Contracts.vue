<template>
  <div>
    <h1 class="text-h4 mb-4">Контракты</h1>

    <div class="d-flex justify-end mb-4 gap-2">
        <v-btn color="secondary" class="mr-2" to="/reports">Отчеты</v-btn>
        <v-btn color="primary" @click="openDialog()">Создать контракт</v-btn>
    </div>

    <v-data-table
      :headers="headers"
      :items="contracts"
      :loading="loading"
      class="elevation-1"
    >
      <template v-slot:item.manager="{ item }">
        {{ item.manager_details?.username || item.manager }}
      </template>
      <template v-slot:item.year_month="{ item }">
        {{ new Date(item.date_signed).toISOString().substring(0, 7) }}
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon size="small" class="me-2" @click="openDialog(item)">mdi-pencil</v-icon>
        <v-icon size="small" color="error" @click="deleteItem(item)">mdi-delete</v-icon>
      </template>
    </v-data-table>

    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ editedId ? 'Редактировать контракт' : 'Новый контракт' }}</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="editedItem.number"
                  label="Номер контракта"
                  :rules="[v => !!v || 'Required']"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="editedItem.date_signed"
                  label="Дата подписания"
                  type="date"
                  :rules="[v => !!v || 'Required']"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="editedItem.book"
                  :items="books"
                  item-title="title"
                  item-value="id"
                  label="Книга"
                  :rules="[v => !!v || 'Required']"
                ></v-select>
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="editedItem.manager"
                  :items="users"
                  item-title="username"
                  item-value="id"
                  label="Менеджер"
                  :rules="[v => !!v || 'Required']"
                ></v-select>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue-darken-1" variant="text" @click="closeDialog">Отмена</v-btn>
          <v-btn color="blue-darken-1" variant="text" @click="save">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="deleteDialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">Вы уверены?</v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue-darken-1" variant="text" @click="closeDelete">Отмена</v-btn>
          <v-btn color="error" variant="text" @click="confirmDelete">OK</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import typography from '@/api/typography'
import { useAlertStore } from '@/stores/alert'

const alertStore = useAlertStore()

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Номер', key: 'number' },
  { title: 'Дата', key: 'date_signed' },
  { title: 'Менеджер', key: 'manager' },
  { title: 'Книга ID', key: 'book' },
  { title: 'Действия', key: 'actions', sortable: false },
]

const contracts = ref([])
const books = ref([])
const users = ref([])
const loading = ref(false)
const dialog = ref(false)
const deleteDialog = ref(false)
const editedId = ref(null)
const editedItem = ref({ number: '', date_signed: '', book: null, manager: null })
const itemToDelete = ref(null)

const fetchData = async () => {
  loading.value = true
  try {
    const [cntRes, booksRes, usersRes] = await Promise.all([
        typography.getContracts(),
        typography.getBooks(),
        typography.getUsers()
    ])
    contracts.value = cntRes.data
    books.value = booksRes.data
    console.log('Users response:', usersRes)
    if (Array.isArray(usersRes.data)) {
        users.value = usersRes.data
    } else if (usersRes.data && Array.isArray(usersRes.data.results)) {
        users.value = usersRes.data.results
    } else {
        users.value = []
    }
  } catch (e) {
    console.error(e)
    alertStore.showError(e)
  } finally {
    loading.value = false
  }
}

const openDialog = (item = null) => {
  if (item) {
    editedId.value = item.id
    editedItem.value = { ...item }
  } else {
    editedId.value = null
    editedItem.value = { number: '', date_signed: new Date().toISOString().substring(0, 10), book: null, manager: null }
  }
  dialog.value = true
}

const closeDialog = () => {
  dialog.value = false
}

const save = async () => {
  try {
    if (editedId.value) {
      await typography.updateContract(editedId.value, editedItem.value)
      alertStore.show('Контракт обновлен', 'success')
    } else {
      await typography.createContract(editedItem.value)
      alertStore.show('Контракт создан', 'success')
    }
    fetchData()
    closeDialog()
  } catch (e) {
    console.error(e)
    alertStore.showError(e)
  }
}

const deleteItem = (item) => {
  itemToDelete.value = item
  deleteDialog.value = true
}

const closeDelete = () => {
  deleteDialog.value = false
  itemToDelete.value = null
}

const confirmDelete = async () => {
  if (itemToDelete.value) {
    try {
      await typography.deleteContract(itemToDelete.value.id)
      alertStore.show('Контракт удален', 'success')
      fetchData()
    } catch (e) {
      console.error(e)
      alertStore.showError(e)
    }
  }
  closeDelete()
}

onMounted(() => {
  fetchData()
})
</script>
