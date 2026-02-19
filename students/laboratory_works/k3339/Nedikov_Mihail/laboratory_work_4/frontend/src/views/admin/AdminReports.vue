<template>
  <div>
    <h1 class="text-h4 mb-6">
      <v-icon class="mr-2">mdi-chart-bar</v-icon>
      Отчеты
    </h1>

    <!-- Вкладки с отчетами -->
    <v-tabs v-model="activeTab" grow class="mb-6">
      <v-tab value="revenue">
        <v-icon left>mdi-cash</v-icon>
        Доходы по аренде
      </v-tab>
      <v-tab value="utilization">
        <v-icon left>mdi-chart-line</v-icon>
        Загрузка автопарка
      </v-tab>
      <v-tab value="maintenance">
        <v-icon left>mdi-wrench</v-icon>
        Затраты на обслуживание
      </v-tab>
    </v-tabs>

    <!-- Содержимое вкладок -->
    <v-window v-model="activeTab">
      <!-- Отчет по доходам -->
      <v-window-item value="revenue">
        <v-card>
          <v-card-title>
            <v-icon class="mr-2">mdi-cash</v-icon>
            Доходы по аренде автомобилей
          </v-card-title>

          <v-card-text>
            <div v-if="revenueLoading" class="text-center py-8">
              <v-progress-circular indeterminate></v-progress-circular>
              <div class="mt-4">Загрузка отчета...</div>
            </div>

            <div v-else>
              <!-- Итоговая статистика -->
              <v-alert type="info" class="mb-4">
                <div class="d-flex justify-space-between">
                  <span>Всего договоров:</span>
                  <strong>{{ revenueStats.totalLeases }}</strong>
                </div>
                <div class="d-flex justify-space-between mt-2">
                  <span>Общий доход:</span>
                  <strong class="text-h6">{{ revenueStats.totalIncome.toFixed(2) }} ₽</strong>
                </div>
              </v-alert>

              <!-- Таблица -->
              <table class="elevation-1" style="width: 100%; border-collapse: collapse; background-color: white;">
                <thead>
                <tr style="background-color: #f5f5f5;">
                  <th style="width: 25%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Марка</th>
                  <th style="width: 25%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Модель</th>
                  <th style="width: 25%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Кол-во аренд</th>
                  <th style="width: 25%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Общий доход</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="item in revenueData" :key="item.make + '-' + item.model" style="border-bottom: 1px solid #e0e0e0;">
                  <td style="width: 25%; padding: 12px; text-align: center;">{{ item.make || '-' }}</td>
                  <td style="width: 25%; padding: 12px; text-align: center;">{{ item.model || '-' }}</td>
                  <td style="width: 25%; padding: 12px; text-align: center;">{{ item.leasings_count !== null ? item.leasings_count : '-' }}</td>
                  <td style="width: 25%; padding: 12px; text-align: center;" :class="item.total_income ? 'text-green' : 'text-grey'">
                    {{ item.total_income ? `${item.total_income.toFixed(2)} ₽` : '-' }}
                  </td>
                </tr>
                <tr v-if="revenueData.length === 0">
                  <td colspan="4" style="padding: 16px; text-align: center; color: #9E9E9E;">Нет данных для отображения</td>
                </tr>
                </tbody>
              </table>
            </div>
          </v-card-text>
        </v-card>
      </v-window-item>

      <!-- Отчет по загрузке -->
      <v-window-item value="utilization">
        <v-card>
          <v-card-title>
            <v-icon class="mr-2">mdi-chart-line</v-icon>
            Загрузка автопарка
          </v-card-title>

          <v-card-text>
            <div v-if="utilizationLoading" class="text-center py-8">
              <v-progress-circular indeterminate></v-progress-circular>
              <div class="mt-4">Загрузка отчета...</div>
            </div>

            <div v-else>
              <!-- Итоговая статистика -->
              <v-alert type="info" class="mb-4">
                <div class="d-flex justify-space-between">
                  <span>Средняя загрузка:</span>
                  <strong class="text-h6">{{ utilizationStats.avgUtilization.toFixed(1) }}%</strong>
                </div>
                <div class="d-flex justify-space-between mt-2">
                  <span>Всего дней аренды:</span>
                  <strong>{{ utilizationStats.totalLeaseDays }}</strong>
                </div>
              </v-alert>

              <!-- Таблица -->
              <table class="elevation-1" style="width: 100%; border-collapse: collapse; background-color: white;">
                <thead>
                <tr style="background-color: #f5f5f5;">
                  <th style="width: 15%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Марка</th>
                  <th style="width: 15%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Модель</th>
                  <th style="width: 25%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Гос. номер</th>
                  <th style="width: 15%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Дней аренды</th>
                  <th style="width: 30%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Загрузка</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="item in utilizationData" :key="item.license_plate" style="border-bottom: 1px solid #e0e0e0;">
                  <td style="width: 15%; padding: 12px; text-align: center;">{{ item.make || '-' }}</td>
                  <td style="width: 15%; padding: 12px; text-align: center;">{{ item.model || '-' }}</td>
                  <td style="width: 25%; padding: 12px; text-align: center;">{{ item.license_plate || '-' }}</td>
                  <td style="width: 15%; padding: 12px; text-align: center;">{{ item.lease_days !== null ? item.lease_days : '-' }}</td>
                  <td style="width: 30%; padding: 12px; text-align: center;">
                    <div class="d-flex align-center justify-center">
                      <v-progress-linear
                          :value="item.utilization * 100"
                          height="20"
                          :color="getUtilizationColor(item.utilization)"
                          class="mr-3"
                          style="width: 70%"
                      >
                        <template v-slot:default>
                          <strong>{{ (item.utilization * 100).toFixed(1) }}%</strong>
                        </template>
                      </v-progress-linear>
                      <span class="text-caption">{{ item.lease_days }} дн.</span>
                    </div>
                  </td>
                </tr>
                <tr v-if="utilizationData.length === 0">
                  <td colspan="6" style="padding: 16px; text-align: center; color: #9E9E9E;">Нет данных для отображения</td>
                </tr>
                </tbody>
              </table>
            </div>
          </v-card-text>
        </v-card>
      </v-window-item>

      <!-- Отчет по обслуживанию -->
      <v-window-item value="maintenance">
        <v-card>
          <v-card-title>
            <v-icon class="mr-2">mdi-wrench</v-icon>
            Затраты на обслуживание
          </v-card-title>

          <v-card-text>
            <div v-if="maintenanceLoading" class="text-center py-8">
              <v-progress-circular indeterminate></v-progress-circular>
              <div class="mt-4">Загрузка отчета...</div>
            </div>

            <div v-else>
              <!-- Итоговая статистика -->
              <v-alert type="info" class="mb-4">
                <div class="d-flex justify-space-between">
                  <span>Общие затраты:</span>
                  <strong class="text-h6">{{ maintenanceStats.totalCost.toFixed(2) }} ₽</strong>
                </div>
                <div class="d-flex justify-space-between mt-2">
                  <span>Средние затраты на авто:</span>
                  <strong>{{ maintenanceStats.avgCost.toFixed(2) }} ₽</strong>
                </div>
              </v-alert>

              <!-- Таблица -->
              <table class="elevation-1" style="width: 100%; border-collapse: collapse; background-color: white;">
                <thead>
                <tr style="background-color: #f5f5f5;">
                  <th style="width: 10%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">ID авто</th>
                  <th style="width: 50%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Автомобиль</th>
                  <th style="width: 40%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Затраты на обслуживание</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="item in maintenanceData" :key="item.car_id" style="border-bottom: 1px solid #e0e0e0;">
                  <td style="width: 10%; padding: 12px; text-align: center;">{{ item.car_id !== null ? item.car_id : '-' }}</td>
                  <td style="width: 50%; padding: 12px; text-align: center;">{{ item.car || '-' }}</td>
                  <td style="width: 40%; padding: 12px; text-align: center;" class="text-red">
                    {{ item.total_maintenance_cost ? `${item.total_maintenance_cost.toFixed(2)} ₽` : '-' }}
                  </td>
                </tr>
                <tr v-if="maintenanceData.length === 0">
                  <td colspan="4" style="padding: 16px; text-align: center; color: #9E9E9E;">Нет данных для отображения</td>
                </tr>
                </tbody>
              </table>
            </div>
          </v-card-text>
        </v-card>
      </v-window-item>
    </v-window>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminReports',
  data() {
    return {
      activeTab: 'revenue',

      // Доходы
      revenueData: [],
      revenueLoading: false,
      revenueStats: {
        totalLeases: 0,
        totalIncome: 0
      },
      revenueHeaders: [
        { text: 'Марка', value: 'make' },
        { text: 'Модель', value: 'model' },
        { text: 'Кол-во аренд', value: 'leasings_count', align: 'center' },
        { text: 'Общий доход', value: 'total_income', align: 'right' },
      ],

      // Загрузка
      utilizationData: [],
      utilizationLoading: false,
      utilizationStats: {
        avgUtilization: 0,
        totalLeaseDays: 0
      },
      utilizationHeaders: [
        { text: 'Марка', value: 'make' },
        { text: 'Модель', value: 'model' },
        { text: 'Гос. номер', value: 'license_plate' },
        { text: 'Дней аренды', value: 'lease_days', align: 'center' },
        { text: 'Загрузка', value: 'utilization' },
        { text: 'Действия', value: 'actions', sortable: false, width: '80px' }
      ],

      // Обслуживание
      maintenanceData: [],
      maintenanceLoading: false,
      maintenanceStats: {
        totalCost: 0,
        avgCost: 0
      },
      maintenanceHeaders: [
        { text: 'ID авто', value: 'car_id', width: '100px', align: 'center' },
        { text: 'Автомобиль', value: 'car' },
        { text: 'Затраты на обслуживание', value: 'total_maintenance_cost', align: 'right' },
        { text: 'Действия', value: 'actions', sortable: false, width: '80px' }
      ]
    }
  },
  watch: {
    activeTab(newTab) {
      this.loadReport(newTab)
    }
  },
  methods: {
    async loadReport(reportType) {
      switch (reportType) {
        case 'revenue':
          if (this.revenueData.length === 0) {
            await this.fetchRevenueReport()
          }
          break
        case 'utilization':
          if (this.utilizationData.length === 0) {
            await this.fetchUtilizationReport()
          }
          break
        case 'maintenance':
          if (this.maintenanceData.length === 0) {
            await this.fetchMaintenanceReport()
          }
          break
      }
    },

    async fetchRevenueReport() {
      try {
        this.revenueLoading = true
        const response = await axios.get('admin/reports/revenue/')
        this.revenueData = response.data.results

        // Расчет статистики
        this.revenueStats.totalLeases = this.revenueData.reduce((sum, item) => sum + (item.leasings_count || 0), 0)
        this.revenueStats.totalIncome = this.revenueData.reduce((sum, item) => sum + (item.total_income || 0), 0)

        console.log('Отчет по доходам загружен:', this.revenueData.length)
      } catch (error) {
        console.error('Ошибка загрузки отчета по доходам:', error)
      } finally {
        this.revenueLoading = false
      }
    },

    async fetchUtilizationReport() {
      try {
        this.utilizationLoading = true
        const response = await axios.get('admin/reports/utilization/')
        this.utilizationData = response.data.results

        // Расчет статистики
        const totalUtilization = this.utilizationData.reduce((sum, item) => sum + (item.utilization || 0), 0)
        this.utilizationStats.avgUtilization = this.utilizationData.length > 0
            ? (totalUtilization / this.utilizationData.length) * 100
            : 0
        this.utilizationStats.totalLeaseDays = this.utilizationData.reduce((sum, item) => sum + (item.lease_days || 0), 0)

        console.log('Отчет по загрузке загружен:', this.utilizationData.length)
      } catch (error) {
        console.error('Ошибка загрузки отчета по загрузке:', error)
      } finally {
        this.utilizationLoading = false
      }
    },

    async fetchMaintenanceReport() {
      try {
        this.maintenanceLoading = true
        const response = await axios.get('admin/reports/maintenance_costs/')
        this.maintenanceData = response.data.results

        // Расчет статистики
        this.maintenanceStats.totalCost = this.maintenanceData.reduce((sum, item) => sum + (item.total_maintenance_cost || 0), 0)
        this.maintenanceStats.avgCost = this.maintenanceData.length > 0
            ? this.maintenanceStats.totalCost / this.maintenanceData.length
            : 0

        console.log('Отчет по обслуживанию загружен:', this.maintenanceData.length)
      } catch (error) {
        console.error('Ошибка загрузки отчета по обслуживанию:', error)
      } finally {
        this.maintenanceLoading = false
      }
    },

    getUtilizationColor(utilization) {
      if (utilization > 0.7) return 'green'
      if (utilization > 0.4) return 'orange'
      return 'red'
    },

    goToCarDetailsById(carId) {
      this.$router.push(`/admin/cars/${carId}`)
    },

    goToCarByPlate(licensePlate) {
      // Нужна дополнительная информация о бэкенде для этого метода
      // Пока оставлю заглушку
      console.log('Переход к автомобилю с номером:', licensePlate)
      // this.$router.push(`/admin/cars/?plate=${licensePlate}`)
    }
  },

  mounted() {
    this.loadReport(this.activeTab)
  }
}
</script>

<style scoped>
.text-green {
  color: #4CAF50;
}
.text-red {
  color: #F44336;
}
.text-grey {
  color: #9E9E9E;
}

/* Стили для строк таблицы */
.revenue-header,
.utilization-header,
.maintenance-header {
  background-color: #f5f5f5;
  border-bottom: 1px solid #e0e0e0;
}

.revenue-row:nth-child(even),
.utilization-row:nth-child(even),
.maintenance-row:nth-child(even) {
  background-color: #fafafa;
}

.revenue-row:hover,
.utilization-row:hover,
.maintenance-row:hover {
  background-color: #f0f0f0;
}

.revenue-row,
.utilization-row,
.maintenance-row {
  border-bottom: 1px solid #e0e0e0;
}

.revenue-row:last-child,
.utilization-row:last-child,
.maintenance-row:last-child {
  border-bottom: none;
}
</style>