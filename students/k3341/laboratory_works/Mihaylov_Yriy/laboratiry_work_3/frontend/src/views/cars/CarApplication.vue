<template>
  <v-container>
    <v-btn @click="$router.push(`/cars/${carId}`)" class="mb-4" color="secondary">
      <v-icon left>mdi-arrow-left</v-icon>
      Назад к автомобилю
    </v-btn>

    <v-row>
      <v-col cols="12" md="8" offset-md="2">
        <v-card>
          <v-card-title class="headline">
            <v-icon class="mr-2">mdi-file-document-edit</v-icon>
            Заявка на аренду автомобиля
          </v-card-title>

          <v-card-subtitle v-if="car">
            {{ car.make }} {{ car.model }} ({{ car.license_plate }})
          </v-card-subtitle>

          <v-card-text>
            <!-- Проверка доступности автомобиля -->
            <v-alert v-if="car && car.status !== 'available'" type="error" class="mb-6">
              <h4 class="text-h6">Автомобиль недоступен!</h4>
              <p>Автомобиль {{ car.make }} {{ car.model }} в данный момент
                <strong>{{ getStatusText(car.status).toLowerCase() }}</strong>
                и не может быть арендован.
              </p>
              <v-btn @click="$router.push('/cars')" color="primary" class="mt-2">
                Выбрать другой автомобиль
              </v-btn>
            </v-alert>

            <!-- Информация об автомобиле -->
            <v-alert v-if="car && car.status === 'available'" type="info" class="mb-6">
              <h4 class="text-h6">Выбранный автомобиль:</h4>
              <p><strong>Марка/Модель:</strong> {{ car.make }} {{ car.model }}</p>
              <p><strong>Гос. номер:</strong> {{ car.license_plate }}</p>
              <p><strong>Год выпуска:</strong> {{ car.year }}</p>
              <p><strong>VIN:</strong> {{ car.vin }}</p>
              <p v-if="car.current_mileage"><strong>Пробег:</strong> {{ car.current_mileage.toLocaleString() }} км</p>
            </v-alert>

            <!-- Форма заявки (только если автомобиль доступен) -->
            <v-form
                v-if="car && car.status === 'available'"
                @submit.prevent="submitApplication"
                ref="form"
                v-model="valid"
            >
              <h3 class="text-h6 mb-4">Данные компании*</h3>

              <v-text-field
                  v-model="formData.company_name"
                  label="Название компании*"
                  :rules="[
                  v => !!v || 'Обязательное поле',
                  v => (v && v.length <= 255) || 'Максимум 255 символов'
                ]"
                  required
                  prepend-icon="mdi-office-building"
                  counter="255"
              ></v-text-field>

              <v-text-field
                  v-model="formData.inn"
                  label="ИНН*"
                  :rules="[
                  v => !!v || 'Обязательное поле',
                  v => (v && v.length === 10) || 'ИНН должен содержать ровно 10 цифр',
                  v => /^\d+$/.test(v) || 'ИНН должен содержать только цифры'
                ]"
                  required
                  prepend-icon="mdi-card-account-details"
                  hint="10 цифр для юридических лиц"
                  counter="10"
              ></v-text-field>

              <h3 class="text-h6 mb-4 mt-6">Контактная информация</h3>

              <v-text-field
                  v-model="formData.contact_person"
                  label="Контактное лицо"
                  prepend-icon="mdi-account"
                  hint="ФИО ответственного лица"
                  :rules="[
                  v => !v || (v && v.length <= 255) || 'Максимум 255 символов'
                ]"
                  counter="255"
              ></v-text-field>

              <v-text-field
                  v-model="formData.email"
                  label="Email"
                  type="email"
                  prepend-icon="mdi-email"
                  :rules="[
                  v => !v || /.+@.+\..+/.test(v) || 'Введите корректный email'
                ]"
              ></v-text-field>

              <v-text-field
                  v-model="formData.phone"
                  label="Телефон*"
                  prepend-icon="mdi-phone"
                  :rules="[
                  v => !!v || 'Обязательное поле',
                  v => (v && v.length <= 50) || 'Максимум 50 символов'
                ]"
                  required
                  counter="50"
              ></v-text-field>

              <v-text-field
                  v-model="formData.address"
                  label="Адрес"
                  prepend-icon="mdi-map-marker"
                  :rules="[
                  v => !v || (v && v.length <= 255) || 'Максимум 255 символов'
                ]"
                  counter="255"
              ></v-text-field>

              <v-textarea
                  v-model="formData.additional_notes"
                  label="Дополнительные комментарии или пожелания"
                  rows="3"
                  prepend-icon="mdi-note-text"
                  placeholder="Укажите дополнительные требования к аренде, желаемые сроки и т.д."
                  class="mt-4"
              ></v-textarea>

              <!-- Сообщения об ошибках/успехе -->
              <v-alert v-if="success" type="success" class="mt-4">
                <h4 class="text-h6">Заявка успешно создана!</h4>
                <p><strong>Номер заявки:</strong> {{ applicationData.application.id }}</p>
                <p><strong>Дата создания:</strong> {{ formatDateTime(applicationData.application.created_at) }}</p>
                <p><strong>Статус:</strong> Ожидает рассмотрения</p>

                <div v-if="applicationData.client_created" class="mt-3">
                  <v-icon color="success">mdi-check-circle</v-icon>
                  <strong>Новая компания добавлена в базу:</strong>
                  <p class="mt-1 mb-0">{{ applicationData.application.client.company_name }}</p>
                  <p class="mt-0">ИНН: {{ applicationData.application.client.inn }}</p>
                </div>
                <div v-else class="mt-3">
                  <v-icon color="info">mdi-information</v-icon>
                  <span>Использована существующая компания из базы</span>
                </div>

                <v-btn @click="goToHome" color="success" class="mt-3">
                  <v-icon left>mdi-home</v-icon>
                  Вернуться на главную
                </v-btn>
                <v-btn @click="goToCars" color="primary" class="mt-3 ml-2">
                  <v-icon left>mdi-car</v-icon>
                  Посмотреть другие автомобили
                </v-btn>
              </v-alert>

              <v-alert v-if="error" type="error" class="mt-4">
                {{ errorMessage }}
              </v-alert>
            </v-form>
          </v-card-text>

          <v-card-actions v-if="car && car.status === 'available'">
            <v-spacer></v-spacer>
            <v-btn
                @click="submitApplication"
                color="primary"
                :loading="loading"
                :disabled="!valid || success"
                large
            >
              <v-icon left>mdi-send</v-icon>
              Отправить заявку
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CarApplication',
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      car: null,
      loading: false,
      valid: false,
      success: false,
      error: false,
      errorMessage: '',
      applicationData: null,

      formData: {
        company_name: '',
        inn: '',
        contact_person: '',
        email: '',
        phone: '',
        address: '',
        additional_notes: ''
      }
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
        const response = await axios.get(`cars/${this.carId}/`)
        this.car = response.data.car

        // Если автомобиль недоступен, показываем ошибку сразу
        if (this.car.status !== 'available') {
          this.error = true
          this.errorMessage = `Автомобиль ${this.car.make} ${this.car.model} в данный момент ${this.getStatusText(this.car.status).toLowerCase()} и не может быть арендован.`
        }
      } catch (error) {
        console.error('Ошибка загрузки автомобиля:', error)
        this.error = true
        this.errorMessage = 'Не удалось загрузить данные автомобиля'
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

    formatDateTime(dateTimeString) {
      if (!dateTimeString) return 'Не указана'
      return new Date(dateTimeString).toLocaleString('ru-RU')
    },

    async submitApplication() {
      if (!this.$refs.form.validate()) return

      this.loading = true
      this.error = false

      try {
        // Подготавливаем данные для отправки
        const payload = {
          company_name: this.formData.company_name.trim(),
          inn: this.formData.inn.trim(),
          contact_person: this.formData.contact_person.trim() || '',
          email: this.formData.email.trim() || '',
          phone: this.formData.phone.trim() || '',
          address: this.formData.address.trim() || ''
        }

        console.log('Отправляем заявку:', payload)

        const response = await axios.post(`cars/${this.carId}/application/`, payload)

        this.success = true
        this.applicationData = response.data
        console.log('Заявка создана:', response.data)

        // Очищаем форму
        this.formData = {
          company_name: '',
          inn: '',
          contact_person: '',
          email: '',
          phone: '',
          address: '',
          additional_notes: ''
        }
        this.$refs.form.resetValidation()

      } catch (error) {
        console.error('Ошибка отправки заявки:', error)
        this.error = true

        // Обработка ошибок от сервера
        if (error.response?.status === 400 && error.response?.data?.error) {
          this.errorMessage = error.response.data.error
        } else if (error.response?.data?.detail) {
          this.errorMessage = error.response.data.detail
        } else if (error.response?.data) {
          // Обработка ошибок валидации Django
          const errors = []
          for (const [field, messages] of Object.entries(error.response.data)) {
            const fieldName = this.getFieldLabel(field)
            errors.push(`${fieldName}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
          }
          this.errorMessage = errors.join('; ')
        } else if (error.code === 'ERR_NETWORK') {
          this.errorMessage = 'Ошибка сети. Проверьте подключение к интернету.'
        } else {
          this.errorMessage = 'Ошибка при отправке заявки.'
        }
      } finally {
        this.loading = false
      }
    },

    getFieldLabel(field) {
      const labels = {
        'company_name': 'Название компании',
        'inn': 'ИНН',
        'contact_person': 'Контактное лицо',
        'email': 'Email',
        'phone': 'Телефон',
        'address': 'Адрес'
      }
      return labels[field] || field
    },

    goToHome() {
      this.$router.push('/')
    },

    goToCars() {
      this.$router.push('/cars')
    }
  },

  async mounted() {
    await this.fetchCar()
  }
}
</script>

<style scoped>
/* Дополнительные стили при необходимости */
</style>