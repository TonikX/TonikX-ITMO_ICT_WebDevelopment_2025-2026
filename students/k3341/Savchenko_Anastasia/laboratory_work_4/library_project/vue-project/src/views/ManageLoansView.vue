<template>
  <div class="manage-loans-view">
    <h1>Управление выдачами книг</h1>

    <div v-if="!isAdmin" class="not-admin">
      <p>Эта страница доступна только администраторам.</p>
    </div>

    <div v-else>
      <div class="controls">
        <button @click="loadData" :disabled="loading" class="refresh-btn">
          {{ loading ? 'Загрузка...' : 'Обновить данные' }}
        </button>
      </div>

      <div v-if="loading" class="loading">Загрузка данных...</div>
      <div v-else-if="error" class="error">{{ error }}</div>

      <div v-else class="dashboard">
        <!-- Статистика -->
        <div class="stats">
          <div class="stat-card">
            <h3>Всего читателей</h3>
            <p class="stat-number">{{ readers.length }}</p>
          </div>
          <div class="stat-card">
            <h3>Всего книг</h3>
            <p class="stat-number">{{ books.length }}</p>
          </div>
          <div class="stat-card">
            <h3>Доступные экземпляры</h3>
            <p class="stat-number">{{ availableCopies }}</p>
          </div>
        </div>

        <!-- Информация -->
        <div class="info-section">
          <h2>Информация для администратора</h2>
          <p>Для управления выдачами книг используйте админ-панель Django:</p>
          <a href="http://127.0.0.1:8000/admin/" target="_blank" class="admin-link">
            Перейти в админ-панель
          </a>

          <div class="api-endpoints">
            <h3>Доступные API эндпоинты:</h3>
            <ul>
              <li><strong>/api/reader/register/</strong> - Зарегистрировать нового читателя</li>
              <li><strong>/api/books/decommission/</strong> - Списать книгу</li>
              <li><strong>/api/books/add/</strong> - Добавить книгу в фонд</li>
              <li><strong>/api/copies/transfer-hall/</strong> - Переместить книгу между залами</li>
              <li><strong>/api/books/&lt;id&gt;/update-code/</strong> - Изменить шифр книги</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import apiClient from '../api/client'

const auth = useAuthStore()
const isAdmin = computed(() => auth.isAdmin)

const readers = ref([])
const books = ref([])
const copies = ref([])
const loading = ref(false)
const error = ref(null)

const availableCopies = computed(() => {
  return copies.value.filter(copy =>
    copy.availability_status === 'available'
  ).length
})

const loadData = async () => {
  if (!isAdmin.value) return

  loading.value = true
  error.value = null

  try {
    // Загружаем все данные параллельно
    const [readersRes, booksRes, copiesRes] = await Promise.all([
      apiClient.get('readers/'),
      apiClient.get('books/'),
      apiClient.get('copies/')
    ])

    readers.value = readersRes.data || []
    books.value = booksRes.data || []
    copies.value = copiesRes.data || []

  } catch (err) {
    console.error('Ошибка загрузки данных:', err)
    error.value = 'Не удалось загрузить данные'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (isAdmin.value) {
    loadData()
  }
})
</script>

<style scoped>
.manage-loans-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.not-admin {
  text-align: center;
  padding: 40px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
  color: #6c757d;
}

.controls {
  margin-bottom: 20px;
  display: flex;
  justify-content: flex-end;
}

.refresh-btn {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.refresh-btn:hover:not(:disabled) {
  background: #0069d9;
}

.refresh-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #6c757d;
}

.error {
  padding: 15px;
  background: #f8d7da;
  color: #721c24;
  border-radius: 4px;
  border: 1px solid #f5c6cb;
}

.dashboard {
  margin-top: 30px;
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  padding: 25px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  text-align: center;
  border: 1px solid #e9ecef;
}

.stat-card h3 {
  margin: 0 0 15px 0;
  color: #495057;
  font-size: 16px;
}

.stat-number {
  font-size: 36px;
  font-weight: bold;
  color: #007bff;
  margin: 0;
}

.info-section {
  padding: 30px;
  background: #e8f4fd;
  border-radius: 8px;
  border: 1px solid #b3d7ff;
}

.info-section h2 {
  color: #0056b3;
  margin-bottom: 15px;
}

.info-section p {
  color: #495057;
  margin-bottom: 20px;
}

.admin-link {
  display: inline-block;
  padding: 12px 24px;
  background: #28a745;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 500;
  margin-bottom: 30px;
}

.admin-link:hover {
  background: #218838;
}

.api-endpoints {
  margin-top: 30px;
  padding: 20px;
  background: white;
  border-radius: 6px;
  border: 1px solid #dee2e6;
}

.api-endpoints h3 {
  color: #495057;
  margin-bottom: 15px;
}

.api-endpoints ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.api-endpoints li {
  padding: 10px 0;
  border-bottom: 1px solid #f1f3f4;
  color: #6c757d;
}

.api-endpoints li:last-child {
  border-bottom: none;
}

.api-endpoints strong {
  color: #212529;
  font-family: monospace;
}

@media (max-width: 768px) {
  .stats {
    grid-template-columns: 1fr;
  }
}
</style>