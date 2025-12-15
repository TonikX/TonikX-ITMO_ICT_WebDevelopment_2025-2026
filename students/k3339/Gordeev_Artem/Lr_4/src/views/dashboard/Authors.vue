<template>
  <div>
    <div class="d-flex justify-space-between align-center mb-4">
      <h1 class="text-h4">Авторы</h1>
      <v-btn color="primary" @click="openDialog()">Добавить автора</v-btn>
    </div>

    <v-data-table
      :headers="headers"
      :items="authors"
      :loading="loading"
      class="elevation-1"
    >
      <template v-slot:item.actions="{ item }">
        <v-icon size="small" class="me-2" @click="openDialog(item)">mdi-pencil</v-icon>
        <v-icon size="small" color="error" @click="deleteItem(item)">mdi-delete</v-icon>
      </template>
    </v-data-table>

    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ editedId ? 'Редактировать автора' : 'Новый автор' }}</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.full_name"
                  label="ФИО"
                  :rules="[v => !!v || 'Required']"
                ></v-text-field>
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
import { ref, onMounted } from 'vue'
import typography from '@/api/typography'
import { useAlertStore } from '@/stores/alert'

const alertStore = useAlertStore()

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'ФИО', key: 'full_name' },
  { title: 'Действия', key: 'actions', sortable: false },
]

const authors = ref([])
const loading = ref(false)
const dialog = ref(false)
const deleteDialog = ref(false)
const editedId = ref(null)
const editedItem = ref({ full_name: '' })
const itemToDelete = ref(null)

const fetchAuthors = async () => {
  loading.value = true
  try {
    const response = await typography.getAuthors()
    authors.value = response.data
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
    editedItem.value = { full_name: '' }
  }
  dialog.value = true
}

const closeDialog = () => {
  dialog.value = false
}

const save = async () => {
  try {
    if (editedId.value) {
      await typography.updateAuthor(editedId.value, editedItem.value)
      alertStore.show('Автор обновлен', 'success')
    } else {
      await typography.createAuthor(editedItem.value)
      alertStore.show('Автор создан', 'success')
    }
    fetchAuthors()
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
      await typography.deleteAuthor(itemToDelete.value.id)
      alertStore.show('Автор удален', 'success')
      fetchAuthors()
    } catch (e) {
      console.error(e)
      alertStore.showError(e)
    }
  }
  closeDelete()
}

onMounted(() => {
  fetchAuthors()
})
</script>
