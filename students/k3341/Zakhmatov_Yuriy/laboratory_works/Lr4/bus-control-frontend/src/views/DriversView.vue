<template>
  <div>
    <!-- Заголовок и кнопка добавления -->
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card color="primary" dark>
          <v-card-title class="text-h4">
            <v-icon icon="mdi-account-group" size="large" class="mr-3"></v-icon>
            Управление водителями
          </v-card-title>
          <v-card-subtitle class="text-h6">
            Всего водителей: {{ drivers.length }}
          </v-card-subtitle>
          <v-card-actions>
            <v-btn color="white" variant="outlined" @click="openCreateDialog">
              <v-icon icon="mdi-account-plus" class="mr-2"></v-icon>
              Добавить водителя
            </v-btn>
            <v-btn color="white" variant="text" @click="fetchDrivers">
              <v-icon icon="mdi-refresh" class="mr-2"></v-icon>
              Обновить
            </v-btn>
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              label="Поиск водителей..."
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              density="compact"
              clearable
              hide-details
              style="max-width: 300px;"
              class="bg-white rounded"
            ></v-text-field>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Таблица водителей -->
    <v-card elevation="2">
      <v-data-table
        :headers="headers"
        :items="filteredDrivers"
        :loading="loading"
        :search="search"
        class="elevation-1"
      >
        <!-- Заголовок таблицы -->
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Список водителей</v-toolbar-title>
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-spacer></v-spacer>
          </v-toolbar>
        </template>

        <!-- Иконка загрузки -->
        <template v-slot:loading>
          <v-skeleton-loader type="table-row@10"></v-skeleton-loader>
        </template>

        <!-- Колонка ID -->
        <template v-slot:item.id="{ item }">
          <v-chip color="grey" variant="outlined" size="small">
            #{{ item.id }}
          </v-chip>
        </template>

        <!-- Колонка ФИО -->
        <template v-slot:item.full_name="{ item }">
          <div class="d-flex align-center">
            <v-avatar color="primary" size="36" class="mr-3">
              <span class="white--text text-h6">{{ getInitials(item) }}</span>
            </v-avatar>
            <div>
              <strong>{{ item.last_name }} {{ item.first_name }}</strong>
              <div class="text-caption text-medium-emphasis">
                Паспорт: {{ item.passport_number }}
              </div>
            </div>
          </div>
        </template>

        <!-- Колонка класса водителя -->
        <template v-slot:item.driver_class.name="{ item }">
          <v-chip :color="getDriverClassColor(item.driver_class?.name)" size="small">
            {{ item.driver_class?.name || 'Не указан' }}
          </v-chip>
        </template>

        <!-- Колонка опыта -->
        <template v-slot:item.experience_years="{ item }">
          <v-chip variant="outlined" size="small">
            {{ item.experience_years }} лет
          </v-chip>
        </template>

        <!-- Колонка зарплаты -->
        <template v-slot:item.salary="{ item }">
          <div class="text-subtitle-1 font-weight-bold text-success">
            {{ formatCurrency(item.salary) }}
          </div>
          <div class="text-caption text-medium-emphasis">
            в месяц
          </div>
        </template>

        <!-- Колонка действий -->
        <template v-slot:item.actions="{ item }">
          <div class="d-flex" style="gap: 8px;">
            <v-btn
              icon="mdi-eye"
              size="small"
              color="info"
              variant="text"
              @click="viewDriver(item)"
              title="Просмотр"
            ></v-btn>
            <v-btn
              icon="mdi-pencil"
              size="small"
              color="warning"
              variant="text"
              @click="editDriver(item)"
              title="Редактировать"
            ></v-btn>
            <v-btn
              icon="mdi-delete"
              size="small"
              color="error"
              variant="text"
              @click="deleteDriver(item)"
              title="Удалить"
            ></v-btn>
          </div>
        </template>

        <!-- Пустая таблица -->
        <template v-slot:no-data>
          <v-alert type="info" variant="tonal" class="ma-4">
            Нет данных о водителях. Нажмите "Добавить водителя", чтобы создать первого.
          </v-alert>
        </template>
      </v-data-table>
    </v-card>

    <!-- Диалог создания/редактирования (УПРОЩЕННАЯ РАБОЧАЯ ФОРМА) -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title class="text-h5">
          <v-icon :icon="editMode ? 'mdi-pencil' : 'mdi-account-plus'" class="mr-2"></v-icon>
          {{ editMode ? 'Редактирование водителя' : 'Новый водитель' }}
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="localForm.first_name"
                  label="Имя*"
                  required
                  variant="outlined"
                  :rules="[v => !!v || 'Имя обязательно']"
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="localForm.last_name"
                  label="Фамилия*"
                  required
                  variant="outlined"
                  :rules="[v => !!v || 'Фамилия обязательна']"
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-text-field
                  v-model="localForm.passport_number"
                  label="Номер паспорта*"
                  required
                  variant="outlined"
                  :rules="[v => !!v || 'Паспорт обязателен']"
                  hint="Пример: 4500 123456"
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="localForm.birth_date"
                  label="Дата рождения*"
                  type="date"
                  required
                  variant="outlined"
                  :rules="[v => !!v || 'Дата рождения обязательна']"
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="6">
                <v-text-field
                  v-model.number="localForm.experience_years"
                  label="Опыт работы (лет)*"
                  type="number"
                  required
                  variant="outlined"
                  :rules="[
                    v => !!v || 'Опыт обязателен',
                    v => v >= 0 || 'Опыт не может быть отрицательным',
                    v => v <= 50 || 'Опыт не может быть больше 50 лет'
                  ]"
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-autocomplete
                  v-model="localForm.driver_class_id"
                  :items="driverClasses"
                  item-title="name"
                  item-value="id"
                  label="Класс водителя*"
                  required
                  variant="outlined"
                  :rules="[v => !!v || 'Класс обязателен']"
                  :loading="loadingClasses"
                  :disabled="loadingClasses"
                >
                  <template v-slot:item="{ props, item }">
                    <v-list-item v-bind="props">
                      <template v-slot:title>
                        {{ item.raw.name }}
                      </template>
                      <template v-slot:subtitle>
                        Базовая зарплата: {{ formatCurrency(item.raw.base_salary) }}
                      </template>
                    </v-list-item>
                  </template>
                </v-autocomplete>
              </v-col>

              <v-col v-if="editMode && localForm.driver_class_id" cols="12">
                <v-alert type="info" variant="tonal">
                  <template v-slot:title>
                    <strong>Расчетная зарплата:</strong>
                    {{ calculateSalary() }}
                  </template>
                  Зарплата = базовая × (1 + опыт × 0.05)
                </v-alert>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="closeDialog">
            Отмена
          </v-btn>
          <v-btn color="primary" variant="flat" @click="saveDriver" :loading="saving">
            Сохранить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог подтверждения удаления -->
    <v-dialog v-model="deleteDialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">Подтверждение удаления</v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить водителя
          <strong>{{ driverToDelete?.last_name }} {{ driverToDelete?.first_name }}</strong>?
          <br>
          <span class="text-error">Это действие нельзя отменить!</span>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="deleteDialog = false">
            Отмена
          </v-btn>
          <v-btn color="error" variant="flat" @click="confirmDelete" :loading="deleting">
            Удалить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог просмотра -->
    <v-dialog v-model="viewDialog" max-width="700px">
      <v-card v-if="viewingDriver">
        <v-card-title class="text-h5">
          <v-icon icon="mdi-account-card-details" class="mr-2"></v-icon>
          Карточка водителя
        </v-card-title>

        <v-card-text>
          <v-row class="mb-4">
            <v-col cols="12" class="text-center">
              <v-avatar color="primary" size="120">
                <span class="white--text text-h2">{{ getInitials(viewingDriver) }}</span>
              </v-avatar>
              <h2 class="mt-4">{{ viewingDriver.last_name }} {{ viewingDriver.first_name }}</h2>
              <v-chip color="grey" variant="outlined" class="mt-2">
                ID: {{ viewingDriver.id }}
              </v-chip>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <v-row>
            <v-col cols="12" md="6">
              <v-list density="compact">
                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-passport"></v-icon>
                  </template>
                  <v-list-item-title>Паспорт</v-list-item-title>
                  <v-list-item-subtitle>{{ viewingDriver.passport_number }}</v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-cake"></v-icon>
                  </template>
                  <v-list-item-title>Дата рождения</v-list-item-title>
                  <v-list-item-subtitle>{{ formatDate(viewingDriver.birth_date) }}</v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-col>

            <v-col cols="12" md="6">
              <v-list density="compact">
                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-license"></v-icon>
                  </template>
                  <v-list-item-title>Класс водителя</v-list-item-title>
                  <v-list-item-subtitle>
                    <v-chip :color="getDriverClassColor(viewingDriver.driver_class?.name)" size="small">
                      {{ viewingDriver.driver_class?.name }}
                    </v-chip>
                  </v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-clock-outline"></v-icon>
                  </template>
                  <v-list-item-title>Опыт работы</v-list-item-title>
                  <v-list-item-subtitle>{{ viewingDriver.experience_years }} лет</v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <v-row>
            <v-col cols="12">
              <v-card color="success" variant="tonal">
                <v-card-text class="text-center">
                  <div class="text-h4">{{ formatCurrency(viewingDriver.salary) }}</div>
                  <div class="text-subtitle-1">Расчетная месячная зарплата</div>
                  <div class="text-caption mt-2">
                    Базовая ставка: {{ formatCurrency(viewingDriver.driver_class?.base_salary) }}
                    × (1 + {{ viewingDriver.experience_years }} × 0.05)
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="text" @click="viewDialog = false">
            Закрыть
          </v-btn>
          <v-btn color="warning" variant="text" @click="editDriver(viewingDriver)">
            Редактировать
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Уведомления -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="3000">
      {{ snackbar.message }}
      <template v-slot:actions>
        <v-btn icon="mdi-close" @click="snackbar.show = false"></v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import { ref, computed, onMounted, reactive } from 'vue'
import apiClient from '@/api/axios'

export default {
  setup() {
    // Состояние
    const drivers = ref([])
    const driverClasses = ref([])
    const loading = ref(false)
    const loadingClasses = ref(false)
    const saving = ref(false)
    const deleting = ref(false)
    const dialog = ref(false)
    const deleteDialog = ref(false)
    const viewDialog = ref(false)
    const editMode = ref(false)
    const search = ref('')

    // Локальная форма для диалога
    const localForm = reactive({
      id: null,
      first_name: '',
      last_name: '',
      passport_number: '',
      birth_date: '',
      experience_years: 0,
      driver_class_id: null
    })

    // Для удаления и просмотра
    const driverToDelete = ref(null)
    const viewingDriver = ref(null)

    // Уведомления
    const snackbar = reactive({
      show: false,
      message: '',
      color: 'success'
    })

    // Заголовки таблицы БЕЗ сортировки
    const headers = ref([
      { title: 'ID', key: 'id', sortable: false, width: '80px' },
      { title: 'ФИО', key: 'full_name', sortable: false },
      { title: 'Класс', key: 'driver_class.name', sortable: false },
      { title: 'Опыт', key: 'experience_years', sortable: false, width: '120px' },
      { title: 'Зарплата', key: 'salary', sortable: false, width: '150px' },
      { title: 'Действия', key: 'actions', sortable: false, width: '150px', align: 'center' }
    ])

    // Отфильтрованные водители
    const filteredDrivers = computed(() => {
      if (!search.value) {
        return drivers.value.map(driver => ({
          ...driver,
          full_name: `${driver.last_name} ${driver.first_name}`
        }))
      }

      const searchLower = search.value.toLowerCase()
      return drivers.value
        .filter(driver =>
          driver.last_name.toLowerCase().includes(searchLower) ||
          driver.first_name.toLowerCase().includes(searchLower) ||
          driver.passport_number.toLowerCase().includes(searchLower) ||
          driver.driver_class?.name?.toLowerCase().includes(searchLower)
        )
        .map(driver => ({
          ...driver,
          full_name: `${driver.last_name} ${driver.first_name}`
        }))
    })

    // Вспомогательные функции
    const formatCurrency = (value) => {
      if (!value) return '0 ₽'
      return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB',
        minimumFractionDigits: 0
      }).format(value)
    }

    const formatDate = (dateString) => {
      if (!dateString) return ''
      return new Date(dateString).toLocaleDateString('ru-RU')
    }

    const getInitials = (driver) => {
      if (!driver || !driver.first_name || !driver.last_name) {
        return '??'
      }
      return `${driver.first_name[0]}${driver.last_name[0]}`.toUpperCase()
    }

    const getDriverClassColor = (className) => {
      const colors = {
        'Первый': 'success',
        'Второй': 'info',
        'Третий': 'warning',
        'default': 'grey'
      }
      return colors[className] || colors.default
    }

    const calculateSalary = () => {
      const driverClass = driverClasses.value.find(c => c.id === localForm.driver_class_id)
      if (!driverClass) return '0 ₽'
      const salary = driverClass.base_salary * (1 + (localForm.experience_years || 0) * 0.05)
      return formatCurrency(salary)
    }

    // API функции
    const fetchDrivers = async () => {
      loading.value = true
      try {
        const response = await apiClient.get('drivers/')
        drivers.value = response.data
      } catch (error) {
        console.error('Ошибка загрузки водителей:', error)
        showSnackbar('Ошибка загрузки данных', 'error')
      } finally {
        loading.value = false
      }
    }

    const fetchDriverClasses = async () => {
      loadingClasses.value = true
      try {
        const response = await apiClient.get('driverclasses/')
        driverClasses.value = response.data
      } catch (error) {
        console.error('Ошибка загрузки классов водителей:', error)
      } finally {
        loadingClasses.value = false
      }
    }

    // CRUD операции
    const openCreateDialog = () => {
      editMode.value = false
      resetForm()
      dialog.value = true
    }

    const editDriver = (driver) => {
      editMode.value = true
      localForm.id = driver.id
      localForm.first_name = driver.first_name || ''
      localForm.last_name = driver.last_name || ''
      localForm.passport_number = driver.passport_number || ''
      localForm.birth_date = driver.birth_date || ''
      localForm.experience_years = driver.experience_years || 0
      localForm.driver_class_id = driver.driver_class?.id || driver.driver_class_id || null

      dialog.value = true
    }

    const viewDriver = (driver) => {
      viewingDriver.value = driver
      viewDialog.value = true
    }

    const saveDriver = async () => {
      // Простая валидация
      if (!localForm.first_name.trim()) {
        showSnackbar('Введите имя', 'error')
        return
      }
      if (!localForm.last_name.trim()) {
        showSnackbar('Введите фамилию', 'error')
        return
      }
      if (!localForm.passport_number.trim()) {
        showSnackbar('Введите номер паспорта', 'error')
        return
      }
      if (!localForm.birth_date) {
        showSnackbar('Выберите дату рождения', 'error')
        return
      }
      if (!localForm.driver_class_id) {
        showSnackbar('Выберите класс водителя', 'error')
        return
      }

      saving.value = true
      try {
        const driverData = {
          first_name: localForm.first_name.trim(),
          last_name: localForm.last_name.trim(),
          passport_number: localForm.passport_number.trim(),
          birth_date: localForm.birth_date,
          experience_years: Number(localForm.experience_years) || 0,
          driver_class_id: Number(localForm.driver_class_id)
        }

        if (editMode.value) {
          await apiClient.put(`drivers/${localForm.id}/`, driverData)
          showSnackbar('Водитель успешно обновлен', 'success')
        } else {
          await apiClient.post('drivers/', driverData)
          showSnackbar('Водитель успешно создан', 'success')
        }

        await fetchDrivers()
        closeDialog()
      } catch (error) {
        console.error('Ошибка сохранения:', error)
        const message = error.response?.data?.detail || error.response?.data || 'Ошибка сохранения'
        showSnackbar(message, 'error')
      } finally {
        saving.value = false
      }
    }

    const deleteDriver = (driver) => {
      driverToDelete.value = driver
      deleteDialog.value = true
    }

    const confirmDelete = async () => {
      if (!driverToDelete.value) return

      deleting.value = true
      try {
        await apiClient.delete(`drivers/${driverToDelete.value.id}/`)

        showSnackbar('Водитель успешно удален', 'success')
        await fetchDrivers()
      } catch (error) {
        console.error('Ошибка удаления:', error)
        showSnackbar('Ошибка удаления', 'error')
      } finally {
        deleting.value = false
        deleteDialog.value = false
        driverToDelete.value = null
      }
    }

    const closeDialog = () => {
      dialog.value = false
      resetForm()
    }

    const resetForm = () => {
      localForm.id = null
      localForm.first_name = ''
      localForm.last_name = ''
      localForm.passport_number = ''
      localForm.birth_date = ''
      localForm.experience_years = 0
      localForm.driver_class_id = null
      editMode.value = false
    }

    const showSnackbar = (message, color = 'success') => {
      snackbar.message = message
      snackbar.color = color
      snackbar.show = true
    }

    // Инициализация
    onMounted(async () => {
      await Promise.all([
        fetchDrivers(),
        fetchDriverClasses()
      ])
    })

    return {
      // Состояние
      drivers,
      driverClasses,
      loading,
      loadingClasses,
      saving,
      deleting,
      dialog,
      deleteDialog,
      viewDialog,
      editMode,
      search,
      localForm,
      driverToDelete,
      viewingDriver,
      snackbar,

      // Данные таблицы
      headers,
      filteredDrivers,

      // Методы
      fetchDrivers,
      openCreateDialog,
      editDriver,
      viewDriver,
      saveDriver,
      deleteDriver,
      confirmDelete,
      closeDialog,

      // Вспомогательные методы
      formatCurrency,
      formatDate,
      getInitials,
      getDriverClassColor,
      calculateSalary,
      showSnackbar
    }
  }
}
</script>

<style scoped>
.v-data-table {
  border-radius: 8px;
  overflow: hidden;
}

.v-avatar {
  transition: transform 0.2s;
}

.v-avatar:hover {
  transform: scale(1.1);
}

.text-success {
  color: #4CAF50;
}

.text-error {
  color: #F44336;
}
</style>
