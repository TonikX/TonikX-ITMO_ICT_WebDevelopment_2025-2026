<template>
  <div class="contracts-view">
    <v-row class="mb-4">
      <v-col cols="12" class="d-flex justify-space-between align-center flex-wrap">
        <h1 class="page-title">
          <v-icon class="mr-2">mdi-file-document-edit</v-icon>
          Контракты
        </h1>
        <v-btn color="primary" @click="openDialog()">
          <v-icon left>mdi-plus</v-icon>
          Создать контракт
        </v-btn>
      </v-col>
    </v-row>

    <v-card>
      <v-card-title class="d-flex flex-wrap gap-4">
        <v-text-field
          v-model="search"
          prepend-inner-icon="mdi-magnify"
          label="Поиск"
          single-line
          hide-details
          density="compact"
          style="max-width: 300px"
        ></v-text-field>

        <v-select
          v-model="statusFilter"
          :items="statusOptions"
          label="Статус"
          clearable
          hide-details
          density="compact"
          style="max-width: 200px"
        ></v-select>
      </v-card-title>

      <v-data-table
        :headers="headers"
        :items="filteredContracts"
        :search="search"
        :loading="loading"
        :items-per-page="10"
        class="elevation-0"
      >
        <template v-slot:item.status="{ item }">
          <v-chip :color="getStatusColor(item.status)" size="small" label>
            {{ getStatusLabel(item.status) }}
          </v-chip>
        </template>

        <template v-slot:item.total_budget="{ item }">
          {{ formatPrice(item.total_budget) }}
        </template>

        <template v-slot:item.advance_payment="{ item }">
          {{ formatPrice(item.advance_payment) }}
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn icon="mdi-pencil" size="small" variant="text" @click="openDialog(item)"></v-btn>
          <v-btn icon="mdi-delete" size="small" variant="text" color="error" @click="confirmDelete(item)"></v-btn>
        </template>

        <template v-slot:no-data>
          <div class="text-center pa-4">
            <v-icon size="48" color="grey">mdi-file-document-remove</v-icon>
            <p class="mt-2 text-medium-emphasis">Контракты не найдены</p>
          </div>
        </template>
      </v-data-table>
    </v-card>

    <!-- Create/Edit Dialog -->
    <v-dialog v-model="dialog" max-width="700" persistent>
      <v-card>
        <v-card-title class="d-flex align-center">
          <v-icon class="mr-2">{{ editingItem ? 'mdi-pencil' : 'mdi-plus' }}</v-icon>
          {{ editingItem ? 'Редактировать контракт' : 'Новый контракт' }}
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="formValid">
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.contract_number"
                  label="Номер контракта"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="formData.status"
                  :items="statusOptions"
                  label="Статус"
                  :rules="[rules.required]"
                ></v-select>
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="formData.book"
                  :items="availableBooks"
                  item-title="title"
                  item-value="id"
                  label="Книга"
                  :rules="[rules.required]"
                  :disabled="!!editingItem"
                ></v-select>
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="formData.manager"
                  :items="managers"
                  item-title="full_name"
                  item-value="id"
                  label="Менеджер"
                  :rules="[rules.required]"
                ></v-select>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.signed_date"
                  label="Дата подписания"
                  type="date"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.expiry_date"
                  label="Дата окончания"
                  type="date"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model.number="formData.total_budget"
                  label="Общий бюджет"
                  type="number"
                  step="0.01"
                  prefix="₽"
                  :rules="[rules.required, rules.positive]"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model.number="formData.advance_payment"
                  label="Аванс"
                  type="number"
                  step="0.01"
                  prefix="₽"
                  :rules="[rules.required, rules.positive]"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="formData.notes"
                  label="Примечания"
                  rows="2"
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
          Вы уверены, что хотите удалить контракт 
          <strong>{{ itemToDelete?.contract_number }}</strong>?
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
import { ref, reactive, computed, onMounted, inject } from 'vue'
import { contractsApi, booksApi, employeesApi } from '@/services/api'

const showSnackbar = inject('showSnackbar')

const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)
const contracts = ref([])
const books = ref([])
const managers = ref([])
const search = ref('')
const statusFilter = ref(null)

const dialog = ref(false)
const deleteDialog = ref(false)
const form = ref(null)
const formValid = ref(false)
const editingItem = ref(null)
const itemToDelete = ref(null)

const headers = [
  { title: 'ID', key: 'id', width: '80px' },
  { title: '№ Контракта', key: 'contract_number', width: '150px' },
  { title: 'Книга', key: 'book_title' },
  { title: 'Менеджер', key: 'manager_name' },
  { title: 'Статус', key: 'status', width: '130px' },
  { title: 'Бюджет', key: 'total_budget', width: '130px' },
  { title: 'Аванс', key: 'advance_payment', width: '130px' },
  { title: 'Подписан', key: 'signed_date', width: '120px' },
  { title: 'Действия', key: 'actions', sortable: false, width: '120px' }
]

const statusOptions = [
  { title: 'Черновик', value: 'DRAFT' },
  { title: 'Активный', value: 'ACTIVE' },
  { title: 'Завершён', value: 'COMPLETED' },
  { title: 'Расторгнут', value: 'TERMINATED' }
]

const formData = reactive({
  contract_number: '',
  book: null,
  manager: null,
  signed_date: '',
  status: 'DRAFT',
  advance_payment: null,
  total_budget: null,
  expiry_date: '',
  notes: ''
})

const rules = {
  required: (v) => !!v || v === 0 || 'Обязательное поле',
  positive: (v) => v >= 0 || 'Не может быть отрицательным'
}

const filteredContracts = computed(() => {
  if (!statusFilter.value) return contracts.value
  return contracts.value.filter(c => c.status === statusFilter.value)
})

const availableBooks = computed(() => {
  if (editingItem.value) {
    return books.value.filter(b => b.id === editingItem.value.book || !b.contract)
  }
  return books.value.filter(b => !b.contract)
})

const getStatusColor = (status) => {
  const colors = { DRAFT: 'grey', ACTIVE: 'success', COMPLETED: 'info', TERMINATED: 'error' }
  return colors[status] || 'grey'
}

const getStatusLabel = (status) => {
  const labels = { DRAFT: 'Черновик', ACTIVE: 'Активный', COMPLETED: 'Завершён', TERMINATED: 'Расторгнут' }
  return labels[status] || status
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(price)
}

const fetchContracts = async () => {
  loading.value = true
  try {
    const response = await contractsApi.getAll()
    contracts.value = response.data.results || response.data
  } catch (error) {
    showSnackbar('Ошибка загрузки контрактов', 'error')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const fetchBooks = async () => {
  try {
    const response = await booksApi.getAll()
    books.value = response.data.results || response.data
  } catch (error) {
    console.error(error)
  }
}

const fetchManagers = async () => {
  try {
    const response = await employeesApi.getAll({ role: 'MANAGER' })
    managers.value = response.data.results || response.data
  } catch (error) {
    console.error(error)
  }
}

const openDialog = (item = null) => {
  editingItem.value = item
  if (item) {
    Object.assign(formData, {
      contract_number: item.contract_number,
      book: item.book,
      manager: item.manager,
      signed_date: item.signed_date,
      status: item.status,
      advance_payment: item.advance_payment,
      total_budget: item.total_budget,
      expiry_date: item.expiry_date || '',
      notes: item.notes || ''
    })
  } else {
    Object.assign(formData, {
      contract_number: '',
      book: null,
      manager: null,
      signed_date: new Date().toISOString().split('T')[0],
      status: 'DRAFT',
      advance_payment: null,
      total_budget: null,
      expiry_date: '',
      notes: ''
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
    if (!data.expiry_date) delete data.expiry_date

    if (editingItem.value) {
      await contractsApi.update(editingItem.value.id, data)
      showSnackbar('Контракт обновлён', 'success')
    } else {
      await contractsApi.create(data)
      showSnackbar('Контракт создан', 'success')
    }
    closeDialog()
    fetchContracts()
    fetchBooks()
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
    await contractsApi.delete(itemToDelete.value.id)
    showSnackbar('Контракт удалён', 'success')
    deleteDialog.value = false
    fetchContracts()
    fetchBooks()
  } catch (error) {
    showSnackbar('Ошибка удаления', 'error')
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  fetchContracts()
  fetchBooks()
  fetchManagers()
})
</script>

<style scoped>
.contracts-view {
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

