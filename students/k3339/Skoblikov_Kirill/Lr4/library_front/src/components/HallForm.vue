<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <h3>{{ isEdit ? 'Редактировать зал' : 'Добавить зал' }}</h3>

      <form @submit.prevent="handleSubmit">
        <!-- Номер зала: при редактировании недоступен для изменения -->
        <div class="form-group">
          <label>Номер зала *</label>
          <input
            v-model="form.hall_number"
            type="number"
            :disabled="isEdit"
            required
          />
          <small v-if="isEdit" class="hint">Номер зала нельзя изменить</small>
        </div>

        <div class="form-group">
          <label>Название зала *</label>
          <input v-model="form.hall_name" required />
        </div>

        <div class="form-group">
          <label>Вместимость *</label>
          <input v-model="form.capacity" type="number" required min="1" />
        </div>

        <div class="modal-actions">
          <AppButton type="submit" :disabled="loading">
            {{ loading ? 'Сохранение...' : 'Сохранить' }}
          </AppButton>
          <AppButton type="button" @click="$emit('close')">Отмена</AppButton>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue';
import AppButton from '@/components/UI/AppButton.vue';

const props = defineProps({
  hall: { type: Object, default: null }
});

const emit = defineEmits(['save', 'close']);

const isEdit = !!props.hall;
const loading = ref(false);

const form = reactive({
  hall_number: null,
  hall_name: '',
  capacity: null
});

// Заполнение формы при редактировании
watch(() => props.hall, (newHall) => {
  if (newHall) {
    form.hall_number = newHall.hall_number;
    form.hall_name = newHall.hall_name;
    form.capacity = newHall.capacity;
  }
}, { immediate: true });

const handleSubmit = async () => {
  // Приводим числа к нужному типу
  const data = {
    hall_number: Number(form.hall_number),
    hall_name: form.hall_name.trim(),
    capacity: Number(form.capacity)
  };
  loading.value = true;
  try {
    emit('save', data);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 20px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.form-group {
  margin-bottom: 20px;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
}

.form-group input:disabled {
  background: #f7fafc;
  color: #718096;
  cursor: not-allowed;
}

.hint {
  font-size: 0.8rem;
  color: #718096;
  margin-top: 4px;
  display: block;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}
</style>