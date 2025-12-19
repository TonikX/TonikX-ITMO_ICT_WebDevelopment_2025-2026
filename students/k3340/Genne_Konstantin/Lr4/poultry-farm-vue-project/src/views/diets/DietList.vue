<template>
  <v-container>
    <v-card>
      <v-card-title>Диеты</v-card-title>
      <v-card-actions>
        <v-btn to="/diets/new" color="primary">Добавить диету</v-btn>
      </v-card-actions>
      <v-table>
        <thead>
          <tr>
            <th>Номер</th>
            <th>Описание</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>{{ item.number }}</td>
            <td>{{ item.structure }}</td>
            <td>
              <v-btn size="small" :to="`/diets/${item.id}/edit`" class="me-2">Редактировать</v-btn>
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
import { getDiets, deleteDiet } from '@/api/diets'

const items = ref([])

onMounted(async () => {
  items.value = await getDiets()
})

const deleteItem = async (id) => {
  if (confirm('Вы уверены?')) {
    try {
      await deleteDiet(id)
      items.value = items.value.filter(i => i.id !== id)
      // Уведомление о успешном удалении убрано
    } catch (err) {
      // Обработка ошибок оставлена, но без Snackbar
      console.error(err.response?.data?.error || 'Ошибка удаления')
      alert(err.response?.data?.error || 'Ошибка удаления')
    }
  }
}
</script>