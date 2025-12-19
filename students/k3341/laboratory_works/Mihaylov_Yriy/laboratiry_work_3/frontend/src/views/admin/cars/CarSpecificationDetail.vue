<template>
  <div>
    <v-row class="mb-4">
      <v-col cols="12" md="8" offset-md="2">
        <v-card>
          <v-card-title class="headline">
            <v-icon class="mr-2">mdi-car-info</v-icon>
            Характеристики автомобиля
          </v-card-title>

          <v-card-subtitle>
            Автомобиль: {{ car.make }} {{ car.model }} ({{ car.license_plate }})
          </v-card-subtitle>

          <v-card-text v-if="loading">
            <v-progress-linear indeterminate></v-progress-linear>
            <div class="text-center mt-4">Загрузка характеристик...</div>
          </v-card-text>

          <v-card-text v-else-if="!specification">
            <div class="text-center py-8">
              <v-icon size="64" color="grey">mdi-car-info</v-icon>
              <div class="text-h6 mt-4">Характеристики не добавлены</div>
              <div class="text-grey mt-2">Для этого автомобиля еще не добавлены характеристики</div>
              <v-btn
                  color="primary"
                  class="mt-4"
                  @click="$router.push(`/admin/cars/${id}/specifications/create`)"
              >
                <v-icon left>mdi-plus</v-icon>
                Добавить характеристики
              </v-btn>
            </div>
          </v-card-text>

          <v-card-text v-else>
            <v-row>
              <!-- Основные характеристики -->
              <v-col cols="12" md="6">
                <v-card variant="outlined" class="mb-4">
                  <v-card-title>Двигатель</v-card-title>
                  <v-card-text>
                    <div class="mb-3">
                      <strong>Тип двигателя:</strong>
                      <div class="mt-1">{{ getEngineTypeText(specification.engine_type) }}</div>
                    </div>

                    <div class="mb-3">
                      <strong>Объём двигателя:</strong>
                      <div class="mt-1">{{ specification.engine_volume ? `${specification.engine_volume} л` : '—' }}</div>
                    </div>

                    <div class="mb-3">
                      <strong>Мощность:</strong>
                      <div class="mt-1">{{ specification.horsepower ? `${specification.horsepower} л.с.` : '—' }}</div>
                    </div>

                    <div class="mb-3">
                      <strong>Расход топлива:</strong>
                      <div class="mt-1">{{ specification.fuel_consumption ? `${specification.fuel_consumption} л/100км` : '—' }}</div>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>

              <!-- Трансмиссия и кузов -->
              <v-col cols="12" md="6">
                <v-card variant="outlined" class="mb-4">
                  <v-card-title>Трансмиссия и кузов</v-card-title>
                  <v-card-text>
                    <div class="mb-3">
                      <strong>Коробка передач:</strong>
                      <div class="mt-1">{{ getTransmissionText(specification.transmission) }}</div>
                    </div>

                    <div class="mb-3">
                      <strong>Привод:</strong>
                      <div class="mt-1">{{ getDrivetrainText(specification.drivetrain) }}</div>
                    </div>

                    <div class="mb-3">
                      <strong>Тип кузова:</strong>
                      <div class="mt-1">{{ getBodyTypeText(specification.body_type) }}</div>
                    </div>

                    <div class="mb-3">
                      <strong>Цвет:</strong>
                      <div class="mt-1">{{ specification.color || '—' }}</div>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>

              <!-- Дополнительные опции -->
              <v-col cols="12">
                <v-card variant="outlined">
                  <v-card-title>Дополнительные опции</v-card-title>
                  <v-card-text>
                    <div v-if="specification.additional_options">
                      {{ specification.additional_options }}
                    </div>
                    <div v-else class="text-grey">
                      Дополнительные опции не указаны
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>

              <!-- Мета-информация -->
              <v-col cols="12">
                <v-card variant="outlined">
                  <v-card-title>Информация</v-card-title>
                  <v-card-text>
                    <div class="mb-2">
                      <strong>Дата создания:</strong>
                      <div class="mt-1">{{ formatDateTime(specification.created_at) }}</div>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>

            <!-- Кнопки действий -->
            <div class="d-flex justify-space-between mt-6">
              <v-btn @click="$router.back()" color="secondary">
                <v-icon left>mdi-arrow-left</v-icon>
                Назад
              </v-btn>

              <div v-if="!specification">
                <v-btn
                    color="primary"
                    @click="$router.push(`/admin/cars/${id}/specifications/create`)"
                >
                  <v-icon left>mdi-plus</v-icon>
                  Добавить характеристики
                </v-btn>
              </div>

              <!-- Пока убираем кнопку редактирования, так как нет эндпоинта -->
              <!--
              <v-btn
                v-if="specification"
                color="warning"
                @click="$router.push(`/admin/cars/${id}/specifications/edit`)"
              >
                <v-icon left>mdi-pencil</v-icon>
                Редактировать
              </v-btn>
              -->
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
  name: 'CarSpecificationDetail',
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      car: {},
      specification: null,
      loading: true,
      error: false,
      errorMessage: ''
    }
  },
  methods: {
    async fetchData() {
      try {
        this.loading = true

        // Загружаем автомобиль
        const carResponse = await axios.get(`admin/cars/${this.id}/`)
        this.car = carResponse.data.car

        // Проверяем, есть ли характеристики
        if (this.car.specification) {
          this.specification = this.car.specification
        }

        console.log('Данные загружены:', {
          car: this.car,
          specification: this.specification
        })

      } catch (error) {
        console.error('Ошибка загрузки данных:', error)
        this.error = true
        this.errorMessage = 'Не удалось загрузить данные'
      } finally {
        this.loading = false
      }
    },

    // Методы для преобразования значений в текст
    getEngineTypeText(value) {
      const map = {
        'petrol': 'Бензин',
        'diesel': 'Дизель',
        'electric': 'Электро',
        'hybrid': 'Гибрид',
        'other': 'Другое'
      }
      return map[value] || value || '—'
    },

    getTransmissionText(value) {
      const map = {
        'auto': 'Автомат',
        'manual': 'Механика',
        'cvt': 'Вариатор',
        'robot': 'Робот'
      }
      return map[value] || value || '—'
    },

    getDrivetrainText(value) {
      const map = {
        'fwd': 'Передний',
        'rwd': 'Задний',
        'awd': 'Полный'
      }
      return map[value] || value || '—'
    },

    getBodyTypeText(value) {
      const map = {
        'sedan': 'Седан',
        'hatchback': 'Хэтчбек',
        'suv': 'SUV',
        'wagon': 'Универсал',
        'van': 'Фургон',
        'coupe': 'Купе',
        'other': 'Другое'
      }
      return map[value] || value || '—'
    },

    formatDateTime(dateTimeString) {
      if (!dateTimeString) return '—'
      return new Date(dateTimeString).toLocaleString('ru-RU')
    }
  },
  mounted() {
    this.fetchData()
  }
}
</script>