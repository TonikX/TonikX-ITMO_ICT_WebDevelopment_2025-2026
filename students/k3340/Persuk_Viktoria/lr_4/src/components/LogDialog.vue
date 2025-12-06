<template>
  <v-dialog :model-value="modelValue" max-width="600" persistent @update:model-value="handleClose">
    <v-card>
      <v-card-title>
        {{ editingLog ? 'Редактировать лог' : 'Добавить лог' }}
      </v-card-title>
      <v-card-text>
        <v-form ref="formRef" v-model="formValid">
          <v-text-field
            v-model="formData.timestamp"
            label="Дата и время"
            type="datetime-local"
            :rules="[v => !!v || 'Обязательное поле']"
            variant="outlined"
            class="mb-2"
          ></v-text-field>
          <v-row>
            <v-col cols="12" md="4">
              <v-text-field
                v-model.number="formData.latitude"
                label="Широта"
                type="number"
                step="0.000001"
                :rules="[v => !!v || 'Обязательное поле']"
                variant="outlined"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model.number="formData.longtitude"
                label="Долгота"
                type="number"
                step="0.000001"
                :rules="[v => !!v || 'Обязательное поле']"
                variant="outlined"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model.number="formData.altitude"
                label="Высота (м)"
                type="number"
                :rules="[v => !!v || 'Обязательное поле']"
                variant="outlined"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-text-field
            v-model.number="formData.battery"
            label="Заряд батареи (%)"
            type="number"
            :rules="[v => !!v || 'Обязательное поле', v => v >= 0 && v <= 100 || 'От 0 до 100']"
            variant="outlined"
            class="mb-2"
          ></v-text-field>
          <v-textarea
            v-model="formData.message"
            label="Сообщение"
            variant="outlined"
            rows="3"
          ></v-textarea>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn variant="text" @click="handleClose">Отмена</v-btn>
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
import * as logsAPI from '@/api/logs'

const props = defineProps({
  modelValue: Boolean,
  flightId: Number,
  log: Object,
})

const emit = defineEmits(['update:modelValue', 'saved'])

const showSnackbar = inject('showSnackbar')
const saving = ref(false)
const formRef = ref(null)
const formValid = ref(false)
const editingLog = ref(null)

const formData = ref({
  timestamp: '',
  latitude: null,
  longtitude: null,
  altitude: null,
  battery: null,
  message: '',
})

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

watch(() => props.log, (newLog) => {
  if (newLog) {
    editingLog.value = newLog
    formData.value = {
      timestamp: formatDateTimeLocal(newLog.timestamp),
      latitude: newLog.latitude || null,
      longtitude: newLog.longtitude || null,
      altitude: newLog.altitude || null,
      battery: newLog.battery || null,
      message: newLog.message || '',
    }
  } else {
    editingLog.value = null
    resetForm()
  }
}, { immediate: true })

const resetForm = () => {
  formData.value = {
    timestamp: '',
    latitude: null,
    longtitude: null,
    altitude: null,
    battery: null,
    message: '',
  }
}

const handleClose = (value) => {
  editingLog.value = null
  resetForm()
  emit('update:modelValue', value)
}

const save = async () => {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  saving.value = true
  try {
    const data = { ...formData.value }

    // Преобразуем дату из datetime-local в ISO формат
    if (data.timestamp) {
      data.timestamp = new Date(data.timestamp).toISOString()
    }

    if (editingLog.value) {
      await logsAPI.updateLog(editingLog.value.id, data)
      showSnackbar('Лог успешно обновлён', 'success')
    } else {
      await logsAPI.createLog(data, props.flightId)
      showSnackbar('Лог успешно создан', 'success')
    }
    handleClose(false)
    emit('saved')
  } catch (error) {
    const message = error.response?.data?.detail ||
                   Object.values(error.response?.data || {})[0]?.[0] ||
                   'Ошибка сохранения лога'
    showSnackbar(message, 'error')
  } finally {
    saving.value = false
  }
}
</script>
