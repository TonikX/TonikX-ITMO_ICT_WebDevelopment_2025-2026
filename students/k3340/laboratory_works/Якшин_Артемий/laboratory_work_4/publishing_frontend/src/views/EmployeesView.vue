<template>
  <div class="employees-view">
    <v-row class="mb-4">
      <v-col cols="12" class="d-flex justify-space-between align-center flex-wrap">
        <h1 class="page-title">
          <v-icon class="mr-2">mdi-account-group</v-icon>
          Сотрудники
        </h1>
        <v-btn color="primary" @click="openDialog()">
          <v-icon left>mdi-plus</v-icon>
          Добавить сотрудника
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
          v-model="roleFilter"
          :items="roleOptions"
          label="Роль"
          clearable
          hide-details
          density="compact"
          style="max-width: 200px"
        ></v-select>
      </v-card-title>

      <v-data-table
        :headers="headers"
        :items="employees"
        :search="search"
        :loading="loading"
        :items-per-page="10"
        class="elevation-0"
      >
        <template v-slot:item.role="{ item }">
          <v-chip :color="getRoleColor(item.role)" size="small" label>
            {{ getRoleLabel(item.role) }}
          </v-chip>
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn icon="mdi-pencil" size="small" variant="text" @click="openDialog(item)"></v-btn>
          <v-btn icon="mdi-delete" size="small" variant="text" color="error" @click="confirmDelete(item)"></v-btn>
        </template>

        <template v-slot:no-data>
          <div class="text-center pa-4">
            <v-icon size="48" color="grey">mdi-account-off</v-icon>
            <p class="mt-2 text-medium-emphasis">Сотрудники не найдены</p>
          </div>
        </template>
      </v-data-table>
    </v-card>

    <!-- Create/Edit Dialog -->
    <v-dialog v-model="dialog" max-width="600" persistent>
      <v-card>
        <v-card-title class="d-flex align-center">
          <v-icon class="mr-2">{{ editingItem ? 'mdi-pencil' : 'mdi-plus' }}</v-icon>
          {{ editingItem ? 'Редактировать сотрудника' : 'Новый сотрудник' }}
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="formValid">
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.last_name"
                  label="Фамилия"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.first_name"
                  label="Имя"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.middle_name"
                  label="Отчество"
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
                <v-select
                  v-model="formData.role"
                  :items="roleOptions"
                  label="Роль"
                  :rules="[rules.required]"
                ></v-select>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.position_title"
                  label="Должность"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.hire_date"
                  label="Дата приёма"
                  type="date"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.phone"
                  label="Телефон"
                ></v-text-field>
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
          Вы уверены, что хотите удалить сотрудника 
          <strong>{{ itemToDelete?.full_name }}</strong>?
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
import { ref, reactive, onMounted, inject, watch } from 'vue'
import { employeesApi } from '@/services/api'

const showSnackbar = inject('showSnackbar')

const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)
const employees = ref([])
const search = ref('')
const roleFilter = ref(null)

const dialog = ref(false)
const deleteDialog = ref(false)
const form = ref(null)
const formValid = ref(false)
const editingItem = ref(null)
const itemToDelete = ref(null)

const headers = [
  { title: 'ID', key: 'id', width: '80px' },
  { title: 'ФИО', key: 'full_name' },
  { title: 'Email', key: 'email' },
  { title: 'Роль', key: 'role', width: '150px' },
  { title: 'Должность', key: 'position_title' },
  { title: 'Дата приёма', key: 'hire_date', width: '130px' },
  { title: 'Действия', key: 'actions', sortable: false, width: '120px' }
]

const roleOptions = [
  { title: 'Менеджер', value: 'MANAGER' },
  { title: 'Редактор', value: 'EDITOR' },
  { title: 'Другое', value: 'OTHER' }
]

const formData = reactive({
  first_name: '',
  last_name: '',
  middle_name: '',
  email: '',
  role: 'OTHER',
  position_title: '',
  hire_date: '',
  phone: ''
})

const rules = {
  required: (v) => !!v || 'Обязательное поле',
  email: (v) => /.+@.+\..+/.test(v) || 'Введите корректный email'
}

const getRoleColor = (role) => {
  const colors = {
    MANAGER: 'primary',
    EDITOR: 'secondary',
    OTHER: 'grey'
  }
  return colors[role] || 'grey'
}

const getRoleLabel = (role) => {
  const labels = {
    MANAGER: 'Менеджер',
    EDITOR: 'Редактор',
    OTHER: 'Другое'
  }
  return labels[role] || role
}

const fetchEmployees = async () => {
  loading.value = true
  try {
    const params = roleFilter.value ? { role: roleFilter.value } : {}
    const response = await employeesApi.getAll(params)
    employees.value = response.data.results || response.data
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
      first_name: item.first_name,
      last_name: item.last_name,
      middle_name: item.middle_name || '',
      email: item.email,
      role: item.role,
      position_title: item.position_title,
      hire_date: item.hire_date,
      phone: item.phone || ''
    })
  } else {
    Object.assign(formData, {
      first_name: '',
      last_name: '',
      middle_name: '',
      email: '',
      role: 'OTHER',
      position_title: '',
      hire_date: new Date().toISOString().split('T')[0],
      phone: ''
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
      await employeesApi.update(editingItem.value.id, formData)
      showSnackbar('Сотрудник обновлён', 'success')
    } else {
      await employeesApi.create(formData)
      showSnackbar('Сотрудник создан', 'success')
    }
    closeDialog()
    fetchEmployees()
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
    await employeesApi.delete(itemToDelete.value.id)
    showSnackbar('Сотрудник удалён', 'success')
    deleteDialog.value = false
    fetchEmployees()
  } catch (error) {
    showSnackbar('Ошибка удаления', 'error')
  } finally {
    deleting.value = false
  }
}

watch(roleFilter, fetchEmployees)

onMounted(fetchEmployees)
</script>

<style scoped>
.employees-view {
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

