<template>
  <div>
    <v-row class="mb-4">
      <v-col cols="12">
        <v-card>
          <v-card-title class="headline">
            <v-icon class="mr-2">mdi-file-document</v-icon>
            Заявки на аренду автомобилей
          </v-card-title>

          <v-card-subtitle>
            Всего заявок: {{ applications.length }}
          </v-card-subtitle>

          <v-card-text v-if="loading">
            <v-progress-linear indeterminate></v-progress-linear>
            <div class="text-center mt-4">Загрузка заявок...</div>
          </v-card-text>

          <v-card-text v-else>
            <v-data-table
                :headers="headers"
                :items="applications"
                :items-per-page="10"
                class="elevation-1"
            >
              <template v-slot:item.car="{ item }">
                <div>
                  <strong>{{ item.car.make }} {{ item.car.model }}</strong>
                  <div class="text-caption">{{ item.car.license_plate }}</div>
                </div>
              </template>

              <template v-slot:item.client="{ item }">
                <div>
                  <strong>{{ item.client.company_name }}</strong>
                  <div class="text-caption">ИНН: {{ item.client.inn }}</div>
                </div>
              </template>

              <template v-slot:item.created_at="{ item }">
                {{ formatDateTime(item.created_at) }}
              </template>

              <template v-slot:item.actions="{ item }">
                <v-btn
                    color="primary"
                    small
                    @click="$router.push(`/admin/applications/${item.id}`)"
                >
                  <v-icon small>mdi-eye</v-icon>
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
  name: 'AdminApplicationList',
  data() {
    return {
      applications: [],
      loading: true,
      error: null,
      headers: [
        { text: 'ID', value: 'id', width: '80px' },
        { text: 'Автомобиль', value: 'car' },
        { text: 'Клиент', value: 'client' },
        { text: 'Дата подачи', value: 'created_at' },
        { text: 'Действия', value: 'actions', sortable: false, width: '120px' }
      ]
    }
  },
  methods: {
    async fetchApplications() {
      try {
        this.loading = true
        const response = await axios.get('admin/lease_applications/')
        this.applications = response.data.applications
        console.log('Заявки загружены:', this.applications.length)
      } catch (error) {
        console.error('Ошибка загрузки заявок:', error)
        this.error = 'Не удалось загрузить список заявок'
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
    this.fetchApplications()
  }
}
</script>