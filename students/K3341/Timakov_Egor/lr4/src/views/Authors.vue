<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span class="text-h5">Авторы</span>
            <v-btn color="primary" @click="openDialog()">
              <v-icon start>mdi-plus</v-icon>
              Добавить автора
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-text-field
                v-model="search"
                label="Поиск по имени"
                prepend-inner-icon="mdi-magnify"
                variant="outlined"
                class="mb-4"
                @input="loadAuthors"
            ></v-text-field>

            <v-data-table
                :headers="headers"
                :items="authors"
                :loading="loading"
                item-key="id"
            >
              <template v-slot:item.full_name="{ item }">
                <strong>{{ item.full_name }}</strong>
              </template>
              <template v-slot:item.books_count="{ item }">
                <v-chip>{{ item.books_count }}</v-chip>
              </template>
              <template v-slot:item.actions="{ item }">
                <v-btn icon="mdi-book" size="small" @click="viewBooks(item)"></v-btn>
                <v-btn icon="mdi-pencil" size="small" @click="openDialog(item)"></v-btn>
                <v-btn
                    icon="mdi-delete"
                    size="small"
                    color="error"
                    @click="deleteItem(item)"
                ></v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Диалог создания/редактирования -->
    <v-dialog v-model="dialog" max-width="600">
      <v-card>
        <v-card-title>{{ editingItem ? 'Редактировать' : 'Добавить' }} автора</v-card-title>
        <v-card-text>
          <v-form ref="formRef" @submit.prevent="saveItem">
            <v-text-field
                v-model="form.first_name"
                label="Имя"
                variant="outlined"
                required
            ></v-text-field>
            <v-text-field
                v-model="form.last_name"
                label="Фамилия"
                variant="outlined"
                required
            ></v-text-field>
            <v-text-field
                v-model="form.middle_name"
                label="Отчество"
                variant="outlined"
            ></v-text-field>
            <v-text-field
                v-model="form.birth_date"
                label="Дата рождения"
                type="date"
                variant="outlined"
            ></v-text-field>
            <v-text-field
                v-model="form.email"
                label="Email"
                type="email"
                variant="outlined"
            ></v-text-field>
            <v-text-field
                v-model="form.phone"
                label="Телефон"
                variant="outlined"
            ></v-text-field>
            <v-textarea
                v-model="form.biography"
                label="Биография"
                variant="outlined"
            ></v-textarea>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" @click="saveItem">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог книг автора -->
    <v-dialog v-model="booksDialog" max-width="800">
      <v-card>
        <v-card-title>Книги автора: {{ selectedAuthor?.full_name }}</v-card-title>
        <v-card-text>
          <v-list v-if="authorBooks.length">
            <v-list-item v-for="book in authorBooks" :key="book.id">
              <v-list-item-title>{{ book.title }}</v-list-item-title>
              <v-list-item-subtitle>
                Статус: {{ book.status_display }}
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>
          <p v-else>У автора пока нет книг</p>
        </v-card-text>
        <v-card-actions>
          <v-btn @click="closeBooksDialog">Закрыть</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { authorsApi } from '../services/api'

export default {
  name: 'Authors',
  setup() {
    const authors = ref([])
    const authorBooks = ref([])
    const loading = ref(false)
    const search = ref('')
    const dialog = ref(false)
    const booksDialog = ref(false)
    const editingItem = ref(null)
    const selectedAuthor = ref(null)

    const defaultForm = {
      first_name: '',
      last_name: '',
      middle_name: '',
      birth_date: '',
      email: '',
      phone: '',
      biography: ''
    }

    const form = reactive({ ...defaultForm })

    const headers = [
      { title: 'Полное имя', key: 'full_name' },
      { title: 'Email', key: 'email' },
      { title: 'Телефон', key: 'phone' },
      { title: 'Количество книг', key: 'books_count' },
      { title: 'Действия', key: 'actions', sortable: false }
    ]

    const resetForm = () => {
      Object.assign(form, defaultForm)
    }

    const loadAuthors = async () => {
      loading.value = true
      try {
        const params = search.value ? { search: search.value } : {}
        const response = await authorsApi.getAll(params)
        authors.value = response.data.results || response.data
      } catch (error) {
        console.error('Ошибка загрузки авторов:', error)
      } finally {
        loading.value = false
      }
    }

    const openDialog = (item = null) => {
      editingItem.value = item
      if (item) {
        Object.assign(form, {
          first_name: item.first_name,
          last_name: item.last_name,
          middle_name: item.middle_name || '',
          birth_date: item.birth_date || '',
          email: item.email || '',
          phone: item.phone || '',
          biography: item.biography || ''
        })
      } else {
        resetForm()
      }
      dialog.value = true
    }

    const closeDialog = () => {
      resetForm()
      editingItem.value = null
      dialog.value = false
    }

    const saveItem = async () => {
      try {
        if (editingItem.value) {
          await authorsApi.update(editingItem.value.id, form)
        } else {
          await authorsApi.create(form)
        }
        closeDialog()
        loadAuthors()
      } catch (error) {
        console.error('Ошибка сохранения автора:', error)
      }
    }

    const deleteItem = async (item) => {
      if (confirm('Удалить автора?')) {
        try {
          await authorsApi.delete(item.id)
          loadAuthors()
        } catch (error) {
          console.error('Ошибка удаления:', error)
        }
      }
    }

    const viewBooks = async (author) => {
      selectedAuthor.value = author
      try {
        const response = await authorsApi.getBooks(author.id)
        authorBooks.value = response.data
        booksDialog.value = true
      } catch (error) {
        console.error('Ошибка загрузки книг автора:', error)
      }
    }

    const closeBooksDialog = () => {
      booksDialog.value = false
      authorBooks.value = []
    }

    onMounted(loadAuthors)

    return {
      authors,
      authorBooks,
      loading,
      search,
      dialog,
      booksDialog,
      editingItem,
      selectedAuthor,
      form,
      headers,
      loadAuthors,
      openDialog,
      closeDialog,
      saveItem,
      deleteItem,
      viewBooks,
      closeBooksDialog
    }
  }
}
</script>