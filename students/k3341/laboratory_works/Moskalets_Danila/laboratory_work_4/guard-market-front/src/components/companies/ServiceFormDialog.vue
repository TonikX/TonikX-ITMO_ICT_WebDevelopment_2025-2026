<template>
  <v-dialog :model-value="dialog" max-width="600" @update:model-value="$emit('update:dialog', $event)">
    <v-card>
      <v-card-title>
        {{ editingService ? 'Редактировать услугу' : 'Добавить новую услугу' }}
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="submitForm" ref="serviceForm">
          <v-text-field
              v-model="localFormData.name"
              label="Название услуги"
              :rules="[rules.required]"
              class="mb-3"
              :disabled="loading"
          ></v-text-field>

          <v-textarea
              v-model="localFormData.description"
              label="Описание услуги"
              rows="3"
              class="mb-3"
              :disabled="loading"
          ></v-textarea>

          <v-text-field
              v-model="localFormData.price"
              label="Цена (руб.)"
              type="number"
              :rules="[rules.required, rules.price]"
              class="mb-3"
              :disabled="loading"
          ></v-text-field>

          <v-alert
              v-if="error"
              type="error"
              class="mb-4"
              @click:close="$emit('error-cleared')"
              closable
          >
            {{ error }}
          </v-alert>

          <div class="d-flex justify-end">
            <v-btn
                @click="$emit('close')"
                class="mr-2"
                :disabled="loading"
            >
              Отмена
            </v-btn>
            <v-btn
                type="submit"
                color="primary"
                :loading="loading"
            >
              {{ editingService ? 'Сохранить' : 'Добавить' }}
            </v-btn>
          </div>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  dialog: {
    type: Boolean,
    required: true
  },
  editingService: {
    type: Object,
    default: null
  },
  serviceFormData: {
    type: Object,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: null
  }
})

const emit = defineEmits([
  'close',
  'submit-service',
  'error-cleared',
  'update:dialog'
])

// Локальная копия формы для редактирования
const localFormData = ref({
  name: '',
  description: '',
  price: ''
})

// Инициализация формы при открытии диалога
watch(() => props.dialog, (isOpen) => {
  if (isOpen) {
    // Копируем данные из props в локальное состояние
    localFormData.value = {
      name: props.serviceFormData.name || '',
      description: props.serviceFormData.description || '',
      price: props.serviceFormData.price || ''
    }
  }
}, { immediate: true })

const rules = {
  required: value => !!value || 'Обязательное поле',
  price: value => {
    const num = parseFloat(value)
    return (num > 0 && !isNaN(num)) || 'Цена должна быть больше 0'
  }
}

const submitForm = () => {
  emit('submit-service', { ...localFormData.value })
}
</script>