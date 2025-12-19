<template>
  <div>
    <!-- Навигация -->
    <v-row class="mb-4">
      <v-col cols="12">
        <v-btn @click="$router.push('/admin/leases')" color="secondary" class="mr-2">
          <v-icon left>mdi-arrow-left</v-icon>
          К списку договоров
        </v-btn>

        <v-btn
            @click="$router.push(`/admin/cars/${lease.car.id}`)"
            color="primary"
            class="mr-2"
            v-if="lease"
        >
          <v-icon left>mdi-car</v-icon>
          К автомобилю
        </v-btn>
      </v-col>
    </v-row>

    <!-- Загрузка -->
    <v-row v-if="loading">
      <v-col cols="12">
        <v-progress-linear indeterminate color="primary"></v-progress-linear>
        <div class="text-center mt-4">Загрузка данных договора...</div>
      </v-col>
    </v-row>

    <!-- Основная информация -->
    <v-row v-else-if="lease">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title class="headline">
            Договор аренды #{{ lease.id }}
            <v-chip class="ml-4" :color="getStatusColor(lease.status)" dark large>
              {{ getStatusText(lease.status) }}
            </v-chip>
          </v-card-title>

          <v-card-subtitle>
            Создан: {{ formatDateTime(lease.created_at) }}
          </v-card-subtitle>

          <v-divider class="my-4"></v-divider>

          <v-card-text>
            <!-- Информация об автомобиле -->
            <h3 class="text-h6 mb-3">
              <v-icon class="mr-2">mdi-car</v-icon>
              Автомобиль
            </h3>

            <v-card outlined class="mb-6">
              <v-card-text>
                <v-row>
                  <v-col cols="6" md="4">
                    <v-list-item>
                      <v-list-item-title>Марка/Модель</v-list-item-title>
                      <v-list-item-subtitle class="text-h6">
                        {{ lease.car.make }} {{ lease.car.model }}
                      </v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="6" md="4">
                    <v-list-item>
                      <v-list-item-title>Гос. номер</v-list-item-title>
                      <v-list-item-subtitle class="text-h6">
                        {{ lease.car.license_plate }}
                      </v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="6" md="4">
                    <v-list-item>
                      <v-list-item-title>Статус авто</v-list-item-title>
                      <v-list-item-subtitle>
                        <v-chip :color="getCarStatusColor(lease.car.status)" dark small>
                          {{ getCarStatusText(lease.car.status) }}
                        </v-chip>
                      </v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="6" md="4">
                    <v-list-item>
                      <v-list-item-title>Год выпуска</v-list-item-title>
                      <v-list-item-subtitle>{{ lease.car.year }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="6" md="4">
                    <v-list-item>
                      <v-list-item-title>VIN</v-list-item-title>
                      <v-list-item-subtitle>{{ lease.car.vin }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="6" md="4">
                    <v-list-item>
                      <v-list-item-title>Пробег</v-list-item-title>
                      <v-list-item-subtitle>{{ lease.car.current_mileage?.toLocaleString() || '0' }} км</v-list-item-subtitle>
                    </v-list-item>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>

            <!-- Информация о клиенте -->
            <h3 class="text-h6 mb-3">
              <v-icon class="mr-2">mdi-account-group</v-icon>
              Клиент
            </h3>

            <v-card outlined class="mb-6">
              <v-card-text>
                <v-row>
                  <v-col cols="12" md="6">
                    <v-list-item>
                      <v-list-item-title>Название компании</v-list-item-title>
                      <v-list-item-subtitle class="text-h6">
                        {{ lease.client.company_name }}
                      </v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="12" md="6">
                    <v-list-item>
                      <v-list-item-title>ИНН</v-list-item-title>
                      <v-list-item-subtitle class="text-h6">
                        {{ lease.client.inn }}
                      </v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="12" md="6" v-if="lease.client.contact_person">
                    <v-list-item>
                      <v-list-item-title>Контактное лицо</v-list-item-title>
                      <v-list-item-subtitle>{{ lease.client.contact_person }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="12" md="6" v-if="lease.client.email">
                    <v-list-item>
                      <v-list-item-title>Email</v-list-item-title>
                      <v-list-item-subtitle>{{ lease.client.email }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="12" md="6" v-if="lease.client.phone">
                    <v-list-item>
                      <v-list-item-title>Телефон</v-list-item-title>
                      <v-list-item-subtitle>{{ lease.client.phone }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="12" md="6" v-if="lease.client.address">
                    <v-list-item>
                      <v-list-item-title>Адрес</v-list-item-title>
                      <v-list-item-subtitle>{{ lease.client.address }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>

            <!-- Детали договора -->
            <h3 class="text-h6 mb-3">
              <v-icon class="mr-2">mdi-file-document</v-icon>
              Детали договора
            </h3>

            <v-card outlined>
              <v-card-text>
                <v-row>
                  <v-col cols="6" md="3">
                    <v-list-item>
                      <v-list-item-title>Дата начала</v-list-item-title>
                      <v-list-item-subtitle class="text-h6">
                        {{ formatDate(lease.start_date) }}
                      </v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="6" md="3">
                    <v-list-item>
                      <v-list-item-title>Дата окончания</v-list-item-title>
                      <v-list-item-subtitle class="text-h6">
                        {{ lease.end_date ? formatDate(lease.end_date) : 'Не указана' }}
                      </v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="6" md="3">
                    <v-list-item>
                      <v-list-item-title>Ежемесячная оплата</v-list-item-title>
                      <v-list-item-subtitle class="text-h6">
                        {{ parseFloat(lease.monthly_payment).toFixed(2) }} ₽
                      </v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="6" md="3">
                    <v-list-item>
                      <v-list-item-title>Общая стоимость</v-list-item-title>
                      <v-list-item-subtitle class="text-h6">
                        {{ calculateTotalPayment() }} ₽
                      </v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="6" md="3">
                    <v-list-item>
                      <v-list-item-title>Создатель договора</v-list-item-title>
                      <v-list-item-subtitle>Сотрудник #{{ lease.created_by_admin }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="6" md="3">
                    <v-list-item>
                      <v-list-item-title>Статус договора</v-list-item-title>
                      <v-list-item-subtitle>
                        <v-chip :color="getStatusColor(lease.status)" dark>
                          {{ getStatusText(lease.status) }}
                        </v-chip>
                      </v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="6" md="3">
                    <v-list-item>
                      <v-list-item-title>ID договора</v-list-item-title>
                      <v-list-item-subtitle>#{{ lease.id }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="6" md="3">
                    <v-list-item>
                      <v-list-item-title>Дата создания</v-list-item-title>
                      <v-list-item-subtitle>{{ formatDateTime(lease.created_at) }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Боковая панель -->
      <v-col cols="12" md="4">
        <!-- Быстрые действия -->
        <v-card class="mb-4">
          <v-card-title>Быстрые действия</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item
                  @click="copyLeaseInfo"
                  prepend-icon="mdi-content-copy"
              >
                <v-list-item-title>Копировать информацию</v-list-item-title>
              </v-list-item>

              <v-list-item
                  @click="printLease"
                  prepend-icon="mdi-printer"
              >
                <v-list-item-title>Распечатать договор</v-list-item-title>
              </v-list-item>

              <v-list-item
                  @click="$router.push(`/admin/cars/${lease.car.id}/leasings`)"
                  prepend-icon="mdi-history"
              >
                <v-list-item-title>История аренд этого авто</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>

        <!-- Статусы -->
        <v-card>
          <v-card-title>Статусы</v-card-title>
          <v-card-text>
            <div class="mb-4">
              <div class="text-subtitle-2 mb-2">Статус договора:</div>
              <v-chip :color="getStatusColor(lease.status)" dark large block>
                {{ getStatusText(lease.status) }}
              </v-chip>
            </div>

            <div>
              <div class="text-subtitle-2 mb-2">Статус автомобиля:</div>
              <v-chip :color="getCarStatusColor(lease.car.status)" dark large block>
                {{ getCarStatusText(lease.car.status) }}
              </v-chip>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Ошибка -->
    <v-alert v-else-if="error" type="error">
      {{ errorMessage }}
      <v-btn @click="fetchLease" class="mt-2" color="error">Попробовать снова</v-btn>
    </v-alert>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminLeaseDetail',
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      lease: null,
      loading: true,
      error: false,
      errorMessage: ''
    }
  },
  computed: {
    leaseId() {
      return parseInt(this.id)
    }
  },
  methods: {
    async fetchLease() {
      try {
        this.loading = true
        this.error = false

        const response = await axios.get(`admin/leases/${this.leaseId}/`)
        this.lease = response.data
        console.log('Данные договора загружены:', this.lease)

      } catch (error) {
        console.error('Ошибка загрузки договора:', error)
        this.error = true
        this.errorMessage = error.response?.data?.detail || 'Не удалось загрузить данные договора'
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

    getCarStatusColor(status) {
      const colors = {
        'available': 'green',
        'leased': 'orange',
        'maintenance': 'red',
        'sold': 'grey'
      }
      return colors[status] || 'blue'
    },

    getCarStatusText(status) {
      const texts = {
        'available': 'Доступен',
        'leased': 'В аренде',
        'maintenance': 'На обслуживании',
        'sold': 'Продан'
      }
      return texts[status] || status
    },

    formatDate(dateString) {
      if (!dateString) return '—'
      return new Date(dateString).toLocaleDateString('ru-RU')
    },

    formatDateTime(dateTimeString) {
      if (!dateTimeString) return '—'
      return new Date(dateTimeString).toLocaleString('ru-RU')
    },

    calculateTotalPayment() {
      if (!this.lease.start_date || !this.lease.end_date || !this.lease.monthly_payment) {
        return '0.00'
      }

      const start = new Date(this.lease.start_date)
      const end = new Date(this.lease.end_date)
      const monthly = parseFloat(this.lease.monthly_payment)

      if (isNaN(monthly) || monthly <= 0) return '0.00'

      const months = Math.ceil((end - start) / (1000 * 60 * 60 * 24 * 30.44))
      const total = months * monthly

      return total.toFixed(2)
    },

    copyLeaseInfo() {
      const text = `Договор аренды #${this.lease.id}
Автомобиль: ${this.lease.car.make} ${this.lease.car.model} (${this.lease.car.license_plate})
Клиент: ${this.lease.client.company_name} (ИНН: ${this.lease.client.inn})
Даты: ${this.formatDate(this.lease.start_date)} - ${this.lease.end_date ? this.formatDate(this.lease.end_date) : 'без срока'}
Оплата: ${parseFloat(this.lease.monthly_payment).toFixed(2)} ₽/мес
Статус: ${this.getStatusText(this.lease.status)}
Создан: ${this.formatDateTime(this.lease.created_at)}`

      navigator.clipboard.writeText(text)
          .then(() => {
            alert('Информация скопирована в буфер обмена')
          })
          .catch(err => {
            console.error('Ошибка копирования:', err)
          })
    },

    printLease() {
      window.print()
    }
  },

  mounted() {
    this.fetchLease()
  },

  watch: {
    id() {
      this.fetchLease()
    }
  }
}
</script>

<style scoped>
@media print {
  .v-btn, .v-toolbar, .v-footer, .v-navigation-drawer {
    display: none !important;
  }
}
</style>