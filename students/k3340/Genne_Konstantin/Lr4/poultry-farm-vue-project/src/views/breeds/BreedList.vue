<template>
  <v-container>
    <v-card>
      <v-card-title>Породы</v-card-title>
      <v-card-actions>
        <v-btn to="/breeds/new" color="primary">Добавить породу</v-btn>
      </v-card-actions>
      <v-table>
        <thead>
          <tr>
            <th>Название</th>
            <th>Яйценоскость</th>
            <th>Вес (г)</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>{{ item.name }}</td>
            <td>{{ item.efficiency }}</td>
            <td>{{ item.mean_weight }}</td>
            <td>
              <v-btn size="small" :to="`/breeds/${item.id}/edit`" class="me-2">Редактировать</v-btn>
              <v-btn size="small" color="error" @click="deleteItem(item.id)">Удалить</v-btn>
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getBreeds, deleteBreed } from '@/api/breeds'

const items = ref([])

onMounted(async () => {
  items.value = await getBreeds()
})

const deleteItem = async (id) => {
  if (confirm('Вы уверены?')) {
    try {
      await deleteBreed(id)
      items.value = items.value.filter(i => i.id !== id)
    } catch (err) {
      console.error(err.response?.data?.error || 'Ошибка удаления')
      alert(err.response?.data?.error || 'Ошибка удаления')
    }
  }
}
</script>