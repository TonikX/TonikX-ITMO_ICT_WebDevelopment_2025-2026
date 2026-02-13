<template>
  <div class="books-page">
    <div class="books-container">
      <h2 class="page-title">Список книг</h2>
      <div class="filter-section">
        <div class="filter-row">
          <div class="filter-item">
            <label>Название</label>
            <input
              v-model="filters.title"
              type="text"
              placeholder="Введите название"
              class="filter-input"
            />
          </div>
          <div class="filter-item">
            <label>Автор</label>
            <input
              v-model="filters.author"
              type="text"
              placeholder="Автор"
              class="filter-input"
            />
          </div>
          <div class="filter-item">
            <label>Год</label>
            <input
              v-model="filters.year"
              type="number"
              placeholder="Год"
              class="filter-input"
            />
          </div>
          <div class="filter-item">
            <label>Издательство</label>
            <input
              v-model="filters.publisher"
              type="text"
              placeholder="Издательство"
              class="filter-input"
            />
          </div>
            <div class="filter-item button-item">
              <AppButton @click="resetFilters" variant="secondary" class="reset-btn">
                Сбросить
              </AppButton>
            </div>
        </div>
      </div>

      <div v-if="filteredBooks.length" class="table-wrapper">
        <table class="books-table">
          <thead>
            <tr>
              <th>Название</th>
              <th>Авторы</th>
              <th>Год</th>
              <th>Издательство</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="book in filteredBooks"
              :key="book.id"
              @click="selectBook(book.id)"
              :class="{ selected: selectedBookId === book.id }"
            >
              <td class="title-cell">{{ book.name }}</td>
              <td class="authors-cell">{{ book.authors }}</td>
              <td class="year-cell">{{ formatYear(book.publication_year) }}</td>
              <td class="publisher-cell">{{ book.publishing_house || '—' }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <p v-else class="empty-message">
        {{ books.length ? 'Книги по вашему запросу не найдены' : 'Книг пока нет' }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import authAPI from '@/api/api.js';
import AppButton from '@/components/UI/AppButton.vue';

const books = ref([]);
const selectedBookId = ref(null);

const filters = ref({
  title: '',
  author: '',
  year: '',
  publisher: ''
});

const loadBooks = async () => {
  try {
    const response = await authAPI.getBooks();
    books.value = response.data.Books?.map(book => ({
      id: book.book_id,
      name: book.book_name,
      authors: book.authors,
      publishing_house: book.publishing_house,
      publication_year: book.publication_year,
      cipher: book.cipher,
    })) || [];
  } catch (error) {
    console.error('Ошибка загрузки книг:', error);
    if (error.response?.status === 401) {
      window.location.href = '/login';
    }
  }
};

const formatYear = (dateString) => {
  if (!dateString) return '—';
  try {
    return new Date(dateString).getFullYear();
  } catch {
    return dateString.slice(0, 4);
  }
};

const selectBook = (id) => {
  selectedBookId.value = selectedBookId.value === id ? null : id;
};

const resetFilters = () => {
  filters.value = {
    title: '',
    author: '',
    year: '',
    publisher: ''
  };
};

const filteredBooks = computed(() => {
  return books.value.filter(book => {
    const titleMatch = !filters.value.title ||
      book.name.toLowerCase().includes(filters.value.title.toLowerCase());

    const authorMatch = !filters.value.author ||
      book.authors.toLowerCase().includes(filters.value.author.toLowerCase());

    const yearMatch = !filters.value.year ||
      formatYear(book.publication_year) === Number(filters.value.year);

    const publisherMatch = !filters.value.publisher ||
      (book.publishing_house?.toLowerCase() || '').includes(filters.value.publisher.toLowerCase());

    return titleMatch && authorMatch && yearMatch && publisherMatch;
  });
});

defineExpose({
  loadBooks,
  selectedBookId,
  books,
  filteredBooks,
  resetFilters
});

onMounted(loadBooks);
</script>

<style scoped>
.books-page {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  padding: 40px 20px;
  box-sizing: border-box;
}

.books-container {
  width: 100%;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  padding: 40px 30px;
  transition: all 0.3s ease;
}

.filter-row {
  gap: 30px;
  justify-content: space-between;
}

.filter-item {
  flex: 1 1 160px;
}

.filter-item.button-item {
  width: auto;
  min-width: 130px;
  align-items: flex-end;
}

.reset-btn {
  width: 100%;
  white-space: nowrap;
  height: 38px;
  font-size: 0.9rem;
  margin: 0;
}

.books-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 1rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.books-table thead tr {
  background: #f7fafc;
  border-bottom: 2px solid #e2e8f0;
}

.books-table th {
  padding: 16px 12px;
  text-align: left;
  font-weight: 600;
  color: #2d3748;
  white-space: nowrap;
}

.books-table td {
  padding: 14px 12px;
  border-bottom: 1px solid #edf2f7;
  transition: background 0.15s;
}

.books-table tbody tr:nth-child(even) {
  background-color: #fafafa;
}

.books-table tbody tr:hover {
  background-color: #f0f5ff;
  cursor: pointer;
}

.books-table tbody tr.selected {
  background-color: #e6f7ff;
  border-left: 4px solid #1890ff;
  box-shadow: inset 0 0 0 1px #1890ff;
}
</style>