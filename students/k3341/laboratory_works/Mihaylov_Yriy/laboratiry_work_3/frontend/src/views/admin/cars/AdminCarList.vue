<template>
  <div>
    <v-row class="mb-4">
      <v-col cols="12">
        <v-card>
          <v-card-title class="headline">
            <v-icon class="mr-2">mdi-car</v-icon>
            Управление автомобилями
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="$router.push('/admin/cars/new')">
              <v-icon left>mdi-plus</v-icon>
              Добавить автомобиль
            </v-btn>
          </v-card-title>

          <v-card-subtitle>
            Всего автомобилей: {{ cars.length }} (Показано: {{ paginatedCars.length }})
          </v-card-subtitle>

          <v-card-text v-if="loading">
            <v-progress-linear indeterminate></v-progress-linear>
            <div class="text-center mt-4">Загрузка автомобилей...</div>
          </v-card-text>

          <v-card-text v-else>
            <!-- Таблица автомобилей -->
            <table class="elevation-1" style="width: 100%; border-collapse: collapse; background-color: white;">
              <thead>
              <tr style="background-color: #f5f5f5;">
                <th style="width: 5%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">ID</th>
                <th style="width: 10%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Марка</th>
                <th style="width: 10%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Модель</th>
                <th style="width: 8%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Год</th>
                <th style="width: 12%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Гос. номер</th>
                <th style="width: 15%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">VIN</th>
                <th style="width: 10%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Пробег</th>
                <th style="width: 12%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Статус</th>
                <th style="width: 8%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Хар-ки</th>
                <th style="width: 10%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Действия</th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="item in paginatedCars" :key="item.id" style="border-bottom: 1px solid #e0e0e0;">
                <td style="width: 5%; padding: 12px; text-align: center;">{{ item.id || '-' }}</td>
                <td style="width: 10%; padding: 12px; text-align: center;">{{ item.make || '-' }}</td>
                <td style="width: 10%; padding: 12px; text-align: center;">{{ item.model || '-' }}</td>
                <td style="width: 8%; padding: 12px; text-align: center;">{{ item.year || '-' }}</td>
                <td style="width: 12%; padding: 12px; text-align: center;">{{ item.license_plate || '-' }}</td>
                <td style="width: 15%; padding: 12px; text-align: center;">{{ item.vin || '-' }}</td>
                <td style="width: 10%; padding: 12px; text-align: center;">{{ item.current_mileage || '0' }} км</td>
                <td style="width: 12%; padding: 12px; text-align: center;">
                  <v-chip :color="getStatusColor(item.status)" dark small style="margin: 0 auto;">
                    {{ getStatusText(item.status) }}
                  </v-chip>
                </td>
                <td style="width: 8%; padding: 12px; text-align: center;">
                  <div v-if="item.specification">
                    <v-icon small color="green" title="Есть характеристики">mdi-check-circle</v-icon>
                  </div>
                  <div v-else>
                    <v-icon small color="grey" title="Нет характеристик">mdi-minus-circle</v-icon>
                  </div>
                </td>
                <td style="width: 10%; padding: 12px; text-align: center;">
                  <v-btn
                      color="primary"
                      small
                      @click="$router.push(`/admin/cars/${item.id}`)"
                      style="margin-right: 4px;"
                  >
                    <v-icon small>mdi-eye</v-icon>
                  </v-btn>

                  <v-btn
                      color="warning"
                      small
                      @click="$router.push(`/admin/cars/${item.id}/edit`)"
                  >
                    <v-icon small>mdi-pencil</v-icon>
                  </v-btn>

                </td>
              </tr>
              <tr v-if="paginatedCars.length === 0">
                <td colspan="10" style="padding: 16px; text-align: center; color: #9E9E9E;">
                  Нет автомобилей для отображения
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
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminCarList',
  data() {
    return {
      cars: [],
      loading: true,
      error: null,
      currentPage: 1,
      itemsPerPage: 5,
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.cars.length / this.itemsPerPage)
    },

    paginatedCars() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.cars.slice(start, end)
    }
  },
  methods: {
    async fetchCars() {
      try {
        this.loading = true
        const response = await axios.get('admin/cars/')
        this.cars = response.data.cars
        console.log('Автомобили загружены:', this.cars.length)
      } catch (error) {
        console.error('Ошибка загрузки автомобилей:', error)
        this.error = 'Не удалось загрузить список автомобилей'
      } finally {
        this.loading = false
      }
    },
    getStatusColor(status) {
      const colors = {
        'available': 'green',
        'leased': 'orange',
        'maintenance': 'red',
        'sold': 'grey'
      }
      return colors[status] || 'blue'
    },
    getStatusText(status) {
      const texts = {
        'available': 'Доступен',
        'leased': 'В аренде',
        'maintenance': 'На обслуживании',
        'sold': 'Продан'
      }
      return texts[status] || status
    }
  },
  mounted() {
    this.fetchCars()
  }
}
</script>