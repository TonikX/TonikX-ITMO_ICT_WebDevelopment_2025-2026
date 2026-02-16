<template>
  <div class="books-view">
    <!-- Шапка с кнопкой обновления -->
    <div class="header">
      <h1>Книги в библиотеке</h1>
      <button @click="loadBooks" :disabled="loading" class="refresh-btn">
        {{ loading ? 'Обновление...' : 'Обновить' }}
      </button>
    </div>

    <!-- Состояния загрузки/ошибки -->
    <div v-if="loading" class="loading">Загрузка книг...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <!-- Список книг -->
    <div v-else class="books-list">
      <div v-for="book in books" :key="book.book_id" class="book-card">
        <h3>{{ book.title }}</h3>
        <p><strong>Год:</strong> {{ book.publication_year }}</p>
        <p><strong>Издательство:</strong> {{ book.publisher }}</p>
        <p><strong>Раздел:</strong> {{ book.section }}</p>
        <p><strong>Инв. номер:</strong> {{ book.inventory_code }}</p>

        <!-- Доступные экземпляры с цветовым индикатором -->
        <div class="copies-info">
          <span class="copies-label">📚 Доступно:</span>
          <span :class="['copies-count', { 'copies-zero': book.available_copies === 0 }]">
            {{ book.available_copies || 0 }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '../api/client'

// Состояние
const books = ref([])      // список книг
const loading = ref(false) // флаг загрузки
const error = ref(null)    // сообщение об ошибке

// Загрузка книг с количеством доступных экземпляров
const loadBooks = async () => {
  loading.value = true
  error.value = null
  try {
    const res = await apiClient.get('books/with-copies/')
    books.value = res.data
  } catch (err) {
    console.error(err)
    error.value = 'Не удалось загрузить книги'
  } finally {
    loading.value = false
  }
}

// Загрузка при монтировании компонента
onMounted(loadBooks)
</script>

<style scoped>
.books-view { padding: 20px; width: 100%; }

/* Шапка */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}
.header h1 { margin: 0; color: #2c3e50; }

/* Кнопка обновления */
.refresh-btn {
  padding: 10px 20px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.refresh-btn:hover:not(:disabled) { background: #2980b9; }
.refresh-btn:disabled { background: #ccc; cursor: not-allowed; }

/* Состояния */
.loading { text-align: center; padding: 40px; color: #7f8c8d; }
.error {
  color: #e74c3c;
  padding: 15px;
  background: #fde8e8;
  border-radius: 4px;
  text-align: center;
}

/* Сетка книг */
.books-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

/* Карточка книги */
.book-card {
  border: 1px solid #e0e0e0;
  padding: 20px;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
.book-card h3 { margin: 0 0 15px; color: #2c3e50; }
.book-card p { margin: 8px 0; color: #555; }

/* Информация о доступных экземплярах */
.copies-info {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: space-between;
}
.copies-label { font-weight: 600; color: #34495e; }
.copies-count {
  font-weight: bold;
  color: #27ae60;
  padding: 4px 12px;
  background: #e8f8f5;
  border-radius: 20px;
}
.copies-zero { color: #e74c3c; background: #fde8e8; }
</style>