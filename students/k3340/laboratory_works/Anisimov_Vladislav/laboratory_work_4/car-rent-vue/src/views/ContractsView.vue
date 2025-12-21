<!-- views/ContractsView.vue -->
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
      <v-col cols="12" class="d-flex align-center">
        <v-icon icon="mdi-file-document" size="32" class="mr-3 text-primary"></v-icon>
        <div>
          <h1 class="text-h4 font-weight-bold">Договоры аренды</h1>
          <p class="text-subtitle-1 text-medium-emphasis">
            Управление договорами аренды автомобилей
          </p>
        </div>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          prepend-icon="mdi-plus"
          @click="showAddDialog = true"
        >
          Новый договор
        </v-btn>
      </v-col>
    </v-row>

    <!-- Фильтры и быстрые действия -->
    <v-row class="mb-6">
      <v-col cols="12" md="3">
        <v-select
          v-model="statusFilter"
          label="Статус договора"
          :items="statusOptions"
          variant="outlined"
          clearable
        ></v-select>
      </v-col>
      <v-col cols="12" md="3">
        <v-menu
          v-model="dateMenuStart"
          :close-on-content-click="false"
        >
          <template v-slot:activator="{ props }">
            <v-text-field
              v-model="dateStartText"
              label="Начало аренды"
              prepend-inner-icon="mdi-calendar"
              variant="outlined"
              readonly
              v-bind="props"
              clearable
              @click:clear="clearStartDate"
            ></v-text-field>
          </template>
          <v-date-picker
            v-model="dateStart"
            @update:model-value="dateMenuStart = false"
          ></v-date-picker>
        </v-menu>
      </v-col>
            <v-col cols="12" md="3">
        <v-menu
          v-model="dateMenuEnd"
          :close-on-content-click="false"
        >
          <template v-slot:activator="{ props }">
            <v-text-field
              v-model="dateEndText"
              label="Конец аренды"
              prepend-inner-icon="mdi-calendar"
              variant="outlined"
              readonly
              v-bind="props"
              clearable
              @click:clear="clearEndDate"
              ></v-text-field>
          </template>
          <v-date-picker
            v-model="dateEnd"
            @update:model-value="dateMenuEnd = false"
          ></v-date-picker>
        </v-menu>
      </v-col>
      <v-col cols="12" md="3">
        <v-select
          v-model="clientFilter"
          label="Клиент"
          :items="clients"
          variant="outlined"
          clearable
          item-title="name"
          item-value="id"
        ></v-select>
      </v-col>
    </v-row>

    <v-card>
      <v-data-table
        :headers="headers"
        :items="filteredContracts"
        :loading="loading"
        :items-per-page="10"
        class="elevation-1"
      >
        <template v-slot:item.id="{ item }">
          <strong>#{{ item.id }}</strong>
        </template>

        <template v-slot:item.client="{ item }">
          {{ item.client?.user?.first_name }} {{ item.client?.user?.last_name }}
        </template>

        <template v-slot:item.car_instance="{ item }">
          <div>
            <div>{{ item.car_instance?.car?.car_info?.brand }} {{ item.car_instance?.car?.car_info?.model }}</div>
            <div class="text-caption">{{ item.car_instance?.license_plate }}</div>
          </div>
        </template>

        <template v-slot:item.start_date="{ item }">
          {{ formatDate(item.start_date) }}
        </template>

        <template v-slot:item.return_date="{ item }">
          {{ formatDate(item.return_date) }}
        </template>

        <template v-slot:item.status="{ item }">
          <v-chip :color="getStatusColor(item)" size="small">
            {{ getStatusText(item) }}
          </v-chip>
        </template>

        <template v-slot:item.price="{ item }">
          <span class="font-weight-bold text-primary">
            {{ calculateContractPrice(item) }}
          </span>
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn
            icon
            size="small"
            @click="editContract(item)"
            class="mr-1"
          >
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-btn
            icon
            size="small"
            @click="deleteContract(item)"
            color="error"
          >
            <v-icon>mdi-delete</v-icon>
          </v-btn>
          <v-btn
            v-if="!item.real_return_date"
            icon
            size="small"
            @click="closeContract(item)"
            color="success"
          >
            <v-icon>mdi-check</v-icon>
          </v-btn>
        </template>
      </v-data-table>
    </v-card>

    <!-- Диалог добавления/редактирования -->
    <v-dialog
      v-model="showAddDialog"
      max-width="800"
      persistent
    >
      <v-card>
        <v-card-title class="d-flex align-center">
          <span class="text-h5">{{ editMode ? 'Редактирование' : 'Новый' }} договор</span>
          <v-spacer></v-spacer>
          <v-btn icon @click="closeDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text>
          <v-form ref="contractForm" @submit.prevent="saveContract">
            <v-row>
              <v-col cols="12" md="6" v-if="!editMode">
                <v-select
                  v-model="form.client"
                  label="Клиент"
                  :items="clients"
                  item-title="name"
                  item-value="id"
                  variant="outlined"
                  :rules="[rules.required]"
                ></v-select>
              </v-col>

              <v-col cols="12" md="6" v-if="!editMode">
                <v-select
                  v-model="form.car_instance"
                  label="Автомобиль"
                  :items="availableCars"
                  item-title="name"
                  item-value="id"
                  variant="outlined"
                  :rules="[rules.required]"
                ></v-select>
              </v-col>

              <v-col cols="12" md="6">
                <v-select
                  v-model="form.worker"
                  label="Сотрудник"
                  :items="workers"
                  item-title="name"
                  item-value="id"
                  variant="outlined"
                  :rules="[rules.required]"
                ></v-select>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.start_date"
                  label="Дата начала"
                  type="datetime-local"
                  variant="outlined"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.return_date"
                  label="Дата возврата"
                  type="datetime-local"
                  variant="outlined"
                  :rules="[rules.required, rules.dateAfterStart]"
                ></v-text-field>
              </v-col>

              <v-col cols="12" v-if="editMode">
                <v-text-field
                  v-model="form.real_return_date"
                  label="Фактическая дата возврата"
                  type="datetime-local"
                  variant="outlined"
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-card variant="outlined" class="mt-4">
                  <v-card-title class="text-subtitle-1">
                    <v-icon icon="mdi-calculator" class="mr-2"></v-icon>
                    Расчет стоимости
                  </v-card-title>
                  <v-card-text>
                    <div class="d-flex justify-space-between align-center">
                      <span>Продолжительность:</span>
                      <strong>{{ calculateDays() }} дней</strong>
                    </div>
                    <div class="d-flex justify-space-between align-center mt-2">
                      <span>Цена за день:</span>
                      <strong>{{ formatPrice(selectedCarPrice) }}</strong>
                    </div>
                    <v-divider class="my-2"></v-divider>
                    <div class="d-flex justify-space-between align-center">
                      <span class="text-h6">Итого:</span>
                      <span class="text-h5 text-primary">{{ calculateTotalPrice() }}</span>
                    </div>
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
            @click="saveContract"
            :loading="saving"
          >
            {{ editMode ? 'Сохранить' : 'Создать договор' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-container>
</template>

<script setup>
import { ref, onMounted, computed, watch  } from 'vue'
import { rentContractsApi, clientsApi, carInstanceApi, workersApi } from '@/services/api'
import { useSnackbar } from '@/composables/useSnackbar'
import { format, parseISO, differenceInDays } from 'date-fns'

const { showSuccess, showError } = useSnackbar()

// Состояние
const contracts = ref([])
const clients = ref([])
const cars = ref([])
const workers = ref([])
const loading = ref(false)
const saving = ref(false)
const statusFilter = ref(null)
const clientFilter = ref(null)
const dateStart = ref(null)
const dateEnd= ref(null)
const dateMenuStart = ref(false)
const dateMenuEnd = ref(false)
//const viewMode = ref('grid') // 'grid' или 'table'
const showAddDialog = ref(false)
const editMode = ref(false)
const carsMap = {}
const timeZone = 'Europe/Moscow';
// Форма
const form = ref({
  client: null,
  client_id: null,
  car_instance: null,
  worker_id: null,
  worker: null,
  start_date: '',
  return_date: '',
  real_return_date: '',
  price_per_day: 0
})

// Правила валидации
const rules = {
  required: value => !!value || 'Обязательное поле',
  min: min => value => value >= min || `Минимум ${min}`,
  dateAfterStart: value => {
    if (!form.value.start_date || !value) return true
    return new Date(value) > new Date(form.value.start_date) || 'Дата возврата должна быть позже даты начала'
  }
}

// Заголовки таблицы
const headers = [
  { title: '№', key: 'id', sortable: true },
  { title: 'Клиент', key: 'client', sortable: false },
  { title: 'Автомобиль', key: 'car_instance', sortable: false },
  { title: 'Начало', key: 'start_date', sortable: true },
  { title: 'Возврат', key: 'return_date' },
  { title: 'Статус', key: 'status', sortable: false },
  { title: 'Стоимость', key: 'price', sortable: true },
  { title: 'Действия', key: 'actions', sortable: false }
]

// Опции для фильтров
const statusOptions = [
  { title: 'Активный', value: 'active' },
  { title: 'Завершен', value: 'completed' },
  { title: 'Просрочен', value: 'overdue' }
]

const clientOptions = computed(() => {
  return clients.value.map(client => ({
    id: client.id,
    name: `${client.user?.first_name} ${client.user?.last_name}`
  }))
})

// Хлебные крошки
const breadcrumbs = ref([
  {
    title: 'Главная',
    disabled: false,
    href: '/'
  },
  {
    title: 'Договоры',
    disabled: true,
    href: '/contracts'
  }
])

// Вычисляемые свойства
const filteredContracts = computed(() => {
  let filtered = [...contracts.value]
  
  if (statusFilter.value) {
    filtered = filtered.filter(contract => {
      if (statusFilter.value === 'active') {
        return !contract.real_return_date && new Date(contract.return_date) > new Date()
      }
      if (statusFilter.value === 'completed') {
        return contract.real_return_date
      }
      if (statusFilter.value === 'overdue') {
        return !contract.real_return_date && new Date(contract.return_date) < new Date()
      }
      return true
    })
  }
  
  if (clientFilter.value) {
    filtered = filtered.filter(contract => 
      contract.client?.id === clientFilter.value
    )
  }
  
  if (dateStart.value) {
    //const [start, end] = dateStart, .value
    filtered = filtered.filter(contract => {
      const contractDate = new Date(contract.start_date)
      return contractDate >= new Date(dateStart.value)
    })
  }

  if (dateEnd.value) {
    //const [start, end] = dateStart, .value
    filtered = filtered.filter(contract => {
      const contractDate = new Date(contract.start_date)
      return contractDate <= new Date(dateEnd.value)
    })
  }
  
  return filtered
})

const clearStartDate = () =>
{
  dateStart.value = null
}

const clearEndDate = () =>
{
  dateEnd.value = null
}

const dateStartText = computed(() => {
  if (dateStart.value ) {
    return `${formatDate(dateStart.value)}`
  }
  return 'Выберите дату'
})

const dateEndText = computed(() => {
  if (dateEnd.value ) {
    return `${formatDate(dateEnd.value)}`
  }
  return 'Выберите дату'
})


const availableCars = computed(() => {
  return cars.value.filter(car => {
    // Проверяем, что автомобиль не в активной аренде
    const activeContract = contracts.value.find(contract => 
      contract.car_instance?.id === car.id && 
      !contract.real_return_date
    )
    return !activeContract
  }).map(car => ({
    id: car.id,
    name: `${car.car?.car_info?.brand} ${car.car?.car_info?.model} - ${car.license_plate} (${formatPrice(car.price)}/день)`,
    price: car.price
  }))
})

const selectedCarPrice = computed(() => {
  if (!form.value.car_instance) return 0
  const car = cars.value.find(c => c.id === form.value.car_instance)
  return car?.price || 0
})

// Загрузка данных
const loadContracts = async () => {
  loading.value = true
  try {
    const response = await rentContractsApi.getAll()
    contracts.value = response.data.results || response.data
    //console.log(contracts)
  } catch (error) {
    console.error('Ошибка загрузки договоров:', error)
    showError('Не удалось загрузить список договоров')
  } finally {
    loading.value = false
  }
}

const loadClients = async () => {
  try {
    const response = await clientsApi.getAll()
    //console.log(response.data)
    clients.value = response.data.results || response.data.map(client => ({
      id: client.id,
      name: `${client.user?.first_name} ${client.user?.last_name} (${client.user?.username})`
    }))
  } catch (error) {
    console.error('Ошибка загрузки клиентов:', error)
  }
}

const loadCars = async () => {
  try {
    const response = await carInstanceApi.getAll()
    cars.value = response.data.results || response.data
    
    mapCarsOnContracts()
  } catch (error) {
    console.error('Ошибка загрузки автомобилей:', error)
  }
}

const mapCarsOnContracts = () => {
  cars.value.forEach(car => {
    carsMap[car.id] = car
  })
  
  contracts.value = contracts.value.map(contract => {
    contract['car_instance'] = carsMap[contract['car_instance_id']]
    return contract
  })
}

const loadWorkers = async () => {
  try {
    const response = await workersApi.getAll()
    //console.log(response.data)
    workers.value = response.data.results || response.data.map(worker => ({
      id: worker.id,
      name: `${worker.user?.first_name} ${worker.user?.last_name} (${worker.position})`
    }))
  } catch (error) {
    console.error('Ошибка загрузки сотрудников:', error)
  }
}

// Вспомогательные методы
const formatDate = (dateString) => {
  if (!dateString) return ''
  const tzoffset = (new Date(dateString)).getTimezoneOffset() * 60000;
  const date = new Date(new Date(dateString) - tzoffset).toLocaleDateString("ru-RU")
  return date
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    minimumFractionDigits: 0
  }).format(price)
}

const getStatusColor = (contract) => {
  if (contract.real_return_date) return 'success' // Завершен
  if (new Date(contract.return_date) < new Date()) return 'error' // Просрочен
  return 'primary' // Активен
}

const getStatusText = (contract) => {
  if (contract.real_return_date) return 'Завершен'
  if (new Date(contract.return_date) < new Date()) return 'Просрочен'
  return 'Активен'
}

const calculateContractPrice = (contract) => {
  if (!contract.start_date || !contract.return_date) return '0 ₽'
  
  const start = parseISO(contract.start_date)
  const end = parseISO(contract.return_date)
  const days = differenceInDays(end, start)
  const pricePerDay = contract.car_instance?.price || 0
  
  return formatPrice(days * pricePerDay)
}

const calculateDays = () => {
  if (!form.value.start_date || !form.value.return_date) return 0
  
  const start = new Date(form.value.start_date)
  const end = new Date(form.value.return_date)
  return differenceInDays(end, start)
}

const calculateTotalPrice = () => {
  const days = calculateDays()
  return formatPrice(days * selectedCarPrice.value)
}

// Действия с договорами
const viewContractDetails = (contract) => {
  // Открыть детальный просмотр
  console.log('Просмотр договора:', contract)
}

const editContract = (contract) => {
  editMode.value = true
  form.value = {
    client: contract.client?.id,
    car_instance: contract.car_instance?.id,
    worker: contract.worker?.id,
    start_date: contract.start_date ? contract.start_date.slice(0, 16) : '',
    return_date: contract.return_date ? contract.return_date.slice(0, 16) : '',
    real_return_date: contract.real_return_date ? contract.real_return_date.slice(0, 16) : '',
    price_per_day: contract.car_instance?.price || 0
  }
  selectedContractId.value = contract.id
  showAddDialog.value = true
}

const deleteContract = async (contract) => {
  if (!confirm(`Удалить контракт ${contract.id}?`)) return

  try {
    await rentContractsApi.delete(contract.id)
    showSuccess('Контракт успешно удален')
    await loadContracts()
    mapCarsOnContracts()
  } catch (error) {
    console.error('Ошибка удаления:', error)
    showError('Не удалось удалить клиента')
  }
}

const closeContract = async (contract) => {
  if (!confirm(`Закрыть договор #${contract.id}?`)) return

  try {
    const tzoffset = (new Date()).getTimezoneOffset() * 60000;
    const now = new Date(new Date() - tzoffset).toISOString().slice(0, 16)//.toISOString().slice(0, 16)
    //console.log( new Intl.Locale("ru-RU").getTimeZones())
    //console.log(tzoffset)
    //console.log(new Date(now - tzoffset).toISOString().slice(0, 16))
    //console.log(now)
    await rentContractsApi.update(contract.id, { real_return_date: now })
    showSuccess('Договор успешно закрыт')
    await loadContracts()
    mapCarsOnContracts()
  } catch (error) {
    console.error('Ошибка закрытия договора:', error)
    showError('Не удалось закрыть договор')
  }
}

const saveContract = async () => {
  try {
    saving.value = true
    
    const data = {
      client: form.value.client,
      car_instance: form.value.car_instance,
      worker: form.value.worker,
      start_date: form.value.start_date,
      return_date: form.value.return_date
    }
    
    if (form.value.real_return_date) {
      data.real_return_date = form.value.real_return_date
    }
    
    if (editMode.value) {
      await rentContractsApi.update(selectedContractId.value, data)
      showSuccess('Договор успешно обновлен')
    } else {
      await rentContractsApi.create(data)
      showSuccess('Договор успешно создан')
    }
    
    closeDialog()
    await loadContracts()
    mapCarsOnContracts()
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
    client: null,
    car_instance: null,
    worker: null,
    start_date: '',
    return_date: '',
    real_return_date: '',
    price_per_day: 0
  }
  selectedContractId.value = null
}

// Наблюдатели
watch(() => form.value.car_instance, (newCarId) => {
  if (newCarId) {
    const car = cars.value.find(c => c.id === newCarId)
    form.value.price_per_day = car?.price || 0
  }
})

// Переменная для хранения ID редактируемой записи
const selectedContractId = ref(null)

// Инициализация
onMounted(async () => {
  await loadContracts()
  loadClients()
  loadCars()
  loadWorkers()
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

.text-right {
  text-align: right;
}
</style>