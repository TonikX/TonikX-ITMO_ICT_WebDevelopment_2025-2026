<template>
  <div>
    <v-row class="mb-4">
      <v-col cols="12" md="6">
        <h1 class="text-h4">Дроны</h1>
      </v-col>
      <v-col cols="12" md="6" class="text-right">
        <v-btn
          color="primary"
          prepend-icon="mdi-plus"
          @click="showCreateDialog = true"
        >
          Добавить дрон
        </v-btn>
      </v-col>
    </v-row>

    <v-card v-if="loading">
      <v-card-text>
        <v-progress-circular
          indeterminate
          color="primary"
          class="d-block mx-auto"
        ></v-progress-circular>
      </v-card-text>
    </v-card>

    <v-row v-else>
      <v-col
        v-for="drone in drones"
        :key="drone.id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <v-card
          class="drone-card"
          hover
          @click="$router.push(`/drones/${drone.id}`)"
        >
          <v-card-title class="d-flex justify-space-between align-center" @click.stop>
            <div style="flex: 1; cursor: pointer;" @click="$router.push(`/drones/${drone.id}`)">
              {{ drone.manufacturer }} {{ drone.model }}
            </div>
            <v-menu location="bottom end">
              <template v-slot:activator="{ props: menuProps }">
                <v-btn
                  icon
                  variant="text"
                  v-bind="menuProps"
                  @click.stop
                >
                  <v-icon>mdi-dots-vertical</v-icon>
                </v-btn>
              </template>
              <v-list>
                <v-list-item
                  prepend-icon="mdi-pencil"
                  title="Редактировать"
                  @click="editDrone(drone)"
                ></v-list-item>
                <v-list-item
                  prepend-icon="mdi-delete"
                  title="Удалить"
                  @click="confirmDelete(drone)"
                ></v-list-item>
              </v-list>
            </v-menu>
          </v-card-title>
          <v-card-subtitle @click="$router.push(`/drones/${drone.id}`)" style="cursor: pointer;">
            {{ drone.serial_number }}
          </v-card-subtitle>
          <v-card-text @click="$router.push(`/drones/${drone.id}`)" style="cursor: pointer;">
            <v-chip
              :color="getStatusColor(drone.status)"
              size="small"
              class="mb-2"
            >
              {{ getStatusLabel(drone.status) }}
            </v-chip>
            <v-chip
              :color="getCategoryColor(drone.category)"
              size="small"
              class="ml-2"
            >
              {{ getCategoryLabel(drone.category) }}
            </v-chip>
            <div class="mt-2 text-body-2">
              Полётов: {{ drone.flights?.length || 0 }}<br>
              Документов: {{ drone.documents?.length || 0 }}
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col v-if="drones.length === 0" cols="12">
        <v-card>
          <v-card-text class="text-center text-h6">
            Дроны не найдены
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Диалог создания/редактирования дрона -->
    <v-dialog v-model="showCreateDialog" max-width="800" persistent>
      <v-card>
        <v-card-title>
          {{ editingDrone ? 'Редактировать дрон' : 'Добавить дрон' }}
        </v-card-title>
        <v-card-text>
          <v-form ref="formRef" v-model="formValid">
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.manufacturer"
                  label="Производитель"
                  :rules="[v => !!v || 'Обязательное поле']"
                  variant="outlined"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.model"
                  label="Модель"
                  :rules="[v => !!v || 'Обязательное поле']"
                  variant="outlined"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.serial_number"
                  label="Серийный номер"
                  :rules="[v => !!v || 'Обязательное поле']"
                  variant="outlined"
                  :disabled="!!editingDrone"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="formData.category"
                  :items="categoryOptions"
                  label="Категория"
                  variant="outlined"
                ></v-select>
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="formData.status"
                  :items="statusOptions"
                  label="Статус"
                  variant="outlined"
                ></v-select>
              </v-col>
              <v-col cols="12" md="6">
                <v-checkbox
                  v-model="formData.has_camera"
                  label="Наличие камеры"
                ></v-checkbox>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model.number="formData.weight"
                  label="Вес (кг)"
                  type="number"
                  variant="outlined"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model.number="formData.max_speed"
                  label="Максимальная скорость (км/ч)"
                  type="number"
                  variant="outlined"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model.number="formData.length"
                  label="Длина (см)"
                  type="number"
                  variant="outlined"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model.number="formData.width"
                  label="Ширина (см)"
                  type="number"
                  variant="outlined"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model.number="formData.height"
                  label="Высота (см)"
                  type="number"
                  variant="outlined"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model.number="formData.max_flight_distance"
                  label="Максимальная дистанция полёта (км)"
                  type="number"
                  variant="outlined"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="closeDialog">Отмена</v-btn>
          <v-btn
            color="primary"
            :loading="saving"
            :disabled="!formValid || saving"
            @click="saveDrone"
          >
            Сохранить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог подтверждения удаления -->
    <v-dialog v-model="showDeleteDialog" max-width="400">
      <v-card>
        <v-card-title>Подтверждение удаления</v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить дрон {{ deletingDrone?.manufacturer }} {{ deletingDrone?.model }}?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="showDeleteDialog = false">Отмена</v-btn>
          <v-btn color="error" @click="deleteDrone">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import { useRouter } from 'vue-router'
import * as dronesAPI from '@/api/drones'

const router = useRouter()
const showSnackbar = inject('showSnackbar')

const loading = ref(false)
const saving = ref(false)
const drones = ref([])
const showCreateDialog = ref(false)
const editingDrone = ref(null)
const deletingDrone = ref(null)
const showDeleteDialog = ref(false)
const formRef = ref(null)
const formValid = ref(false)

const formData = ref({
  manufacturer: '',
  model: '',
  serial_number: '',
  category: 'commercial',
  status: 'active',
  has_camera: false,
  weight: null,
  length: null,
  width: null,
  height: null,
  max_speed: null,
  max_flight_distance: null,
})

const categoryOptions = [
  { title: 'Любительский', value: 'hobby' },
  { title: 'Коммерческий', value: 'commercial' },
  { title: 'Профессиональный', value: 'pro' },
]

const statusOptions = [
  { title: 'Активен', value: 'active' },
  { title: 'Требуется проверка', value: 'pending' },
  { title: 'Архивирован', value: 'archived' },
]

const getStatusLabel = (status) => {
  const option = statusOptions.find(opt => opt.value === status)
  return option ? option.title : status
}

const getStatusColor = (status) => {
  const colors = {
    active: 'success',
    pending: 'warning',
    archived: 'grey',
  }
  return colors[status] || 'grey'
}

const getCategoryLabel = (category) => {
  const option = categoryOptions.find(opt => opt.value === category)
  return option ? option.title : category
}

const getCategoryColor = (category) => {
  const colors = {
    hobby: 'info',
    commercial: 'primary',
    pro: 'purple',
  }
  return colors[category] || 'grey'
}

const loadDrones = async () => {
  loading.value = true
  try {
    drones.value = await dronesAPI.getDrones()
  } catch (error) {
    showSnackbar('Ошибка загрузки дронов', 'error')
  } finally {
    loading.value = false
  }
}

const closeDialog = () => {
  showCreateDialog.value = false
  editingDrone.value = null
  resetForm()
}

const resetForm = () => {
  formData.value = {
    manufacturer: '',
    model: '',
    serial_number: '',
    category: 'commercial',
    status: 'active',
    has_camera: false,
    weight: null,
    length: null,
    width: null,
    height: null,
    max_speed: null,
    max_flight_distance: null,
  }
}

const editDrone = (drone) => {
  editingDrone.value = drone
  formData.value = { ...drone }
  showCreateDialog.value = true
}

const confirmDelete = (drone) => {
  deletingDrone.value = drone
  showDeleteDialog.value = true
}

const deleteDrone = async () => {
  if (!deletingDrone.value) return

  try {
    await dronesAPI.deleteDrone(deletingDrone.value.id)
    showSnackbar('Дрон успешно удалён', 'success')
    showDeleteDialog.value = false
    deletingDrone.value = null
    loadDrones()
  } catch (error) {
    showSnackbar('Ошибка удаления дрона', 'error')
  }
}

const saveDrone = async () => {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  saving.value = true
  try {
    const data = { ...formData.value }
    // Удаляем пустые значения
    Object.keys(data).forEach(key => {
      if (data[key] === '' || data[key] === null) {
        delete data[key]
      }
    })

    if (editingDrone.value) {
      await dronesAPI.updateDrone(editingDrone.value.id, data)
      showSnackbar('Дрон успешно обновлён', 'success')
    } else {
      await dronesAPI.createDrone(data)
      showSnackbar('Дрон успешно создан', 'success')
    }
    closeDialog()
    loadDrones()
  } catch (error) {
    const message = error.response?.data?.detail ||
                   Object.values(error.response?.data || {})[0]?.[0] ||
                   'Ошибка сохранения дрона'
    showSnackbar(message, 'error')
  } finally {
    saving.value = false
  }
}

const initializeDrones = () => {
  loadDrones()
}

onMounted(() => {
  initializeDrones()
})
</script>

<style scoped>
.drone-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.drone-card:hover {
  transform: translateY(-4px);
}
</style>
