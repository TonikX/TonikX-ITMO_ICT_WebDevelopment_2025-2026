<template>
  <v-container>
    <v-btn @click="$router.push('/cars')" class="mb-4" color="secondary">
      <v-icon left>mdi-arrow-left</v-icon>
      Назад к списку
    </v-btn>

    <v-row v-if="loading">
      <v-col cols="12">
        <v-progress-linear indeterminate color="primary"></v-progress-linear>
        <div class="text-center mt-4">Загрузка данных автомобиля...</div>
      </v-col>
    </v-row>

    <v-row v-else-if="car">
      <!-- Основная информация -->
      <v-col cols="12">
        <v-card>
          <v-card-title class="text-h4">
            {{ car.make }} {{ car.model }}
            <v-chip class="ml-4" :color="getStatusColor(car.status)" dark large>
              {{ getStatusText(car.status) }}
            </v-chip>
          </v-card-title>

          <v-card-subtitle class="text-h6">
            <v-icon class="mr-2">mdi-numeric</v-icon>
            {{ car.license_plate }}
            <v-icon class="ml-4 mr-2">mdi-calendar</v-icon>
            {{ car.year }} год
            <v-icon class="ml-4 mr-2">mdi-gauge</v-icon>
            {{ car.current_mileage?.toLocaleString() || '0' }} км
            <v-icon class="ml-4 mr-2">mdi-barcode</v-icon>
            VIN: {{ car.vin }}
          </v-card-subtitle>

          <v-divider class="my-4"></v-divider>

          <v-card-text>
            <!-- Основные данные -->
            <v-row>
              <v-col cols="6" md="3">
                <v-list-item>
                  <v-list-item-title>Дата покупки</v-list-item-title>
                  <v-list-item-subtitle>{{ formatDate(car.purchase_date) }}</v-list-item-subtitle>
                </v-list-item>
              </v-col>

              <v-col cols="6" md="3">
                <v-list-item>
                  <v-list-item-title>Дата добавления</v-list-item-title>
                  <v-list-item-subtitle>{{ formatDateTime(car.created_at) }}</v-list-item-subtitle>
                </v-list-item>
              </v-col>

              <v-col cols="6" md="3">
                <v-list-item>
                  <v-list-item-title>Статус</v-list-item-title>
                  <v-list-item-subtitle>
                    <v-chip :color="getStatusColor(car.status)" dark small>
                      {{ getStatusText(car.status) }}
                    </v-chip>
                  </v-list-item-subtitle>
                </v-list-item>
              </v-col>
            </v-row>

            <!-- Характеристики если есть -->
            <div v-if="car.specification" class="mt-6">
              <h3 class="text-h6 mb-3">
                <v-icon class="mr-2">mdi-cog</v-icon>
                Технические характеристики
              </h3>

              <v-row>
                <template v-for="(value, key) in specificationFields" :key="key">
                  <v-col cols="6" md="4" v-if="car.specification[value.field]">
                    <v-list-item>
                      <v-list-item-title>{{ value.label }}</v-list-item-title>
                      <v-list-item-subtitle>
                        {{ getFieldValue(value.field, car.specification[value.field]) }}
                      </v-list-item-subtitle>
                    </v-list-item>
                  </v-col>
                </template>
              </v-row>

              <!-- Дополнительные опции -->
              <div v-if="car.specification.additional_options" class="mt-4">
                <h4 class="text-subtitle-1">Дополнительные опции:</h4>
                <p>{{ car.specification.additional_options }}</p>
              </div>
            </div>

            <!-- Автопарк если есть -->
            <div v-if="car.car_fleet" class="mt-6">
              <h3 class="text-h6 mb-3">
                <v-icon class="mr-2">mdi-garage</v-icon>
                Автопарк
              </h3>
              <v-card outlined>
                <v-card-text>
                  <p><strong>Название:</strong> {{ car.car_fleet.fleet.name }}</p>
                  <p v-if="car.car_fleet.fleet.address">
                    <strong>Адрес:</strong> {{ car.car_fleet.fleet.address }}
                  </p>
                  <p v-if="car.car_fleet.assigned_at">
                    <strong>Прикреплён:</strong> {{ formatDate(car.car_fleet.assigned_at) }}
                  </p>
                </v-card-text>
              </v-card>
            </div>

            <v-alert v-else-if="!car.specification" type="info" class="mt-6">
              Технические характеристики не указаны
            </v-alert>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
                color="primary"
                large
                @click="$router.push(`/cars/${car.id}/application`)"
                :disabled="car.status !== 'available'"
            >
              <v-icon left>mdi-file-document-edit</v-icon>
              Подать заявку на аренду
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-alert v-else-if="error" type="error">
      {{ error }}
      <v-btn @click="fetchCar" class="mt-2" color="error">Попробовать снова</v-btn>
    </v-alert>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CarDetail',
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      car: null,
      loading: true,
      error: null,
      specificationFields: [
        { field: 'engine_type', label: 'Тип двигателя' },
        { field: 'engine_volume', label: 'Объём двигателя', suffix: ' л' },
        { field: 'horsepower', label: 'Мощность', suffix: ' л.с.' },
        { field: 'transmission', label: 'Коробка передач' },
        { field: 'drivetrain', label: 'Привод' },
        { field: 'body_type', label: 'Тип кузова' },
        { field: 'fuel_consumption', label: 'Расход топлива', suffix: ' л/100км' },
        { field: 'color', label: 'Цвет' }
      ]
    }
  },
  computed: {
    carId() {
      return parseInt(this.id)
    }
  },
  methods: {
    async fetchCar() {
      try {
        this.loading = true
        this.error = null

        const response = await axios.get(`cars/${this.carId}/`)
        this.car = response.data.car
        console.log('Данные автомобиля загружены:', this.car)
      } catch (error) {
        console.error('Ошибка загрузки автомобиля:', error)
        this.error = error.response?.data?.detail || 'Не удалось загрузить данные автомобиля'
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
    },

    getFieldValue(field, value) {
      // Преобразование значений для определённых полей
      const mappings = {
        'engine_type': {
          'petrol': 'Бензин',
          'diesel': 'Дизель',
          'electric': 'Электро',
          'hybrid': 'Гибрид',
          'other': 'Другое'
        },
        'transmission': {
          'auto': 'Автомат',
          'manual': 'Механика',
          'cvt': 'Вариатор',
          'robot': 'Робот'
        },
        'drivetrain': {
          'fwd': 'Передний',
          'rwd': 'Задний',
          'awd': 'Полный'
        },
        'body_type': {
          'sedan': 'Седан',
          'hatchback': 'Хэтчбек',
          'suv': 'SUV',
          'wagon': 'Универсал',
          'van': 'Фургон',
          'coupe': 'Купе',
          'other': 'Другое'
        }
      }

      if (mappings[field] && mappings[field][value]) {
        return mappings[field][value]
      }

      // Добавляем суффикс если нужно
      const fieldConfig = this.specificationFields.find(f => f.field === field)
      if (fieldConfig?.suffix && value) {
        return value + fieldConfig.suffix
      }

      return value || '—'
    },

    formatDate(dateString) {
      if (!dateString) return 'Не указана'
      return new Date(dateString).toLocaleDateString('ru-RU')
    },

    formatDateTime(dateTimeString) {
      if (!dateTimeString) return 'Не указана'
      return new Date(dateTimeString).toLocaleString('ru-RU')
    }
  },

  mounted() {
    this.fetchCar()
  },

  watch: {
    id() {
      this.fetchCar()
    }
  }
}
</script>