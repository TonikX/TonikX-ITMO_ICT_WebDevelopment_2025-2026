<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>Сотрудники</span>
            <v-btn color="primary" @click="openDialog(null)">Добавить</v-btn>
          </v-card-title>
          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="items"
              :loading="loading"
              item-key="id"
            >
              <template v-slot:item.employed="{ item }">
                <v-chip :color="item.employed ? 'success' : 'error'">
                  {{ item.employed ? 'Работает' : 'Уволен' }}
                </v-chip>
              </template>
              <template v-slot:item.actions="{ item }">
                <v-btn icon="mdi-pencil" size="small" @click="openDialog(item)" class="mr-2"></v-btn>
                <v-btn icon="mdi-delete" size="small" color="error" @click="deleteItem(item)"></v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title>{{ editingItem ? 'Редактировать' : 'Добавить' }} сотрудника</v-card-title>
        <v-card-text>
          <v-form ref="formRef" v-model="valid" lazy-validation>
            <v-text-field
              v-model="form.last_name"
              label="Фамилия"
              :rules="[v => !!v || 'Обязательное поле']"
              variant="outlined"
            />
            <v-text-field
              v-model="form.first_name"
              label="Имя"
              :rules="[v => !!v || 'Обязательное поле']"
              variant="outlined"
            />
            <v-text-field
              v-model="form.middle_name"
              label="Отчество"
              variant="outlined"
            />
            <v-checkbox
              v-model="form.employed"
              label="Работает"
            />
          </v-form>
          <v-alert v-if="error" type="error" class="mt-3">{{ error }}</v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="dialog = false">Отмена</v-btn>
          <v-btn color="primary" :disabled="!valid || saving" @click="saveItem">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { hotelAPI } from '../services/api'

const items = ref([])
const loading = ref(false)
const dialog = ref(false)
const valid = ref(false)
const saving = ref(false)
const error = ref('')
const editingItem = ref(null)

const form = ref({
  last_name: '',
  first_name: '',
  middle_name: '',
  employed: true,
})

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Фамилия', key: 'last_name' },
  { title: 'Имя', key: 'first_name' },
  { title: 'Отчество', key: 'middle_name' },
  { title: 'Статус', key: 'employed' },
  { title: 'Действия', key: 'actions', sortable: false },
]

const loadData = async () => {
  loading.value = true
  try {
    const response = await hotelAPI.employees.list()
    items.value = response.data
  } catch (err) {
    error.value = 'Ошибка при загрузке данных'
  } finally {
    loading.value = false
  }
}

const openDialog = (item) => {
  editingItem.value = item
  if (item) {
    form.value = { ...item }
  } else {
    form.value = {
      last_name: '',
      first_name: '',
      middle_name: '',
      employed: true,
    }
  }
  error.value = ''
  dialog.value = true
}

const formRef = ref(null)

const saveItem = async () => {
  error.value = ''
  
  if (!valid.value) {
    return
  }

  saving.value = true
  try {
    if (editingItem.value) {
      await hotelAPI.employees.update(editingItem.value.id, form.value)
    } else {
      await hotelAPI.employees.create(form.value)
    }
    dialog.value = false
    await loadData()
  } catch (err) {
    if (err.response?.data) {
      const data = err.response.data
      if (typeof data === 'object') {
        error.value = Object.values(data).flat().join(', ')
      } else {
        error.value = data
      }
    } else {
      error.value = 'Ошибка при сохранении'
    }
  } finally {
    saving.value = false
  }
}

const deleteItem = async (item) => {
  if (!confirm(`Удалить сотрудника ${item.last_name} ${item.first_name}?`)) return
  try {
    await hotelAPI.employees.delete(item.id)
    await loadData()
  } catch (err) {
    error.value = 'Ошибка при удалении'
  }
}

onMounted(() => {
  loadData()
})
</script>

