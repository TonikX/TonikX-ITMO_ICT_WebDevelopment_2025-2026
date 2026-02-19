<template>
  <div>
    <!-- Навигация -->
    <v-row class="mb-4">
      <v-col cols="12">
        <v-btn @click="$router.push('/admin/cars')" color="secondary" class="mr-2">
          <v-icon left>mdi-arrow-left</v-icon>
          К списку автомобилей
        </v-btn>

        <v-btn @click="$router.push(`/admin/cars/${carId}/edit`)" color="warning" class="mr-2">
          <v-icon left>mdi-pencil</v-icon>
          Редактировать
        </v-btn>

        <!-- Кнопка обслуживания -->
        <v-btn color="info" @click="$router.push(`/admin/cars/${carId}/maintenance`)" class="mr-2">
          <v-icon left>mdi-wrench</v-icon>
          Обслуживание
        </v-btn>

        <!-- Кнопка удаления (пока disabled) -->
        <v-btn color="error" disabled>
          <v-icon left>mdi-delete</v-icon>
          Удалить
        </v-btn>
      </v-col>
    </v-row>

    <!-- Загрузка -->
    <v-row v-if="loading">
      <v-col cols="12">
        <v-progress-linear indeterminate color="primary"></v-progress-linear>
        <div class="text-center mt-4">Загрузка данных автомобиля...</div>
      </v-col>
    </v-row>

    <!-- Основная информация -->
    <v-row v-else-if="car">
      <v-col cols="12" md="8">
        <!-- Карточка основная информация -->
        <v-card class="mb-4">
          <v-card-title class="headline d-flex align-center">
            <div>
              {{ car.make }} {{ car.model }}
              <v-chip class="ml-4" :color="getStatusColor(car.status)" dark large>
                {{ getStatusText(car.status) }}
              </v-chip>
            </div>
          </v-card-title>

          <v-card-subtitle class="text-h6 d-flex align-center flex-wrap">
            <div class="d-flex align-center mr-4 mb-1">
              <v-icon class="mr-2">mdi-numeric</v-icon>
              {{ car.license_plate || 'Нет номера' }}
            </div>
            <div class="d-flex align-center mr-4 mb-1">
              <v-icon class="mr-2">mdi-calendar</v-icon>
              {{ car.year }} год
            </div>
            <div class="d-flex align-center mr-4 mb-1">
              <v-icon class="mr-2">mdi-gauge</v-icon>
              {{ car.current_mileage?.toLocaleString('ru-RU') || '0' }} км
            </div>
            <div class="d-flex align-center mb-1">
              <v-icon class="mr-2">mdi-barcode</v-icon>
              VIN: {{ car.vin || 'Не указан' }}
            </div>
          </v-card-subtitle>

          <v-divider class="my-4"></v-divider>

          <v-card-text>
            <v-row>
              <v-col cols="6" md="3">
                <div class="info-item">
                  <div class="text-caption text-grey">Дата добавления</div>
                  <div class="text-body-1 font-weight-medium">{{ formatDateTime(car.created_at) }}</div>
                </div>
              </v-col>

              <v-col cols="6" md="3">
                <div class="info-item">
                  <div class="text-caption text-grey">ID</div>
                  <div class="text-body-1 font-weight-medium">#{{ car.id }}</div>
                </div>
              </v-col>

              <v-col cols="6" md="3">
                <div class="info-item">
                  <div class="text-caption text-grey">Статус</div>
                  <div>
                    <v-chip :color="getStatusColor(car.status)" dark small>
                      {{ getStatusText(car.status) }}
                    </v-chip>
                  </div>
                </div>
              </v-col>

              <v-col cols="6" md="3">
                <div class="info-item">
                  <div class="text-caption text-grey">Дата покупки</div>
                  <div class="text-body-1 font-weight-medium">{{ formatDate(car.purchase_date) }}</div>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <!-- Характеристики -->
        <v-card>
          <v-card-title class="headline d-flex justify-space-between align-center">
            <div>
              <v-icon class="mr-2">mdi-car-info</v-icon>
              Технические характеристики
            </div>
            <div v-if="car.specification">
              <v-btn
                  color="warning"
                  size="small"
                  @click="showEditSpecDialog"
                  class="mr-2"
              >
                <v-icon left small>mdi-pencil</v-icon>
                Редактировать
              </v-btn>
              <v-btn
                  color="error"
                  size="small"
                  @click="showDeleteSpecDialog"
              >
                <v-icon left small>mdi-delete</v-icon>
                Удалить
              </v-btn>
            </div>
          </v-card-title>

          <v-card-text>
            <!-- Если характеристики есть -->
            <div v-if="car.specification">
              <v-row>
                <!-- Левая колонка -->
                <v-col cols="12" md="6">
                  <div class="spec-item mb-4">
                    <div class="text-caption text-grey">Тип двигателя</div>
                    <div class="text-body-1 font-weight-medium">{{ getEngineTypeText(car.specification.engine_type) }}</div>
                  </div>

                  <div class="spec-item mb-4">
                    <div class="text-caption text-grey">Объём двигателя</div>
                    <div class="text-body-1 font-weight-medium">{{ car.specification.engine_volume ? `${car.specification.engine_volume} л` : '—' }}</div>
                  </div>

                  <div class="spec-item mb-4">
                    <div class="text-caption text-grey">Мощность</div>
                    <div class="text-body-1 font-weight-medium">{{ car.specification.horsepower ? `${car.specification.horsepower} л.с.` : '—' }}</div>
                  </div>

                  <div class="spec-item mb-4">
                    <div class="text-caption text-grey">Коробка передач</div>
                    <div class="text-body-1 font-weight-medium">{{ getTransmissionText(car.specification.transmission) }}</div>
                  </div>
                </v-col>

                <!-- Правая колонка -->
                <v-col cols="12" md="6">
                  <div class="spec-item mb-4">
                    <div class="text-caption text-grey">Привод</div>
                    <div class="text-body-1 font-weight-medium">{{ getDrivetrainText(car.specification.drivetrain) }}</div>
                  </div>

                  <div class="spec-item mb-4">
                    <div class="text-caption text-grey">Тип кузова</div>
                    <div class="text-body-1 font-weight-medium">{{ getBodyTypeText(car.specification.body_type) }}</div>
                  </div>

                  <div class="spec-item mb-4">
                    <div class="text-caption text-grey">Расход топлива</div>
                    <div class="text-body-1 font-weight-medium">{{ car.specification.fuel_consumption ? `${car.specification.fuel_consumption} л/100км` : '—' }}</div>
                  </div>

                  <div class="spec-item mb-4">
                    <div class="text-caption text-grey">Цвет</div>
                    <div class="text-body-1 font-weight-medium">{{ car.specification.color || '—' }}</div>
                  </div>
                </v-col>
              </v-row>

              <!-- Дополнительные опции -->
              <div v-if="car.specification.additional_options" class="mt-6">
                <v-card variant="outlined">
                  <v-card-title class="text-subtitle-1 font-weight-bold">Дополнительные опции</v-card-title>
                  <v-card-text>
                    {{ car.specification.additional_options }}
                  </v-card-text>
                </v-card>
              </div>

              <v-alert type="info" class="mt-4">
                <div class="d-flex justify-space-between align-center">
                  <span>Характеристики созданы: {{ formatDateTime(car.specification.created_at) }}</span>
                  <span>ID: {{ car.specification.id }}</span>
                </div>
              </v-alert>
            </div>

            <!-- Если характеристик нет -->
            <div v-else>
              <v-alert type="warning" class="mb-4">
                Технические характеристики не указаны
              </v-alert>

              <div class="text-center">
                <v-btn
                    color="primary"
                    @click="$router.push(`/admin/cars/${car.id}/specifications/create`)"
                    size="large"
                >
                  <v-icon left>mdi-plus</v-icon>
                  Добавить характеристики
                </v-btn>
                <div class="text-caption text-grey mt-2">
                  Добавьте технические характеристики автомобиля для полной информации
                </div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Боковая панель -->
      <v-col cols="12" md="4">
        <!-- Быстрые действия -->
        <v-card class="mb-4">
          <v-card-title>Быстрые действия</v-card-title>
          <v-card-text>
            <v-list density="comfortable">
              <v-list-item
                  @click="copyCarInfo"
                  prepend-icon="mdi-content-copy"
                  title="Копировать информацию"
                  value="copy"
              ></v-list-item>

              <v-list-item
                  @click="$router.push(`/admin/cars/${car.id}/maintenance`)"
                  prepend-icon="mdi-wrench"
                  title="Обслуживание"
                  value="maintenance"
              ></v-list-item>

              <v-list-item
                  v-if="!car.specification"
                  @click="$router.push(`/admin/cars/${car.id}/specifications/create`)"
                  prepend-icon="mdi-car-info"
                  title="Добавить характеристики"
                  value="add-spec"
              ></v-list-item>

              <v-list-item
                  @click="$router.push(`/admin/leases?car_id=${car.id}`)"
                  prepend-icon="mdi-history"
                  title="История аренд"
                  value="leases"
              ></v-list-item>
            </v-list>
          </v-card-text>
        </v-card>

        <!-- Статус автомобиля -->
        <v-card>
          <v-card-title>Статус автомобиля</v-card-title>
          <v-card-text>
            <div class="text-center">
              <v-chip
                  :color="getStatusColor(car.status)"
                  dark
                  size="large"
                  class="mb-4"
              >
                <v-icon left>{{ getStatusIcon(car.status) }}</v-icon>
                {{ getStatusText(car.status) }}
              </v-chip>

              <div class="text-caption text-grey">
                {{ getStatusDescription(car.status) }}
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Ошибка -->
    <v-alert v-else-if="error" type="error">
      {{ errorMessage }}
      <v-btn @click="fetchCar" class="mt-2" color="error">Попробовать снова</v-btn>
    </v-alert>

    <!-- Диалог редактирования характеристик -->
    <v-dialog v-model="editSpecDialog" max-width="600">
      <v-card>
        <v-card-title>Редактирование характеристик</v-card-title>
        <v-card-text>
          <v-form ref="editSpecForm" v-model="editSpecValid">
            <!-- Тип двигателя -->
            <v-select
                v-model="editSpecForm.engine_type"
                :items="engineTypeOptions"
                item-title="text"
                item-value="value"
                label="Тип двигателя"
                prepend-icon="mdi-engine"
                clearable
            ></v-select>

            <!-- Объем двигателя -->
            <v-text-field
                v-model="editSpecForm.engine_volume"
                label="Объём двигателя (л)"
                type="number"
                step="0.01"
                min="0"
                prepend-icon="mdi-engine-outline"
            ></v-text-field>

            <!-- Мощность -->
            <v-text-field
                v-model="editSpecForm.horsepower"
                label="Мощность (л.с.)"
                type="number"
                min="0"
                prepend-icon="mdi-speedometer"
            ></v-text-field>

            <!-- Коробка передач -->
            <v-select
                v-model="editSpecForm.transmission"
                :items="transmissionOptions"
                item-title="text"
                item-value="value"
                label="Коробка передач"
                prepend-icon="mdi-cog"
                clearable
            ></v-select>

            <!-- Привод -->
            <v-select
                v-model="editSpecForm.drivetrain"
                :items="drivetrainOptions"
                item-title="text"
                item-value="value"
                label="Привод"
                prepend-icon="mdi-car"
                clearable
            ></v-select>

            <!-- Тип кузова -->
            <v-select
                v-model="editSpecForm.body_type"
                :items="bodyTypeOptions"
                item-title="text"
                item-value="value"
                label="Тип кузова"
                prepend-icon="mdi-car-estate"
                clearable
            ></v-select>

            <!-- Расход топлива -->
            <v-text-field
                v-model="editSpecForm.fuel_consumption"
                label="Расход топлива (л/100км)"
                type="number"
                step="0.01"
                min="0"
                prepend-icon="mdi-gas-station"
            ></v-text-field>

            <!-- Цвет -->
            <v-text-field
                v-model="editSpecForm.color"
                label="Цвет"
                prepend-icon="mdi-palette"
            ></v-text-field>

            <!-- Дополнительные опции -->
            <v-textarea
                v-model="editSpecForm.additional_options"
                label="Дополнительные опции"
                prepend-icon="mdi-checkbox-multiple-marked"
                rows="3"
            ></v-textarea>

            <v-alert v-if="editSpecError" type="error" class="mt-4">
              {{ editSpecErrorMessage }}
            </v-alert>

            <v-alert v-if="editSpecSuccess" type="success" class="mt-4">
              Характеристики успешно обновлены!
            </v-alert>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="editSpecDialog = false" color="secondary">Отмена</v-btn>
          <v-btn
              @click="updateSpecification"
              color="primary"
              :loading="editSpecLoading"
              :disabled="!editSpecValid || editSpecSuccess"
          >
            Сохранить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог удаления характеристик -->
    <v-dialog v-model="deleteSpecDialog" max-width="500">
      <v-card>
        <v-card-title class="headline">Подтверждение удаления</v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить характеристики автомобиля?
          <v-alert type="warning" class="mt-4">
            Это действие нельзя отменить. Все технические характеристики будут удалены.
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="deleteSpecDialog = false" color="secondary">Отмена</v-btn>
          <v-btn @click="deleteSpecification" color="error" :loading="deleteSpecLoading">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminCarDetail',
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
      error: false,
      errorMessage: '',

      // Диалог редактирования характеристик
      editSpecDialog: false,
      editSpecLoading: false,
      editSpecValid: false,
      editSpecError: false,
      editSpecSuccess: false,
      editSpecErrorMessage: '',

      editSpecForm: {
        engine_type: null,
        engine_volume: '',
        horsepower: '',
        transmission: null,
        drivetrain: null,
        body_type: null,
        fuel_consumption: '',
        color: '',
        additional_options: ''
      },

      // Диалог удаления характеристик
      deleteSpecDialog: false,
      deleteSpecLoading: false,

      // Опции для селектов
      engineTypeOptions: [
        { value: 'petrol', text: 'Бензин' },
        { value: 'diesel', text: 'Дизель' },
        { value: 'electric', text: 'Электро' },
        { value: 'hybrid', text: 'Гибрид' },
        { value: 'other', text: 'Другое' }
      ],

      transmissionOptions: [
        { value: 'auto', text: 'Автомат' },
        { value: 'manual', text: 'Механика' },
        { value: 'cvt', text: 'Вариатор' },
        { value: 'robot', text: 'Робот' }
      ],

      drivetrainOptions: [
        { value: 'fwd', text: 'Передний' },
        { value: 'rwd', text: 'Задний' },
        { value: 'awd', text: 'Полный' }
      ],

      bodyTypeOptions: [
        { value: 'sedan', text: 'Седан' },
        { value: 'hatchback', text: 'Хэтчбек' },
        { value: 'suv', text: 'SUV' },
        { value: 'wagon', text: 'Универсал' },
        { value: 'van', text: 'Фургон' },
        { value: 'coupe', text: 'Купе' },
        { value: 'other', text: 'Другое' }
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
        this.error = false

        const response = await axios.get(`admin/cars/${this.carId}/`)
        this.car = response.data.car
        console.log('Данные автомобиля загружены:', this.car)

      } catch (error) {
        console.error('Ошибка загрузки автомобиля:', error)
        this.error = true
        this.errorMessage = error.response?.data?.detail || 'Не удалось загрузить данные автомобиля'
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

    getStatusIcon(status) {
      const icons = {
        'available': 'mdi-check-circle',
        'leased': 'mdi-car-key',
        'maintenance': 'mdi-wrench',
        'sold': 'mdi-cash'
      }
      return icons[status] || 'mdi-car'
    },

    getStatusDescription(status) {
      const descriptions = {
        'available': 'Автомобиль доступен для аренды',
        'leased': 'Автомобиль находится в аренде',
        'maintenance': 'Автомобиль проходит техническое обслуживание',
        'sold': 'Автомобиль продан и недоступен для аренды'
      }
      return descriptions[status] || 'Статус автомобиля'
    },

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

    formatDate(dateString) {
      if (!dateString) return 'Не указана'
      return new Date(dateString).toLocaleDateString('ru-RU')
    },

    formatDateTime(dateTimeString) {
      if (!dateTimeString) return 'Не указана'
      return new Date(dateTimeString).toLocaleString('ru-RU')
    },

    showEditSpecDialog() {
      if (!this.car.specification) return

      // Заполняем форму текущими данными
      this.editSpecForm = {
        engine_type: this.car.specification.engine_type || null,
        engine_volume: this.car.specification.engine_volume || '',
        horsepower: this.car.specification.horsepower || '',
        transmission: this.car.specification.transmission || null,
        drivetrain: this.car.specification.drivetrain || null,
        body_type: this.car.specification.body_type || null,
        fuel_consumption: this.car.specification.fuel_consumption || '',
        color: this.car.specification.color || '',
        additional_options: this.car.specification.additional_options || ''
      }

      this.editSpecDialog = true
      this.editSpecError = false
      this.editSpecSuccess = false
    },

    showDeleteSpecDialog() {
      this.deleteSpecDialog = true
    },

    async updateSpecification() {
      if (!this.$refs.editSpecForm.validate()) return

      this.editSpecLoading = true
      this.editSpecError = false
      this.editSpecSuccess = false

      try {
        const payload = {
          id: this.car.specification.id,
          ...this.editSpecForm,
          // Преобразуем пустые строки в null
          engine_volume: this.editSpecForm.engine_volume || null,
          horsepower: this.editSpecForm.horsepower || null,
          fuel_consumption: this.editSpecForm.fuel_consumption || null,
          color: this.editSpecForm.color || '',
          additional_options: this.editSpecForm.additional_options || '',
          // Обязательное поле для связи
          car: this.car.id
        }

        console.log('Обновляем характеристики:', payload)

        const response = await axios.patch('admin/car_specifications/', payload)

        this.editSpecSuccess = true
        console.log('Характеристики обновлены:', response.data)

        // Обновляем данные автомобиля через 2 секунды
        setTimeout(() => {
          this.fetchCar()
          this.editSpecDialog = false
        }, 2000)

      } catch (error) {
        console.error('Ошибка обновления характеристик:', error)
        this.editSpecError = true

        if (error.response?.status === 400 && error.response?.data?.error) {
          this.editSpecErrorMessage = error.response.data.error
        } else if (error.response?.data?.detail) {
          this.editSpecErrorMessage = error.response.data.detail
        } else if (error.response?.data) {
          // Ошибки валидации Django
          const errors = Object.values(error.response.data).flat()
          this.editSpecErrorMessage = errors.join(', ')
        } else {
          this.editSpecErrorMessage = 'Ошибка при обновлении характеристик'
        }
      } finally {
        this.editSpecLoading = false
      }
    },

    async deleteSpecification() {
      this.deleteSpecLoading = true

      try {
        const payload = {
          id: this.car.specification.id
        }

        console.log('Удаляем характеристики:', payload)

        await axios.delete('admin/car_specifications/', { data: payload })

        // Обновляем данные автомобиля
        this.fetchCar()
        this.deleteSpecDialog = false

      } catch (error) {
        console.error('Ошибка удаления характеристик:', error)

        if (error.response?.status === 400 && error.response?.data?.error) {
          alert(`Ошибка: ${error.response.data.error}`)
        } else if (error.response?.data?.detail) {
          alert(`Ошибка: ${error.response.data.detail}`)
        } else {
          alert('Ошибка при удалении характеристик')
        }
      } finally {
        this.deleteSpecLoading = false
      }
    },

    copyCarInfo() {
      const text = `Автомобиль: ${this.car.make} ${this.car.model}
ID: ${this.car.id}
Гос. номер: ${this.car.license_plate}
VIN: ${this.car.vin}
Год: ${this.car.year}
Статус: ${this.getStatusText(this.car.status)}
Пробег: ${this.car.current_mileage} км`

      navigator.clipboard.writeText(text)
          .then(() => {
            alert('Информация скопирована в буфер обмена')
          })
          .catch(err => {
            console.error('Ошибка копирования:', err)
          })
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

<style scoped>
.info-item {
  padding: 8px 0;
}

.spec-item {
  padding: 8px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}

.spec-item:last-child {
  border-bottom: none;
}
</style>