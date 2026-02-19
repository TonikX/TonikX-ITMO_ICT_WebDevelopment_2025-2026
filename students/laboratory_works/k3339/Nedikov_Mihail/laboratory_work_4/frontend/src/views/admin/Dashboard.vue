<template>
  <div>
    <h1 class="text-h4 mb-6">Админ-панель лизинга авто</h1>

    <!-- Статистика -->
    <v-row class="mb-6">
      <v-col cols="12" md="3">
        <v-card color="blue" dark>
          <v-card-title class="text-h6">
            <v-icon class="mr-2">mdi-car</v-icon>
            Автомобили
          </v-card-title>
          <v-card-text class="text-h4 text-center">
            {{ stats.cars || 0 }}
          </v-card-text>
          <v-card-actions>
            <v-btn text @click="$router.push('/admin/cars')">
              Управление
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" md="3">
        <v-card color="orange" dark>
          <v-card-title class="text-h6">
            <v-icon class="mr-2">mdi-file-document</v-icon>
            Заявки
          </v-card-title>
          <v-card-text class="text-h4 text-center">
            {{ stats.applications || 0 }}
          </v-card-text>
          <v-card-actions>
            <v-btn text @click="$router.push('/admin/applications')">
              Просмотр
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" md="3">
        <v-card color="green" dark>
          <v-card-title class="text-h6">
            <v-icon class="mr-2">mdi-file-sign</v-icon>
            Договоры
          </v-card-title>
          <v-card-text class="text-h4 text-center">
            {{ stats.leases || 0 }}
          </v-card-text>
          <v-card-actions>
            <v-btn text @click="$router.push('/admin/leases')">
              Управление
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" md="3">
        <v-card color="purple" dark>
          <v-card-title class="text-h6">
            <v-icon class="mr-2">mdi-account-group</v-icon>
            Клиенты
          </v-card-title>
          <v-card-text class="text-h4 text-center">
            {{ stats.clients || 0 }}
          </v-card-text>
          <v-card-actions>
            <v-btn text @click="$router.push('/admin/clients')">
              Список
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Быстрые действия -->
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>Быстрые действия</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="4">
                <v-card hover @click="$router.push('/admin/cars/new')" class="pa-4 text-center">
                  <v-icon size="48" color="primary" class="mb-2">mdi-car-plus</v-icon>
                  <div class="text-h6">Добавить автомобиль</div>
                  <div class="text-body-2 text-grey">Добавление нового автомобиля в автопарк</div>
                </v-card>
              </v-col>

              <v-col cols="12" md="4">
                <v-card hover @click="$router.push('/admin/applications')" class="pa-4 text-center">
                  <v-icon size="48" color="primary" class="mb-2">mdi-file-check</v-icon>
                  <div class="text-h6">Обработать заявки</div>
                  <div class="text-body-2 text-grey">Просмотр и одобрение заявок на аренду</div>
                </v-card>
              </v-col>

              <v-col cols="12" md="4">
                <v-card hover @click="$router.push('/admin/leases')" class="pa-4 text-center">
                  <v-icon size="48" color="primary" class="mb-2">mdi-file-edit</v-icon>
                  <div class="text-h6">Управление договорами</div>
                  <div class="text-body-2 text-grey">Изменение статусов договоров аренды</div>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Последние заявки -->
    <v-row class="mt-6">
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <v-icon class="mr-2">mdi-history</v-icon>
            Последние заявки
            <v-spacer></v-spacer>
            <v-btn small @click="$router.push('/admin/applications')">Все заявки</v-btn>
          </v-card-title>
          <v-card-text>
            <v-data-table
                :headers="applicationHeaders"
                :items="recentApplications"
                :loading="loading"
                hide-default-footer
                class="elevation-1"
            >
              <template v-slot:item.created_at="{ item }">
                {{ formatDateTime(item.created_at) }}
              </template>
              <template v-slot:item.actions="{ item }">
                <v-btn
                    small
                    color="primary"
                    @click="$router.push(`/admin/applications/${item.id}`)"
                >
                  Просмотр
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Dashboard',
  data() {
    return {
      stats: {
        cars: 0,
        applications: 0,
        leases: 0,
        clients: 0
      },
      recentApplications: [],
      loading: false,
      applicationHeaders: [
        { text: 'ID', value: 'id' },
        { text: 'Автомобиль', value: 'car.make' },
        { text: 'Клиент', value: 'client.company_name' },
        { text: 'Дата подачи', value: 'created_at' },
        { text: 'Действия', value: 'actions', sortable: false }
      ]
    }
  },
  methods: {
    async fetchStats() {
      try {
        this.loading = true

        // Загрузка статистики (можно объединить в один endpoint)
        const [carsRes, appsRes, leasesRes, clientsRes] = await Promise.all([
          axios.get('admin/cars/').catch(() => ({ data: { cars: [] } })),
          axios.get('admin/lease_applications/').catch(() => ({ data: { applications: [] } })),
          axios.get('admin/leases/').catch(() => ({ data: [] })),
          axios.get('admin/clients/').catch(() => ({ data: { clients: [] } }))
        ])

        this.stats.cars = carsRes.data.cars?.length || 0
        this.stats.applications = appsRes.data.applications?.length || 0
        this.stats.leases = leasesRes.data?.length || 0
        this.stats.clients = clientsRes.data.clients?.length || 0

        // Последние 5 заявок
        this.recentApplications = appsRes.data.applications?.slice(0, 5) || []

      } catch (error) {
        console.error('Ошибка загрузки статистики:', error)
      } finally {
        this.loading = false
      }
    },
    formatDateTime(dateTimeString) {
      if (!dateTimeString) return '—'
      return new Date(dateTimeString).toLocaleString('ru-RU')
    }
  },
  mounted() {
    this.fetchStats()
  }
}
</script>