<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <h3>{{ isEdit ? 'Редактировать книгу' : 'Добавить книгу' }}</h3>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Название</label>
          <input v-model="form.book_name" required />
        </div>

        <div class="form-group">
          <label>Авторы</label>
          <input v-model="form.authors" required />
        </div>

        <div class="form-group">
          <label>Издательство</label>
          <input v-model="form.publishing_house" />
        </div>

        <div class="form-group">
          <label>Год издания</label>
          <input type="date" v-model="form.publication_year" />
        </div>

        <div class="form-group">
          <label>Шифр</label>
          <input v-model="form.cipher" />
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
  book: { type: Object, default: null }
});

const emit = defineEmits(['save', 'close']);
const isEdit = !!props.book;
const form = reactive({
  book_name: '',
  authors: '',
  publishing_house: '',
  publication_year: '',
  cipher: ''
});

watch(() => props.book, (newBook) => {
  if (newBook) {
    form.book_name = newBook.name || newBook.book_name || '';
    form.authors = newBook.authors || '';
    form.publishing_house = newBook.publishing_house || '';
    form.publication_year = newBook.publication_year || '';
    form.cipher = newBook.cipher || '';
  }
}, { immediate: true });

const loading = ref(false);

const handleSubmit = async () => {
  loading.value = true;
  try {
    await emit('save', { ...form });
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
  margin-bottom: 15px;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}
</style>