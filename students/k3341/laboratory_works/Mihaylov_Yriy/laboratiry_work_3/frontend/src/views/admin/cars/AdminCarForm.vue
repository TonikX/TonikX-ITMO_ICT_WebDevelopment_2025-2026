<template>
  <div>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="headline">
            <v-icon class="mr-2">mdi-car</v-icon>
            {{ isEditMode ? 'Редактировать автомобиль' : 'Добавить новый автомобиль' }}
          </v-card-title>

          <v-card-subtitle v-if="isEditMode && car">
            ID: {{ car.id }} • {{ car.make }} {{ car.model }}
          </v-card-subtitle>

          <v-card-text>
            <v-form @submit.prevent="submitForm" ref="form" v-model="valid">
              <!-- Основная информация -->
              <h3 class="text-h6 mb-4">Основная информация</h3>

              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                      v-model="formData.make"
                      label="Марка*"
                      :rules="[v => !!v || 'Обязательное поле']"
                      required
                      prepend-icon="mdi-car"
                  ></v-text-field>
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                      v-model="formData.model"
                      label="Модель*"
                      :rules="[v => !!v || 'Обязательное поле']"
                      required
                      prepend-icon="mdi-car-info"
                  ></v-text-field>
                </v-col>
              </v-row>

              <v-row>
                <v-col cols="12" md="4">
                  <v-text-field
                      v-model="formData.year"
                      label="Год выпуска*"
                      :rules="[
                      v => !!v || 'Обязательное поле',
                      v => /^\d{4}$/.test(v) || 'Год должен быть 4 цифры',
                      v => parseInt(v) > 1900 || 'Некорректный год',
                      v => parseInt(v) <= new Date().getFullYear() + 1 || 'Год из будущего'
                    ]"
                      required
                      type="number"
                      prepend-icon="mdi-calendar"
                  ></v-text-field>
                </v-col>

                <v-col cols="12" md="4">
                  <v-text-field
                      v-model="formData.current_mileage"
                      label="Пробег (км)"
                      type="number"
                      :rules="[
                      v => !v || v >= 0 || 'Пробег не может быть отрицательным'
                    ]"
                      prepend-icon="mdi-gauge"
                      hint="Текущий пробег в километрах"
                  ></v-text-field>
                </v-col>

                <v-col cols="12" md="4">
                  <v-menu
                      v-model="purchaseDateMenu"
                      :close-on-content-click="false"
                      transition="scale-transition"
                      offset-y
                      min-width="auto"
                  >
                    <template v-slot:activator="{ on, attrs }">
                      <v-text-field
                          v-model="formData.purchase_date"
                          label="Дата покупки"
                          prepend-icon="mdi-calendar-check"
                          readonly
                          v-bind="attrs"
                          v-on="on"
                      ></v-text-field>
                    </template>
                    <v-date-picker
                        v-model="formData.purchase_date"
                        @input="purchaseDateMenu = false"
                        locale="ru-ru"
                    ></v-date-picker>
                  </v-menu>
                </v-col>
              </v-row>

              <!-- Уникальные идентификаторы -->
              <h3 class="text-h6 mb-4 mt-6">Уникальные идентификаторы</h3>

              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                      v-model="formData.vin"
                      label="VIN*"
                      :rules="[
                      v => !!v || 'Обязательное поле',
                      v => (v && v.length >= 10) || 'VIN должен быть не менее 10 символов'
                    ]"
                      required
                      prepend-icon="mdi-barcode"
                      hint="Уникальный идентификатор автомобиля"
                  ></v-text-field>
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                      v-model="formData.license_plate"
                      label="Государственный номер*"
                      :rules="[v => !!v || 'Обязательное поле']"
                      required
                      prepend-icon="mdi-numeric"
                      hint="Пример: А123БВ77"
                  ></v-text-field>
                </v-col>
              </v-row>

              <!-- Статус (только при редактировании) -->
              <div v-if="isEditMode" class="mt-6">
                <h3 class="text-h6 mb-4">Статус автомобиля</h3>

                <v-select
                    v-model="formData.status"
                    :items="statusOptions"
                    item-title="title"
                    item-value="value"
                    label="Статус"
                    clearable
                    prepend-icon="mdi-information"
                    :rules="[v => !!v || 'Выберите статус']"
                    required
                ></v-select>
              </div>

              <!-- Сообщения об ошибках/успехе -->
              <v-alert v-if="success" type="success" class="mt-4">
                <h4 class="text-h6">{{ successMessage }}</h4>
                <v-btn @click="goToList" color="success" class="mt-2">
                  Вернуться к списку
                </v-btn>
                <v-btn
                    v-if="!isEditMode"
                    @click="resetForm"
                    color="primary"
                    class="mt-2 ml-2"
                >
                  Добавить ещё один
                </v-btn>
              </v-alert>

              <v-alert v-if="error" type="error" class="mt-4">
                {{ errorMessage }}
              </v-alert>
            </v-form>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
                @click="goToList"
                color="secondary"
                class="mr-2"
            >
              <v-icon left>mdi-arrow-left</v-icon>
              Отмена
            </v-btn>

            <v-btn
                @click="submitForm"
                color="primary"
                :loading="loading"
                :disabled="!valid || success"
            >
              <v-icon left>{{ isEditMode ? 'mdi-content-save' : 'mdi-plus' }}</v-icon>
              {{ isEditMode ? 'Сохранить изменения' : 'Создать автомобиль' }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminCarForm',
  props: {
    id: {
      type: [String, Number],
      default: null
    }
  },
  data() {
    return {
      car: null,
      loading: false,
      valid: false,
      success: false,
      error: false,
      successMessage: '',
      errorMessage: '',
      purchaseDateMenu: false,

      formData: {
        make: '',
        model: '',
        year: '',
        vin: '',
        license_plate: '',
        current_mileage: '',
        purchase_date: '',
        status: 'available'  // По умолчанию для нового авто
      },

      statusOptions: [
        { title: 'Доступен', value: 'available' },
        { title: 'В аренде', value: 'leased' },
        { title: 'На обслуживании', value: 'maintenance' },
        { title: 'Продан', value: 'sold' }
      ]
    }
  },
  computed: {
    isEditMode() {
      return !!this.id
    },
    carId() {
      return this.id ? parseInt(this.id) : null
    }
  },
  methods: {
    async fetchCar() {
      if (!this.isEditMode) return

      try {
        this.loading = true
        const response = await axios.get(`admin/cars/${this.carId}/`)
        this.car = response.data.car

        // Заполняем форму данными авто
        this.formData = {
          make: this.car.make || '',
          model: this.car.model || '',
          year: this.car.year || '',
          vin: this.car.vin || '',
          license_plate: this.car.license_plate || '',
          current_mileage: this.car.current_mileage || '',
          purchase_date: this.car.purchase_date || '',
          status: this.car.status || 'available'
        }

      } catch (error) {
        console.error('Ошибка загрузки автомобиля:', error)
        this.error = true
        this.errorMessage = 'Не удалось загрузить данные автомобиля'
      } finally {
        this.loading = false
      }
    },

    async submitForm() {
      if (!this.$refs.form.validate()) return

      this.loading = true
      this.error = false
      this.success = false

      try {
        // Подготавливаем данные
        const payload = {
          make: this.formData.make.trim(),
          model: this.formData.model.trim(),
          year: parseInt(this.formData.year),
          vin: this.formData.vin.trim(),
          license_plate: this.formData.license_plate.trim(),
          status: this.formData.status, // При создании будет "available"
          current_mileage: this.formData.current_mileage ? parseInt(this.formData.current_mileage) : 0,
          purchase_date: this.formData.purchase_date || null
        }

        console.log('Отправляем данные:', payload)

        let response
        if (this.isEditMode) {
          // Редактирование (PATCH)
          response = await axios.patch(`admin/cars/${this.carId}/`, payload)
          this.successMessage = `Автомобиль "${this.formData.make} ${this.formData.model}" успешно обновлен!`
        } else {
          // Создание (POST)
          response = await axios.post('admin/cars/create/', payload)
          this.successMessage = `Автомобиль "${this.formData.make} ${this.formData.model}" успешно создан!`
        }

        console.log('Ответ сервера:', response.data)
        this.success = true

        // Если создаём новый - очищаем форму
        if (!this.isEditMode) {
          this.resetForm()
        }

      } catch (error) {
        console.error('Ошибка сохранения автомобиля:', error)
        this.error = true

        // Обработка ошибок от сервера
        if (error.response?.status === 400) {
          if (error.response.data?.error) {
            this.errorMessage = error.response.data.error
          } else if (error.response.data) {
            // Обработка ошибок валидации Django
            const errors = []
            for (const [field, messages] of Object.entries(error.response.data)) {
              const fieldName = this.getFieldLabel(field)
              errors.push(`${fieldName}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
            }
            this.errorMessage = errors.join('; ')
          } else {
            this.errorMessage = 'Ошибка при сохранении автомобиля'
          }
        } else if (error.code === 'ERR_NETWORK') {
          this.errorMessage = 'Ошибка сети. Проверьте подключение.'
        } else {
          this.errorMessage = 'Ошибка при сохранении автомобиля'
        }
      } finally {
        this.loading = false
      }
    },

    getFieldLabel(field) {
      const labels = {
        'make': 'Марка',
        'model': 'Модель',
        'year': 'Год выпуска',
        'vin': 'VIN',
        'license_plate': 'Гос. номер',
        'current_mileage': 'Пробег',
        'purchase_date': 'Дата покупки',
        'status': 'Статус'
      }
      return labels[field] || field
    },

    resetForm() {
      this.formData = {
        make: '',
        model: '',
        year: '',
        vin: '',
        license_plate: '',
        current_mileage: '',
        purchase_date: '',
        status: 'available'
      }
      this.$refs.form.resetValidation()
      this.success = false
    },

    goToList() {
      this.$router.push('/admin/cars')
    }
  },

  async mounted() {
    if (this.isEditMode) {
      await this.fetchCar()
    }
  }
}
</script>