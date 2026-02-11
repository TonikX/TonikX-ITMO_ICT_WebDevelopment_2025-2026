<template>
  <div class="books-view">
    <div class="header">
      <h1>Книги в библиотеке</h1>
      <button @click="loadBooks" :disabled="loading" class="refresh-btn">
        {{ loading ? 'Обновление...' : 'Обновить' }}
      </button>
    </div>

    <div v-if="loading" class="loading">Загрузка книг...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else class="books-list">
      <div v-for="book in books" :key="book.book_id" class="book-card">
        <h3>{{ book.title }}</h3>
        <p><strong>Год:</strong> {{ book.publication_year }}</p>
        <p><strong>Издательство:</strong> {{ book.publisher }}</p>
        <p><strong>Раздел:</strong> {{ book.section }}</p>
        <p><strong>Инв. номер:</strong> {{ book.inventory_code }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '../api/client'

const books = ref([])
const loading = ref(false)
const error = ref(null)

const loadBooks = async () => {
  loading.value = true
  error.value = null

  try {
    const response = await apiClient.get('books/')
    books.value = response.data
  } catch (err) {
    error.value = 'Не удалось загрузить книги'
    console.error('Ошибка загрузки книг:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadBooks()
})
</script>

<style scoped>
.books-view {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header h1 {
  margin: 0;
  color: #2c3e50;
}

.refresh-btn {
  padding: 10px 20px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.refresh-btn:hover:not(:disabled) {
  background: #2980b9;
}

.refresh-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
  font-size: 18px;
}

.error {
  color: #e74c3c;
  padding: 15px;
  background: #fde8e8;
  border-radius: 4px;
  text-align: center;
}

.books-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.book-card {
  border: 1px solid #e0e0e0;
  padding: 20px;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.book-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}

.book-card h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #2c3e50;
  font-size: 18px;
}

.book-card p {
  margin: 8px 0;
  color: #555;
  font-size: 14px;
}

.book-card strong {
  color: #34495e;
}
</style>