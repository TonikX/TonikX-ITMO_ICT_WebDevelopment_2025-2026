<!-- views/SpecificationsView.vue -->
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

    <v-row class="mb-6">
      <v-col cols="12" class="d-flex align-center">
        <v-icon icon="mdi-cogs" size="32" class="mr-3 text-primary"></v-icon>
        <div>
          <h1 class="text-h4 font-weight-bold">Характеристики</h1>
          <p class="text-subtitle-1 text-medium-emphasis">
            Технические характеристики автомобилей
          </p>
        </div>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          prepend-icon="mdi-plus"
          @click="showAddDialog = true"
        >
          Добавить характеристики
        </v-btn>
      </v-col>
    </v-row>

    <!-- Таблица характеристик -->
    <v-card>
      <v-data-table
        :headers="headers"
        :items="specifications"
        :loading="loading"
        :items-per-page="10"
        class="elevation-1"
      >
        <template v-slot:item.car_info="{ item }">
          {{ item.car_info?.brand }} {{ item.car_info?.model }}
        </template>

        <template v-slot:item.transmission="{ item }">
          <v-chip size="small" :color="getTransmissionColor(item.transmission)">
            {{ getTransmissionText(item.transmission) }}
          </v-chip>
        </template>

        <template v-slot:item.fuel_type="{ item }">
          <v-chip size="small" variant="outlined">
            {{ getFuelTypeText(item.fuel_type) }}
          </v-chip>
        </template>

        <template v-slot:item.engine_volume="{ item }">
          {{ item.engine_volume }} л
        </template>

        <template v-slot:item.horsepower="{ item }">
          {{ item.horsepower }} л.с.
        </template>

        <template v-slot:item.actions="{ item }">

          <v-btn
            icon
            size="small"
            @click="editSpecification(item)"
            class="mr-1"
          >
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-btn
            icon
            size="small"
            @click="deleteSpecification(item)"
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
      max-width="800"
      persistent
    >
      <v-card>
        <v-card-title class="d-flex align-center">
          <span class="text-h5">{{ editMode ? 'Редактирование' : 'Добавление' }} характеристик</span>
          <v-spacer></v-spacer>
          <v-btn icon @click="closeDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text>
          <v-form ref="specForm" @submit.prevent="saveSpecification">
            <v-row>
              <v-col cols="12" md="6">
                <v-select
                  v-model="form.car_info"
                  label="Модель автомобиля"
                  :items="carInfos"
                  item-title="name"
                  item-value="id"
                  variant="outlined"
                  :rules="[rules.required]"
                ></v-select>
              </v-col>

              <v-col cols="12" md="6">
                <v-select
                  v-model="form.transmission"
                  label="Тип КПП"
                  :items="transmissionOptions"
                  variant="outlined"
                  :rules="[rules.required]"
                ></v-select>
              </v-col>

              <v-col cols="12" md="6">
                <v-select
                  v-model="form.fuel_type"
                  label="Тип топлива"
                  :items="fuelTypeOptions"
                  variant="outlined"
                  :rules="[rules.required]"
                ></v-select>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.capacity"
                  label="Количество мест"
                  type="number"
                  variant="outlined"
                  :rules="[rules.required, rules.min(1)]"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.engine_volume"
                  label="Объем двигателя (л)"
                  type="number"
                  step="0.1"
                  variant="outlined"
                  :rules="[rules.required, rules.min(0.5)]"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.horsepower"
                  label="Мощность двигателя (л.с.)"
                  type="number"
                  variant="outlined"
                  :rules="[rules.required, rules.min(1)]"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.clearance"
                  label="Дорожный просвет (см)"
                  type="number"
                  step="0.1"
                  variant="outlined"
                  :rules="[rules.required, rules.min(1)]"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.trunk_volume"
                  label="Объем багажника (л)"
                  type="number"
                  variant="outlined"
                  :rules="[rules.required, rules.min(1)]"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.tank_volume"
                  label="Объем топливного бака (л)"
                  type="number"
                  variant="outlined"
                  :rules="[rules.required, rules.min(1)]"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.fuel_consumption"
                  label="Расход топлива (л/100км)"
                  type="number"
                  step="0.1"
                  variant="outlined"
                  :rules="[rules.required, rules.min(1)]"
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-text-field
                  v-model="form.gen"
                  label="Поколение"
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
            @click="saveSpecification"
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
import { ref, onMounted } from 'vue'
import { carApi, carInfoApi } from '@/services/api'
//import { useSnackbar } from '@/composables/useSnackbar'

//const { //showSuccess, //showError } = useSnackbar()


const specifications = ref([])
const carInfos = ref([])
const loading = ref(false)
const saving = ref(false)
const showAddDialog = ref(false)
const editMode = ref(false)
const selectedSpecId = ref(-1)

const form = ref({
  car_info: null,
  capacity: '',
  engine_volume: '',
  horsepower: '',
  fuel_type: null,
  transmission: null,
  clearance: '',
  trunk_volume: '',
  tank_volume: '',
  fuel_consumption: '',
  gen: ''
})


const rules = {
  required: value => !!value || 'Обязательное поле',
  min: min => value => value >= min || `Минимум ${min}`,
  max: max => value => value <= max || `Максимум ${max}`
}


const transmissionOptions = [
  { title: 'Автоматическая', value: 'A' },
  { title: 'Механическая', value: 'M' }
]

const fuelTypeOptions = [
  { title: 'АИ-92', value: 1 },
  { title: 'АИ-95', value: 2 },
  { title: 'АИ-98', value: 3 },
  { title: 'АИ-100', value: 4 },
  { title: 'ДТ', value: 5 },
  { title: 'Электрический', value: 6 },
  { title: 'Гибрид', value: 7 }
]


const headers = [
  { title: 'Марка и модель', key: 'car_info' },
  { title: 'КПП', key: 'transmission' },
  { title: 'Тип топлива', key: 'fuel_type' },
  { title: 'Объем двигателя', key: 'engine_volume' },
  { title: 'Мощность', key: 'horsepower', sortable: true },
  { title: 'Мест', key: 'capacity', sortable: true },
  { title: 'Расход', key: 'fuel_consumption' },
  { title: 'Действия', key: 'actions', sortable: false }
]


const breadcrumbs = ref([
  {
    title: 'Главная',
    disabled: false,
    href: '/'
  },
  {
    title: 'Характеристики',
    disabled: true,
    href: '/specifications'
  }
])


const loadSpecifications = async () => {
  loading.value = true
  try {
    const response = await carApi.getAll()
    specifications.value = response.data.results || response.data
  } catch (error) {
    console.error('Ошибка загрузки характеристик:', error)
    //showError('Не удалось загрузить характеристики')
  } finally {
    loading.value = false
  }
}

const loadCarInfos = async () => {
  try {
    const response = await carInfoApi.getAll()
    const infos = response.data.results || response.data
    carInfos.value = infos.map(info => ({
      id: info.id,
      name: `${info.brand} ${info.model}`
    }))
  } catch (error) {
    console.error('Ошибка загрузки моделей:', error)
  }
}


const getTransmissionText = (transmission) => {
  const types = {
    'A': 'Автомат',
    'M': 'Механика'
  }
  return types[transmission] || transmission
}

const getTransmissionColor = (transmission) => {
  return transmission === 'A' ? 'blue' : 'orange'
}

const getFuelTypeText = (fuelType) => {
  const types = {
    1: 'АИ-92',
    2: 'АИ-95',
    3: 'АИ-98',
    4: 'АИ-100',
    5: 'ДТ',
    6: 'Электрический',
    7: 'Гибрид'
  }
  return types[fuelType] || 'Неизвестно'
}


const viewSpecification = (spec) => {
  
  console.log('Просмотр:', spec)
}

const editSpecification = (spec) => {
  editMode.value = true
  selectedSpecId.value = spec.id
  form.value = {
    car_info: spec.car_info?.id,
    capacity: spec.capacity,
    engine_volume: spec.engine_volume,
    horsepower: spec.horsepower,
    fuel_type: spec.fuel_type,
    transmission: spec.transmission,
    clearance: spec.clearance,
    trunk_volume: spec.trunk_volume,
    tank_volume: spec.tank_volume,
    fuel_consumption: spec.fuel_consumption,
    gen: spec.gen
  }
  showAddDialog.value = true
}

const deleteSpecification = async (spec) => {
  if (!confirm(`Удалить характеристики для ${spec.car_info?.brand} ${spec.car_info?.model}?`)) return

  try {
    await carApi.delete(spec.id)
    //showSuccess('Характеристики успешно удалены')
    loadSpecifications()
  } catch (error) {
    console.error('Ошибка удаления:', error)
    //showError('Не удалось удалить характеристики')
  }
}

const saveSpecification = async () => {
  try {
    saving.value = true
    const data = { ...form.value }

    if (editMode.value) {
      await carApi.update(selectedSpecId.value, data)
      //showSuccess('Характеристики успешно обновлены')
    } else {
      await carApi.create(data)
      //showSuccess('Характеристики успешно добавлены')
    }

    closeDialog()
    loadSpecifications()
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
    car_info: null,
    capacity: '',
    engine_volume: '',
    horsepower: '',
    fuel_type: null,
    transmission: null,
    clearance: '',
    trunk_volume: '',
    tank_volume: '',
    fuel_consumption: '',
    gen: ''
  }
}


onMounted(() => {
  loadSpecifications()
  loadCarInfos()
})
</script>