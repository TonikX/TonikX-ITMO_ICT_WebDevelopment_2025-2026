<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { booksApi, bookCopiesApi, readingRoomsApi, type Book, type BookCopy, type ReadingRoom } from '../shared/api/library'

const books = ref<Book[]>([])
const rooms = ref<ReadingRoom[]>([])
const loading = ref(true)
const error = ref('')
const filterActive = ref<string>('true')
const dialog = ref(false)
const dialogDelete = ref(false)
const dialogCopies = ref(false)
const editing = ref<Book | null>(null)
const deleting = ref<Book | null>(null)
const form = ref({
  title: '',
  authors: '',
  publisher: '',
  publication_year: new Date().getFullYear(),
  section: '',
  code: '',
})
const formError = ref('')
const submitLoading = ref(false)

const copyForm = ref({ bookId: 0, bookTitle: '', roomId: 0, quantity: 1 })
const copyFormError = ref('')
const copySubmitLoading = ref(false)

onMounted(async () => {
  await load()
  try {
    const data = await readingRoomsApi.list()
    rooms.value = data.results ?? []
  } catch {
    // ignore
  }
})

async function load() {
  loading.value = true
  error.value = ''
  try {
    const data = await booksApi.list({ is_active: filterActive.value })
    books.value = data.results ?? []
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Ошибка загрузки'
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editing.value = null
  form.value = {
    title: '',
    authors: '',
    publisher: '',
    publication_year: new Date().getFullYear(),
    section: '',
    code: '',
  }
  formError.value = ''
  dialog.value = true
}

function openEdit(b: Book) {
  editing.value = b
  form.value = {
    title: b.title,
    authors: b.authors,
    publisher: b.publisher,
    publication_year: b.publication_year,
    section: b.section,
    code: b.code,
  }
  formError.value = ''
  dialog.value = true
}

function openDelete(b: Book) {
  deleting.value = b
  dialogDelete.value = true
}

function openAddCopies(b: Book) {
  copyForm.value = { bookId: b.id, bookTitle: b.title, roomId: rooms.value[0]?.id ?? 0, quantity: 1 }
  copyFormError.value = ''
  dialogCopies.value = true
}

async function submit() {
  formError.value = ''
  if (!form.value.title?.trim() || !form.value.code?.trim()) {
    formError.value = 'Заполните название и шифр книги'
    return
  }
  submitLoading.value = true
  try {
    if (editing.value) {
      await booksApi.update(editing.value.id, form.value)
    } else {
      await booksApi.create(form.value)
    }
    dialog.value = false
    await load()
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e)
    formError.value = typeof msg === 'string' ? msg : JSON.stringify(msg)
  } finally {
    submitLoading.value = false
  }
}

async function submitCopies() {
  copyFormError.value = ''
  if (!copyForm.value.roomId || copyForm.value.quantity < 1) {
    copyFormError.value = 'Выберите зал и укажите количество (≥1)'
    return
  }
  copySubmitLoading.value = true
  try {
    const list = await bookCopiesApi.list({})
    const results: BookCopy[] = list.results ?? []
    const existing = results.find(
      (c) => c.book === copyForm.value.bookId && c.reading_room === copyForm.value.roomId
    )
    if (existing) {
      await bookCopiesApi.update(existing.id, { quantity: existing.quantity + copyForm.value.quantity })
    } else {
      await bookCopiesApi.create({
        book: copyForm.value.bookId,
        reading_room: copyForm.value.roomId,
        quantity: copyForm.value.quantity,
      })
    }
    dialogCopies.value = false
    await load()
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e)
    copyFormError.value = typeof msg === 'string' ? msg : JSON.stringify(msg)
  } finally {
    copySubmitLoading.value = false
  }
}

async function confirmDelete() {
  if (!deleting.value) return
  try {
    await booksApi.delete(deleting.value.id)
    dialogDelete.value = false
    deleting.value = null
    await load()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Ошибка удаления'
  }
}
</script>

<template>
  <div>
    <h1 class="text-h4 mb-4">Книги</h1>
    <v-btn color="primary" class="mb-4" @click="openCreate">Добавить книгу</v-btn>
    <v-select
      v-model="filterActive"
      :items="[
        { title: 'В фонде', value: 'true' },
        { title: 'Списаны', value: 'false' },
        { title: 'Все', value: '' },
      ]"
      label="Фильтр"
      density="compact"
      class="mb-4 ml-4"
      style="max-width: 200px; display: inline-block"
      @update:model-value="load"
    />
    <v-alert v-if="error" type="error">{{ error }}</v-alert>
    <v-progress-linear v-if="loading" indeterminate />
    <v-table v-else>
      <thead>
        <tr>
          <th>Шифр</th>
          <th>Название</th>
          <th>Автор(ы)</th>
          <th>Раздел</th>
          <th>Экз.</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="b in books" :key="b.id">
          <td>{{ b.code }}</td>
          <td>{{ b.title }}</td>
          <td>{{ b.authors }}</td>
          <td>{{ b.section }}</td>
          <td>{{ b.total_copies ?? 0 }}</td>
          <td>
            <v-btn v-if="b.is_active" size="small" variant="text" @click="openEdit(b)">Изменить</v-btn>
            <v-btn v-if="b.is_active" size="small" variant="text" @click="openAddCopies(b)">Добавить в зал</v-btn>
            <v-btn v-if="b.is_active" size="small" variant="text" color="error" @click="openDelete(b)">Списать</v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
    <p v-if="!loading && !error && books.length === 0" class="text-medium-emphasis">Нет книг</p>

    <v-dialog v-model="dialog" max-width="600" persistent>
      <v-card>
        <v-card-title>{{ editing ? 'Редактировать книгу' : 'Добавить книгу' }}</v-card-title>
        <v-card-text>
          <v-text-field v-model="form.title" label="Название" required />
          <v-text-field v-model="form.authors" label="Автор(ы)" />
          <v-text-field v-model="form.publisher" label="Издательство" />
          <v-text-field v-model.number="form.publication_year" type="number" label="Год издания" />
          <v-text-field v-model="form.section" label="Раздел" />
          <v-text-field v-model="form.code" label="Шифр книги" required />
          <v-alert v-if="formError" type="error" density="compact" class="mt-2">{{ formError }}</v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="dialog = false">Отмена</v-btn>
          <v-btn color="primary" :loading="submitLoading" @click="submit">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="dialogDelete" max-width="400" persistent>
      <v-card>
        <v-card-title>Списать книгу?</v-card-title>
        <v-card-text v-if="deleting">
          Книга «{{ deleting.title }}» будет списана из фонда.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="dialogDelete = false; deleting = null">Отмена</v-btn>
          <v-btn color="error" @click="confirmDelete">Списать</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="dialogCopies" max-width="400" persistent>
      <v-card>
        <v-card-title>Добавить экземпляры в зал</v-card-title>
        <v-card-text>
          <p class="text-body2 mb-2">{{ copyForm.bookTitle }}</p>
          <v-select
            v-model="copyForm.roomId"
            :items="rooms.map((r) => ({ title: r.name, value: r.id }))"
            label="Читальный зал"
          />
          <v-text-field v-model.number="copyForm.quantity" type="number" label="Количество" min="1" />
          <v-alert v-if="copyFormError" type="error" density="compact" class="mt-2">{{ copyFormError }}</v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="dialogCopies = false">Отмена</v-btn>
          <v-btn color="primary" :loading="copySubmitLoading" @click="submitCopies">Добавить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
