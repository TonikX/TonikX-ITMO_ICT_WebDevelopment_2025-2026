<template>
  <div>
    <div class="d-flex justify-space-between align-center mb-4">
      <h1 class="text-h4">Управление читателями</h1>
      <v-btn color="primary" @click="openDialog()">
        <v-icon start>mdi-plus</v-icon>
        Добавить читателя
      </v-btn>
    </div>

    <v-card>
      <v-data-table
        :headers="headers"
        :items="readers"
        :loading="loading"
        item-key="id"
        no-data-text="Нет данных"
        items-per-page-text="Строк на странице:"
        loading-text="Загрузка..."
      >
        <template v-slot:item.actions="{ item }">
          <v-btn icon="mdi-pencil" size="small" @click="openDialog(item)"></v-btn>
          <v-btn icon="mdi-delete" size="small" color="error" @click="deleteReader(item.id)"></v-btn>
        </template>
      </v-data-table>
    </v-card>

    <v-dialog v-model="dialog" max-width="600">
      <v-card>
        <v-card-title>{{ editingReader ? 'Редактировать читателя' : 'Добавить читателя' }}</v-card-title>
        <v-card-text>
          <v-form ref="formRef">
            <v-text-field 
              v-model="form.library_card" 
              label="Номер читательского билета"
              variant="outlined"
              density="comfortable"
              class="mb-3"
              required
            ></v-text-field>
            <v-text-field 
              v-model="form.last_name" 
              label="Фамилия"
              variant="outlined"
              density="comfortable"
              class="mb-3"
              required
            ></v-text-field>
            <v-text-field 
              v-model="form.first_name" 
              label="Имя"
              variant="outlined"
              density="comfortable"
              class="mb-3"
              required
            ></v-text-field>
            <v-text-field 
              v-model="form.patronymic" 
              label="Отчество"
              variant="outlined"
              density="comfortable"
              class="mb-3"
            ></v-text-field>
            <v-text-field 
              v-model="form.phone" 
              label="Телефон"
              variant="outlined"
              density="comfortable"
              class="mb-3"
              required
            ></v-text-field>
            <v-text-field 
              v-model="form.email" 
              label="Email" 
              type="email"
              variant="outlined"
              density="comfortable"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="dialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="saveReader" :loading="saving">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { readersAPI } from '@/services/api'

const readers = ref([])
const loading = ref(false)
const dialog = ref(false)
const editingReader = ref(null)
const saving = ref(false)

const form = ref({
  library_card: '',
  last_name: '',
  first_name: '',
  patronymic: '',
  phone: '',
  email: ''
})

const headers = [
  { title: 'Билет', key: 'library_card' },
  { title: 'Фамилия', key: 'last_name' },
  { title: 'Имя', key: 'first_name' },
  { title: 'Отчество', key: 'patronymic' },
  { title: 'Телефон', key: 'phone' },
  { title: 'Email', key: 'email' },
  { title: 'Действия', key: 'actions', sortable: false }
]

const loadReaders = async () => {
  try {
    loading.value = true
    const response = await readersAPI.getAll()
    readers.value = response.data.results || response.data
  } catch (error) {
    console.error('Ошибка загрузки читателей:', error)
  } finally {
    loading.value = false
  }
}

const openDialog = (reader = null) => {
  editingReader.value = reader
  if (reader) {
    form.value = { ...reader }
  } else {
    form.value = {
      library_card: '',
      last_name: '',
      first_name: '',
      patronymic: '',
      phone: '',
      email: ''
    }
  }
  dialog.value = true
}

const saveReader = async () => {
  try {
    saving.value = true
    if (editingReader.value) {
      await readersAPI.update(editingReader.value.id, form.value)
    } else {
      await readersAPI.create(form.value)
    }
    dialog.value = false
    loadReaders()
  } catch (error) {
    console.error('Ошибка сохранения читателя:', error)
  } finally {
    saving.value = false
  }
}

const deleteReader = async (id) => {
  if (confirm('Удалить читателя?')) {
    try {
      await readersAPI.delete(id)
      loadReaders()
    } catch (error) {
      console.error('Ошибка удаления читателя:', error)
    }
  }
}

onMounted(() => {
  loadReaders()
})
</script>

