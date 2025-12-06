<template>
  <v-dialog :model-value="modelValue" max-width="800" persistent @update:model-value="$emit('update:modelValue', $event)">
    <v-card>
      <v-card-title>
        {{ editingFlight ? 'Редактировать полёт' : 'Добавить полёт' }}
      </v-card-title>
      <v-card-text>
        <v-form ref="formRef" v-model="formValid">
          <v-row>
            <v-col cols="12" md="6" v-if="!droneId">
              <v-select
                v-model="formData.drone_id"
                :items="drones"
                item-title="label"
                item-value="id"
                label="Дрон"
                :rules="[v => !!v || 'Обязательное поле']"
                variant="outlined"
              ></v-select>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.start_datetime"
                label="Дата и время начала"
                type="datetime-local"
                :rules="[v => !!v || 'Обязательное поле']"
                variant="outlined"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.end_datetime"
                label="Дата и время окончания"
                type="datetime-local"
                :rules="[v => !!v || 'Обязательное поле']"
                variant="outlined"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.location"
                label="Регион полёта"
                :rules="[v => !!v || 'Обязательное поле']"
                variant="outlined"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.purpose"
                label="Причина полёта"
                :rules="[v => !!v || 'Обязательное поле']"
                variant="outlined"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model.number="formData.distance"
                label="Дистанция (км)"
                type="number"
                :rules="[v => !!v || 'Обязательное поле', v => v > 0 || 'Должна быть больше 0']"
                variant="outlined"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model.number="formData.battery_usage"
                label="Использованная батарея (%)"
                type="number"
                :rules="[v => !!v || 'Обязательное поле', v => v >= 0 && v <= 100 || 'От 0 до 100']"
                variant="outlined"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-textarea
                v-model="formData.notes"
                label="Заметки"
                variant="outlined"
                rows="3"
              ></v-textarea>
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
import { ref, watch, onMounted, inject } from 'vue'
import * as flightsAPI from '@/api/flights'
import * as dronesAPI from '@/api/drones'

const props = defineProps({
  modelValue: Boolean,
  droneId: Number,
  flight: Object,
})

const emit = defineEmits(['update:modelValue', 'saved'])

const showSnackbar = inject('showSnackbar')
const saving = ref(false)
const formRef = ref(null)
const formValid = ref(false)
const drones = ref([])
const editingFlight = ref(null)

const formData = ref({
  drone_id: null,
  start_datetime: '',
  end_datetime: '',
  location: '',
  purpose: '',
  distance: null,
  battery_usage: null,
  notes: '',
})

watch(() => props.flight, (newFlight) => {
  if (newFlight) {
    editingFlight.value = newFlight
    formData.value = {
      drone_id: typeof newFlight.drone_id === 'object' ? newFlight.drone_id.id : newFlight.drone_id,
      start_datetime: formatDateTimeLocal(newFlight.start_datetime),
      end_datetime: formatDateTimeLocal(newFlight.end_datetime),
      location: newFlight.location || '',
      purpose: newFlight.purpose || '',
      distance: newFlight.distance || null,
      battery_usage: newFlight.battery_usage || null,
      notes: newFlight.notes || '',
    }
  } else {
    editingFlight.value = null
    resetForm()
  }
}, { immediate: true })

const formatDateTimeLocal = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${year}-${month}-${day}T${hours}:${minutes}`
}

const resetForm = () => {
  formData.value = {
    drone_id: props.droneId || null,
    start_datetime: '',
    end_datetime: '',
    location: '',
    purpose: '',
    distance: null,
    battery_usage: null,
    notes: '',
  }
}

const loadDrones = async () => {
  try {
    const dronesList = await dronesAPI.getDrones()
    drones.value = dronesList.map(d => ({
      id: d.id,
      label: `${d.manufacturer} ${d.model} (${d.serial_number})`,
    }))
  } catch (error) {
    console.error('Ошибка загрузки дронов:', error)
  }
}

const save = async () => {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  saving.value = true
  try {
    const data = {
      ...formData.value,
      drone_id: props.droneId || formData.value.drone_id,
    }

    // Преобразуем даты из datetime-local в ISO формат
    if (data.start_datetime) {
      data.start_datetime = new Date(data.start_datetime).toISOString()
    }
    if (data.end_datetime) {
      data.end_datetime = new Date(data.end_datetime).toISOString()
    }

    if (editingFlight.value) {
      await flightsAPI.updateFlight(editingFlight.value.id, data)
      showSnackbar('Полёт успешно обновлён', 'success')
    } else {
      await flightsAPI.createFlight(data, props.droneId)
      showSnackbar('Полёт успешно создан', 'success')
    }
    emit('update:modelValue', false)
    emit('saved')
  } catch (error) {
    const message = error.response?.data?.detail ||
                   Object.values(error.response?.data || {})[0]?.[0] ||
                   'Ошибка сохранения полёта'
    showSnackbar(message, 'error')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  if (!props.droneId) {
    loadDrones()
  }
})
</script>
