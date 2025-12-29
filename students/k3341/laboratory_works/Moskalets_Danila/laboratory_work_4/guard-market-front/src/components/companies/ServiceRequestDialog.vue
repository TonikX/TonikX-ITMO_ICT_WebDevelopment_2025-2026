<template>
  <v-dialog :model-value="dialog" max-width="500" @update:model-value="$emit('update:dialog', $event)">
    <v-card>
      <v-card-title>Оставить заявку</v-card-title>
      <v-card-text>
        <p class="mb-4">
          Вы оставляете заявку на услугу: <strong>{{ selectedService?.name }}</strong>
        </p>

        <div v-if="selectedService?.current_discount" class="mb-4">
          <v-alert type="info" density="compact">
            Действует скидка: -{{ selectedService.current_discount.discount_percent }}%
          </v-alert>
        </div>

        <v-alert
            v-if="error"
            type="error"
            class="mb-4"
            @click:close="$emit('error-cleared')"
            closable
        >
          {{ error }}
        </v-alert>

        <v-form @submit.prevent="submitForm">
          <v-textarea
              v-model="localRequestForm.description"
              label="Описание заявки"
              :rules="[rules.required]"
              rows="3"
              placeholder="Опишите подробно, что вам нужно..."
              class="mb-4"
              :disabled="loading"
          ></v-textarea>

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
              Отправить заявку
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
  selectedService: {
    type: Object,
    default: null
  },
  requestForm: {
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
  'submit-request',
  'error-cleared',
  'update:dialog'
])

// Локальная копия формы
const localRequestForm = ref({
  description: ''
})

// Инициализация формы при открытии диалога
watch(() => props.dialog, (isOpen) => {
  if (isOpen) {
    localRequestForm.value = {
      description: props.requestForm.description || ''
    }
  }
}, { immediate: true })

const rules = {
  required: value => !!value || 'Обязательное поле'
}

const submitForm = () => {
  emit('submit-request', { ...localRequestForm.value })
}
</script>