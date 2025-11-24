<template>
  <div>
    <h1 class="text-h4 mb-4">Добро пожаловать!</h1>
    <v-row>
      <v-col v-for="item in stats" :key="item.title" cols="12" md="3">
        <v-card>
          <v-card-title>{{ item.title }}</v-card-title>
          <v-card-text class="text-h5">{{ item.count }}</v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <h2 class="text-h5 mt-6 mb-4">Отчёт за последний квартал</h2>
    <v-data-table :headers="reportHeaders" :items="quarterReport" :loading="loading">
      <template #item.total_cost="{ item }">{{ item.total_cost }} ₽</template>
      <template #bottom>
        <div class="pa-4 text-right font-weight-bold">
          Итого: {{ totalCost }} ₽
        </div>
      </template>
    </v-data-table>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/api'

const stats = ref([
  { title: 'Клиенты', count: 0 },
  { title: 'Услуги', count: 0 },
  { title: 'Заказы', count: 0 },
  { title: 'Платежи', count: 0 }
])
const quarterReport = ref([])
const loading = ref(false)

const reportHeaders = [
  { title: 'Исполнитель', key: 'executor_name' },
  { title: 'Стоимость работ', key: 'total_cost' }
]

const totalCost = computed(() =>
  quarterReport.value.reduce((sum, r) => sum + parseFloat(r.total_cost || 0), 0)
)

onMounted(async () => {
  loading.value = true
  const [clients, services, orders, payments, report] = await Promise.all([
    api.get('/clients/'), api.get('/services/'), api.get('/orders/'), api.get('/payments/'),
    api.get('/payments/quarter_report/')
  ])
  stats.value[0].count = clients.data.count ?? clients.data.length
  stats.value[1].count = services.data.count ?? services.data.length
  stats.value[2].count = orders.data.count ?? orders.data.length
  stats.value[3].count = payments.data.count ?? payments.data.length
  quarterReport.value = report.data.results || report.data
  loading.value = false
})
</script>
