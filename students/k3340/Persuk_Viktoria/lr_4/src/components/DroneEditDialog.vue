<template>
  <v-dialog :model-value="modelValue" max-width="800" persistent @update:model-value="$emit('update:modelValue', $event)">
    <v-card>
      <v-card-title>
        Редактировать дрон
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
            <v-col cols="12">
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
        <v-btn variant="text" @click="$emit('update:modelValue', false)">Отмена</v-btn>
        <v-btn
          color="primary"
          :loading="saving"
          :disabled="!formValid || saving"
          @click="save"
        >
          Сохранить
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, watch, inject } from 'vue'
import * as dronesAPI from '@/api/drones'

const props = defineProps({
  modelValue: Boolean,
  drone: Object,
})

const emit = defineEmits(['update:modelValue', 'saved'])

const showSnackbar = inject('showSnackbar')
const saving = ref(false)
const formRef = ref(null)
const formValid = ref(false)

const formData = ref({
  manufacturer: '',
  model: '',
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

watch(() => props.drone, (newDrone) => {
  if (newDrone) {
    formData.value = { ...newDrone }
  }
}, { immediate: true })

const save = async () => {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  saving.value = true
  try {
    const data = { ...formData.value }
    Object.keys(data).forEach(key => {
      if (data[key] === '' || data[key] === null) {
        delete data[key]
      }
    })

    await dronesAPI.updateDrone(props.drone.id, data)
    showSnackbar('Дрон успешно обновлён', 'success')
    emit('update:modelValue', false)
    emit('saved')
  } catch (error) {
    const message = error.response?.data?.detail ||
                   Object.values(error.response?.data || {})[0]?.[0] ||
                   'Ошибка обновления дрона'
    showSnackbar(message, 'error')
  } finally {
    saving.value = false
  }
}
</script>
