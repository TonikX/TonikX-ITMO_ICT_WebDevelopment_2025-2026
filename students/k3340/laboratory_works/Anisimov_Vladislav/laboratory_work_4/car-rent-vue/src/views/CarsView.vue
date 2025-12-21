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

    <!-- Заголовок и действия -->
    <v-row class="mb-6">
      <v-col cols="12" class="d-flex align-center">
        <v-icon icon="mdi-car" size="32" class="mr-3 text-primary"></v-icon>
        <div>
          <h1 class="text-h4 font-weight-bold">Автомобили</h1>
          <p class="text-subtitle-1 text-medium-emphasis">
            Управление парком автомобилей
          </p>
        </div>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          prepend-icon="mdi-plus"
          @click="showAddDialog = true"
        >
          Добавить автомобиль
        </v-btn>
      </v-col>
    </v-row>

    <!-- Фильтры и поиск -->
    <v-row class="mb-4">
      <v-col cols="12" md="4">
        <v-text-field
          v-model="search"
          label="Поиск автомобиля"
          prepend-inner-icon="mdi-magnify"
          variant="outlined"
          clearable
          @update:model-value="loadCarInstances"
        ></v-text-field>
      </v-col>
      <!--<v-col cols="12" md="4">
        <v-select
          v-model="statusFilter"
          label="Статус"
          :items="statusOptions"
          variant="outlined"
          clearable
          @update:model-value="loadCarInstances"
        ></v-select>
      </v-col>-->
      <v-col cols="12" md="4">
        <v-select
          v-model="brandFilter"
          label="Марка"
          :items="brandOptions"
          variant="outlined"
          clearable
          @update:model-value="loadCarInstances"
        ></v-select>
      </v-col>
    </v-row>

    <!-- Карточки автомобилей -->
    <v-row v-if="viewMode === 'grid'">
      <v-col
        v-for="car in carInstances"
        :key="car.id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <v-card class="h-100" hover>
          <v-img
            :src="getCarImage(car)"
            height="160"
            cover
            class="align-end"
          >
            <v-chip
              :color="getStatusColor(car.status)"
              size="small"
              class="ma-2"
            >
              {{ getStatusText(car.status) }}
            </v-chip>
          </v-img>

          <v-card-item>
            <v-card-title class="text-h6">
              {{ car.car?.car_info?.brand }} {{ car.car?.car_info?.model }}
            </v-card-title>
            <v-card-subtitle>
              {{ car.license_plate }} • {{ car.year }} год
            </v-card-subtitle>
          </v-card-item>

          <v-card-text>
            <v-row dense>
              <v-col cols="6">
                <div class="text-caption text-medium-emphasis">Цвет</div>
                <div class="text-body-2">
                  <v-icon
                    :color="getColorCode(car.color)"
                    size="small"
                    class="mr-1"
                  >
                    mdi-square
                  </v-icon>
                  {{ car.color }}
                </div>
              </v-col>
              <v-col cols="6">
                <div class="text-caption text-medium-emphasis">Цена</div>
                <div class="text-h6 text-primary">
                  {{ formatPrice(car.price) }}
                </div>
              </v-col>
            </v-row>
          </v-card-text>

          <v-card-actions>
            <v-btn
              variant="text"
              color="primary"
              @click="viewCarDetails(car)"
            >
              Подробнее
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn
              icon
              size="small"
              @click="editCar(car)"
            >
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <v-btn
              icon
              size="small"
              @click="deleteCar(car)"
            >
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Табличное представление -->
    <v-card v-else>
      <v-data-table
        :headers="headers"
        :items="carInstances"
        :search="search"
        :loading="loading"
        :items-per-page="10"
        class="elevation-1"
      >
        <template v-slot:item.status="{ item }">
          <v-chip
            :color="getStatusColor(item.status)"
            size="small"
          >
            {{ getStatusText(item.status) }}
          </v-chip>
        </template>

        <template v-slot:item.price="{ item }">
          <span class="font-weight-bold text-primary">
            {{ formatPrice(item.price) }}
          </span>
        </template>

        <template v-slot:item.car.car_info="{ item }">
          {{ item.car?.car_info?.brand }} {{ item.car?.car_info?.model }}
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn
            icon
            size="small"
            @click="viewCarDetails(item)"
            class="mr-1"
          >
            <v-icon>mdi-eye</v-icon>
          </v-btn>
          <v-btn
            icon
            size="small"
            @click="editCar(item)"
            class="mr-1"
          >
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-btn
            icon
            size="small"
            @click="deleteCar(item)"
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
          <span class="text-h5">{{ editMode ? 'Редактирование' : 'Добавление' }} автомобиля</span>
          <v-spacer></v-spacer>
          <v-btn
            icon
            @click="closeDialog"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text>
          <v-form ref="carForm" @submit.prevent="saveCar">
            <v-row>
              <v-col cols="12" md="6">
                <v-select
                  v-model="form.car"
                  label="Модель автомобиля"
                  :items="cars"
                  item-title="name"
                  item-value="id"
                  variant="outlined"
                  :rules="[rules.required]"
                  @update:model-value="onCarSelect"
                ></v-select>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.license_plate"
                  label="Госномер"
                  variant="outlined"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.vincode"
                  label="VIN-код"
                  variant="outlined"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.price"
                  label="Цена проката (в сутки)"
                  type="number"
                  variant="outlined"
                  :rules="[rules.required, rules.min(1)]"
                  suffix="₽"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.color"
                  label="Цвет"
                  variant="outlined"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.year"
                  label="Год выпуска"
                  type="number"
                  variant="outlined"
                  :rules="[rules.required, rules.min(1900), rules.max(new Date().getFullYear())]"
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
            @click="saveCar"
            :loading="saving"
          >
            {{ editMode ? 'Сохранить' : 'Добавить' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог подробной информации -->
    <v-dialog
      v-model="showDetailsDialog"
      max-width="800"
    >
      <CarDetailsDialog
        v-if="selectedCar"
        :car="selectedCar"
        @close="showDetailsDialog = false"
      />
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { carInstanceApi, carApi } from '@/services/api'
import CarDetailsDialog from '@/components/CarDetailsDialog.vue'
import { da } from 'date-fns/locale'
//import { useSnackbar } from '@/composables/useSnackbar'

//const { //showSuccess, //showError } = useSnackbar()

// Состояние
const carInstances = ref([])
const cars = ref([])
const loading = ref(false)
const saving = ref(false)
const search = ref('')
const statusFilter = ref(null)
const brandFilter = ref(null)
const viewMode = ref('grid') // 'grid' или 'table'
const showAddDialog = ref(false)
const showDetailsDialog = ref(false)
const editMode = ref(false)
const selectedCar = ref(null)

// Форма
const form = ref({
  car: null,
  license_plate: '',
  vincode: '',
  price: '',
  color: '',
  year: ''
})

// Правила валидации
const rules = {
  required: value => !!value || 'Обязательное поле',
  min: min => value => value >= min || `Минимум ${min}`,
  max: max => value => value <= max || `Максимум ${max}`
}

// Заголовки таблицы
const headers = [
  { title: 'Госномер', key: 'license_plate' },
  { title: 'Марка и модель', key: 'car.car_info' },
  { title: 'Год', key: 'year' },
  { title: 'Цвет', key: 'color' },
  { title: 'Цена', key: 'price', sortable: true },
  { title: 'Статус', key: 'status' },
  { title: 'Действия', key: 'actions', sortable: false }
]

// Опции для фильтров
const statusOptions = [
  { title: 'Доступен', value: 'available' },
  { title: 'В аренде', value: 'rented' },
  { title: 'На обслуживании', value: 'maintenance' },
  { title: 'Сломан', value: 'broken' }
]

const brandOptions = computed(() => {
  const brands = new Set()
  carInstances.value.forEach(car => {
    if (car.car?.car_info?.brand) {
      brands.add(car.car.car_info.brand)
    }
  })
  return Array.from(brands).map(brand => ({ title: brand, value: brand }))
})

// Хлебные крошки
const breadcrumbs = ref([
  {
    title: 'Главная',
    disabled: false,
    href: '/'
  },
  {
    title: 'Автомобили',
    disabled: true,
    href: '/cars'
  }
])

// Загрузка данных
const loadCarInstances = async () => {
  loading.value = true
  try {
    const response = await carInstanceApi.getAll()
    carInstances.value = response.data.results || response.data
  } catch (error) {
    console.error('Ошибка загрузки автомобилей:', error)
    //showError('Не удалось загрузить список автомобилей')
  } finally {
    loading.value = false
  }
}

const loadCars = async () => {
  try {
    const response = await carApi.getAll()
    const carsData = response.data.results || response.data
    cars.value = carsData.map(car => ({
      id: car.id,
      name: `${car.car_info?.brand} ${car.car_info?.model} (${car.transmission})`
    }))
  } catch (error) {
    console.error('Ошибка загрузки моделей:', error)
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

const getStatusColor = (status) => {
  const colors = {
    available: 'success',
    rented: 'warning',
    maintenance: 'info',
    broken: 'error'
  }
  return colors[status] || 'default'
}

const getStatusText = (status) => {
  const texts = {
    available: 'Доступен',
    rented: 'В аренде',
    maintenance: 'На обслуживании',
    broken: 'Сломан'
  }
  return texts[status] || 'Неизвестно'
}

const getCarImage = (car) => {
  const brand = car.car?.car_info?.brand?.toLowerCase() || 'car'
  return `https://source.unsplash.com/featured/400x300/?${brand},car`
}

const getColorCode = (color) => {
  const colorMap = {
    'черный': '#000000',
    'белый': '#ffffff',
    'серебристый': '#c0c0c0',
    'серый': '#808080',
    'синий': '#0000ff',
    'красный': '#ff0000',
    'зеленый': '#008000'
  }
  return colorMap[color?.toLowerCase()] || '#757575'
}

// Действия с автомобилями
const viewCarDetails = (car) => {
  selectedCar.value = car
  showDetailsDialog.value = true
}

const editCar = (car) => {
  selectedCar.value = car
  editMode.value = true
  form.value = {
    car: car.car?.id,
    license_plate: car.license_plate,
    vincode: car.vincode,
    price: car.price,
    color: car.color,
    year: car.year
  }
  showAddDialog.value = true
}

const deleteCar = async (car) => {
  if (!confirm(`Удалить автомобиль ${car.license_plate}?`)) return

  try {
    await carInstanceApi.delete(car.id)
    //showSuccess('Автомобиль успешно удален')
    loadCarInstances()
  } catch (error) {
    console.error('Ошибка удаления:', error)
    //showError('Не удалось удалить автомобиль')
  }
}

const onCarSelect = (carId) => {
  // Здесь можно загрузить дополнительные данные выбранной модели
}

const saveCar = async () => {
  try {
    saving.value = true
    const data = { ...form.value }

    if (editMode.value) {
      console.log(selectedCar)
      await carInstanceApi.update(selectedCar.value.id, data)
      //showSuccess('Автомобиль успешно обновлен')
    } else {
      await carInstanceApi.create(data)
      //showSuccess('Автомобиль успешно добавлен')
    }

    closeDialog()
    loadCarInstances()
  } catch (error) {
    console.error('Ошибка сохранения:', error)
    const errorMsg = error.response?.data || 'Ошибка сохранения'
    //showError(typeof errorMsg === 'object' ? JSON.stringify(errorMsg) : errorMsg)
  } finally {
    saving.value = false
  }
}

const closeDialog = () => {
  showAddDialog.value = false
  editMode.value = false
  form.value = {
    car: null,
    license_plate: '',
    vincode: '',
    price: '',
    color: '',
    year: ''
  }
  selectedCar.value = null
}

// Инициализация
onMounted(() => {
  loadCarInstances()
  loadCars()
})
</script>

<style scoped>
.h-100 {
  height: 100%;
}

.text-subtitle-1 {
  font-size: 1rem;
}
</style>