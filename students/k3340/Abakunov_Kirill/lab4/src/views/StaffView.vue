<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4">
          <v-icon class="mr-2">mdi-account-hard-hat</v-icon>
          Служащие
        </h1>
      </v-col>
      <v-col cols="auto" v-if="authStore.isAuthenticated">
        <v-btn color="primary" @click="openHireDialog">
          <v-icon left>mdi-account-plus</v-icon>
          Принять на работу
        </v-btn>
      </v-col>
    </v-row>

    <!-- Фильтры -->
    <v-card class="mb-4 pa-4">
      <v-row align="center">
        <v-col cols="12" sm="6">
          <v-text-field
            v-model="search"
            label="Поиск"
            prepend-inner-icon="mdi-magnify"
            clearable
            hide-details
          ></v-text-field>
        </v-col>
        <v-col cols="12" sm="6">
          <v-btn-toggle v-model="staffFilter" mandatory color="primary">
            <v-btn value="all">Все</v-btn>
            <v-btn value="active">Работают</v-btn>
            <v-btn value="fired">Уволены</v-btn>
          </v-btn-toggle>
        </v-col>
      </v-row>
    </v-card>

    <v-progress-linear v-if="loading" indeterminate color="primary"></v-progress-linear>

    <!-- Таблица служащих -->
    <v-card>
      <v-data-table
        :headers="headers"
        :items="filteredStaff"
        :search="search"
        :loading="loading"
        class="elevation-1"
      >
        <template v-slot:item.full_name="{ item }">
          {{ item.full_name }}
        </template>

        <template v-slot:item.status="{ item }">
          <v-chip :color="item.is_active ? 'success' : 'grey'" size="small">
            {{ item.is_active ? 'Работает' : 'Уволен' }}
          </v-chip>
        </template>

        <template v-slot:item.actions="{ item }" v-if="authStore.isAuthenticated">
          <v-btn 
            v-if="item.is_active" 
            icon 
            size="small" 
            color="warning"
            @click="openFireDialog(item)"
          >
            <v-icon>mdi-account-off</v-icon>
            <v-tooltip activator="parent">Уволить</v-tooltip>
          </v-btn>
          <v-btn icon size="small" @click="editStaff(item)">
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-btn icon size="small" color="error" @click="confirmDelete(item)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>
      </v-data-table>
    </v-card>

    <!-- Диалог найма -->
    <v-dialog v-model="hireDialog" max-width="500">
      <v-card>
        <v-card-title>{{ isEditing ? 'Редактировать служащего' : 'Принять на работу' }}</v-card-title>
        <v-card-text>
          <v-form ref="hireFormRef">
            <v-text-field
              v-model="staffForm.last_name"
              label="Фамилия"
              :rules="[rules.required]"
            ></v-text-field>
            <v-text-field
              v-model="staffForm.first_name"
              label="Имя"
              :rules="[rules.required]"
            ></v-text-field>
            <v-text-field
              v-model="staffForm.middle_name"
              label="Отчество"
            ></v-text-field>
            <v-text-field
              v-model="staffForm.hire_date"
              label="Дата приема"
              type="date"
              :rules="[rules.required]"
            ></v-text-field>
            <v-text-field
              v-if="isEditing"
              v-model="staffForm.fire_date"
              label="Дата увольнения"
              type="date"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="hireDialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="saveStaff" :loading="saving">
            {{ isEditing ? 'Сохранить' : 'Принять' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог увольнения -->
    <v-dialog v-model="fireDialog" max-width="400">
      <v-card>
        <v-card-title>Увольнение служащего</v-card-title>
        <v-card-text>
          <p class="mb-4">Уволить {{ staffToFire?.full_name }}?</p>
          <v-text-field
            v-model="fireDate"
            label="Дата увольнения"
            type="date"
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="fireDialog = false">Отмена</v-btn>
          <v-btn color="warning" @click="fireStaff" :loading="saving">Уволить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог удаления -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>Подтверждение удаления</v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить запись о служащем {{ staffToDelete?.full_name }}?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="deleteDialog = false">Отмена</v-btn>
          <v-btn color="error" @click="deleteStaff" :loading="saving">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, inject } from 'vue'
import { staffAPI } from '@/api'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const showSnackbar = inject('showSnackbar')

const staff = ref([])
const loading = ref(false)
const saving = ref(false)
const search = ref('')
const staffFilter = ref('all')

const hireDialog = ref(false)
const fireDialog = ref(false)
const deleteDialog = ref(false)
const isEditing = ref(false)
const editingId = ref(null)
const staffToFire = ref(null)
const staffToDelete = ref(null)
const fireDate = ref('')
const hireFormRef = ref(null)

const headers = [
  { title: 'ФИО', key: 'full_name' },
  { title: 'Дата приема', key: 'hire_date' },
  { title: 'Дата увольнения', key: 'fire_date' },
  { title: 'Статус', key: 'status' },
  { title: 'Действия', key: 'actions', sortable: false },
]

const staffForm = reactive({
  last_name: '',
  first_name: '',
  middle_name: '',
  hire_date: '',
  fire_date: '',
})

const rules = {
  required: (v) => !!v || 'Обязательное поле',
}

const filteredStaff = computed(() => {
  let result = staff.value

  if (staffFilter.value === 'active') {
    result = result.filter(s => s.is_active)
  } else if (staffFilter.value === 'fired') {
    result = result.filter(s => !s.is_active)
  }

  return result
})

const loadStaff = async () => {
  loading.value = true
  try {
    const response = await staffAPI.getAll()
    staff.value = response.data.results || response.data
  } catch (error) {
    showSnackbar('Ошибка загрузки служащих', 'error')
  } finally {
    loading.value = false
  }
}

const openHireDialog = () => {
  isEditing.value = false
  editingId.value = null
  Object.assign(staffForm, {
    last_name: '',
    first_name: '',
    middle_name: '',
    hire_date: new Date().toISOString().split('T')[0],
    fire_date: '',
  })
  hireDialog.value = true
}

const editStaff = (staffMember) => {
  isEditing.value = true
  editingId.value = staffMember.id
  Object.assign(staffForm, {
    last_name: staffMember.last_name,
    first_name: staffMember.first_name,
    middle_name: staffMember.middle_name,
    hire_date: staffMember.hire_date,
    fire_date: staffMember.fire_date || '',
  })
  hireDialog.value = true
}

const saveStaff = async () => {
  const { valid } = await hireFormRef.value.validate()
  if (!valid) return

  saving.value = true
  try {
    const data = { ...staffForm }
    if (!data.fire_date) delete data.fire_date

    if (isEditing.value) {
      await staffAPI.update(editingId.value, data)
      showSnackbar('Данные служащего обновлены', 'success')
    } else {
      await staffAPI.hire(data)
      showSnackbar('Служащий принят на работу', 'success')
    }
    hireDialog.value = false
    loadStaff()
  } catch (error) {
    const errorMessage = error.response?.data?.error || error.response?.data?.detail || 'Ошибка сохранения'
    showSnackbar(errorMessage, 'error')
  } finally {
    saving.value = false
  }
}

const openFireDialog = (staffMember) => {
  staffToFire.value = staffMember
  fireDate.value = new Date().toISOString().split('T')[0]
  fireDialog.value = true
}

const fireStaff = async () => {
  saving.value = true
  try {
    await staffAPI.fire(staffToFire.value.id, { fire_date: fireDate.value })
    showSnackbar('Служащий уволен', 'success')
    fireDialog.value = false
    loadStaff()
  } catch (error) {
    showSnackbar('Ошибка увольнения', 'error')
  } finally {
    saving.value = false
  }
}

const confirmDelete = (staffMember) => {
  staffToDelete.value = staffMember
  deleteDialog.value = true
}

const deleteStaff = async () => {
  saving.value = true
  try {
    await staffAPI.delete(staffToDelete.value.id)
    showSnackbar('Запись удалена', 'success')
    deleteDialog.value = false
    loadStaff()
  } catch (error) {
    const errorMessage = error.response?.data?.error || error.response?.data?.detail || 'Ошибка удаления'
    showSnackbar(errorMessage, 'error')
  } finally {
    saving.value = false
  }
}

onMounted(loadStaff)
</script>
