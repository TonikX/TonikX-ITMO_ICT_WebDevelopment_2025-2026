<template>
  <div class="admin-books">
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex align-center">
            <span class="text-h5">📚 Управление книгами</span>
            <v-spacer></v-spacer>

            <!-- Кнопки действий -->
            <v-btn
              color="success"
              prepend-icon="mdi-book-plus"
              @click="$router.push('/admin/issue-book')"
              class="mr-2"
            >
              Выдать книгу
            </v-btn>
            <v-btn
              color="primary"
              prepend-icon="mdi-book-plus"
              @click="$router.push('/admin/books/add')"
              class="mr-2"
            >
              Добавить книгу
            </v-btn>
            <v-btn
              color="warning"
              prepend-icon="mdi-book-remove"
              @click="$router.push('/admin/books/decommission')"
            >
              Списать книгу
            </v-btn>
          </v-card-title>

          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="books"
              :loading="loading"
              class="elevation-1"
            >
              <!-- Действия с книгой -->
              <template v-slot:item.actions="{ item }">
                <v-btn
                  icon="mdi-pencil"
                  size="small"
                  color="warning"
                  variant="text"
                  @click="openEditDialog(item)"
                  title="Изменить шифр"
                ></v-btn>
                <v-btn
                  icon="mdi-swap-horizontal"
                  size="small"
                  color="primary"
                  variant="text"
                  @click="openTransferDialog(item)"
                  title="Переместить экземпляр"
                ></v-btn>
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
          <p><strong>Книга:</strong> {{ selectedBook.title }}</p>
          <p><strong>Текущий шифр:</strong> {{ selectedBook.inventory_code }}</p>
          <v-text-field v-model="newCode" label="Новый шифр" :rules="[v => !!v]" class="mt-4"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" variant="text" @click="codeDialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="updateBookCode" :loading="updating">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог перемещения экземпляра -->
    <v-dialog v-model="transferDialog" max-width="500px">
      <v-card v-if="selectedCopy">
        <v-card-title>🔄 Перемещение экземпляра</v-card-title>
        <v-card-text>
          <p><strong>Книга:</strong> {{ selectedCopy.book_id?.title }}</p>
          <p><strong>Экземпляр ID:</strong> {{ selectedCopy.copy_book_id }}</p>
          <p><strong>Текущий зал:</strong> {{ selectedCopy.hall_id?.name }}</p>
          <v-select v-model="newHallId" :items="halls" item-title="name" item-value="hall_id" label="Новый зал" class="mt-4"></v-select>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" variant="text" @click="transferDialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="transferCopy" :loading="transferring">Переместить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '../../api/client'

// ===== DATA =====
const books = ref([])
const copies = ref([])
const halls = ref([])
const loading = ref(false)
const updating = ref(false)
const transferring = ref(false)

const codeDialog = ref(false)
const transferDialog = ref(false)
const selectedBook = ref(null)
const selectedCopy = ref(null)
const newCode = ref('')
const newHallId = ref(null)

// ===== HEADERS =====
const headers = [
  { title: 'Шифр', key: 'inventory_code' },
  { title: 'Название', key: 'title' },
  { title: 'Автор', key: 'author' },
  { title: 'Год', key: 'publication_year' },
  { title: 'Издательство', key: 'publisher' },
  { title: 'Раздел', key: 'section' },
  { title: 'Статус', key: 'is_in_catalog' },
  { title: 'Действия', key: 'actions', sortable: false }
]

// ===== METHODS =====
const loadBooks = async () => {
  loading.value = true
  try {
    const res = await apiClient.get('books/')
    books.value = res.data
  } catch (e) { console.error(e) } finally { loading.value = false }
}

const loadCopies = async () => {
  try {
    const res = await apiClient.get('copies/')
    copies.value = res.data
  } catch (e) { console.error(e) }
}

const loadHalls = async () => {
  try {
    const res = await apiClient.get('halls/')
    halls.value = res.data
  } catch (e) { console.error(e) }
}

const openEditDialog = (book) => {
  selectedBook.value = book
  newCode.value = book.inventory_code
  codeDialog.value = true
}

const openTransferDialog = (book) => {
  const copy = copies.value.find(c => c.book_id?.book_id === book.book_id)
  if (copy) {
    selectedCopy.value = copy
    newHallId.value = copy.hall_id
    transferDialog.value = true
  }
}

const updateBookCode = async () => {
  if (!newCode.value) return
  updating.value = true
  try {
    await apiClient.post(`books/${selectedBook.value.book_id}/update-code/`, { new_code: newCode.value })
    codeDialog.value = false
    await loadBooks()
  } catch (e) { console.error(e) } finally { updating.value = false }
}

const transferCopy = async () => {
  if (!newHallId.value) return
  transferring.value = true
  try {
    await apiClient.post('copies/transfer-hall/', {
      copy_id: selectedCopy.value.copy_book_id,
      hall_id: newHallId.value
    })
    transferDialog.value = false
    await loadCopies()
  } catch (e) { console.error(e) } finally { transferring.value = false }
}

onMounted(() => { loadBooks(); loadCopies(); loadHalls() })
</script>