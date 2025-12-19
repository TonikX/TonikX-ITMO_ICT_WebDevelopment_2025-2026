<template>
  <div>
    <!-- Навигация -->
    <v-row class="mb-4">
      <v-col cols="12">
        <v-btn @click="$router.push(`/admin/cars/${carId}`)" color="secondary" class="mr-2">
          <v-icon left>mdi-arrow-left</v-icon>
          Назад к автомобилю
        </v-btn>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="headline">
            <v-icon class="mr-2">mdi-history</v-icon>
            История аренд автомобиля
          </v-card-title>

          <v-card-subtitle v-if="car">
            {{ car.make }} {{ car.model }} ({{ car.license_plate }})
          </v-card-subtitle>

          <v-card-text v-if="loading">
            <v-progress-linear indeterminate></v-progress-linear>
            <div class="text-center mt-4">Загрузка истории аренд...</div>
          </v-card-text>

          <v-card-text v-else>
            <v-alert v-if="leasings.length === 0" type="info">
              У этого автомобиля ещё не было аренд
            </v-alert>

            <v-data-table
                v-else
                :headers="headers"
                :items="leasings"
                :items-per-page="10"
                class="elevation-1"
            >
              <template v-slot:item.client="{ item }">
                <div>
                  <strong>{{ item.client.company_name }}</strong>
                  <div class="text-caption">ИНН: {{ item.client.inn }}</div>
                </div>
              </template>

              <template v-slot:item.dates="{ item }">
                <div>
                  <div>С: {{ formatDate(item.start_date) }}</div>
                  <div v-if="item.end_date">По: {{ formatDate(item.end_date) }}</div>
                  <div v-else class="text-grey">Без срока</div>
                </div>
              </template>

              <template v-slot:item.payment="{ item }">
                <div>
                  <strong>{{ parseFloat(item.monthly_payment).toFixed(2) }} ₽/мес</strong>
                  <div class="text-caption">
                    Итого: ~{{ calculateTotal(item) }} ₽
                  </div>
                </div>
              </template>

              <template v-slot:item.status="{ item }">
                <v-chip :color="getStatusColor(item.status)" dark small>
                  {{ getStatusText(item.status) }}
                </v-chip>
              </template>

              <template v-slot:item.actions="{ item }">
                <v-btn
                    color="primary"
                    small
                    @click="$router.push(`/admin/leases/${item.id}`)"
                >
                  <v-icon small>mdi-eye</v-icon>
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
  name: 'CarLeasings',
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      car: null,
      leasings: [],
      loading: true,
      headers: [
        { text: 'ID', value: 'id', width: '80px' },
        { text: 'Клиент', value: 'client' },
        { text: 'Даты аренды', value: 'dates' },
        { text: 'Оплата', value: 'payment' },
        { text: 'Статус', value: 'status' },
        { text: 'Создан', value: 'created_at' },
        { text: 'Действия', value: 'actions', sortable: false, width: '80px' }
      ]
    }
  },
  computed: {
    carId() {
      return parseInt(this.id)
    }
  },
  methods: {
    async fetchData() {
      try {
        this.loading = true

        // Загружаем данные авто и историю аренд
        const [carResponse, leasingsResponse] = await Promise.all([
          axios.get(`admin/cars/${this.carId}/`),
          axios.get(`admin/cars/${this.carId}/leasings`)
        ])

        this.car = carResponse.data.car
        this.leasings = leasingsResponse.data.leasings

        console.log('История аренд загружена:', this.leasings.length)

      } catch (error) {
        console.error('Ошибка загрузки данных:', error)
      } finally {
        this.loading = false
      }
    },

    getStatusColor(status) {
      const colors = {
        'active': 'green',
        'completed': 'blue',
        'cancelled': 'red'
      }
      return colors[status] || 'grey'
    },

    getStatusText(status) {
      const texts = {
        'active': 'Активный',
        'completed': 'Завершён',
        'cancelled': 'Отменён'
      }
      return texts[status] || status
    },

    formatDate(dateString) {
      if (!dateString) return '—'
      return new Date(dateString).toLocaleDateString('ru-RU')
    },

    calculateTotal(lease) {
      if (!lease.start_date || !lease.end_date || !lease.monthly_payment) {
        return '0.00'
      }

      const start = new Date(lease.start_date)
      const end = new Date(lease.end_date)
      const monthly = parseFloat(lease.monthly_payment)

      if (isNaN(monthly) || monthly <= 0) return '0.00'

      const months = Math.ceil((end - start) / (1000 * 60 * 60 * 24 * 30.44))
      const total = months * monthly

      return total.toFixed(2)
    }
  },

  mounted() {
    this.fetchData()
  }
}
</script>