<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span class="text-h5">Сотрудники</span>
            <v-btn color="primary" @click="openDialog()">
              <v-icon start>mdi-plus</v-icon>
              Добавить сотрудника
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-text-field
                v-model="search"
                label="Поиск по отделу"
                prepend-inner-icon="mdi-magnify"
                variant="outlined"
                class="mb-4"
                @input="loadEmployees"
            ></v-text-field>

            <v-data-table
                :headers="headers"
                :items="filteredEmployees"
                :loading="loading"
                item-key="id"
            >
              <template v-slot:item.user="{ item }">
                {{ item.user?.first_name }} {{ item.user?.last_name }}
              </template>
              <template v-slot:item.position_display="{ item }">
                <v-chip :color="getPositionColor(item.position)">
                  {{ item.position_display }}
                </v-chip>
              </template>
              <template v-slot:item.actions="{ item }">
                <v-btn icon="mdi-pencil" size="small" @click="openDialog(item)"></v-btn>
                <v-btn icon="mdi-delete" size="small" color="error" @click="deleteItem(item)"></v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Диалог создания/редактирования -->
    <v-dialog v-model="dialog" max-width="600">
      <v-card>
        <v-card-title>{{ editingItem ? 'Редактировать сотрудника' : 'Добавить сотрудника' }}</v-card-title>
        <v-card-text>
          <v-form ref="formRef" @submit.prevent="saveItem">
            <v-select
                v-model="form.user"
                :items="users"
                item-title="username"
                item-value="id"
                label="Пользователь"
                variant="outlined"
                required
            ></v-select>
            <v-select
                v-model="form.position"
                :items="positions"
                item-title="title"
                item-value="value"
                label="Должность"
                variant="outlined"
                required
            ></v-select>
            <v-text-field
                v-model="form.phone"
                label="Телефон"
                variant="outlined"
                required
            ></v-text-field>
            <v-text-field
                v-model="form.hire_date"
                label="Дата найма"
                type="date"
                variant="outlined"
                required
            ></v-text-field>
            <v-text-field
                v-model="form.salary"
                label="Зарплата"
                type="number"
                variant="outlined"
            ></v-text-field>
            <v-text-field
                v-model="form.department"
                label="Отдел"
                variant="outlined"
                required
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" @click="saveItem">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { employeesApi } from '../services/api'

export default {
  name: 'Employees',
  setup() {
    const employees = ref([]) // Список сотрудников
    const users = ref([]) // Список пользователей
    const loading = ref(false) // Для индикатора загрузки
    const search = ref('') // Поле поиска сотрудников по отделу
    const dialog = ref(false) // Для управления состоянием диалога
    const editingItem = ref(null) // Текущий редактируемый сотрудник
    const form = reactive({
      user: null,
      position: '',
      phone: '',
      hire_date: '',
      salary: '',
      department: ''
    })

    // Заголовки таблицы
    const headers = [
      { title: 'Пользователь', key: 'user' },
      { title: 'Должность', key: 'position_display' },
      { title: 'Телефон', key: 'phone' },
      { title: 'Дата найма', key: 'hire_date' },
      { title: 'Зарплата', key: 'salary' },
      { title: 'Отдел', key: 'department' },
      { title: 'Действия', key: 'actions', sortable: false }
    ]

    // Доступные позиции
    const positions = [
      { title: 'Редактор', value: 'editor' },
      { title: 'Менеджер', value: 'manager' },
      { title: 'Дизайнер', value: 'designer' },
      { title: 'Печатник', value: 'printer' },
      { title: 'Бухгалтер', value: 'accountant' },
      { title: 'Директор', value: 'director' }
    ]

    // Функция, возвращающая цвет позиции
    const getPositionColor = (position) => {
      const colors = {
        editor: 'blue',
        manager: 'green',
        designer: 'purple',
        printer: 'orange',
        accountant: 'red',
        director: 'indigo'
      }
      return colors[position] || 'grey'
    }

    // Загрузка сотрудников
    const loadEmployees = async () => {
      loading.value = true
      try {
        const response = await employeesApi.getAll()
        employees.value = response.data.results || response.data
      } catch (error) {
        console.error('Ошибка загрузки сотрудников:', error)
      } finally {
        loading.value = false
      }
    }

    // Загрузка пользователей
    const loadUsers = async () => {
      try {
        const response = await employeesApi.getAll({ include: 'users' }) // Если API возвращает доступных пользователей
        users.value = response.data.results || response.data
      } catch (error) {
        console.error('Ошибка загрузки пользователей:', error)
      }
    }

    // Открытие диалогового окна редактирования/добавления
    const openDialog = (item = null) => {
      editingItem.value = item
      if (item) {
        // Если редактируется существующая запись
        form.user = item.user?.id || null
        form.position = item.position || ''
        form.phone = item.phone || ''
        form.hire_date = item.hire_date || ''
        form.salary = item.salary || ''
        form.department = item.department || ''
      } else {
        // Если добавляется новый сотрудник
        resetForm()
      }
      dialog.value = true
    }

    // Сброс формы
    const resetForm = () => {
      form.user = null
      form.position = ''
      form.phone = ''
      form.hire_date = ''
      form.salary = ''
      form.department = ''
    }

    // Закрытие диалогового окна
    const closeDialog = () => {
      resetForm()
      dialog.value = false
    }

    // Сохранение сотрудника
    const saveItem = async () => {
      try {
        if (editingItem.value) {
          // Обновление существующего сотрудника
          await employeesApi.update(editingItem.value.id, { ...form })
        } else {
          // Создание нового сотрудника
          await employeesApi.create({ ...form })
        }
        loadEmployees()
        closeDialog()
      } catch (error) {
        console.error('Ошибка сохранения:', error)
      }
    }

    // Удаление сотрудника
    const deleteItem = async (item) => {
      if (confirm('Удалить сотрудника?')) {
        try {
          await employeesApi.delete(item.id)
          loadEmployees()
        } catch (error) {
          console.error('Ошибка удаления:', error)
        }
      }
    }

    // Фильтрация сотрудников по поиску
    const filteredEmployees = computed(() =>
        employees.value.filter((employee) =>
            employee.department.toLowerCase().includes(search.value.toLowerCase())
        )
    )

    onMounted(() => {
      loadEmployees()
      loadUsers()
    })

    return {
      employees,
      users,
      positions,
      filteredEmployees,
      form,
      headers,
      dialog,
      editingItem,
      search,
      loading,
      getPositionColor,
      openDialog,
      closeDialog,
      saveItem,
      deleteItem
    }
  }
}
</script>