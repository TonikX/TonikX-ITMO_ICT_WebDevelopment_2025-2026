<template>
  <div>
    <h1 class="text-h4 mb-4">Книги</h1>

    <v-card class="mb-4 pa-4">
      <v-row dense>
        <v-col cols="12" md="3">
          <v-text-field
            v-model="filters.title"
            label="Поиск по названию"
            density="compact"
            variant="outlined"
            prepend-inner-icon="mdi-magnify"
            hide-details
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field
            v-model="filters.isbn"
            label="ISBN"
            density="compact"
            variant="outlined"
            hide-details
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="3">
           <v-select
            v-model="filters.has_illustrations"
            label="Иллюстрации"
            :items="[{title: 'Все', value: null}, {title: 'Да', value: true}, {title: 'Нет', value: false}]"
            density="compact"
            variant="outlined"
            hide-details
           ></v-select>
        </v-col>
         <v-col cols="12" md="3">
          <v-btn color="primary" block @click="fetchBooks">Применить</v-btn>
         </v-col>
      </v-row>
    </v-card>

    <div class="d-flex justify-end mb-4">
      <v-btn color="primary" @click="openDialog()">Добавить книгу</v-btn>
    </div>

    <v-data-table
      :headers="headers"
      :items="filteredBooks"
      :loading="loading"
      class="elevation-1"
    >
      <template v-slot:item.has_illustrations="{ item }">
        <v-icon :color="item.has_illustrations ? 'success' : 'grey'">
          {{ item.has_illustrations ? 'mdi-check' : 'mdi-close' }}
        </v-icon>
      </template>
      <template v-slot:item.authors_details="{ item }">
        <div v-if="item.authors_details">
            <v-chip
                v-for="(author, index) in parseAuthors(item.authors_details)"
                :key="index"
                class="ma-1"
                size="small"
            >
                {{ author.author_name }}
            </v-chip>
        </div>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon size="small" class="me-2" @click="openDialog(item)">mdi-pencil</v-icon>
        <v-icon size="small" color="error" @click="deleteItem(item)">mdi-delete</v-icon>
      </template>
    </v-data-table>

    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ editedId ? 'Редактировать книгу' : 'Новая книга' }}</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.title"
                  label="Название"
                  :rules="[v => !!v || 'Required']"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="editedItem.isbn"
                  label="ISBN"
                  :rules="[v => !!v || 'Required', v => v.length <= 13 || 'Max 13 chars']"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="editedItem.pages_count"
                  label="Страниц"
                  type="number"
                  :rules="[v => !!v || 'Required']"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-checkbox
                  v-model="editedItem.has_illustrations"
                  label="Есть иллюстрации"
                ></v-checkbox>
              </v-col>
              <v-col cols="12">
                 <v-autocomplete
                    v-model="selectedAuthors"
                    :items="authors"
                    item-title="full_name"
                    item-value="id"
                    label="Авторы"
                    multiple
                    chips
                    closable-chips
                 ></v-autocomplete>
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
import { ref, computed, onMounted } from 'vue'
import typography from '@/api/typography'
import { useAlertStore } from '@/stores/alert'

const alertStore = useAlertStore()

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Название', key: 'title' },
  { title: 'ISBN', key: 'isbn' },
  { title: 'Страниц', key: 'pages_count' },
  { title: 'Иллюстрации', key: 'has_illustrations' },
  { title: 'Авторы', key: 'authors_details' },
  { title: 'Действия', key: 'actions', sortable: false },
]

const books = ref([])
const loading = ref(false)
const dialog = ref(false)
const deleteDialog = ref(false)
const editedId = ref(null)
const editedItem = ref({ title: '', isbn: '', pages_count: 0, has_illustrations: false })
const selectedAuthors = ref([])
const authors = ref([])
const itemToDelete = ref(null)

const filters = ref({
    isbn: '',
    has_illustrations: null,
    title: '' 
})

const parseAuthors = (details) => {
    if (!details) return []
    try {
        if (typeof details === 'object') return details
        return JSON.parse(details.replace(/'/g, '"'))
    } catch (e) {
        console.error('Failed to parse authors:', details, e)
        return []
    }
}

const fetchBooks = async () => {
  loading.value = true
  const params = {}
  if (filters.value.isbn) params.isbn = filters.value.isbn
  if (filters.value.has_illustrations !== null) params.has_illustrations = filters.value.has_illustrations
  
  try {
    const response = await typography.getBooks(params)
    books.value = response.data
  } catch (e) {
    alertStore.showError(e)
  } finally {
    loading.value = false
  }
}

const fetchAuthors = async () => {
    try {
        const res = await typography.getAuthors()
        authors.value = res.data
    } catch (e) {
        alertStore.showError(e)
    }
}

const filteredBooks = computed(() => {
    if (!filters.value.title) return books.value
    return books.value.filter(b => b.title.toLowerCase().includes(filters.value.title.toLowerCase()))
})

const openDialog = async (item = null) => {
  if (item) {
    editedId.value = item.id
    editedItem.value = { ...item }
    selectedAuthors.value = []
    try {
        const res = await typography.getBookAuthors(item.id)
        selectedAuthors.value = relevant.map(ba => ba.author)
    } catch (e) {
        alertStore.showError(e)
    }
  } else {
    editedId.value = null
    editedItem.value = { title: '', isbn: '', pages_count: 0, has_illustrations: false }
    selectedAuthors.value = []
  }
  dialog.value = true
}

const closeDialog = () => {
  dialog.value = false
}

const save = async () => {
  try {
    let bookId = editedId.value
    if (editedId.value) {
      await typography.updateBook(editedId.value, editedItem.value)
      alertStore.show('Книга обновлена', 'success')
    } else {
      const res = await typography.createBook(editedItem.value)
      bookId = res.data.id
      alertStore.show('Книга создана', 'success')
    }

    // Управление авторами
    const currentRes = await typography.getBookAuthors(bookId)
    const currentLinks = currentRes.data.filter(ba => ba.book === bookId) 
    const currentAuthorIds = currentLinks.map(l => l.author)
    
    // 2. Определяем, кого добавить
    const toAdd = selectedAuthors.value.filter(id => !currentAuthorIds.includes(id))
    
    // 3. Определяем, кого удалить
    const toRemove = currentLinks.filter(l => !selectedAuthors.value.includes(l.author))
    
    // 4. Выполняем промисы
    const promises = []
    toAdd.forEach(authorId => {
        promises.push(typography.createBookAuthor({
            book: bookId,
            author: authorId,
            order_position: 1
        }))
    })
    toRemove.forEach(link => {
        promises.push(typography.deleteBookAuthor(link.id))
    })
    
    await Promise.all(promises)

    fetchBooks()
    closeDialog()
  } catch (e) {
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
            await typography.deleteBook(itemToDelete.value.id)
            alertStore.show('Книга удалена', 'success')
            fetchBooks()
        } catch (e) {
            alertStore.showError(e)
        }
    }
    closeDelete()
}

onMounted(() => {
  fetchBooks()
  fetchAuthors()
})
</script>
