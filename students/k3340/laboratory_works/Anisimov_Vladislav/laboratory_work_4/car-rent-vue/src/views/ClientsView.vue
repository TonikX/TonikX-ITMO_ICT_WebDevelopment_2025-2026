<!-- views/ClientsView.vue -->
<template>
  <v-container class="py-6">
    <v-row>
      <v-col cols="12">
        <v-breadcrumbs :items="breadcrumbs" class="px-0">
          <template v-slot:divider>
            <v-icon icon="mdi-chevron-right"></v-icon>
          </template>
        </v-breadcrumbs>
      </v-col>
    </v-row>

    <!-- Заголовок и статистика -->
    <v-row class="mb-6">
      <v-col cols="12" md="8" class="d-flex align-center">
        <v-icon icon="mdi-account-group" size="32" class="mr-3 text-primary"></v-icon>
        <div>
          <h1 class="text-h4 font-weight-bold">Клиенты</h1>
          <p class="text-subtitle-1 text-medium-emphasis">
            Управление клиентами
          </p>
        </div>
      </v-col>
      <v-col cols="12" md="4" class="text-right">
        <v-chip color="primary" variant="outlined" class="mr-2">
          <v-icon start icon="mdi-account"></v-icon>
          Всего клиентов: {{ clients.length }}
        </v-chip>

      </v-col>
    </v-row>

    <!-- Действия и фильтры -->
    <v-row class="mb-4">
      <v-col cols="12" md="4">
        <v-text-field
          v-model="search"
          label="Поиск клиента"
          prepend-inner-icon="mdi-magnify"
          variant="outlined"
          clearable
        ></v-text-field>
      </v-col>
      <v-spacer>
      </v-spacer>
      <v-col cols="12" md="4" class="d-flex justify-end">
        <v-btn
          color="primary"
          prepend-icon="mdi-account-plus"
          @click="showAddDialog = true"
        >
          Добавить клиента
        </v-btn>
      </v-col>
    </v-row>

    <!-- Табличное представление -->
    <v-card>
      <v-data-table
        :headers="headers"
        :items="filteredClients"
        :loading="loading"
        :items-per-page="10"
        class="elevation-1"
      >
        <template v-slot:item.user="{ item }">
          <div class="d-flex align-center">
            <v-avatar size="36" color="primary" class="mr-3">
              <span class="text-white">{{ getInitials(item.user) }}</span>
            </v-avatar>
            <div>
              <div class="font-weight-medium">
                {{ item.user?.first_name }} {{ item.user?.last_name }}
              </div>
              <div class="text-caption text-medium-emphasis">
                {{ item.user?.email }}
              </div>
            </div>
          </div>
        </template>

        <template v-slot:item.contracts_count="{ item }">
          <v-chip :color="getContractsColor(item.id)" size="small">
            {{ getClientContractsCount(item.id) }}
          </v-chip>
        </template>

        <template v-slot:item.status="{ item }">
          <v-chip :color="getStatusColor(item)" size="small">
            {{ getStatusText(item) }}
          </v-chip>
        </template>

        <template v-slot:item.phone="{ item }">
          <v-btn
            variant="text"
            size="small"
            :href="`tel:${item.user?.phone}`"
            prepend-icon="mdi-phone"
          >
            {{ item.user?.phone }}
          </v-btn>
        </template>

        <template v-slot:item.actions="{ item }">

          <v-btn
            icon
            size="small"
            @click="editClient(item)"
            class="mr-1"
          >
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-btn
            icon
            size="small"
            @click="deleteClient(item)"
            color="error"
          >
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>
      </v-data-table>
    </v-card>

    <!-- Диалог добавления/редактирования -->
    <v-dialog
      v-model="showAddDialog"
      max-width="600"
      persistent
    >
      <v-card>
        <v-card-title class="d-flex align-center">
          <span class="text-h5">{{ editMode ? 'Редактирование' : 'Добавление' }} клиента</span>
          <v-spacer></v-spacer>
          <v-btn icon @click="closeDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text>
          <v-form ref="clientForm" @submit.prevent="saveClient">
            <v-row>
              <v-col cols="12" v-if="!editMode">
                <v-text-field
                  v-model="form.user.username"
                  label="Логин"
                  variant="outlined"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="form.user.first_name"
                  label="Имя"
                  variant="outlined"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="form.user.last_name"
                  label="Фамилия"
                  variant="outlined"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="form.user.email"
                  label="Email"
                  type="email"
                  variant="outlined"
                  :rules="[rules.required, rules.email]"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.user.phone"
                  label="Телефон"
                  variant="outlined"
                  :rules="[rules.required, rules.phone]"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.user.passport"
                  label="Паспортные данные"
                  variant="outlined"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6" v-if="!editMode">
                <v-text-field
                  v-model="form.user.password"
                  label="Пароль"
                  type="password"
                  variant="outlined"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            variant="text"
            @click="closeDialog"
          >
            Отмена
          </v-btn>
          <v-btn
            color="primary"
            @click="saveClient"
            :loading="saving"
          >
            {{ editMode ? 'Сохранить' : 'Добавить' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { clientsApi, rentContractsApi, usersApi } from '@/services/api'
import { useSnackbar } from '@/composables/useSnackbar'
import axios from 'axios';
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const { showSuccess, showError } = useSnackbar()

// Состояние
const clients = ref([])
const contracts = ref([])
const loading = ref(false)
const saving = ref(false)
const search = ref('')
const statusFilter = ref(null)
const users = ref([])
//const viewMode = ref('grid') // 'grid' или 'table'
const showAddDialog = ref(false)
const editMode = ref(false)

// Форма
const form = ref({
  user_id: '',
  user: {
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    passport: '',
    username: '',
    password: ''
  }
})

// Правила валидации
const rules = {
  required: value => !!value || 'Обязательное поле',
  email: value => {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return pattern.test(value) || 'Неверный формат email'
  },
  phone: value => {
    const pattern = /^[\d\s\-\+\(\)]+$/
    return pattern.test(value) || 'Неверный формат телефона'
  },
  minLength: min => value => value.length >= min || `Минимум ${min} символов`
}

// Заголовки таблицы
const headers = [
  { title: 'Клиент', key: 'user', sortable: false },
  { title: 'Телефон', key: 'phone', sortable: false },
  { title: 'Паспорт', key: 'user.passport' },
  { title: 'Статус', key: 'status' },
  { title: 'Действия', key: 'actions', sortable: false, width: '120px' }
]

// Опции для фильтров
const statusOptions = [
  { title: 'Активен', value: 'active' },
  { title: 'Заблокирован', value: 'blocked' },
  { title: 'Новый', value: 'new' }
]

// Хлебные крошки
const breadcrumbs = ref([
  {
    title: 'Главная',
    disabled: false,
    href: '/'
  },
  {
    title: 'Клиенты',
    disabled: true,
    href: '/clients'
  }
])

// Вычисляемые свойства
const filteredClients = computed(() => {
  let filtered = [...clients.value]
  
  if (statusFilter.value) {
    filtered = filtered.filter(client => {
        client.user.status === statusFilter.value
        //console.log(client.user)
    })
  }

  if (search.value != "")
  {
     filtered = filtered.filter(client => 
     {
         const user = client.user
         search.value = search.value.toLowerCase()
         //console.log(user.first_name.toLowerCase())
         //console.log(search.value)
        return (
            (user.first_name && user.first_name.toLowerCase().includes(search.value)) || 
            (user.last_name && user.last_name.toLowerCase().includes(search.value)) || 
            (user.email && user.email.toLowerCase().includes(search.value)) || 
            (user.username && user.username.toLowerCase().includes(search.value)))
    })  
  }
  
  return filtered
})

const totalContracts = computed(() => {
  return contracts.value.length
})

// Загрузка данных
const loadClients = async () => {
  loading.value = true
  try {
    const response = await clientsApi.getAll()
    //console.log(response.data)

    clients.value = response.data.results || response.data
  } catch (error) {
    console.error('Ошибка загрузки клиентов:', error)
    showError('Не удалось загрузить список клиентов')
  } finally {
    loading.value = false
  }
}

const loadContracts = async () => {
  try {
    const response = await rentContractsApi.getAll()
    contracts.value = response.data.results || response.data
  } catch (error) {
    console.error('Ошибка загрузки договоров:', error)
  }
}

// Вспомогательные методы
const getInitials = (user) => {
  if (!user) return '??'
  return `${user.first_name?.charAt(0) || ''}${user.last_name?.charAt(0) || ''}`.toUpperCase()
}

const getClientContractsCount = (clientId) => {
  return contracts.value.filter(contract => 
    contract.client?.id === clientId
  ).length
}

const getContractsColor = (clientId) => {
  const count = getClientContractsCount(clientId)
  if (count === 0) return 'grey'
  if (count < 3) return 'blue'
  if (count < 10) return 'green'
  return 'orange'
}

const getStatusColor = (client) => {
  const count = getClientContractsCount(client.id)
  if (count === 0) return 'grey' // Новый клиент
  return 'success' // Активный клиент
}

const getStatusText = (client) => {
  const count = getClientContractsCount(client.id)
  if (count === 0) return 'Новый'
  return 'Активен'
}

// Действия с клиентами
const viewClientDetails = (client) => {
  // Открыть детальный просмотр с историей договоров
  console.log('Просмотр клиента:', client)
}

const editClient = (client) => {
  editMode.value = true
  form.value = {
    user: {
      first_name: client.user?.first_name || '',
      last_name: client.user?.last_name || '',
      email: client.user?.email || '',
      phone: client.user?.phone || '',
      passport: client.user?.passport || '',
      username: client.user?.username || ''
    }
  }
  selectedClientId.value = client.id
  showAddDialog.value = true
}

const deleteClient = async (client) => {
  const name = `${client.user?.first_name} ${client.user?.last_name}`
  if (!confirm(`Удалить клиента ${name}?`)) return

  try {
    await clientsApi.delete(client.id)
    showSuccess('Клиент успешно удален')
    loadClients()
  } catch (error) {
    console.error('Ошибка удаления:', error)
    showError('Не удалось удалить клиента')
  }
}

const saveClient = async () => {
  try {
    saving.value = true
    
    const data = {
      user: form.value.user
    }
    //console.log(data)
    //console.log(form.value.user)
    if (editMode.value) {
      //await clientsApi.update(selectedClientId.value, data)
      await usersApi.update(selectedClientId.value, form.value.user)
      showSuccess('Данные клиента обновлены')
    } else {
        const userData = {
            username: form.value.user.username,
            first_name: form.value.user.first_name,
            last_name: form.value.user.last_name,
            email: form.value.user.email,
            phone: form.value.user.phone,
            passport: form.value.user.passport,
            password: form.value.user.password,
        }
        //console.log(userData)
        //console.log(JSON.stringify(form.value.user))
        const response = await authStore.register(userData)//JSON.stringify(form.value.user))
        //console.log(.data.id)
        await clientsApi.create({user: response.data.id})
      showSuccess('Клиент успешно добавлен')
    }
    
    closeDialog()
    loadClients()
  } catch (error) {
    console.error('Ошибка сохранения:', error)
    const errorMsg = error.response?.data || 'Ошибка сохранения'
    showError(typeof errorMsg === 'object' ? JSON.stringify(errorMsg) : errorMsg)
  } finally {
    saving.value = false
  }
}

const closeDialog = () => {
  showAddDialog.value = false
  editMode.value = false
  form.value = {
    user: {
      first_name: '',
      last_name: '',
      email: '',
      phone: '',
      passport: '',
      username: '',
      password: ''
    }
  }
  selectedClientId.value = null
}

// Переменная для хранения ID редактируемой записи
const selectedClientId = ref(null)

// Инициализация
onMounted(() => {
  loadClients()
  loadContracts()
})
</script>

<style scoped>
.h-100 {
  height: 100%;
}

.float-right {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 100;
}
</style>