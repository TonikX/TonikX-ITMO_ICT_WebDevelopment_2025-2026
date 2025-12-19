<template>
  <div>
    <v-row class="mb-4">
      <v-col cols="12" md="8" offset-md="2">
        <v-card>
          <v-card-title class="headline">
            <v-icon class="mr-2">mdi-wrench</v-icon>
            {{ isEdit ? 'Редактирование компании' : 'Добавление новой компании' }}
          </v-card-title>

          <v-card-text>
            <v-form ref="form" v-model="valid" @submit.prevent="submitForm">
              <v-text-field
                  v-model="formData.name"
                  label="Название компании*"
                  :rules="[v => !!v || 'Обязательное поле']"
                  required
                  prepend-icon="mdi-office-building"
              ></v-text-field>

              <v-text-field
                  v-model="formData.phone"
                  label="Телефон"
                  prepend-icon="mdi-phone"
              ></v-text-field>

              <v-text-field
                  v-model="formData.address"
                  label="Адрес"
                  prepend-icon="mdi-map-marker"
              ></v-text-field>

              <v-alert v-if="error" type="error" class="mt-4">
                {{ errorMessage }}
              </v-alert>

              <v-alert v-if="success" type="success" class="mt-4">
                {{ successMessage }}
              </v-alert>

              <div class="d-flex justify-space-between mt-6">
                <v-btn @click="$router.back()" color="secondary">
                  <v-icon left>mdi-arrow-left</v-icon>
                  Назад
                </v-btn>

                <v-btn
                    type="submit"
                    color="primary"
                    :loading="loading"
                    :disabled="!valid || success"
                >
                  {{ isEdit ? 'Сохранить изменения' : 'Добавить компанию' }}
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
  name: 'AdminMaintenanceCompanyForm',
  props: {
    id: {
      type: [String, Number],
      default: null
    }
  },
  data() {
    return {
      formData: {
        name: '',
        phone: '',
        address: ''
      },
      valid: false,
      loading: false,
      error: false,
      success: false,
      errorMessage: '',
      successMessage: ''
    }
  },
  computed: {
    isEdit() {
      return !!this.id
    }
  },
  methods: {
    async fetchCompany() {
      if (!this.id) return

      try {
        this.loading = true
        const response = await axios.get(`admin/maintenance_companies/${this.id}/`)
        this.formData = response.data.company
        console.log('Компания загружена:', this.formData)
      } catch (error) {
        console.error('Ошибка загрузки компании:', error)
        this.error = true
        this.errorMessage = 'Не удалось загрузить данные компании'
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
        if (this.isEdit) {
          // Редактирование существующей компании
          await axios.patch(`admin/maintenance_companies/${this.id}/`, this.formData)
          this.successMessage = 'Компания успешно обновлена!'
        } else {
          // Добавление новой компании
          await axios.post('admin/maintenance_companies/', this.formData)
          this.successMessage = 'Компания успешно добавлена!'
          this.$refs.form.reset()
        }

        this.success = true

        // Через 2 секунды перейти обратно к списку
        if (!this.isEdit) {
          setTimeout(() => {
            this.$router.push('/admin/maintenance_companies')
          }, 2000)
        }

      } catch (error) {
        console.error('Ошибка сохранения компании:', error)
        this.error = true

        if (error.response?.status === 400 && error.response?.data?.error) {
          this.errorMessage = error.response.data.error
        } else if (error.response?.data?.detail) {
          this.errorMessage = error.response.data.detail
        } else {
          this.errorMessage = 'Ошибка при сохранении компании'
        }
      } finally {
        this.loading = false
      }
    }
  },
  mounted() {
    if (this.isEdit) {
      this.fetchCompany()
    }
  }
}
</script>