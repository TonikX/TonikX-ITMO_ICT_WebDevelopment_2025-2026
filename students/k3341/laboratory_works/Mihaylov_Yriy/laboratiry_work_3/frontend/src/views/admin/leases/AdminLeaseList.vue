<template>
  <div>
    <v-row class="mb-4">
      <v-col cols="12">
        <v-card>
          <v-card-title class="headline">
            <v-icon class="mr-2">mdi-file-sign</v-icon>
            Договоры аренды
          </v-card-title>

          <v-card-subtitle>
            Всего договоров: {{ filteredLeases.length }} (Показано: {{ paginatedLeases.length }})
          </v-card-subtitle>

          <v-card-text>
            <!-- Фильтры (уменьшенная высота) -->
            <v-row class="mb-2" style="min-height: 80px;">
              <v-col cols="12" md="4">
                <v-select
                    v-model="filters.status"
                    :items="statusOptions"
                    label="Фильтр по статусу"
                    clearable
                    prepend-icon="mdi-filter"
                    density="comfortable"
                    variant="outlined"
                ></v-select>
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                    v-model="filters.search"
                    label="Поиск по марке или клиенту"
                    prepend-icon="mdi-magnify"
                    clearable
                    density="comfortable"
                    variant="outlined"
                ></v-text-field>
              </v-col>

            </v-row>

            <!-- Загрузка -->
            <div v-if="loading" class="text-center py-8">
              <v-progress-circular indeterminate color="primary"></v-progress-circular>
              <div class="mt-4">Загрузка договоров...</div>
            </div>

            <!-- Список -->
            <div v-else>
              <!-- Таблица договоров -->
              <table class="elevation-1" style="width: 100%; border-collapse: collapse; background-color: white;">
                <thead>
                <tr style="background-color: #f5f5f5;">
                  <th style="width: 5%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">ID</th>
                  <th style="width: 20%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Автомобиль</th>
                  <th style="width: 20%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Клиент</th>
                  <th style="width: 15%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Даты аренды</th>
                  <th style="width: 15%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Оплата</th>
                  <th style="width: 10%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Статус</th>
                  <th style="width: 10%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Создан</th>
                  <th style="width: 5%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Действия</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="item in paginatedLeases" :key="item.id" style="border-bottom: 1px solid #e0e0e0;">
                  <td style="width: 5%; padding: 12px; text-align: center;">{{ item.id || '-' }}</td>
                  <td style="width: 20%; padding: 12px; text-align: center;">
                    <div>
                      <strong>{{ item.car.make }} {{ item.car.model }}</strong>
                      <div class="text-caption">{{ item.car.license_plate }}</div>
                    </div>
                  </td>
                  <td style="width: 20%; padding: 12px; text-align: center;">
                    <div>
                      <strong>{{ item.client.company_name }}</strong>
                      <div class="text-caption">ИНН: {{ item.client.inn }}</div>
                    </div>
                  </td>
                  <td style="width: 15%; padding: 12px; text-align: center;">
                    <div>
                      <div>С: {{ formatDate(item.start_date) }}</div>
                      <div v-if="item.end_date">По: {{ formatDate(item.end_date) }}</div>
                      <div v-else class="text-grey">Без срока</div>
                    </div>
                  </td>
                  <td style="width: 15%; padding: 12px; text-align: center;">
                    <div>
                      <strong>{{ parseFloat(item.monthly_payment).toFixed(2) }} ₽/мес</strong>
                      <div class="text-caption" v-if="item.start_date && item.end_date">
                        Итого: ~{{ calculateTotal(item) }} ₽
                      </div>
                    </div>
                  </td>
                  <td style="width: 10%; padding: 12px; text-align: center;">
                    <v-chip :color="getStatusColor(item.status)" dark small style="margin: 0 auto;">
                      {{ getStatusText(item.status) }}
                    </v-chip>
                  </td>
                  <td style="width: 10%; padding: 12px; text-align: center;">
                    {{ formatDateTime(item.created_at) }}
                  </td>
                  <td style="width: 5%; padding: 12px; text-align: center;">
                    <v-btn
                        color="primary"
                        small
                        @click="$router.push(`/admin/leases/${item.id}`)"
                        style="margin-right: 4px;"
                    >
                      <v-icon small>mdi-eye</v-icon>
                    </v-btn>
                    <v-btn
                        color="warning"
                        small
                        @click="showUpdateDialog(item)"
                    >
                      <v-icon small>mdi-pencil</v-icon>
                    </v-btn>
                  </td>
                </tr>
                <tr v-if="paginatedLeases.length === 0">
                  <td colspan="8" style="padding: 16px; text-align: center; color: #9E9E9E;">
                    Нет договоров для отображения
                  </td>
                </tr>
                </tbody>
              </table>

              <!-- Пагинация -->
              <div class="d-flex justify-center align-center mt-4">
                <v-btn
                    :disabled="currentPage === 1"
                    @click="currentPage--"
                    size="small"
                    variant="text"
                >
                  <v-icon>mdi-chevron-left</v-icon>
                </v-btn>

                <span class="mx-4">
                  Страница {{ currentPage }} из {{ totalPages }}
                </span>

                <v-btn
                    :disabled="currentPage >= totalPages"
                    @click="currentPage++"
                    size="small"
                    variant="text"
                >
                  <v-icon>mdi-chevron-right</v-icon>
                </v-btn>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Диалог обновления статуса -->
    <v-dialog v-model="updateDialog" max-width="500">
      <v-card>
        <v-card-title>Обновление договора #{{ selectedLease?.id }}</v-card-title>
        <v-card-text>
          <v-form v-if="selectedLease" ref="updateForm" v-model="updateValid">
            <v-select
                v-model="updateForm.status"
                :items="statusOptions"
                label="Статус договора*"
                :rules="[v => !!v || 'Обязательное поле']"
                required
            ></v-select>

            <v-text-field
                v-model="updateForm.start_date"
                label="Дата начала"
                type="date"
            ></v-text-field>

            <v-text-field
                v-model="updateForm.end_date"
                label="Дата окончания"
                type="date"
                :min="updateForm.start_date"
            ></v-text-field>

            <v-text-field
                v-model="updateForm.monthly_payment"
                label="Ежемесячная оплата"
                type="number"
                step="0.01"
                suffix="₽"
            ></v-text-field>

            <v-alert v-if="updateError" type="error" class="mt-4">
              {{ updateErrorMessage }}
            </v-alert>

            <v-alert v-if="updateSuccess" type="success" class="mt-4">
              Статус успешно обновлён!
            </v-alert>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="updateDialog = false" color="secondary">Отмена</v-btn>
          <v-btn
              @click="updateLease"
              color="primary"
              :loading="updateLoading"
              :disabled="!updateValid || updateSuccess"
          >
            Сохранить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminLeaseList',
  data() {
    return {
      leases: [],
      loading: true,
      currentPage: 1,
      itemsPerPage: 5,

      filters: {
        status: null,
        search: ''
      },

      // Исправлено: теперь просто строковые значения
      statusOptions: ['Активный', 'Завершён', 'Отменён'],

      // Диалог обновления
      updateDialog: false,
      selectedLease: null,
      updateLoading: false,
      updateValid: false,
      updateError: false,
      updateSuccess: false,
      updateErrorMessage: '',

      updateForm: {
        status: '',
        start_date: '',
        end_date: '',
        monthly_payment: ''
      }
    }
  },
  computed: {
    filteredLeases() {
      return this.leases.filter(lease => {
        // Фильтр по статусу - сравниваем текстовое представление
        if (this.filters.status) {
          const statusText = this.getStatusText(lease.status)
          if (statusText !== this.filters.status) {
            return false
          }
        }

        // Поиск по марке/модели/клиенту
        if (this.filters.search) {
          const searchLower = this.filters.search.toLowerCase()
          const carText = `${lease.car.make} ${lease.car.model}`.toLowerCase()
          const clientText = lease.client.company_name.toLowerCase()

          if (!carText.includes(searchLower) && !clientText.includes(searchLower)) {
            return false
          }
        }

        return true
      })
    },

    totalPages() {
      return Math.ceil(this.filteredLeases.length / this.itemsPerPage)
    },

    paginatedLeases() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredLeases.slice(start, end)
    }
  },
  watch: {
    filters: {
      handler() {
        this.currentPage = 1 // Сбрасываем на первую страницу при изменении фильтров
      },
      deep: true
    }
  },
  methods: {
    async fetchLeases() {
      try {
        this.loading = true
        const response = await axios.get('admin/leases/')
        this.leases = response.data
        console.log('Договоры загружены:', this.leases.length)
      } catch (error) {
        console.error('Ошибка загрузки договоров:', error)
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

    formatDateTime(dateTimeString) {
      if (!dateTimeString) return '—'
      return new Date(dateTimeString).toLocaleString('ru-RU')
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
    },

    showUpdateDialog(lease) {
      this.selectedLease = lease
      // Преобразуем статус для отображения в форме
      const statusText = this.getStatusText(lease.status)
      this.updateForm = {
        status: statusText,
        start_date: lease.start_date || '',
        end_date: lease.end_date || '',
        monthly_payment: lease.monthly_payment || ''
      }
      this.updateError = false
      this.updateSuccess = false
      this.updateDialog = true
    },

    async updateLease() {
      if (!this.$refs.updateForm.validate()) return

      this.updateLoading = true
      this.updateError = false
      this.updateSuccess = false

      try {
        // Преобразуем текстовый статус обратно в значение для API
        const statusMap = {
          'Активный': 'active',
          'Завершён': 'completed',
          'Отменён': 'cancelled'
        }

        const payload = {
          lease_id: this.selectedLease.id,
          status: statusMap[this.updateForm.status] || this.updateForm.status,
          start_date: this.updateForm.start_date || null,
          end_date: this.updateForm.end_date || null,
          monthly_payment: this.updateForm.monthly_payment || null
        }

        console.log('Обновляем договор:', payload)

        const response = await axios.patch('admin/leases/', payload)

        this.updateSuccess = true
        console.log('Договор обновлён:', response.data)

        // Обновляем список через 2 секунды
        setTimeout(() => {
          this.fetchLeases()
          this.updateDialog = false
        }, 2000)

      } catch (error) {
        console.error('Ошибка обновления договора:', error)
        this.updateError = true

        if (error.response?.status === 400 && error.response?.data?.error) {
          this.updateErrorMessage = error.response.data.error
        } else if (error.response?.data?.detail) {
          this.updateErrorMessage = error.response.data.detail
        } else {
          this.updateErrorMessage = 'Ошибка при обновлении договора'
        }
      } finally {
        this.updateLoading = false
      }
    }
  },

  mounted() {
    this.fetchLeases()
  }
}
</script>