<template>
  <div>
    <div class="d-flex justify-space-between align-center mb-4">
      <h1 class="text-h4">Управление библиотекарями</h1>
      <v-btn color="primary" @click="openDialog()">
        <v-icon start>mdi-plus</v-icon>
        Добавить библиотекаря
      </v-btn>
    </div>

    <v-card>
      <v-data-table
        :headers="headers"
        :items="librarians"
        :loading="loading"
        item-key="id"
        no-data-text="Нет данных"
        items-per-page-text="Строк на странице:"
        loading-text="Загрузка..."
      >
        <template v-slot:item.is_active="{ item }">
          <v-chip :color="item.is_active ? 'success' : 'grey'">
            {{ item.is_active ? 'Активен' : 'Неактивен' }}
          </v-chip>
        </template>
        <template v-slot:item.actions="{ item }">
          <v-btn
            v-if="item.is_active"
            icon="mdi-account-off"
            size="small"
            color="warning"
            @click="fireLibrarian(item.id)"
          ></v-btn>
          <v-btn
            v-else
            icon="mdi-account-check"
            size="small"
            color="success"
            @click="hireLibrarian(item.id)"
          ></v-btn>
          <v-btn icon="mdi-pencil" size="small" @click="openDialog(item)"></v-btn>
          <v-btn icon="mdi-delete" size="small" color="error" @click="deleteLibrarian(item.id)"></v-btn>
        </template>
      </v-data-table>
    </v-card>

    <v-dialog v-model="dialog" max-width="600">
      <v-card>
        <v-card-title>{{ editingLibrarian ? 'Редактировать библиотекаря' : 'Добавить библиотекаря' }}</v-card-title>
        <v-card-text>
          <v-form ref="formRef">
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
            <v-checkbox 
              v-model="form.is_active" 
              label="Активен"
              color="primary"
            ></v-checkbox>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="dialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="saveLibrarian" :loading="saving">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { librariansAPI } from '@/services/api'

const librarians = ref([])
const loading = ref(false)
const dialog = ref(false)
const editingLibrarian = ref(null)
const saving = ref(false)

const form = ref({
  last_name: '',
  first_name: '',
  patronymic: '',
  is_active: true
})

const headers = [
  { title: 'Фамилия', key: 'last_name' },
  { title: 'Имя', key: 'first_name' },
  { title: 'Отчество', key: 'patronymic' },
  { title: 'Статус', key: 'is_active' },
  { title: 'Действия', key: 'actions', sortable: false }
]

const loadLibrarians = async () => {
  try {
    loading.value = true
    const response = await librariansAPI.getAll()
    librarians.value = response.data.results || response.data
  } catch (error) {
    console.error('Ошибка загрузки библиотекарей:', error)
  } finally {
    loading.value = false
  }
}

const openDialog = (librarian = null) => {
  editingLibrarian.value = librarian
  if (librarian) {
    form.value = { ...librarian }
  } else {
    form.value = {
      last_name: '',
      first_name: '',
      patronymic: '',
      is_active: true
    }
  }
  dialog.value = true
}

const saveLibrarian = async () => {
  try {
    saving.value = true
    if (editingLibrarian.value) {
      await librariansAPI.update(editingLibrarian.value.id, form.value)
    } else {
      await librariansAPI.create(form.value)
    }
    dialog.value = false
    loadLibrarians()
  } catch (error) {
    console.error('Ошибка сохранения библиотекаря:', error)
  } finally {
    saving.value = false
  }
}

const deleteLibrarian = async (id) => {
  if (confirm('Удалить библиотекаря?')) {
    try {
      await librariansAPI.delete(id)
      loadLibrarians()
    } catch (error) {
      console.error('Ошибка удаления библиотекаря:', error)
    }
  }
}

const fireLibrarian = async (id) => {
  try {
    await librariansAPI.fire(id)
    loadLibrarians()
  } catch (error) {
    console.error('Ошибка увольнения библиотекаря:', error)
  }
}

const hireLibrarian = async (id) => {
  try {
    await librariansAPI.hire(id)
    loadLibrarians()
  } catch (error) {
    console.error('Ошибка приема библиотекаря:', error)
  }
}

onMounted(() => {
  loadLibrarians()
})
</script>

