<template>
  <div>
    <v-row class="mb-4">
      <v-col cols="12" md="8" offset-md="2">
        <v-card>
          <v-card-title class="headline">
            <v-icon class="mr-2">mdi-car-info</v-icon>
            {{ isEdit ? 'Редактирование характеристик' : 'Добавление характеристик' }}
          </v-card-title>

          <v-card-subtitle>
            Автомобиль: {{ car.make }} {{ car.model }} ({{ car.license_plate }})
          </v-card-subtitle>

          <v-card-text v-if="loading">
            <v-progress-linear indeterminate></v-progress-linear>
            <div class="text-center mt-4">Загрузка данных...</div>
          </v-card-text>

          <v-card-text v-else>
            <v-form ref="form" v-model="valid" @submit.prevent="submitForm">
              <!-- Тип двигателя -->
              <v-select
                  v-model="formData.engine_type"
                  :items="engineTypeOptions"
                  item-title="text"
                  item-value="value"
                  label="Тип двигателя"
                  prepend-icon="mdi-engine"
                  clearable
              ></v-select>

              <!-- Объем двигателя -->
              <v-text-field
                  v-model="formData.engine_volume"
                  label="Объём двигателя (л)"
                  type="number"
                  step="0.01"
                  min="0"
                  prepend-icon="mdi-engine-outline"
              ></v-text-field>

              <!-- Мощность -->
              <v-text-field
                  v-model="formData.horsepower"
                  label="Мощность (л.с.)"
                  type="number"
                  min="0"
                  prepend-icon="mdi-speedometer"
              ></v-text-field>

              <!-- Коробка передач -->
              <v-select
                  v-model="formData.transmission"
                  :items="transmissionOptions"
                  item-title="text"
                  item-value="value"
                  label="Коробка передач"
                  prepend-icon="mdi-cog"
                  clearable
              ></v-select>

              <!-- Привод -->
              <v-select
                  v-model="formData.drivetrain"
                  :items="drivetrainOptions"
                  item-title="text"
                  item-value="value"
                  label="Привод"
                  prepend-icon="mdi-car"
                  clearable
              ></v-select>

              <!-- Тип кузова -->
              <v-select
                  v-model="formData.body_type"
                  :items="bodyTypeOptions"
                  item-title="text"
                  item-value="value"
                  label="Тип кузова"
                  prepend-icon="mdi-car-estate"
                  clearable
              ></v-select>

              <!-- Расход топлива -->
              <v-text-field
                  v-model="formData.fuel_consumption"
                  label="Расход топлива (л/100км)"
                  type="number"
                  step="0.01"
                  min="0"
                  prepend-icon="mdi-gas-station"
              ></v-text-field>

              <!-- Цвет -->
              <v-text-field
                  v-model="formData.color"
                  label="Цвет"
                  prepend-icon="mdi-palette"
              ></v-text-field>

              <!-- Дополнительные опции -->
              <v-textarea
                  v-model="formData.additional_options"
                  label="Дополнительные опции"
                  prepend-icon="mdi-checkbox-multiple-marked"
                  rows="3"
              ></v-textarea>

              <v-alert v-if="error" type="error" class="mt-4">
                {{ errorMessage }}
              </v-alert>

              <v-alert v-if="success" type="success" class="mt-4">
                {{ successMessage }}
              </v-alert>

              <div class="d-flex justify-space-between mt-6">
                <v-btn @click="goBack" color="secondary">
                  <v-icon left>mdi-arrow-left</v-icon>
                  Назад
                </v-btn>

                <v-btn
                    type="submit"
                    color="primary"
                    :loading="submitting"
                    :disabled="!valid || success"
                >
                  {{ isEdit ? 'Сохранить изменения' : 'Добавить характеристики' }}
                </v-btn>
              </div>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CarSpecificationForm',
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      car: {},
      loading: true,
      valid: false,
      submitting: false,
      error: false,
      success: false,
      errorMessage: '',
      successMessage: '',

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
      ],

      // Форма
      formData: {
        engine_type: null,
        engine_volume: '',
        horsepower: '',
        transmission: null,
        drivetrain: null,
        body_type: null,
        fuel_consumption: '',
        color: '',
        additional_options: ''
      }
    }
  },
  computed: {
    isEdit() {
      // Здесь можно проверить, если у автомобиля уже есть характеристики
      return false // Пока только создание, так как нет эндпоинта для редактирования
    }
  },
  methods: {
    async fetchCar() {
      try {
        this.loading = true
        const response = await axios.get(`admin/cars/${this.id}/`)
        this.car = response.data.car
        console.log('Автомобиль загружен:', this.car)
      } catch (error) {
        console.error('Ошибка загрузки автомобиля:', error)
        this.error = true
        this.errorMessage = 'Не удалось загрузить данные автомобиля'
      } finally {
        this.loading = false
      }
    },

    goBack() {
      this.$router.push(`/admin/cars/${this.id}`)
    },

    async submitForm() {
      if (!this.$refs.form.validate()) return

      this.submitting = true
      this.error = false
      this.success = false

      try {
        // Подготавливаем данные для отправки
        const payload = {
          ...this.formData,
          // Преобразуем пустые строки в null
          engine_volume: this.formData.engine_volume || null,
          horsepower: this.formData.horsepower || null,
          fuel_consumption: this.formData.fuel_consumption || null,
          color: this.formData.color || '',
          additional_options: this.formData.additional_options || ''
        }

        console.log('Отправляем характеристики:', payload)

        // Отправляем POST запрос
        const response = await axios.post(`admin/cars/${this.id}/specifications/create`, payload)

        this.successMessage = 'Характеристики успешно добавлены!'
        this.success = true

        // Через 2 секунды переходим обратно к автомобилю
        setTimeout(() => {
          this.$router.push(`/admin/cars/${this.id}`)
        }, 2000)

      } catch (error) {
        console.error('Ошибка сохранения характеристик:', error)
        this.error = true

        if (error.response?.status === 400) {
          // Ошибки валидации от Django
          if (error.response.data) {
            // Преобразуем ошибки валидации в строку
            const errors = Object.values(error.response.data).flat()
            this.errorMessage = errors.join(', ')
          } else {
            this.errorMessage = 'Ошибка валидации данных'
          }
        } else if (error.response?.data?.detail) {
          this.errorMessage = error.response.data.detail
        } else {
          this.errorMessage = 'Ошибка при сохранении характеристик'
        }
      } finally {
        this.submitting = false
      }
    }
  },
  mounted() {
    this.fetchCar()
  }
}
</script>