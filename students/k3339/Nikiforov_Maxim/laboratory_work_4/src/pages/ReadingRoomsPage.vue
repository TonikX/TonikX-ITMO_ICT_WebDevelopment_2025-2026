<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { readingRoomsApi, type ReadingRoom } from '../shared/api/library'

const rooms = ref<ReadingRoom[]>([])
const loading = ref(true)
const error = ref('')
const dialog = ref(false)
const dialogDelete = ref(false)
const editing = ref<ReadingRoom | null>(null)
const deleting = ref<ReadingRoom | null>(null)
const form = ref({ number: '', name: '', capacity: 1 })
const formError = ref('')
const submitLoading = ref(false)

onMounted(load)

async function load() {
  loading.value = true
  error.value = ''
  try {
    const data = await readingRoomsApi.list()
    rooms.value = data.results ?? []
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Ошибка загрузки'
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editing.value = null
  form.value = { number: '', name: '', capacity: 1 }
  formError.value = ''
  dialog.value = true
}

function openEdit(room: ReadingRoom) {
  editing.value = room
  form.value = { number: room.number, name: room.name, capacity: room.capacity }
  formError.value = ''
  dialog.value = true
}

function openDelete(room: ReadingRoom) {
  deleting.value = room
  dialogDelete.value = true
}

async function submit() {
  formError.value = ''
  if (!form.value.number?.trim() || !form.value.name?.trim() || form.value.capacity < 1) {
    formError.value = 'Заполните номер, название и вместимость (≥1)'
    return
  }
  submitLoading.value = true
  try {
    if (editing.value) {
      await readingRoomsApi.update(editing.value.id, form.value)
    } else {
      await readingRoomsApi.create(form.value)
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
    await readingRoomsApi.delete(deleting.value.id)
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
    <h1 class="text-h4 mb-4">Читальные залы</h1>
    <v-btn color="primary" class="mb-4" @click="openCreate">Добавить зал</v-btn>
    <v-alert v-if="error" type="error">{{ error }}</v-alert>
    <v-progress-linear v-if="loading" indeterminate />
    <v-table v-else>
      <thead>
        <tr>
          <th>Номер</th>
          <th>Название</th>
          <th>Вместимость</th>
          <th>Читателей</th>
          <th>Книг</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in rooms" :key="r.id">
          <td>{{ r.number }}</td>
          <td>{{ r.name }}</td>
          <td>{{ r.capacity }}</td>
          <td>{{ r.readers_count ?? 0 }}</td>
          <td>{{ r.total_books_count ?? 0 }}</td>
          <td>
            <v-btn size="small" variant="text" @click="openEdit(r)">Изменить</v-btn>
            <v-btn size="small" variant="text" color="error" @click="openDelete(r)">Удалить</v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
    <p v-if="!loading && !error && rooms.length === 0" class="text-medium-emphasis">Нет залов</p>

    <v-dialog v-model="dialog" max-width="500" persistent>
      <v-card>
        <v-card-title>{{ editing ? 'Редактировать зал' : 'Добавить зал' }}</v-card-title>
        <v-card-text>
          <v-text-field v-model="form.number" label="Номер зала" required />
          <v-text-field v-model="form.name" label="Название" required />
          <v-text-field v-model.number="form.capacity" type="number" label="Вместимость" min="1" />
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
        <v-card-title>Удалить зал?</v-card-title>
        <v-card-text v-if="deleting">
          Зал «{{ deleting.name }}» ({{ deleting.number }}) будет удалён.
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
