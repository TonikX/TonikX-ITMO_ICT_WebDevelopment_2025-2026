<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <h3>{{ isEdit ? 'Редактировать читателя' : 'Добавить читателя' }}</h3>

      <form @submit.prevent="handleSubmit">
        <div class="form-row">
          <div class="form-group">
            <label>Фамилия</label>
            <input v-model="form.last_name" required />
          </div>
          <div class="form-group">
            <label>Имя</label>
            <input v-model="form.first_name" required />
          </div>
          <div class="form-group">
            <label>Отчество</label>
            <input v-model="form.patronymic" />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>№ читательского билета</label>
            <input v-model="form.reader_card_number" required />
          </div>
          <div class="form-group">
            <label>Дата рождения</label>
            <input type="date" v-model="form.birth_date" required />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Паспорт</label>
            <input v-model="form.passport_number" required />
          </div>
          <div class="form-group">
            <label>Телефон</label>
            <input v-model="form.phone_number" required />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Образование</label>
            <select v-model="form.education" required>
              <option value="se">Среднее</option>
              <option value="he">Высшее</option>
              <option value="ad">Учёная степень</option>
            </select>
          </div>
          <div class="form-group checkbox-group">
            <label>
              <input type="checkbox" v-model="form.academic_degree" />
              Есть учёная степень
            </label>
          </div>
        </div>

        <div class="form-group">
          <label>Адрес</label>
          <input v-model="form.address" required />
        </div>

        <div class="form-group">
          <label>Зал</label>
          <select v-model="form.hall">
            <option :value="null">— Не выбран —</option>
            <option
              v-for="hall in halls"
              :key="hall.hall_number"
              :value="hall.hall_number"
            >
              {{ hall.hall_name }}
            </option>
          </select>
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
import { ref, reactive, onMounted, watch } from 'vue';
import AppButton from '@/components/UI/AppButton.vue';
import authAPI from '@/api/api.js';

const props = defineProps({
  reader: { type: Object, default: null }
});

const emit = defineEmits(['save', 'close']);

const isEdit = !!props.reader;
const halls = ref([]);
const loading = ref(false);
const form = reactive({
  last_name: '',
  first_name: '',
  patronymic: '',
  reader_card_number: '',
  birth_date: '',
  passport_number: '',
  phone_number: '',
  education: 'se',
  academic_degree: false,
  address: '',
  hall: null
});

onMounted(async () => {
  try {
    const response = await authAPI.getHalls();
    halls.value = response.data.Halls || response.data;
  } catch (error) {
    console.error('Ошибка загрузки залов:', error);
  }
});

watch(() => props.reader, (newReader) => {
  if (newReader) {
    form.last_name = newReader.last_name || '';
    form.first_name = newReader.first_name || '';
    form.patronymic = newReader.patronymic || '';
    form.reader_card_number = newReader.reader_card_number || '';
    form.birth_date = newReader.birth_date || '';
    form.passport_number = newReader.passport_number || '';
    form.phone_number = newReader.phone_number || '';
    form.education = newReader.education || 'se';
    form.academic_degree = newReader.academic_degree || false;
    form.address = newReader.address || '';
    form.hall = newReader.hall_id || null;
  }
}, { immediate: true });

const handleSubmit = async () => {
  loading.value = true;
  try {
    emit('save', { ...form });
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
  max-width: 700px;
  max-height: 90vh;
  overflow-y: auto;
}

.form-row {
  display: flex;
  gap: 25px;
  margin-bottom: 15px;
}

.form-group {
  flex: 1;
  margin-bottom: 15px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
}

.checkbox-group {
  display: flex;
  align-items: center;
  margin-top: 23px;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: normal;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}
</style>