<template>
  <div class="customers-view">
    <v-row class="mb-4">
      <v-col cols="12" class="d-flex justify-space-between align-center flex-wrap">
        <h1 class="page-title">
          <v-icon class="mr-2">mdi-account-tie</v-icon>
          Заказчики
        </h1>
        <v-btn color="primary" @click="openDialog()">
          <v-icon left>mdi-plus</v-icon>
          Добавить заказчика
        </v-btn>
      </v-col>
    </v-row>

    <v-card>
      <v-card-title>
        <v-text-field
          v-model="search"
          prepend-inner-icon="mdi-magnify"
          label="Поиск"
          single-line
          hide-details
          density="compact"
          style="max-width: 300px"
        ></v-text-field>
      </v-card-title>

      <v-data-table
        :headers="headers"
        :items="customers"
        :search="search"
        :loading="loading"
        :items-per-page="10"
        class="elevation-0"
      >
        <template v-slot:item.orders_count="{ item }">
          <v-chip size="small" color="primary" variant="tonal">
            {{ item.orders_count }} заказов
          </v-chip>
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn icon="mdi-pencil" size="small" variant="text" @click="openDialog(item)"></v-btn>
          <v-btn icon="mdi-delete" size="small" variant="text" color="error" @click="confirmDelete(item)"></v-btn>
        </template>

        <template v-slot:no-data>
          <div class="text-center pa-4">
            <v-icon size="48" color="grey">mdi-account-off</v-icon>
            <p class="mt-2 text-medium-emphasis">Заказчики не найдены</p>
          </div>
        </template>
      </v-data-table>
    </v-card>

    <!-- Create/Edit Dialog -->
    <v-dialog v-model="dialog" max-width="600" persistent>
      <v-card>
        <v-card-title class="d-flex align-center">
          <v-icon class="mr-2">{{ editingItem ? 'mdi-pencil' : 'mdi-plus' }}</v-icon>
          {{ editingItem ? 'Редактировать заказчика' : 'Новый заказчик' }}
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="formValid">
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.name"
                  label="Имя"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.company_name"
                  label="Компания"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.email"
                  label="Email"
                  type="email"
                  :rules="[rules.required, rules.email]"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.phone"
                  label="Телефон"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="formData.address"
                  label="Адрес"
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
          Вы уверены, что хотите удалить заказчика 
          <strong>{{ itemToDelete?.name }}</strong>?
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
import { ref, reactive, onMounted, inject } from 'vue'
import { customersApi } from '@/services/api'

const showSnackbar = inject('showSnackbar')

const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)
const customers = ref([])
const search = ref('')

const dialog = ref(false)
const deleteDialog = ref(false)
const form = ref(null)
const formValid = ref(false)
const editingItem = ref(null)
const itemToDelete = ref(null)

const headers = [
  { title: 'ID', key: 'id', width: '80px' },
  { title: 'Имя', key: 'name' },
  { title: 'Компания', key: 'company_name' },
  { title: 'Email', key: 'email' },
  { title: 'Телефон', key: 'phone' },
  { title: 'Заказы', key: 'orders_count', width: '120px' },
  { title: 'Действия', key: 'actions', sortable: false, width: '120px' }
]

const formData = reactive({
  name: '',
  company_name: '',
  email: '',
  phone: '',
  address: ''
})

const rules = {
  required: (v) => !!v || 'Обязательное поле',
  email: (v) => /.+@.+\..+/.test(v) || 'Введите корректный email'
}

const fetchCustomers = async () => {
  loading.value = true
  try {
    const response = await customersApi.getAll()
    customers.value = response.data.results || response.data
  } catch (error) {
    showSnackbar('Ошибка загрузки данных', 'error')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const openDialog = (item = null) => {
  editingItem.value = item
  if (item) {
    Object.assign(formData, {
      name: item.name,
      company_name: item.company_name || '',
      email: item.email,
      phone: item.phone,
      address: item.address || ''
    })
  } else {
    Object.assign(formData, {
      name: '',
      company_name: '',
      email: '',
      phone: '',
      address: ''
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
    if (editingItem.value) {
      await customersApi.update(editingItem.value.id, formData)
      showSnackbar('Заказчик обновлён', 'success')
    } else {
      await customersApi.create(formData)
      showSnackbar('Заказчик создан', 'success')
    }
    closeDialog()
    fetchCustomers()
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
    await customersApi.delete(itemToDelete.value.id)
    showSnackbar('Заказчик удалён', 'success')
    deleteDialog.value = false
    fetchCustomers()
  } catch (error) {
    showSnackbar('Ошибка удаления', 'error')
  } finally {
    deleting.value = false
  }
}

onMounted(fetchCustomers)
</script>

<style scoped>
.customers-view {
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

