<template>
  <div>
    <h1 class="text-h4 mb-4">Отчеты</h1>
    <v-card>
      <v-tabs v-model="tab" bg-color="primary">
        <v-tab value="yearly">Статистика за год</v-tab>
        <v-tab value="quarterly">Квартальный отчет</v-tab>
        <v-tab value="managers">Топ менеджеры</v-tab>
      </v-tabs>

      <v-card-text>
        <v-window v-model="tab">
          <!-- Годовая статистика -->
          <v-window-item value="yearly">
             <div class="mb-4 text-h6">Контракты за последний год</div>
             <v-btn size="small" class="mb-2" @click="fetchYearly">Обновить</v-btn>
             <v-table>
                <thead>
                    <tr>
                        <th>Месяц</th>
                        <th>Количество</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(item, index) in yearlyData" :key="index">
                        <td>{{ item.month || 'Неизвестно' }}</td>
                        <td>{{ item.count || item.total || 0 }}</td>
                    </tr>
                    <tr v-if="yearlyData.length === 0">
                        <td colspan="2">Нет данных (или проверьте формат ответа)</td>
                    </tr>
                </tbody>
             </v-table>
          </v-window-item>

          <!-- Квартальный отчет -->
          <v-window-item value="quarterly">
            <div class="mb-4 text-h6">Квартальный отчет</div>
            <v-btn size="small" class="mb-2" @click="fetchQuarterly">Обновить</v-btn>
            <v-data-table
                :headers="quarterlyHeaders"
                :items="quarterlyData"
                class="elevation-1"
            ></v-data-table>
          </v-window-item>

          <!-- Топ менеджеры -->
          <v-window-item value="managers">
            <div class="mb-4 text-h6">Топ менеджеры</div>
            <v-row dense class="mb-4 align-center">
                <v-col cols="12" md="4">
                    <v-text-field type="date" label="Дата начала" v-model="managerRange.start" hide-details></v-text-field>
                </v-col>
                <v-col cols="12" md="4">
                    <v-text-field type="date" label="Дата окончания" v-model="managerRange.end" hide-details></v-text-field>
                </v-col>
                <v-col cols="12" md="2">
                    <v-btn color="primary" @click="fetchManagers">Загрузить</v-btn>
                </v-col>
            </v-row>

            <v-data-table
                :headers="managerHeaders"
                :items="managerData"
                class="elevation-1"
            ></v-data-table>
          </v-window-item>
        </v-window>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import typography from '@/api/typography'
import { useAlertStore } from '@/stores/alert'

const alertStore = useAlertStore()

const tab = ref('yearly')
const loading = ref(false)

// Yearly
const yearlyData = ref([])
const fetchYearly = async () => {
    try {
        const res = await typography.getYearlyStats()
        yearlyData.value = res.data
    } catch (e) {
        console.error(e)
        alertStore.showError(e)
    }
}

// Quarterly
const quarterlyData = ref([])
const quarterlyHeaders = [
    { title: '№ Контракта', key: 'contract_number' },
    { title: 'Книга', key: 'book_title' },
    { title: 'Дата', key: 'date' },
    { title: 'Страницы', key: 'pages' },
    { title: 'Авторов', key: 'authors_count' },
    { title: 'Редакторов', key: 'editors_count' },
]

const fetchQuarterly = async () => {
    try {
        const res = await typography.getQuarterlyReport()
        if (res.data && Array.isArray(res.data.details)) {
             quarterlyData.value = res.data.details
        } else {
             quarterlyData.value = []
        }
    } catch (e) {
        console.error(e)
        alertStore.showError(e)
    }
}

// Managers
const managerData = ref([])
const managerRange = ref({
    start: new Date(new Date().setMonth(new Date().getMonth() - 1)).toISOString().substring(0, 10),
    end: new Date().toISOString().substring(0, 10)
})
const managerHeaders = [
    { title: 'ID', key: 'id' },
    { title: 'Имя пользователя', key: 'username' },
    { title: 'Имя', key: 'first_name' },
    { title: 'Фамилия', key: 'last_name' },
]

const fetchManagers = async () => {
    try {
        const res = await typography.getTopManagers(managerRange.value.start, managerRange.value.end)
        if (Array.isArray(res.data)) {
             managerData.value = res.data
        } else if (res.data && Array.isArray(res.data.managers)) {
             managerData.value = res.data.managers
        } else if (res.data && Array.isArray(res.data.results)) {
             managerData.value = res.data.results
        } else {
             managerData.value = []
        }
    } catch (e) {
        console.error(e)
        alertStore.showError(e)
    }
}

watch(tab, (val) => {
    if (val === 'yearly' && yearlyData.value.length === 0) fetchYearly()
    if (val === 'quarterly' && quarterlyData.value.length === 0) fetchQuarterly()
    if (val === 'managers' && managerData.value.length === 0) fetchManagers()
})

onMounted(() => {
    fetchYearly()
})
</script>
