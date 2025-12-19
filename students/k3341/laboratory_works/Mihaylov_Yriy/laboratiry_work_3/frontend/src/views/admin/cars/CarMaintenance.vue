<template>
  <div>
    <v-row class="mb-4">
      <v-col cols="12">
        <v-card>
          <v-card-title class="headline">
            <v-icon class="mr-2">mdi-wrench</v-icon>
            Обслуживание автомобиля
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="showAddDialog">
              <v-icon left>mdi-plus</v-icon>
              Добавить обслуживание
            </v-btn>
          </v-card-title>

          <v-card-subtitle>
            Автомобиль: {{ car.make }} {{ car.model }} ({{ car.license_plate }})
          </v-card-subtitle>

          <v-card-text v-if="loading">
            <v-progress-linear indeterminate></v-progress-linear>
            <div class="text-center mt-4">Загрузка данных об обслуживании...</div>
          </v-card-text>

          <v-card-text v-else>
            <!-- Таблица обслуживания -->
            <table class="elevation-1" style="width: 100%; border-collapse: collapse; background-color: white;">
              <thead>
              <tr style="background-color: #f5f5f5;">
                <th style="width: 10%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">ID</th>
                <th style="width: 15%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Дата</th>
                <th style="width: 25%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Услуга</th>
                <th style="width: 15%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Стоимость</th>
                <th style="width: 20%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Описание</th>
                <th style="width: 15%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Компания</th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="item in paginatedMaintenances" :key="item.id" style="border-bottom: 1px solid #e0e0e0;">
                <td style="width: 10%; padding: 12px; text-align: center;">{{ item.id || '-' }}</td>
                <td style="width: 15%; padding: 12px; text-align: center;">{{ formatDate(item.date) }}</td>
                <td style="width: 25%; padding: 12px; text-align: center;">{{ item.service || '-' }}</td>
                <td style="width: 15%; padding: 12px; text-align: center; color: #F44336;">
                  {{ item.cost ? `${parseFloat(item.cost).toFixed(2)} ₽` : '-' }}
                </td>
                <td style="width: 20%; padding: 12px; text-align: center;">{{ item.description || '-' }}</td>
                <td style="width: 15%; padding: 12px; text-align: center;">{{ getCompanyName(item.maintenance_company) }}</td>
              </tr>
              <tr v-if="paginatedMaintenances.length === 0">
                <td colspan="6" style="padding: 16px; text-align: center; color: #9E9E9E;">
                  Нет записей об обслуживании
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

    <!-- Диалог добавления обслуживания -->
    <v-dialog v-model="addDialog" max-width="600">
      <v-card>
        <v-card-title>Добавление обслуживания</v-card-title>
        <v-card-text>
          <v-form ref="addForm" v-model="addValid">
            <v-select
                v-model="addForm.maintenance_company"
                :items="companyOptions"
                item-title="name"
                item-value="id"
                label="Компания по обслуживанию*"
                :rules="[v => !!v || 'Обязательное поле']"
                required
                prepend-icon="mdi-office-building"
            ></v-select>

            <v-text-field
                v-model="addForm.date"
                label="Дата обслуживания*"
                type="date"
                :rules="[v => !!v || 'Обязательное поле']"
                required
                prepend-icon="mdi-calendar"
            ></v-text-field>

            <v-text-field
                v-model="addForm.service"
                label="Услуга*"
                :rules="[v => !!v || 'Обязательное поле']"
                required
                prepend-icon="mdi-wrench"
            ></v-text-field>

            <v-text-field
                v-model="addForm.cost"
                label="Стоимость"
                type="number"
                step="0.01"
                suffix="₽"
                prepend-icon="mdi-cash"
            ></v-text-field>

            <v-textarea
                v-model="addForm.description"
                label="Описание"
                prepend-icon="mdi-text-box"
                rows="3"
            ></v-textarea>

            <v-alert v-if="addError" type="error" class="mt-4">
              {{ addErrorMessage }}
            </v-alert>

            <v-alert v-if="addSuccess" type="success" class="mt-4">
              Обслуживание успешно добавлено!
            </v-alert>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="addDialog = false" color="secondary">Отмена</v-btn>
          <v-btn
              @click="addMaintenance"
              color="primary"
              :loading="addLoading"
              :disabled="!addValid || addSuccess"
          >
            Добавить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CarMaintenance',
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      car: {},
      maintenances: [],
      companies: [],
      loading: true,
      currentPage: 1,
      itemsPerPage: 5,

      // Диалог добавления
      addDialog: false,
      addLoading: false,
      addValid: false,
      addError: false,
      addSuccess: false,
      addErrorMessage: '',

      addForm: {
        maintenance_company: null,
        date: new Date().toISOString().split('T')[0], // Сегодняшняя дата
        service: '',
        cost: '',
        description: ''
      }
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.maintenances.length / this.itemsPerPage)
    },

    paginatedMaintenances() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.maintenances.slice(start, end)
    },

    companyOptions() {
      return this.companies.map(company => ({
        id: company.id,
        name: company.name
      }))
    }
  },
  methods: {
    async fetchData() {
      try {
        this.loading = true

        // Загружаем данные автомобиля
        const carResponse = await axios.get(`admin/cars/${this.id}/`)
        this.car = carResponse.data.car

        // Загружаем обслуживание
        const maintenanceResponse = await axios.get(`admin/cars/${this.id}/maintenance/`)
        this.maintenances = maintenanceResponse.data.maintenances

        // Загружаем компании
        const companiesResponse = await axios.get('admin/maintenance_companies/')
        this.companies = companiesResponse.data.maintenance_companies

        console.log('Данные загружены:', {
          car: this.car,
          maintenances: this.maintenances.length,
          companies: this.companies.length
        })

      } catch (error) {
        console.error('Ошибка загрузки данных:', error)
      } finally {
        this.loading = false
      }
    },

    formatDate(dateString) {
      if (!dateString) return '—'
      return new Date(dateString).toLocaleDateString('ru-RU')
    },

    getCompanyName(companyId) {
      const company = this.companies.find(c => c.id === companyId)
      return company ? company.name : `ID: ${companyId}`
    },

    showAddDialog() {
      this.addDialog = true
      this.addError = false
      this.addSuccess = false
      this.addForm = {
        maintenance_company: null,
        date: new Date().toISOString().split('T')[0],
        service: '',
        cost: '',
        description: ''
      }
      if (this.$refs.addForm) {
        this.$refs.addForm.resetValidation()
      }
    },

    async addMaintenance() {
      if (!this.$refs.addForm.validate()) return

      this.addLoading = true
      this.addError = false
      this.addSuccess = false

      try {
        const payload = {
          ...this.addForm,
          car: parseInt(this.id)
        }

        await axios.post(`admin/cars/${this.id}/maintenance/`, payload)

        this.addSuccess = true

        // Обновляем данные через 2 секунды
        setTimeout(() => {
          this.fetchData()
          this.addDialog = false
        }, 2000)

      } catch (error) {
        console.error('Ошибка добавления обслуживания:', error)
        this.addError = true

        if (error.response?.status === 400 && error.response?.data?.error) {
          this.addErrorMessage = error.response.data.error
        } else if (error.response?.data?.detail) {
          this.addErrorMessage = error.response.data.detail
        } else {
          this.addErrorMessage = 'Ошибка при добавлении обслуживания'
        }
      } finally {
        this.addLoading = false
      }
    }
  },
  mounted() {
    this.fetchData()
  }
}
</script>