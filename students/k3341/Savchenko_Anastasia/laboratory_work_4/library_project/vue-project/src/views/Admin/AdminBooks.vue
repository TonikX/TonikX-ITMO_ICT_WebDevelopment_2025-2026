<template>
  <div class="admin-books">
    <v-row>
      <v-col cols="12">
        <v-card>
          <!-- Заголовок с кнопками -->
          <v-card-title class="d-flex align-center">
            <span class="text-h5">📚 Управление книгами</span>
            <v-spacer />
            <v-btn color="success" prepend-icon="mdi-book-plus" @click="$router.push('/admin/issue-book')" class="mr-2">Выдать</v-btn>
            <v-btn color="primary" prepend-icon="mdi-book-plus" @click="$router.push('/admin/books/add')" class="mr-2">Добавить</v-btn>
            <v-btn color="info" prepend-icon="mdi-book-plus-multiple" @click="$router.push('/admin/books/add-copies')" class="mr-2">Экземпляры</v-btn>
            <v-btn color="warning" prepend-icon="mdi-book-remove" @click="$router.push('/admin/books/decommission')">Списать</v-btn>
          </v-card-title>

          <!-- Таблица -->
          <v-card-text>
            <v-data-table :headers="headers" :items="booksWithCount" :loading="loading" class="elevation-1">
              <!-- Количество экземпляров (просто цифра) -->
              <template v-slot:item.copies="{ item }">
                <v-chip size="small" color="primary">
                  {{ item.copies }} экз.
                </v-chip>
              </template>

              <!-- Действия -->
              <template v-slot:item.actions="{ item }">
                <v-btn icon="mdi-pencil" size="small" color="warning" variant="text" @click="openEditDialog(item)" title="Изменить шифр" />
                <v-btn icon="mdi-swap-horizontal" size="small" color="primary" variant="text" @click="openTransferDialog(item)" title="Переместить" />
              </template>

              <!-- Статус книги -->
              <template v-slot:item.is_in_catalog="{ item }">
                <v-chip :color="item.is_in_catalog ? 'success' : 'error'" size="small">
                  {{ item.is_in_catalog ? 'В каталоге' : 'Списана' }}
                </v-chip>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Диалог изменения шифра -->
    <v-dialog v-model="codeDialog" max-width="500px">
      <v-card v-if="selectedBook">
        <v-card-title>✏️ Изменение шифра</v-card-title>
        <v-card-text>
          <p><strong>{{ selectedBook.title }}</strong></p>
          <p>Текущий шифр: {{ selectedBook.inventory_code }}</p>
          <v-text-field v-model="newCode" label="Новый шифр" :rules="[v => !!v]" class="mt-2" />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="grey" variant="text" @click="codeDialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="updateBookCode" :loading="updating">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог перемещения -->
    <v-dialog v-model="transferDialog" max-width="500px">
      <v-card v-if="selectedCopy">
        <v-card-title>🔄 Перемещение</v-card-title>
        <v-card-text>
          <p><strong>{{ selectedCopy.bookTitle }}</strong></p>
          <p>Экз. №{{ selectedCopy.id }} | Текущий зал: {{ selectedCopy.currentHall }}</p>
          <v-select v-model="newHallId" :items="halls" item-title="name" item-value="hall_id" label="Новый зал" class="mt-2" />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="grey" variant="text" @click="transferDialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="transferCopy" :loading="transferring">Переместить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import apiClient from '../../api/client'

// Состояние
const books = ref([])
const allCopies = ref([])
const halls = ref([])
const loading = ref(false)
const updating = ref(false)
const transferring = ref(false)

// Диалоги
const codeDialog = ref(false)
const transferDialog = ref(false)
const selectedBook = ref(null)
const selectedCopy = ref(null)
const newCode = ref('')
const newHallId = ref(null)

// Заголовки
const headers = [
  { title: 'ID', key: 'book_id', width: '70px' },
  { title: 'Шифр', key: 'inventory_code' },
  { title: 'Название', key: 'title' },
  { title: 'Год', key: 'publication_year', width: '80px' },
  { title: 'Издательство', key: 'publisher' },
  { title: 'Раздел', key: 'section' },
  { title: 'Экземпляров', key: 'copies', width: '100px' },
  { title: 'Статус', key: 'is_in_catalog', width: '100px' },
  { title: 'Действия', key: 'actions', sortable: false, width: '100px' }
]

// Книги с количеством экземпляров
const booksWithCount = computed(() => {
  return books.value.map(book => {
    const count = allCopies.value.filter(c => Number(c.book_id) === Number(book.book_id)).length
    return {
      ...book,
      copies: count
    }
  })
})

// Загрузка данных
const loadData = async () => {
  loading.value = true
  try {
    const [booksRes, copiesRes, hallsRes] = await Promise.all([
      apiClient.get('books/'),
      apiClient.get('copies/'),
      apiClient.get('halls/')
    ])
    books.value = booksRes.data
    allCopies.value = copiesRes.data
    halls.value = hallsRes.data
  } catch (e) {
    console.error('Ошибка загрузки:', e)
  } finally {
    loading.value = false
  }
}

// Изменение шифра
const openEditDialog = (book) => {
  selectedBook.value = book
  newCode.value = book.inventory_code
  codeDialog.value = true
}
const updateBookCode = async () => {
  if (!newCode.value) return
  updating.value = true
  try {
    await apiClient.post(`books/${selectedBook.value.book_id}/update-code/`, { new_code: newCode.value })
    codeDialog.value = false
    await loadData()
  } catch (e) {
    alert('Ошибка при изменении шифра')
  } finally {
    updating.value = false
  }
}

// Перемещение
const openTransferDialog = (book) => {
  const available = allCopies.value.filter(c =>
    Number(c.book_id) === Number(book.book_id) &&
    c.availability_status !== 'decommissioned'
  )

  if (!available.length) {
    alert('Нет доступных экземпляров для перемещения')
    return
  }

  const copy = available[0]
  const hall = halls.value.find(h => h.hall_id === copy.hall_id)

  selectedCopy.value = {
    id: copy.copy_book_id,
    bookTitle: book.title,
    currentHall: hall?.name || `Зал #${copy.hall_id}`
  }
  newHallId.value = copy.hall_id
  transferDialog.value = true
}
const transferCopy = async () => {
  if (!newHallId.value) return
  transferring.value = true
  try {
    await apiClient.post('copies/transfer-hall/', {
      copy_id: selectedCopy.value.id,
      hall_id: newHallId.value
    })
    transferDialog.value = false
    await loadData()
  } catch (e) {
    alert('Ошибка при перемещении')
  } finally {
    transferring.value = false
  }
}

onMounted(() => loadData())
</script>