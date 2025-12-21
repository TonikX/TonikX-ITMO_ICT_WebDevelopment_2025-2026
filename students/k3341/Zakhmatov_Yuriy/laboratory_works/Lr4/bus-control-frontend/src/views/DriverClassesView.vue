<template>
  <div>
    <!-- Заголовок и кнопка добавления -->
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card color="indigo-darken-3" dark>
          <v-card-title class="text-h4">
            <v-icon icon="mdi-license" size="large" class="mr-3"></v-icon>
            Классы водителей
          </v-card-title>
          <v-card-subtitle class="text-h6">
            Управление квалификационными классами
          </v-card-subtitle>
          <v-card-actions>
            <v-btn color="white" variant="outlined" @click="openCreateDialog">
              <v-icon icon="mdi-plus-circle" class="mr-2"></v-icon>
              Добавить класс
            </v-btn>
            <v-btn color="white" variant="text" @click="fetchDriverClasses">
              <v-icon icon="mdi-refresh" class="mr-2"></v-icon>
              Обновить
            </v-btn>
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              label="Поиск классов..."
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

    <!-- Статистика (если есть) -->
    <v-row v-if="statistics.length > 0" class="mb-4">
      <v-col cols="12">
        <v-card elevation="2">
          <v-card-title class="text-h6">
            <v-icon icon="mdi-chart-pie" class="mr-2"></v-icon>
            Распределение водителей по классам
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col
                v-for="stat in statistics"
                :key="stat.driver_class__name"
                cols="12" sm="6" md="4" lg="3"
              >
                <v-card variant="tonal" :color="getClassColor(stat.driver_class__name)">
                  <v-card-text class="text-center">
                    <div class="text-h4">{{ stat.total || 0 }}</div>
                    <div class="text-subtitle-1">{{ stat.driver_class__name || 'Без класса' }}</div>
                    <div class="text-caption mt-2">водителей</div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Таблица классов -->
    <v-card elevation="2">
      <v-data-table
        :headers="headers"
        :items="filteredClasses"
        :loading="loading"
        :search="search"
        class="elevation-1"
      >
        <!-- Заголовок таблицы -->
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Список классов водителей</v-toolbar-title>
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

        <!-- Колонка названия -->
        <template v-slot:item.name="{ item }">
          <div class="d-flex align-center">
            <v-avatar :color="getClassColor(item.name)" size="36" class="mr-3">
              <v-icon icon="mdi-license" color="white"></v-icon>
            </v-avatar>
            <div>
              <strong>{{ item.name }}</strong>
              <div class="text-caption text-medium-emphasis">
                ID: {{ item.id }}
              </div>
            </div>
          </div>
        </template>

        <!-- Колонка базовой зарплаты -->
        <template v-slot:item.base_salary="{ item }">
          <div class="text-subtitle-1 font-weight-bold text-success">
            {{ formatCurrency(item.base_salary) }}
          </div>
          <div class="text-caption text-medium-emphasis">
            базовая ставка
          </div>
        </template>

        <!-- Колонка примерной зарплаты -->
        <template v-slot:item.example_salary="{ item }">
          <div class="text-subtitle-1">
            {{ formatCurrency(item.base_salary * 1.25) }}
          </div>
          <div class="text-caption text-medium-emphasis">
            при 5 годах опыта
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
              @click="viewClass(item)"
              title="Просмотр"
            ></v-btn>
            <v-btn
              icon="mdi-pencil"
              size="small"
              color="warning"
              variant="text"
              @click="editClass(item)"
              title="Редактировать"
            ></v-btn>
            <v-btn
              icon="mdi-delete"
              size="small"
              color="error"
              variant="text"
              @click="deleteClass(item)"
              title="Удалить"
              :disabled="isClassInUse(item.id)"
            ></v-btn>
          </div>
        </template>

        <!-- Пустая таблица -->
        <template v-slot:no-data>
          <v-alert type="info" variant="tonal" class="ma-4">
            Нет данных о классах. Нажмите "Добавить класс", чтобы создать первый.
          </v-alert>
        </template>
      </v-data-table>
    </v-card>

    <!-- Диалог создания/редактирования -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">
          <v-icon :icon="editMode ? 'mdi-pencil' : 'mdi-plus-circle'" class="mr-2"></v-icon>
          {{ editMode ? 'Редактирование класса' : 'Новый класс водителей' }}
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="localForm.name"
                  label="Название класса*"
                  required
                  variant="outlined"
                  :rules="[v => !!v || 'Название обязательно']"
                  hint="Пример: Первый, Второй, Третий"
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-text-field
                  v-model.number="localForm.base_salary"
                  label="Базовая зарплата (руб.)*"
                  type="number"
                  required
                  variant="outlined"
                  :rules="[
                    v => !!v || 'Зарплата обязательна',
                    v => v > 0 || 'Зарплата должна быть больше 0',
                    v => v <= 1000000 || 'Зарплата не может превышать 1 000 000'
                  ]"
                  hint="Минимальная зарплата для данного класса"
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-alert v-if="editMode" type="info" variant="tonal">
                  <div class="d-flex justify-space-between align-center">
                    <span>
                      <strong>Пример расчета зарплаты:</strong>
                    </span>
                    <span class="text-h6 text-success">
                      {{ formatCurrency(calculateExampleSalary()) }}
                    </span>
                  </div>
                  <div class="text-caption mt-2">
                    При 5 годах опыта: {{ formatCurrency(localForm.base_salary) }} × (1 + 5 × 0.05)
                  </div>
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
          <v-btn color="primary" variant="flat" @click="saveClass" :loading="saving">
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
          <template v-if="isClassInUse(classToDelete?.id)">
            <v-alert type="warning" variant="tonal" class="mb-4">
              Этот класс используется {{ getDriverCountForClass(classToDelete?.id) }} водителями!
            </v-alert>
            <p>
              Вы не можете удалить класс <strong>{{ classToDelete?.name }}</strong>,
              так как он назначен водителям.
            </p>
            <p class="text-error">
              Сначала измените класс у всех водителей, затем повторите попытку.
            </p>
          </template>
          <template v-else>
            <p>
              Вы уверены, что хотите удалить класс
              <strong>{{ classToDelete?.name }}</strong>?
            </p>
            <p class="text-error">
              Это действие нельзя отменить!
            </p>
          </template>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="deleteDialog = false">
            Отмена
          </v-btn>
          <v-btn
            v-if="!isClassInUse(classToDelete?.id)"
            color="error"
            variant="flat"
            @click="confirmDelete"
            :loading="deleting"
          >
            Удалить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог просмотра -->
    <v-dialog v-model="viewDialog" max-width="600px">
      <v-card v-if="viewingClass">
        <v-card-title class="text-h5">
          <v-icon icon="mdi-license" class="mr-2"></v-icon>
          Информация о классе
        </v-card-title>

        <v-card-text>
          <v-row class="mb-4">
            <v-col cols="12" class="text-center">
              <v-avatar :color="getClassColor(viewingClass.name)" size="120">
                <v-icon icon="mdi-license" size="x-large" color="white"></v-icon>
              </v-avatar>
              <h2 class="mt-4">{{ viewingClass.name }}</h2>
              <v-chip color="grey" variant="outlined" class="mt-2">
                ID: {{ viewingClass.id }}
              </v-chip>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <v-row>
            <v-col cols="12" md="6">
              <v-list density="compact">
                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-cash"></v-icon>
                  </template>
                  <v-list-item-title>Базовая зарплата</v-list-item-title>
                  <v-list-item-subtitle>
                    <span class="text-h6 text-success">
                      {{ formatCurrency(viewingClass.base_salary) }}
                    </span>
                  </v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-account-group"></v-icon>
                  </template>
                  <v-list-item-title>Количество водителей</v-list-item-title>
                  <v-list-item-subtitle>
                    <v-chip size="small">
                      {{ getDriverCountForClass(viewingClass.id) || 0 }}
                    </v-chip>
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-col>

            <v-col cols="12" md="6">
              <v-list density="compact">
                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-calculator"></v-icon>
                  </template>
                  <v-list-item-title>При 1 году опыта</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ formatCurrency(viewingClass.base_salary * 1.05) }}
                  </v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-calculator"></v-icon>
                  </template>
                  <v-list-item-title>При 5 годах опыта</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ formatCurrency(viewingClass.base_salary * 1.25) }}
                  </v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-calculator"></v-icon>
                  </template>
                  <v-list-item-title>При 10 годах опыта</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ formatCurrency(viewingClass.base_salary * 1.5) }}
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <v-row>
            <v-col cols="12">
              <v-card variant="tonal" color="info">
                <v-card-title class="text-h6">
                  <v-icon icon="mdi-information" class="mr-2"></v-icon>
                  Формула расчета зарплаты
                </v-card-title>
                <v-card-text>
                  <div class="text-body-1">
                    <strong>Зарплата = Базовая × (1 + Опыт × 0.05)</strong>
                  </div>
                  <div class="text-caption mt-2">
                    Где:
                    <ul>
                      <li><strong>Базовая</strong> = {{ formatCurrency(viewingClass.base_salary) }}</li>
                      <li><strong>Опыт</strong> = количество полных лет стажа водителя</li>
                      <li><strong>0.05</strong> = коэффициент надбавки за год опыта (5%)</li>
                    </ul>
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
          <v-btn color="warning" variant="text" @click="editClass(viewingClass)">
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
    const driverClasses = ref([])
    const drivers = ref([]) // Для проверки использования классов
    const statistics = ref([])
    const loading = ref(false)
    const loadingStats = ref(false)
    const saving = ref(false)
    const showReport = ref(true)
    const deleting = ref(false)
    const dialog = ref(false)
    const deleteDialog = ref(false)
    const viewDialog = ref(false)
    const editMode = ref(false)
    const search = ref('')

    // Локальная форма для диалога
    const localForm = reactive({
      id: null,
      name: '',
      base_salary: 30000
    })

    // Для удаления и просмотра
    const classToDelete = ref(null)
    const viewingClass = ref(null)

    // Уведомления
    const snackbar = reactive({
      show: false,
      message: '',
      color: 'success'
    })

    // Заголовки таблицы БЕЗ сортировки
    const headers = ref([
      { title: 'ID', key: 'id', sortable: false, width: '80px' },
      { title: 'Название класса', key: 'name', sortable: false },
      { title: 'Базовая зарплата', key: 'base_salary', sortable: false, width: '150px' },
      { title: 'Пример (5 лет)', key: 'example_salary', sortable: false, width: '150px' },
      { title: 'Действия', key: 'actions', sortable: false, width: '150px', align: 'center' }
    ])

    // Отфильтрованные классы
    const filteredClasses = computed(() => {
      if (!search.value) {
        return driverClasses.value.map(cls => ({
          ...cls,
          example_salary: cls.base_salary * 1.25
        }))
      }

      const searchLower = search.value.toLowerCase()
      return driverClasses.value
        .filter(cls =>
          cls.name.toLowerCase().includes(searchLower) ||
          cls.base_salary.toString().includes(searchLower)
        )
        .map(cls => ({
          ...cls,
          example_salary: cls.base_salary * 1.25
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

    const getClassColor = (className) => {
      const colors = {
        'Первый': 'success',
        'Второй': 'info',
        'Третий': 'warning',
        'Четвертый': 'error',
        'default': 'indigo'
      }
      return colors[className] || colors.default
    }

    const calculateExampleSalary = () => {
      if (!localForm.base_salary) return 0
      return localForm.base_salary * 1.25 // 5 лет опыта
    }

    const isClassInUse = (classId) => {
      if (!classId || !drivers.value.length) return false
      return drivers.value.some(driver => driver.driver_class?.id === classId)
    }

    const getDriverCountForClass = (classId) => {
      if (!classId || !drivers.value.length) return 0
      return drivers.value.filter(driver => driver.driver_class?.id === classId).length
    }

    // API функции
    const fetchDriverClasses = async () => {
      loading.value = true
      try {
        const response = await apiClient.get('driverclasses/')
        driverClasses.value = response.data
      } catch (error) {
        console.error('Ошибка загрузки классов:', error)
        showSnackbar('Ошибка загрузки данных', 'error')
      } finally {
        loading.value = false
      }
    }

    const fetchDrivers = async () => {
      try {
        const response = await apiClient.get('drivers/')
        drivers.value = response.data
      } catch (error) {
        console.error('Ошибка загрузки водителей:', error)
      }
    }

    const fetchStatistics = async () => {
      loadingStats.value = true
      try {
        const response = await apiClient.get('driverclasses/statistics/')
        statistics.value = response.data
      } catch (error) {
        console.error('Ошибка загрузки статистики:', error)
        showSnackbar('Ошибка загрузки статистики', 'error')
      } finally {
        loadingStats.value = false
      }
    }

    // CRUD операции
    const openCreateDialog = () => {
      editMode.value = false
      resetForm()
      dialog.value = true
    }

    const editClass = (cls) => {
      editMode.value = true
      localForm.id = cls.id
      localForm.name = cls.name || ''
      localForm.base_salary = cls.base_salary || 30000

      dialog.value = true
    }

    const viewClass = (cls) => {
      viewingClass.value = cls
      viewDialog.value = true
    }

    const saveClass = async () => {
      // Простая валидация
      if (!localForm.name.trim()) {
        showSnackbar('Введите название класса', 'error')
        return
      }
      if (!localForm.base_salary || localForm.base_salary <= 0) {
        showSnackbar('Введите корректную зарплату', 'error')
        return
      }

      saving.value = true
      try {
        const classData = {
          name: localForm.name.trim(),
          base_salary: Number(localForm.base_salary)
        }

        if (editMode.value) {
          await apiClient.put(`driverclasses/${localForm.id}/`, classData)
          showSnackbar('Класс успешно обновлен', 'success')
        } else {
          await apiClient.post('driverclasses/', classData)
          showSnackbar('Класс успешно создан', 'success')
        }

        await Promise.all([
          fetchDriverClasses(),
          fetchStatistics()
        ])
        closeDialog()
      } catch (error) {
        console.error('Ошибка сохранения:', error)
        const message = error.response?.data?.detail || error.response?.data || 'Ошибка сохранения'
        showSnackbar(message, 'error')
      } finally {
        saving.value = false
      }
    }

    const deleteClass = (cls) => {
      classToDelete.value = cls
      deleteDialog.value = true
    }

    const confirmDelete = async () => {
      if (!classToDelete.value) return

      if (isClassInUse(classToDelete.value.id)) {
        showSnackbar('Невозможно удалить класс, который используется водителями', 'error')
        deleteDialog.value = false
        return
      }

      deleting.value = true
      try {
        await apiClient.delete(`driverclasses/${classToDelete.value.id}/`)

        showSnackbar('Класс успешно удален', 'success')
        await Promise.all([
          fetchDriverClasses(),
          fetchStatistics()
        ])
      } catch (error) {
        console.error('Ошибка удаления:', error)
        showSnackbar('Ошибка удаления', 'error')
      } finally {
        deleting.value = false
        deleteDialog.value = false
        classToDelete.value = null
      }
    }

    const closeDialog = () => {
      dialog.value = false
      resetForm()
    }

    const resetForm = () => {
      localForm.id = null
      localForm.name = ''
      localForm.base_salary = 30000
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
        fetchDriverClasses(),
        fetchDrivers(),
        fetchStatistics()
      ])
    })

    return {
      // Состояние
      driverClasses,
      drivers,
      statistics,
      loading,
      loadingStats,
      saving,
      deleting,
      dialog,
      deleteDialog,
      viewDialog,
      editMode,
      search,
      showReport,
      localForm,
      classToDelete,
      viewingClass,
      snackbar,

      // Данные таблицы
      headers,
      filteredClasses,

      // Методы
      fetchDriverClasses,
      fetchStatistics,
      openCreateDialog,
      editClass,
      viewClass,
      saveClass,
      deleteClass,
      confirmDelete,
      closeDialog,

      // Вспомогательные методы
      formatCurrency,
      getClassColor,
      calculateExampleSalary,
      isClassInUse,
      getDriverCountForClass,
      showSnackbar
    }
  }
}
</script>

<style scoped>

.text-success {
  color: #4CAF50;
}

.text-error {
  color: #F44336;
}



</style>
