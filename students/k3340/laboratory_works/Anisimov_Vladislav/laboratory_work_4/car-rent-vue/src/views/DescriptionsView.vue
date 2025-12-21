<!-- views/DescriptionsView.vue -->
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

    <!-- Заголовок -->
    <v-row class="mb-6">
      <v-col cols="12" class="d-flex align-center">
        <v-icon icon="mdi-text-box-multiple" size="32" class="mr-3 text-primary"></v-icon>
        <div>
          <h1 class="text-h4 font-weight-bold">Описания</h1>
          <p class="text-subtitle-1 text-medium-emphasis">
            Модели и описания автомобилей
          </p>
        </div>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          prepend-icon="mdi-plus"
          @click="showAddDialog = true"
        >
          Добавить модель
        </v-btn>
      </v-col>
    </v-row>

    <!-- Карточки моделей -->
    <v-row>
      <v-col
        v-for="carInfo in carInfos"
        :key="carInfo.id"
        cols="12"
        md="6"
        lg="4"
      >
        <v-card class="h-100" hover>
          <v-card-item>
            <v-card-title class="d-flex align-center">
              <v-avatar color="primary" size="48" class="mr-3">
                <span class="text-h6">{{ getCarInitials(carInfo) }}</span>
              </v-avatar>
              <div>
                <div class="text-h6">{{ carInfo.brand }} {{ carInfo.model }}</div>
                <div class="text-caption text-medium-emphasis">
                  {{ getCarCount(carInfo.id) }} автомобилей
                </div>
              </div>
            </v-card-title>
          </v-card-item>

          <v-card-text>
            <div class="text-body-2 mb-3" style="max-height: 100px; overflow: hidden;">
              {{ carInfo.description || 'Описание отсутствует' }}
            </div>
            <div class="text-caption text-medium-emphasis">
              ID: {{ carInfo.id }}
            </div>
          </v-card-text>

          <v-card-actions>

            <v-spacer></v-spacer>
            <v-btn
              icon
              size="small"
              @click="editDescription(carInfo)"
            >
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <v-btn
              icon
              size="small"
              @click="deleteDescription(carInfo)"
            >
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Диалог добавления/редактирования -->
    <v-dialog
      v-model="showAddDialog"
      max-width="600"
      persistent
    >
      <v-card>
        <v-card-title class="d-flex align-center">
          <span class="text-h5">{{ editMode ? 'Редактирование' : 'Добавление' }} модели</span>
          <v-spacer></v-spacer>
          <v-btn icon @click="closeDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text>
          <v-form ref="descForm" @submit.prevent="saveDescription">
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.brand"
                  label="Марка"
                  variant="outlined"
                  :rules="[rules.required]"
                  prepend-inner-icon="mdi-car"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.model"
                  label="Модель"
                  variant="outlined"
                  :rules="[rules.required]"
                  prepend-inner-icon="mdi-car"
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-textarea
                  v-model="form.description"
                  label="Описание"
                  variant="outlined"
                  rows="4"
                  auto-grow
                  prepend-inner-icon="mdi-text"
                  :rules="[rules.maxLength(1000)]"
                ></v-textarea>
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
            @click="saveDescription"
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
import { carInfoApi, carInstanceApi } from '@/services/api'


// Состояние
const carInfos = ref([])
const carInstances = ref([])
const loading = ref(false)
const saving = ref(false)
const showAddDialog = ref(false)
const editMode = ref(false)

// Форма
const form = ref({
  brand: '',
  model: '',
  description: ''
})

// Правила валидации
const rules = {
  required: value => !!value || 'Обязательное поле',
  maxLength: max => value => !value || value.length <= max || `Максимум ${max} символов`
}

const breadcrumbs = ref([
  {
    title: 'Главная',
    disabled: false,
    href: '/'
  },
  {
    title: 'Описания',
    disabled: true,
    href: '/descriptions'
  }
])

// Загрузка данных
const loadCarInfos = async () => {
  loading.value = true
  try {
    const response = await carInfoApi.getAll()
    console.log(response)
    carInfos.value = response.data.results || response.data
  } catch (error) {
    console.error('Ошибка загрузки описаний:', error)
    showError('Не удалось загрузить описания моделей')
  } finally {
    loading.value = false
  }
}

// Вспомогательные методы
const getCarInitials = (carInfo) => {
  return `${carInfo.brand.charAt(0)}${carInfo.model.charAt(0)}`.toUpperCase()
}

const getCarCount = (carInfoId) => {
  return carInstances.value.filter(instance => 
    instance.car?.car_info?.id === carInfoId
  ).length
}

// Действия с описаниями
const viewDescription = (carInfo) => {
  // Можно открыть модальное окно с детальной информацией
  console.log('Просмотр:', carInfo)
}

const editDescription = (carInfo) => {
  editMode.value = true
  form.value = {
    brand: carInfo.brand,
    model: carInfo.model,
    description: carInfo.description || ''
  }
  selectedCarInfoId.value = carInfo.id
  showAddDialog.value = true
}

const deleteDescription = async (carInfo) => {
  if (!confirm(`Удалить модель ${carInfo.brand} ${carInfo.model}?`)) return

  try {
    await carInfoApi.delete(carInfo.id)
    //showSuccess('Модель успешно удалена')
    loadCarInfos()
  } catch (error) {
    console.error('Ошибка удаления:', error)
    //showError('Не удалось удалить модель')
  }
}

const saveDescription = async () => {
  try {
    saving.value = true
    const data = { ...form.value }

    if (editMode.value) {
      await carInfoApi.update(selectedCarInfoId.value, data)
      ////showSuccess('Модель успешно обновлена')
    } else {
      await carInfoApi.create(data)
      ////showSuccess('Модель успешно добавлена')
    }

    closeDialog()
    loadCarInfos()
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
    brand: '',
    model: '',
    description: ''
  }
  selectedCarInfoId.value = null
}

// Переменная для хранения ID редактируемой записи
const selectedCarInfoId = ref(null)

// Инициализация
onMounted(() => {
  loadCarInfos()
})
</script>

<style scoped>
.h-100 {
  height: 100%;
}
</style>