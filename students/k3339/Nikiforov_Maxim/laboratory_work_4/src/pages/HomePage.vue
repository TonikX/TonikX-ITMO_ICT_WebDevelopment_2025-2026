<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { request } from '../shared/api/client'
import type { Paginated } from '../shared/api/library'

const stats = ref({ books: 0, readers: 0, rooms: 0, assignments: 0 })
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const [booksRes, readersRes, roomsRes, assignRes] = await Promise.all([
      request<Paginated<unknown>>('/api/books/', { params: { is_active: 'true' } }),
      request<Paginated<unknown>>('/api/readers/', { params: { is_active: 'true' } }),
      request<Paginated<unknown>>('/api/reading-rooms/'),
      request<Paginated<unknown>>('/api/book-assignments/', { params: { is_returned: 'false' } }),
    ])
    stats.value = {
      books: booksRes.data.count ?? booksRes.data.results?.length ?? 0,
      readers: readersRes.data.count ?? readersRes.data.results?.length ?? 0,
      rooms: roomsRes.data.count ?? roomsRes.data.results?.length ?? 0,
      assignments: assignRes.data.count ?? assignRes.data.results?.length ?? 0,
    }
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Ошибка загрузки'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div>
    <h1 class="text-h4 mb-4">Главная</h1>
    <v-alert v-if="error" type="error">{{ error }}</v-alert>
    <v-progress-linear v-if="loading" indeterminate />
    <v-row v-else>
      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-title>Книги</v-card-title>
          <v-card-text class="text-h4">{{ stats.books }}</v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-title>Читатели</v-card-title>
          <v-card-text class="text-h4">{{ stats.readers }}</v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-title>Читальные залы</v-card-title>
          <v-card-text class="text-h4">{{ stats.rooms }}</v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-title>Активные закрепления</v-card-title>
          <v-card-text class="text-h4">{{ stats.assignments }}</v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>
