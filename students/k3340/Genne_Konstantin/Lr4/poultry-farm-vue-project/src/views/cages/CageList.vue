<template>
  <v-container>
    <v-card>
      <v-card-title>Клетки</v-card-title>
      <v-card-actions>
        <v-btn to="/cages/new" color="primary">Добавить клетку</v-btn>
      </v-card-actions>
      <v-table>
        <thead>
          <tr>
            <th>Клетка</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>
              Цех {{ item.workshop_number }}, ряд {{ item.row_number }}, клетка {{ item.in_row_number }}
            </td>
            <td>
              <!-- Кнопка "Подробнее" -->
              <v-btn
                size="small"
                variant="text"
                color="primary"
                :to="`/cages/${item.id}`"
                class="me-2"
              >
                Подробнее
              </v-btn>
              <!-- Кнопка "Удалить" -->
              <v-btn
                size="small"
                color="error"
                @click="deleteItem(item.id)"
              >
                Удалить
              </v-btn>
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getCages, deleteCage } from '@/api/cages'

const items = ref([])

onMounted(async () => {
  items.value = await getCages()
})

const deleteItem = async (id) => {
  if (confirm('Вы уверены?')) {
    try {
      await deleteCage(id)
      items.value = items.value.filter(i => i.id !== id)
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Нельзя удалить клетку с курами или работниками'
      console.error(errorMsg)
      alert(errorMsg)
    }
  }
}
</script>