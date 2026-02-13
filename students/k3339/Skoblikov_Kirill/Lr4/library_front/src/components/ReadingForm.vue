<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <h3>{{ isEdit ? 'Редактировать выдачу' : 'Выдать книгу' }}</h3>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Книга</label>
          <select v-model="form.book" required>
            <option disabled value="">
              — {{ isLoadingBooks ? 'Загрузка...' : 'Выберите книгу' }} —
            </option>
            <option
              v-for="book in availableBooks"
              :key="book.id"
              :value="book.id"
            >
              {{ book.name }} ({{ book.authors }})
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>Читатель</label>
          <select v-model="form.reader" required>
            <option disabled value="">
              — {{ isLoadingReaders ? 'Загрузка...' : 'Выберите читателя' }} —
            </option>
            <option
              v-for="reader in readers"
              :key="reader.reader_id"
              :value="reader.reader_id"
            >
              {{ reader.fullName }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>Дата выдачи</label>
          <input type="date" v-model="form.issued_date" required />
        </div>

        <div class="form-group">
          <label>Дата возврата</label>
          <input type="date" v-model="form.returned_date" />
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
import { ref, reactive, onMounted, watch, computed } from 'vue';
import AppButton from '@/components/UI/AppButton.vue';
import authAPI from '@/api/api.js';

const props = defineProps({
  reading: { type: Object, default: null }
});

const emit = defineEmits(['save', 'close']);

const isEdit = !!props.reading;
const loading = ref(false);
const isLoadingBooks = ref(false);
const isLoadingReaders = ref(false);

const books = ref([]);
const readers = ref([]);
const unavailableBookIds = ref(new Set());
const form = reactive({
  book: '',
  reader: '',
  issued_date: '',
  returned_date: null
});

onMounted(async () => {
  try {
    isLoadingBooks.value = true;
    isLoadingReaders.value = true;

    const [booksRes, readersRes, readingsRes] = await Promise.all([
      authAPI.getBooks(),
      authAPI.getReaders(),
      authAPI.getReadings()
    ]);

    let rawBooks = [];
    if (Array.isArray(booksRes.data)) rawBooks = booksRes.data;
    else if (booksRes.data.Books) rawBooks = booksRes.data.Books;
    else if (booksRes.data.results) rawBooks = booksRes.data.results;
    books.value = rawBooks.map(book => ({
      id: book.book_id || book.id,
      name: book.book_name || book.title || '—',
      authors: book.authors || '—'
    }));
    isLoadingBooks.value = false;

    let rawReaders = [];
    if (Array.isArray(readersRes.data)) rawReaders = readersRes.data;
    else if (readersRes.data.Readers) rawReaders = readersRes.data.Readers;
    else if (readersRes.data.results) rawReaders = readersRes.data.results;
    readers.value = rawReaders.map(reader => ({
      reader_id: reader.reader_id || reader.id,
      fullName: [reader.last_name, reader.first_name, reader.patronymic]
        .filter(Boolean)
        .join(' ') || '—'
    }));
    isLoadingReaders.value = false;

    let rawReadings = [];
    if (Array.isArray(readingsRes.data)) rawReadings = readingsRes.data;
    else if (readingsRes.data.Readings) rawReadings = readingsRes.data.Readings;
    else if (readingsRes.data.results) rawReadings = readingsRes.data.results;

    const activeReadings = rawReadings.filter(r => !r.returned_date);
    unavailableBookIds.value = new Set(activeReadings.map(r => r.book));

  } catch (error) {
    console.error('Ошибка загрузки данных:', error);
    alert('Не удалось загрузить данные для формы');
    isLoadingBooks.value = false;
    isLoadingReaders.value = false;
  }
});

const availableBooks = computed(() => {
  if (isEdit) return books.value;
  return books.value.filter(book => !unavailableBookIds.value.has(book.id));
});

watch(() => props.reading, (newReading) => {
  if (newReading) {
    form.book = newReading.book_id || '';
    form.reader = newReading.reader_id || '';
    form.issued_date = newReading.issued_date || '';
    form.returned_date = newReading.returned_date || null;
  }
}, { immediate: true });

const handleSubmit = async () => {
  loading.value = true;
  try {
    const payload = {
      ...form,
      returned_date: form.returned_date || null
    };
    emit('save', payload);
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

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  background: white;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}
</style>