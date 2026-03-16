<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { bookAssignmentsApi, booksApi, readersApi, type BookAssignment, type Book, type Reader } from '../shared/api/library'

const assignments = ref<BookAssignment[]>([])
const books = ref<Book[]>([])
const readers = ref<Reader[]>([])
const loading = ref(true)
const error = ref('')
const filterReturned = ref<string>('false')
const dialog = ref(false)
const form = ref({ bookId: 0, readerId: 0 })
const formError = ref('')
const submitLoading = ref(false)

onMounted(async () => {
  await load()
  try {
    const [booksData, readersData] = await Promise.all([
      booksApi.list({ is_active: 'true' }),
      readersApi.list({ is_active: 'true' }),
    ])
    books.value = booksData.results ?? []
    readers.value = readersData.results ?? []
  } catch {
    // ignore
  }
})

async function load() {
  loading.value = true
  error.value = ''
  try {
    const data = await bookAssignmentsApi.list({ is_returned: filterReturned.value })
    assignments.value = data.results ?? []
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Ошибка загрузки'
  } finally {
    loading.value = false
  }
}

function openCreate() {
  form.value = {
    bookId: books.value[0]?.id ?? 0,
    readerId: readers.value[0]?.id ?? 0,
  }
  formError.value = ''
  dialog.value = true
}

async function submit() {
  formError.value = ''
  if (!form.value.bookId || !form.value.readerId) {
    formError.value = 'Выберите книгу и читателя'
    return
  }
  submitLoading.value = true
  try {
    await bookAssignmentsApi.create({ book: form.value.bookId, reader: form.value.readerId })
    dialog.value = false
    await load()
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e)
    formError.value = typeof msg === 'string' ? msg : JSON.stringify(msg)
  } finally {
    submitLoading.value = false
  }
}

async function returnBook(id: number) {
  try {
    await bookAssignmentsApi.returnBook(id)
    await load()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Ошибка возврата'
  }
}
</script>

<template>
  <div>
    <h1 class="text-h4 mb-4">Закрепления книг</h1>
    <v-btn color="primary" class="mb-4" @click="openCreate">Выдать книгу</v-btn>
    <v-select
      v-model="filterReturned"
      :items="[
        { title: 'На руках', value: 'false' },
        { title: 'Возвращённые', value: 'true' },
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
          <th>Книга</th>
          <th>Читатель</th>
          <th>Билет</th>
          <th>Дата выдачи</th>
          <th>Дней</th>
          <th>Действие</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="a in assignments" :key="a.id">
          <td>{{ a.book_title }}</td>
          <td>{{ a.reader_name }}</td>
          <td>{{ a.reader_ticket }}</td>
          <td>{{ a.assignment_date }}</td>
          <td>{{ a.is_returned ? '—' : (a.days_since_assignment ?? '—') }}</td>
          <td>
            <v-btn
              v-if="!a.is_returned"
              size="small"
              variant="tonal"
              @click="returnBook(a.id)"
            >
              Вернуть
            </v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
    <p v-if="!loading && !error && assignments.length === 0" class="text-medium-emphasis">Нет закреплений</p>

    <v-dialog v-model="dialog" max-width="500" persistent>
      <v-card>
        <v-card-title>Выдать книгу читателю</v-card-title>
        <v-card-text>
          <v-select
            v-model="form.bookId"
            :items="books.map((b) => ({ title: `${b.code} — ${b.title}`, value: b.id }))"
            label="Книга"
          />
          <v-select
            v-model="form.readerId"
            :items="readers.map((r) => ({ title: `${r.ticket_number} — ${r.full_name}`, value: r.id }))"
            label="Читатель"
          />
          <v-alert v-if="formError" type="error" density="compact" class="mt-2">{{ formError }}</v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="dialog = false">Отмена</v-btn>
          <v-btn color="primary" :loading="submitLoading" @click="submit">Выдать</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
