<!-- views/StaffView.vue -->
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
        <v-icon icon="mdi-account-tie" size="32" class="mr-3 text-primary"></v-icon>
        <div>
          <h1 class="text-h4 font-weight-bold">Персонал</h1>
          <p class="text-subtitle-1 text-medium-emphasis">
            Управление сотрудниками компании
          </p>
        </div>
      </v-col>
      <v-col cols="12" md="4" class="text-right">
        <v-chip color="primary" variant="outlined" class="mr-2">
          <v-icon start icon="mdi-account-group"></v-icon>
          Всего сотрудников: {{ staff.length }}
        </v-chip>
        <v-chip color="success" variant="outlined">
          <v-icon start icon="mdi-cash"></v-icon>
          Всего ЗП: {{ formatPrice(totalSalary) }}
        </v-chip>
      </v-col>
    </v-row>

    <!-- Действия и фильтры -->
    <v-row class="mb-4">
      <v-col cols="12" md="4">
        <v-text-field
          v-model="search"
          label="Поиск сотрудника"
          prepend-inner-icon="mdi-magnify"
          variant="outlined"
          clearable
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="4">
        <v-select
          v-model="positionFilter"
          label="Должность"
          :items="positionOptions"
          variant="outlined"
          clearable
        ></v-select>
      </v-col>
      <v-col cols="12" md="4" class="d-flex justify-end">
        <v-btn
          color="primary"
          prepend-icon="mdi-account-plus"
          @click="showAddDialog = true"
        >
          Добавить сотрудника
        </v-btn>
      </v-col>
    </v-row>

    <!-- Таблица сотрудников -->
    <v-card>
      <v-data-table
        :headers="headers"
        :items="filteredStaff"
        :loading="loading"
        :items-per-page="10"
        class="elevation-1"
      >
        <template v-slot:item.user="{ item }">
          <div class="d-flex align-center">
            <v-icon icon="mdi-account-tie" size="24" class="mr-3 text-primary"></v-icon>
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

        <template v-slot:item.position="{ item }">
          <v-chip :color="getPositionColor(item.position)" size="small">
            {{ item.position }}
          </v-chip>
        </template>

        <template v-slot:item.salary="{ item }">
          <span class="font-weight-bold text-green">
            {{ formatPrice(item.salary) }}
          </span>
        </template>

        <template v-slot:item.phone="{ item }">
          <span>
            <v-icon icon="mdi-phone" size="16"></v-icon>
            {{ item.user?.phone }}
          </span>
        </template>

        <template v-slot:item.passport="{ item }">
          <span>
            <v-icon icon="mdi-passport" size="16"></v-icon>
            {{ item.user?.passport }}
          </span>
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn
            icon
            size="small"
            @click="editEmployee(item)"
            class="mr-1"
          >
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-btn
            icon
            size="small"
            @click="deleteEmployee(item)"
            color="error"
            v-if="checkSuper()"
          >
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>

        <template v-slot:no-data>
          <div class="py-8 text-center">
            <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-account-off</v-icon>
            <div class="text-h6 text-grey">Сотрудники не найдены</div>
            <div class="text-body-1 text-grey-lighten-1 mt-2">
              Добавьте первого сотрудника
            </div>
          </div>
        </template>
      </v-data-table>
    </v-card>

    <!-- Диалог добавления/редактирования -->
    <v-dialog
      v-model="showAddDialog"
      max-width="700"
      persistent
    >
      <v-card>
        <v-card-title class="d-flex align-center">
          <span class="text-h5">{{ editMode ? 'Редактирование' : 'Добавление' }} сотрудника</span>
          <v-spacer></v-spacer>
          <v-btn icon @click="closeDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text>
          <v-form ref="staffForm" @submit.prevent="saveEmployee">
            <v-row>
              <!-- Личные данные -->
              <v-col cols="12">
                <v-card variant="outlined" class="mb-4">
                  <v-card-title class="text-subtitle-1">
                    <v-icon icon="mdi-account" class="mr-2"></v-icon>
                    Пользователь
                  </v-card-title>
                  <v-card-text>
                    <v-row>
                      <v-col cols="6" md="6" v-if="!editMode">
                        <v-select
                        v-model="form.user_id"
                        label="Аккаунт"
                        :items="users"
                        item-title="name"
                        item-value="id"
                        variant="outlined"
                        :rules="[rules.required]"
                        ></v-select>
                    </v-col>
                    <v-col cols="12" md="6" v-if="editMode">
                        <v-text-field
                          v-model="form.user.first_name"
                          label="Имя"
                          variant="outlined"
                          :rules="[rules.required]"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="6" v-if="editMode">
                        <v-text-field
                          v-model="form.user.last_name"
                          label="Фамилия"
                          variant="outlined"
                          :rules="[rules.required]"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="6" v-if="editMode">
                        <v-text-field
                          v-model="form.user.email"
                          label="Email"
                          type="email"
                          variant="outlined"
                          :rules="[rules.required, rules.email]"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="6" v-if="editMode">
                        <v-text-field
                          v-model="form.user.phone"
                          label="Телефон"
                          variant="outlined"
                          :rules="[rules.required, rules.phone]"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" v-if="editMode">
                        <v-text-field
                          v-model="form.user.passport"
                          label="Паспортные данные"
                          variant="outlined"
                          :rules="[rules.required]"
                        ></v-text-field>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
              </v-col>

              <!-- Рабочая информация -->
              <v-col cols="12">
                <v-card variant="outlined">
                  <v-card-title class="text-subtitle-1">
                    <v-icon icon="mdi-briefcase" class="mr-2"></v-icon>
                    Рабочая информация
                  </v-card-title>
                  <v-card-text>
                    <v-row>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="form.position"
                          label="Должность"
                          variant="outlined"
                          :rules="[rules.required]"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="form.salary"
                          label="Зарплата"
                          type="number"
                          variant="outlined"
                          :rules="[rules.required, rules.min(1)]"
                          suffix="₽"
                        ></v-text-field>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
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
            @click="saveEmployee"
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
import { workersApi, clientsApi, usersApi } from '@/services/api'
import { useSnackbar } from '@/composables/useSnackbar'
import axios from 'axios';

const { showSuccess, showError } = useSnackbar()

// Состояние
const staff = ref([])
const users = ref([])
const loading = ref(false)
const saving = ref(false)
const search = ref('')
const positionFilter = ref(null)
const showAddDialog = ref(false)
const editMode = ref(false)

// Форма
const form = ref({
  position: '',
  salary: '',
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
  min: min => value => value >= min || `Минимум ${min}`,
  minLength: min => value => value.length >= min || `Минимум ${min} символов`
}

// Заголовки таблицы
const headers = [
  { title: 'Сотрудник', key: 'user', sortable: false },
  { title: 'Должность', key: 'position', sortable: false },
  { title: 'Зарплата', key: 'salary', sortable: true },
  { title: 'Телефон', key: 'phone', sortable: false },
  { title: 'Паспорт', key: 'passport' },
  { title: 'Действия', key: 'actions', sortable: false, width: '120px' }
]

// Опции для фильтров
const positionOptions = computed(() => {
  const positions = new Set()
  staff.value.forEach(employee => {
    if (employee.position) {
      positions.add(employee.position)
    }
  })
  return Array.from(positions).map(position => ({ title: position, value: position }))
})

// Хлебные крошки
const breadcrumbs = ref([
  {
    title: 'Главная',
    disabled: false,
    href: '/'
  },
  {
    title: 'Персонал',
    disabled: true,
    href: '/staff'
  }
])

// Вычисляемые свойства
const filteredStaff = computed(() => {
  let filtered = [...staff.value]
  
  if (positionFilter.value) {
    filtered = filtered.filter(employee => employee.position === positionFilter.value)
  }

  if (search.value != "")
  {
     filtered = filtered.filter(employee => 
     {
        const user = employee.user
        search.value = search.value.toLowerCase()
        return (
            (user.first_name && user.first_name.toLowerCase().includes(search.value)) || 
            (user.last_name && user.last_name.toLowerCase().includes(search.value)) || 
            (user.email && user.email.toLowerCase().includes(search.value)) || 
            (user.username && user.username.toLowerCase().includes(search.value)))
    })  
  }

  return filtered
})

const totalSalary = computed(() => {
  return staff.value.reduce((sum, employee) => sum + (employee.salary || 0), 0)
})

// Загрузка данных
const loadStaff = async () => {
  loading.value = true
  try {
    const response = await workersApi.getAll()
    const users_data = await axios.get('http://localhost:8000/core/users')

    const usersMap = {}
    //console.log(users_data)
    users_data.data.forEach(user => {
        usersMap[user.id] = user
    })

    users.value = users_data.data.map(user => ({
      id: user.id,
      name: `${user.first_name} ${user.last_name}`
    }))

    const workersWithUserData = response.data.map(worker => {
        const user = usersMap[worker.user_id]
        return {
            ...worker,
            user
        }
    })
    //console.log(workersWithUserData)

    staff.value = workersWithUserData
    //console.log(staff);
    // Загружаем связанных пользователей если API не возвращает их сразу

  } catch (error) {
    console.error('Ошибка загрузки сотрудников:', error)
    showError('Не удалось загрузить список сотрудников')
  } finally {
    loading.value = false
  }
}

// Вспомогательные методы
const formatPrice = (price) => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    minimumFractionDigits: 0
  }).format(price)
}

const getInitials = (user) => {
  if (!user) return '??'
  return `${user.first_name?.charAt(0) || ''}${user.last_name?.charAt(0) || ''}`.toUpperCase()
}

const getPositionColor = (position) => {
  const colorMap = {
    'Менеджер': 'blue',
    'Администратор': 'purple',
    'Механик': 'orange',
    'Бухгалтер': 'green',
    'Директор': 'red',
    'Водитель': 'indigo'
  }
  return colorMap[position] || 'grey'
}

// Действия с сотрудниками
const viewEmployee = (employee) => {
  // Открыть детальный просмотр
  console.log('Просмотр сотрудника:', employee)
}

const editEmployee = (employee) => {
  editMode.value = true
  form.value = {
    position: employee.position,
    salary: employee.salary,
    user: {
      first_name: employee.user?.first_name || '',
      last_name: employee.user?.last_name || '',
      email: employee.user?.email || '',
      phone: employee.user?.phone || '',
      passport: employee.user?.passport || '',
      username: employee.user?.username || ''
    }
  }

  selectedUserId.value = employee.user_id
  selectedEmployeeId.value = employee.id
  showAddDialog.value = true
}

const deleteEmployee = async (employee) => {
  const name = `${employee.user?.first_name} ${employee.user?.last_name}`
  if (!confirm(`Удалить сотрудника ${name}?`)) return

  try {
    axios.defaults.headers.common['Authorization'] = `Token ${localStorage.getItem('token')}`;
    await workersApi.delete(employee.id)
    showSuccess('Сотрудник успешно удален')
    loadStaff()
  } catch (error) {
    console.error('Ошибка удаления:', error)
    showError('Не удалось удалить сотрудника')
  }
}

const saveEmployee = async () => {
  try {
    saving.value = true
    
    // Подготовка данных для API
    const data = {
      salary: Number(form.value.salary),
      position: form.value.position,
      user: form.value.user_id
    }
    
    const userData = form.value.user
    
    console.log(data)
    if (editMode.value) {
        // Для обновления
        await workersApi.update(selectedEmployeeId.value, data)
        await usersApi.update(selectedUserId.value, userData)
        //await axios.patch('http://localhost:8000/auth/users', userData)
        showSuccess('Данные сотрудника обновлены')
    } else {
      // Для создания
      await workersApi.create(data)
      showSuccess('Сотрудник успешно добавлен')
    }
    
    closeDialog()
    loadStaff()
  } catch (error) {
    console.error('Ошибка сохранения:', error)
    const errorMsg = error.response?.data || 'Ошибка сохранения'
    showError(typeof errorMsg === 'object' ? JSON.stringify(errorMsg) : errorMsg)
  } finally {
    saving.value = false
  }
}

const checkSuper = () =>
{
  return localStorage.getItem('is_superuser') == 'true' ? true : false;
}

const closeDialog = () => {
  showAddDialog.value = false
  editMode.value = false
  form.value = {
    position: '',
    salary: '',
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
  selectedEmployeeId.value = null
  selectedUserId.value = null
}

// Переменная для хранения ID редактируемой записи
const selectedEmployeeId = ref(null)
const selectedUserId = ref(null)

// Инициализация
onMounted(() => {
  loadStaff()
})
</script>

<style scoped>
.text-green {
  color: #4CAF50;
}
</style>