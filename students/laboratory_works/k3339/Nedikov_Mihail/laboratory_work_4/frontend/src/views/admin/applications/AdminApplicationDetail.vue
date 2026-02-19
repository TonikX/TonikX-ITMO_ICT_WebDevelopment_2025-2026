<template>
  <div>
    <!-- Навигация -->
    <v-row class="mb-4">
      <v-col cols="12">
        <v-btn @click="$router.push('/admin/applications')" color="secondary" class="mr-2">
          <v-icon left>mdi-arrow-left</v-icon>
          К списку заявок
        </v-btn>
      </v-col>
    </v-row>

    <!-- Загрузка -->
    <v-row v-if="loading">
      <v-col cols="12">
        <v-progress-linear indeterminate color="primary"></v-progress-linear>
        <div class="text-center mt-4">Загрузка данных заявки...</div>
      </v-col>
    </v-row>

    <!-- Основная информация -->
    <v-row v-else-if="application">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title class="headline">
            Заявка на аренду #{{ application.id }}
            <v-chip class="ml-4" color="orange" dark>
              Ожидает рассмотрения
            </v-chip>
          </v-card-title>

          <v-card-subtitle>
            Подана: {{ formatDateTime(application.created_at) }}
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
                        {{ application.car.make }} {{ application.car.model }}
                      </v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="6" md="4">
                    <v-list-item>
                      <v-list-item-title>Гос. номер</v-list-item-title>
                      <v-list-item-subtitle class="text-h6">
                        {{ application.car.license_plate }}
                      </v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="6" md="4">
                    <v-list-item>
                      <v-list-item-title>Год выпуска</v-list-item-title>
                      <v-list-item-subtitle class="text-h6">
                        {{ application.car.year }}
                      </v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="6" md="4">
                    <v-list-item>
                      <v-list-item-title>Статус авто</v-list-item-title>
                      <v-list-item-subtitle>
                        <v-chip :color="getCarStatusColor(application.car.status)" dark small>
                          {{ getCarStatusText(application.car.status) }}
                        </v-chip>
                      </v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="6" md="4">
                    <v-list-item>
                      <v-list-item-title>VIN</v-list-item-title>
                      <v-list-item-subtitle>{{ application.car.vin }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="6" md="4">
                    <v-list-item>
                      <v-list-item-title>Пробег</v-list-item-title>
                      <v-list-item-subtitle>{{ application.car.current_mileage?.toLocaleString() || '0' }} км</v-list-item-subtitle>
                    </v-list-item>
                  </v-col>
                </v-row>

                <!-- Характеристики если есть -->
                <div v-if="application.car.specification" class="mt-4">
                  <h4 class="text-subtitle-1">Характеристики:</h4>
                  <div class="d-flex flex-wrap">
                    <v-chip small class="mr-1 mb-1">{{ getEngineType(application.car.specification.engine_type) }}</v-chip>
                    <v-chip small class="mr-1 mb-1">{{ application.car.specification.engine_volume }} л</v-chip>
                    <v-chip small class="mr-1 mb-1">{{ application.car.specification.horsepower }} л.с.</v-chip>
                    <v-chip small class="mr-1 mb-1">{{ getTransmission(application.car.specification.transmission) }}</v-chip>
                  </div>
                </div>
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
                        {{ application.client.company_name }}
                      </v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="12" md="6">
                    <v-list-item>
                      <v-list-item-title>ИНН</v-list-item-title>
                      <v-list-item-subtitle class="text-h6">
                        {{ application.client.inn }}
                      </v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="12" md="6" v-if="application.client.contact_person">
                    <v-list-item>
                      <v-list-item-title>Контактное лицо</v-list-item-title>
                      <v-list-item-subtitle>{{ application.client.contact_person }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="12" md="6" v-if="application.client.email">
                    <v-list-item>
                      <v-list-item-title>Email</v-list-item-title>
                      <v-list-item-subtitle>{{ application.client.email }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="12" md="6" v-if="application.client.phone">
                    <v-list-item>
                      <v-list-item-title>Телефон</v-list-item-title>
                      <v-list-item-subtitle>{{ application.client.phone }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-col>

                  <v-col cols="12" md="6" v-if="application.client.address">
                    <v-list-item>
                      <v-list-item-title>Адрес</v-list-item-title>
                      <v-list-item-subtitle>{{ application.client.address }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>

            <!-- Форма одобрения заявки (простая версия без аккордеона) -->
            <div v-if="!approveSuccess">
              <h3 class="text-h6 mb-4">
                <v-icon class="mr-2">mdi-check-circle</v-icon>
                Одобрить заявку и создать договор
              </h3>

              <v-alert v-if="application.car.status !== 'available'" type="error" class="mb-4">
                <div class="text-h6">Автомобиль недоступен!</div>
                <p>Автомобиль {{ application.car.make }} {{ application.car.model }} в статусе
                  <strong>{{ getCarStatusText(application.car.status) }}</strong>.
                  Нельзя создать договор аренды для недоступного автомобиля.
                </p>
                <v-btn @click="$router.push(`/admin/cars/${application.car.id}/edit`)" color="error" class="mt-2">
                  Изменить статус автомобиля
                </v-btn>
              </v-alert>

              <div v-else>
                <v-form @submit.prevent="approveApplication" ref="approveForm" v-model="approveValid">
                  <v-row>
                    <v-col cols="12" md="4">
                      <v-text-field
                          v-model="approveForm.start_date"
                          label="Дата начала*"
                          :rules="[v => !!v || 'Обязательное поле']"
                          required
                          prepend-icon="mdi-calendar-start"
                          type="date"
                          :min="minStartDate"
                      ></v-text-field>
                    </v-col>

                    <v-col cols="12" md="4">
                      <v-text-field
                          v-model="approveForm.end_date"
                          label="Дата окончания"
                          prepend-icon="mdi-calendar-end"
                          type="date"
                          :min="minEndDate"
                      ></v-text-field>
                    </v-col>

                    <v-col cols="12" md="4">
                      <v-text-field
                          v-model="approveForm.monthly_payment"
                          label="Ежемесячная оплата*"
                          :rules="[
                          v => !!v || 'Обязательное поле',
                          v => !isNaN(v) || 'Должно быть числом',
                          v => parseFloat(v) > 0 || 'Оплата должна быть положительной'
                        ]"
                          required
                          type="number"
                          step="0.01"
                          prepend-icon="mdi-cash"
                          suffix="₽"
                      ></v-text-field>
                    </v-col>
                  </v-row>

                  <!-- Предупреждение о датах -->
                  <v-alert v-if="hasDateError" type="warning" class="mb-4" dense>
                    Дата окончания должна быть позже даты начала
                  </v-alert>

                  <!-- Расчётная стоимость -->
                  <v-alert v-if="calculateTotalPayment !== '0.00'" type="info" class="mb-4" dense>
                    <div class="d-flex justify-space-between align-center">
                      <span>Расчётная общая стоимость:</span>
                      <strong class="text-h6">{{ calculateTotalPayment }} ₽</strong>
                    </div>
                  </v-alert>

                  <!-- Сообщения об ошибках -->
                  <v-alert v-if="approveError" type="error" class="mb-4">
                    {{ approveErrorMessage }}
                  </v-alert>

                  <div class="d-flex gap-2 mt-2">
                    <v-btn
                        type="submit"
                        color="primary"
                        :loading="approveLoading"
                        :disabled="!approveValid || hasDateError"
                        class="flex-grow-1"
                    >
                      <v-icon left>mdi-file-sign</v-icon>
                      Создать договор
                    </v-btn>

                    <!-- НОВАЯ КНОПКА: Удалить заявку -->
                    <v-btn
                        color="error"
                        @click="showDeleteDialog"
                        :loading="deleteLoading"
                        :disabled="approveSuccess"
                    >
                      <v-icon left>mdi-delete</v-icon>
                      Удалить
                    </v-btn>
                  </div>
                </v-form>
              </div>
            </div>

            <!-- Сообщение об успехе -->
            <v-alert v-if="approveSuccess" type="success" class="mt-6">
              <h4 class="text-h6">Договор успешно создан!</h4>
              <p><strong>Номер договора:</strong> {{ createdLeaseId }}</p>
              <p><strong>Статус:</strong> Автомобиль переведён в статус "В аренде"</p>
              <p><strong>Заявка:</strong> Удалена после создания договора</p>

              <v-btn @click="goToLease" color="success" class="mt-3">
                <v-icon left>mdi-file-sign</v-icon>
                Перейти к договору
              </v-btn>
              <v-btn @click="goToList" color="primary" class="mt-3 ml-2">
                <v-icon left>mdi-arrow-left</v-icon>
                К списку заявок
              </v-btn>
            </v-alert>
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
                  @click="scrollToApproveForm"
                  prepend-icon="mdi-check-circle"
                  :disabled="application.car.status !== 'available'"
              >
                <v-list-item-title>Одобрить заявку</v-list-item-title>
                <v-list-item-subtitle v-if="application.car.status !== 'available'">
                  Автомобиль недоступен
                </v-list-item-subtitle>
              </v-list-item>

              <v-list-item
                  @click="$router.push(`/admin/cars/${application.car.id}`)"
                  prepend-icon="mdi-car"
              >
                <v-list-item-title>Перейти к автомобилю</v-list-item-title>
              </v-list-item>

              <v-list-item
                  @click="copyApplicationInfo"
                  prepend-icon="mdi-content-copy"
              >
                <v-list-item-title>Копировать информацию</v-list-item-title>
              </v-list-item>

              <v-list-item
                  @click="showDeleteDialog"
                  prepend-icon="mdi-delete"
                  color="error"
              >
                <v-list-item-title class="text-error">Удалить заявку</v-list-item-title>
                <v-list-item-subtitle class="text-error">Без создания договора</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>

        <!-- Статус автомобиля -->
        <v-card>
          <v-card-title>Статус автомобиля</v-card-title>
          <v-card-text>
            <div class="text-center">
              <v-chip :color="getCarStatusColor(application.car.status)" dark large class="mb-2">
                {{ getCarStatusText(application.car.status) }}
              </v-chip>
              <p class="text-caption" :class="application.car.status === 'available' ? 'text-green' : 'text-red'">
                {{ application.car.status === 'available'
                  ? 'Автомобиль доступен для одобрения заявки'
                  : 'Автомобиль недоступен для аренды' }}
              </p>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Ошибка загрузки -->
    <v-alert v-else-if="error" type="error">
      {{ errorMessage }}
      <v-btn @click="fetchApplication" class="mt-2" color="error">Попробовать снова</v-btn>
    </v-alert>

    <!-- Диалог подтверждения удаления -->
    <v-dialog v-model="deleteDialog" max-width="500">
      <v-card>
        <v-card-title class="headline">Подтверждение удаления</v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить заявку #{{ application?.id }}?
          <v-alert type="warning" class="mt-4">
            Это действие нельзя отменить. Заявка будет удалена без создания договора аренды.
          </v-alert>
          <div class="mt-4">
            <strong>Автомобиль:</strong> {{ application?.car.make }} {{ application?.car.model }}<br>
            <strong>Клиент:</strong> {{ application?.client.company_name }}
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="deleteDialog = false" color="secondary">Отмена</v-btn>
          <v-btn @click="deleteApplication" color="error" :loading="deleteLoading">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminApplicationDetail',
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      application: null,
      loading: true,
      error: false,
      errorMessage: '',

      // Форма одобрения
      approveLoading: false,
      approveValid: false,
      approveSuccess: false,
      approveError: false,
      approveErrorMessage: '',
      createdLeaseId: null,

      approveForm: {
        start_date: null,
        end_date: null,
        monthly_payment: ''
      },

      // Удаление заявки
      deleteDialog: false,
      deleteLoading: false
    }
  },
  computed: {
    applicationId() {
      return parseInt(this.id)
    },
    minStartDate() {
      // Минимальная дата - сегодня
      return new Date().toISOString().split('T')[0]
    },
    minEndDate() {
      // Минимальная дата окончания - дата начала или сегодня
      if (this.approveForm.start_date) {
        return this.approveForm.start_date
      }
      return this.minStartDate
    },
    hasDateError() {
      if (this.approveForm.start_date && this.approveForm.end_date) {
        return this.approveForm.start_date >= this.approveForm.end_date
      }
      return false
    },
    calculateTotalPayment() {
      if (!this.approveForm.start_date || !this.approveForm.end_date || !this.approveForm.monthly_payment) {
        return '0.00'
      }

      const start = new Date(this.approveForm.start_date)
      const end = new Date(this.approveForm.end_date)
      const monthly = parseFloat(this.approveForm.monthly_payment)

      if (isNaN(monthly) || monthly <= 0) return '0.00'

      // Рассчитываем количество месяцев
      const months = Math.ceil((end - start) / (1000 * 60 * 60 * 24 * 30.44))
      const total = months * monthly

      return total.toFixed(2)
    }
  },
  methods: {
    async fetchApplication() {
      try {
        this.loading = true
        this.error = false

        const response = await axios.get(`admin/lease_applications/${this.applicationId}/`)
        this.application = response.data.application
        console.log('Данные заявки загружены:', this.application)

      } catch (error) {
        console.error('Ошибка загрузки заявки:', error)
        this.error = true
        this.errorMessage = error.response?.data?.detail || 'Не удалось загрузить данные заявки'
      } finally {
        this.loading = false
      }
    },

    async approveApplication() {
      if (!this.$refs.approveForm.validate() || this.hasDateError) return

      this.approveLoading = true
      this.approveError = false

      try {
        // Подготавливаем данные
        const payload = {
          start_date: this.approveForm.start_date,
          end_date: this.approveForm.end_date || null,
          monthly_payment: parseFloat(this.approveForm.monthly_payment)
        }

        console.log('Отправляем данные для одобрения:', payload)

        const response = await axios.post(`admin/lease_applications/${this.applicationId}/approve/`, payload)

        this.approveSuccess = true
        // Извлекаем ID договора из сообщения
        const match = response.data.success?.match(/Договор #(\d+)/)
        this.createdLeaseId = match ? match[1] : 'неизвестен'
        console.log('Заявка одобрена, договор создан:', response.data)

      } catch (error) {
        console.error('Ошибка одобрения заявки:', error)
        this.approveError = true

        // Обработка ошибок от сервера
        if (error.response?.status === 400 && error.response?.data?.error) {
          this.approveErrorMessage = error.response.data.error
        } else if (error.response?.data?.detail) {
          this.approveErrorMessage = error.response.data.detail
        } else if (error.response?.data) {
          // Обработка ошибок валидации
          const errors = []
          for (const [field, messages] of Object.entries(error.response.data)) {
            const fieldName = this.getApproveFieldLabel(field)
            errors.push(`${fieldName}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
          }
          this.approveErrorMessage = errors.join('; ')
        } else if (error.code === 'ERR_NETWORK') {
          this.approveErrorMessage = 'Ошибка сети. Проверьте подключение.'
        } else {
          this.approveErrorMessage = 'Ошибка при одобрении заявки'
        }
      } finally {
        this.approveLoading = false
      }
    },

    showDeleteDialog() {
      this.deleteDialog = true
    },

    async deleteApplication() {
      this.deleteLoading = true

      try {
        // Отправляем DELETE запрос на тот же эндпоинт
        const response = await axios.delete(`admin/lease_applications/${this.applicationId}/`)

        console.log('Заявка удалена:', response.data)

        // Закрываем диалог и переходим к списку заявок
        this.deleteDialog = false

        // Показываем сообщение об успехе
        alert('Заявка успешно удалена!')

        // Переходим к списку заявок
        this.$router.push('/admin/applications')

      } catch (error) {
        console.error('Ошибка удаления заявки:', error)

        // Обработка ошибок
        let errorMessage = 'Ошибка при удалении заявки'

        if (error.response?.status === 404) {
          errorMessage = 'Заявка не найдена'
        } else if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail
        } else if (error.response?.data?.error) {
          errorMessage = error.response.data.error
        }

        alert(errorMessage)
      } finally {
        this.deleteLoading = false
      }
    },

    getApproveFieldLabel(field) {
      const labels = {
        'start_date': 'Дата начала',
        'end_date': 'Дата окончания',
        'monthly_payment': 'Ежемесячная оплата'
      }
      return labels[field] || field
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

    getEngineType(type) {
      const types = {
        'petrol': 'Бензин',
        'diesel': 'Дизель',
        'electric': 'Электро',
        'hybrid': 'Гибрид',
        'other': 'Другое'
      }
      return types[type] || type
    },

    getTransmission(type) {
      const types = {
        'auto': 'Автомат',
        'manual': 'Механика',
        'cvt': 'Вариатор',
        'robot': 'Робот'
      }
      return types[type] || type
    },

    formatDateTime(dateTimeString) {
      if (!dateTimeString) return '—'
      return new Date(dateTimeString).toLocaleString('ru-RU')
    },

    copyApplicationInfo() {
      const text = `Заявка #${this.application.id}
Автомобиль: ${this.application.car.make} ${this.application.car.model} (${this.application.car.license_plate})
Клиент: ${this.application.client.company_name} (ИНН: ${this.application.client.inn})
Дата подачи: ${this.formatDateTime(this.application.created_at)}`

      navigator.clipboard.writeText(text)
          .then(() => {
            alert('Информация скопирована в буфер обмена')
          })
          .catch(err => {
            console.error('Ошибка копирования:', err)
          })
    },

    scrollToApproveForm() {
      // Прокручиваем к форме одобрения
      const formElement = document.querySelector('.v-form')
      if (formElement) {
        formElement.scrollIntoView({ behavior: 'smooth' })
      }
    },

    goToLease() {
      if (this.createdLeaseId) {
        this.$router.push(`/admin/leases/${this.createdLeaseId}`)
      }
    },

    goToList() {
      this.$router.push('/admin/applications')
    }
  },

  mounted() {
    this.fetchApplication()
  },

  watch: {
    id() {
      this.fetchApplication()
    }
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
.text-error {
  color: #F44336;
}
.gap-2 {
  gap: 8px;
}
.flex-grow-1 {
  flex-grow: 1;
}
</style>