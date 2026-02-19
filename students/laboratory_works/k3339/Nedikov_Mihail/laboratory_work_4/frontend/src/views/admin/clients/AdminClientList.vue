<template>
  <div>
    <v-row class="mb-4">
      <v-col cols="12">
        <v-card>
          <v-card-title class="headline">
            <v-icon class="mr-2">mdi-account-group</v-icon>
            Клиенты компании
          </v-card-title>

          <v-card-subtitle>
            Всего клиентов: {{ clients.length }}
          </v-card-subtitle>

          <v-card-text v-if="loading">
            <v-progress-linear indeterminate></v-progress-linear>
            <div class="text-center mt-4">Загрузка клиентов...</div>
          </v-card-text>

          <v-card-text v-else>
            <!-- Таблица клиентов -->
            <table class="elevation-1" style="width: 100%; border-collapse: collapse; background-color: white;">
              <thead>
              <tr style="background-color: #f5f5f5;">
                <th style="width: 5%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">ID</th>
                <th style="width: 20%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Компания</th>
                <th style="width: 15%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Email</th>
                <th style="width: 20%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Контактная информация</th>
                <th style="width: 15%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Адрес</th>
                <th style="width: 10%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Активен</th>
                <th style="width: 10%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Дата регистрации</th>
                <th style="width: 5%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Действия</th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="item in clients" :key="item.id" style="border-bottom: 1px solid #e0e0e0;">
                <td style="width: 5%; padding: 12px; text-align: center;">{{ item.id || '-' }}</td>
                <td style="width: 20%; padding: 12px; text-align: center;">
                  <div>
                    <strong>{{ item.company_name || '-' }}</strong>
                    <div class="text-caption">ИНН: {{ item.inn || '-' }}</div>
                  </div>
                </td>
                <td style="width: 15%; padding: 12px; text-align: center;">{{ item.email || '-' }}</td>
                <td style="width: 20%; padding: 12px; text-align: center;">
                  <div v-if="item.contact_person || item.phone">
                    <div v-if="item.contact_person">{{ item.contact_person }}</div>
                    <div v-if="item.phone">{{ item.phone }}</div>
                  </div>
                  <div v-else class="text-grey">—</div>
                </td>
                <td style="width: 15%; padding: 12px; text-align: center;">{{ item.address || '-' }}</td>
                <td style="width: 10%; padding: 12px; text-align: center;">
                  <v-icon v-if="item.is_active" color="green">mdi-check-circle</v-icon>
                  <v-icon v-else color="red">mdi-close-circle</v-icon>
                </td>
                <td style="width: 10%; padding: 12px; text-align: center;">
                  {{ formatDateTime(item.created_at) }}
                </td>
                <td style="width: 5%; padding: 12px; text-align: center;">
                  <v-btn
                      color="primary"
                      small
                      @click="$router.push(`/admin/clients/${item.id}`)"
                  >
                    <v-icon small>mdi-eye</v-icon>
                  </v-btn>
                </td>
              </tr>
              <tr v-if="clients.length === 0">
                <td colspan="8" style="padding: 16px; text-align: center; color: #9E9E9E;">
                  Нет клиентов для отображения
                </td>
              </tr>
              </tbody>
            </table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminClientList',
  data() {
    return {
      clients: [],
      loading: true,
    }
  },
  methods: {
    async fetchClients() {
      try {
        this.loading = true
        const response = await axios.get('admin/clients/')
        this.clients = response.data.clients
        console.log('Клиенты загружены:', this.clients.length)
      } catch (error) {
        console.error('Ошибка загрузки клиентов:', error)
      } finally {
        this.loading = false
      }
    },
    formatDateTime(dateTimeString) {
      if (!dateTimeString) return '—'
      return new Date(dateTimeString).toLocaleDateString('ru-RU')
    }
  },
  mounted() {
    this.fetchClients()
  }
}
</script>