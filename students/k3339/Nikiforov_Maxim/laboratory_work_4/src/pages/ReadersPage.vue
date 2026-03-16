<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { readersApi, readingRoomsApi, type Reader, type ReadingRoom } from '../shared/api/library'

const readers = ref<Reader[]>([])
const rooms = ref<ReadingRoom[]>([])
const loading = ref(true)
const error = ref('')
const filterActive = ref<string>('true')
const dialog = ref(false)
const dialogDelete = ref(false)
const editing = ref<Reader | null>(null)
const deleting = ref<Reader | null>(null)
const form = ref({
  ticket_number: '',
  full_name: '',
  passport_number: '',
  birth_date: '',
  address: '',
  phone_number: '',
  education: 'secondary' as string,
  has_degree: false,
  reading_room: null as number | null,
})
const formError = ref('')
const submitLoading = ref(false)

const educationItems = [
  { title: 'Начальное', value: 'primary' },
  { title: 'Среднее', value: 'secondary' },
  { title: 'Высшее', value: 'higher' },
  { title: 'Учёная степень', value: 'degree' },
]

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
    const data = await readersApi.list({ is_active: filterActive.value })
    readers.value = data.results ?? []
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Ошибка загрузки'
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editing.value = null
  form.value = {
    ticket_number: '',
    full_name: '',
    passport_number: '',
    birth_date: '',
    address: '',
    phone_number: '',
    education: 'secondary',
    has_degree: false,
    reading_room: null,
  }
  formError.value = ''
  dialog.value = true
}

function openEdit(r: Reader) {
  editing.value = r
  form.value = {
    ticket_number: r.ticket_number,
    full_name: r.full_name,
    passport_number: r.passport_number,
    birth_date: r.birth_date,
    address: r.address,
    phone_number: r.phone_number,
    education: r.education,
    has_degree: r.has_degree,
    reading_room: r.reading_room,
  }
  formError.value = ''
  dialog.value = true
}

function openDelete(r: Reader) {
  deleting.value = r
  dialogDelete.value = true
}

async function submit() {
  formError.value = ''
  if (!form.value.ticket_number?.trim() || !form.value.full_name?.trim() || !form.value.birth_date) {
    formError.value = 'Заполните номер билета, ФИО и дату рождения'
    return
  }
  submitLoading.value = true
  try {
    const body = { ...form.value, reading_room: form.value.reading_room || null }
    if (editing.value) {
      await readersApi.update(editing.value.id, body)
    } else {
      await readersApi.create(body)
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

async function confirmDelete() {
  if (!deleting.value) return
  try {
    await readersApi.delete(deleting.value.id)
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
    <h1 class="text-h4 mb-4">Читатели</h1>
    <v-btn color="primary" class="mb-4" @click="openCreate">Добавить читателя</v-btn>
    <v-select
      v-model="filterActive"
      :items="[
        { title: 'Активные', value: 'true' },
        { title: 'Неактивные', value: 'false' },
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
          <th>Билет</th>
          <th>ФИО</th>
          <th>Телефон</th>
          <th>Зал</th>
          <th>Книг на руках</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in readers" :key="r.id">
          <td>{{ r.ticket_number }}</td>
          <td>{{ r.full_name }}</td>
          <td>{{ r.phone_number }}</td>
          <td>{{ r.reading_room_name ?? '—' }}</td>
          <td>{{ r.active_books_count ?? 0 }}</td>
          <td>
            <v-btn size="small" variant="text" @click="openEdit(r)">Изменить</v-btn>
            <v-btn size="small" variant="text" color="error" @click="openDelete(r)">Удалить</v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
    <p v-if="!loading && !error && readers.length === 0" class="text-medium-emphasis">Нет читателей</p>

    <v-dialog v-model="dialog" max-width="600" persistent scrollable>
      <v-card>
        <v-card-title>{{ editing ? 'Редактировать читателя' : 'Добавить читателя' }}</v-card-title>
        <v-card-text>
          <v-text-field v-model="form.ticket_number" label="Номер читательского билета" />
          <v-text-field v-model="form.full_name" label="ФИО" />
          <v-text-field v-model="form.passport_number" label="Номер паспорта" />
          <v-text-field v-model="form.birth_date" label="Дата рождения" type="date" />
          <v-text-field v-model="form.address" label="Адрес" />
          <v-text-field v-model="form.phone_number" label="Телефон" />
          <v-select
            v-model="form.education"
            :items="educationItems"
            label="Образование"
          />
          <v-checkbox v-model="form.has_degree" label="Наличие учёной степени" hide-details />
          <v-select
            v-model="form.reading_room"
            :items="rooms.map((room) => ({ title: room.name, value: room.id }))"
            label="Читальный зал"
            clearable
          />
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
        <v-card-title>Удалить читателя?</v-card-title>
        <v-card-text v-if="deleting">
          {{ deleting.full_name }} (билет {{ deleting.ticket_number }}) будет удалён.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="dialogDelete = false; deleting = null">Отмена</v-btn>
          <v-btn color="error" @click="confirmDelete">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
