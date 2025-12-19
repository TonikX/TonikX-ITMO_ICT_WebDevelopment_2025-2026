<template>
  <div class="authors-view">
    <v-row class="mb-4">
      <v-col cols="12" class="d-flex justify-space-between align-center flex-wrap">
        <h1 class="page-title">
          <v-icon class="mr-2">mdi-feather</v-icon>
          Авторы
        </h1>
        <v-btn color="primary" @click="openDialog()">
          <v-icon left>mdi-plus</v-icon>
          Добавить автора
        </v-btn>
      </v-col>
    </v-row>

    <v-card>
      <v-card-title>
        <v-text-field
          v-model="search"
          prepend-inner-icon="mdi-magnify"
          label="Поиск"
          single-line
          hide-details
          density="compact"
          style="max-width: 300px"
        ></v-text-field>
      </v-card-title>

      <v-data-table
        :headers="headers"
        :items="authors"
        :search="search"
        :loading="loading"
        :items-per-page="10"
        class="elevation-0"
      >
        <template v-slot:item.books_count="{ item }">
          <v-chip size="small" color="primary" variant="tonal">
            {{ item.books_count }} книг
          </v-chip>
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn icon="mdi-pencil" size="small" variant="text" @click="openDialog(item)"></v-btn>
          <v-btn icon="mdi-delete" size="small" variant="text" color="error" @click="confirmDelete(item)"></v-btn>
        </template>

        <template v-slot:no-data>
          <div class="text-center pa-4">
            <v-icon size="48" color="grey">mdi-account-off</v-icon>
            <p class="mt-2 text-medium-emphasis">Авторы не найдены</p>
          </div>
        </template>
      </v-data-table>
    </v-card>

    <!-- Create/Edit Dialog -->
    <v-dialog v-model="dialog" max-width="700" persistent>
      <v-card>
        <v-card-title class="d-flex align-center">
          <v-icon class="mr-2">{{ editingItem ? 'mdi-pencil' : 'mdi-plus' }}</v-icon>
          {{ editingItem ? 'Редактировать автора' : 'Новый автор' }}
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="formValid">
            <v-row>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model="formData.last_name"
                  label="Фамилия"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model="formData.first_name"
                  label="Имя"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model="formData.middle_name"
                  label="Отчество"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.email"
                  label="Email"
                  type="email"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.phone"
                  label="Телефон"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.birth_date"
                  label="Дата рождения"
                  type="date"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="formData.bio"
                  label="Биография"
                  rows="3"
                ></v-textarea>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" :loading="saving" :disabled="!formValid" @click="saveItem">
            {{ editingItem ? 'Сохранить' : 'Создать' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title class="text-h6">Подтверждение удаления</v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить автора 
          <strong>{{ itemToDelete?.full_name }}</strong>?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="deleteDialog = false">Отмена</v-btn>
          <v-btn color="error" :loading="deleting" @click="deleteItem">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, inject } from 'vue'
import { authorsApi } from '@/services/api'

const showSnackbar = inject('showSnackbar')

const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)
const authors = ref([])
const search = ref('')

const dialog = ref(false)
const deleteDialog = ref(false)
const form = ref(null)
const formValid = ref(false)
const editingItem = ref(null)
const itemToDelete = ref(null)

const headers = [
  { title: 'ID', key: 'id', width: '80px' },
  { title: 'ФИО', key: 'full_name' },
  { title: 'Email', key: 'email' },
  { title: 'Телефон', key: 'phone' },
  { title: 'Дата рождения', key: 'birth_date', width: '140px' },
  { title: 'Книги', key: 'books_count', width: '100px' },
  { title: 'Действия', key: 'actions', sortable: false, width: '120px' }
]

const formData = reactive({
  first_name: '',
  last_name: '',
  middle_name: '',
  email: '',
  phone: '',
  birth_date: '',
  bio: ''
})

const rules = {
  required: (v) => !!v || 'Обязательное поле'
}

const fetchAuthors = async () => {
  loading.value = true
  try {
    const response = await authorsApi.getAll()
    authors.value = response.data.results || response.data
  } catch (error) {
    showSnackbar('Ошибка загрузки данных', 'error')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const openDialog = (item = null) => {
  editingItem.value = item
  if (item) {
    Object.assign(formData, {
      first_name: item.first_name,
      last_name: item.last_name,
      middle_name: item.middle_name || '',
      email: item.email || '',
      phone: item.phone || '',
      birth_date: item.birth_date || '',
      bio: item.bio || ''
    })
  } else {
    Object.assign(formData, {
      first_name: '',
      last_name: '',
      middle_name: '',
      email: '',
      phone: '',
      birth_date: '',
      bio: ''
    })
  }
  dialog.value = true
}

const closeDialog = () => {
  dialog.value = false
  editingItem.value = null
  form.value?.reset()
}

const saveItem = async () => {
  const { valid } = await form.value.validate()
  if (!valid) return

  saving.value = true
  try {
    const data = { ...formData }
    if (!data.birth_date) delete data.birth_date

    if (editingItem.value) {
      await authorsApi.update(editingItem.value.id, data)
      showSnackbar('Автор обновлён', 'success')
    } else {
      await authorsApi.create(data)
      showSnackbar('Автор создан', 'success')
    }
    closeDialog()
    fetchAuthors()
  } catch (error) {
    const errorMsg = error.response?.data?.detail || 
                     Object.values(error.response?.data || {}).flat().join('. ') ||
                     'Ошибка сохранения'
    showSnackbar(errorMsg, 'error')
  } finally {
    saving.value = false
  }
}

const confirmDelete = (item) => {
  itemToDelete.value = item
  deleteDialog.value = true
}

const deleteItem = async () => {
  deleting.value = true
  try {
    await authorsApi.delete(itemToDelete.value.id)
    showSnackbar('Автор удалён', 'success')
    deleteDialog.value = false
    fetchAuthors()
  } catch (error) {
    showSnackbar('Ошибка удаления', 'error')
  } finally {
    deleting.value = false
  }
}

onMounted(fetchAuthors)
</script>

<style scoped>
.authors-view {
  max-width: 1400px;
  margin: 0 auto;
}

.page-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2rem;
  font-weight: 600;
  color: rgb(var(--v-theme-on-background));
}
</style>

