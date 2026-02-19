<template>
  <div>
    <v-row class="mb-4">
      <v-col cols="12">
        <v-card>
          <v-card-title class="headline">
            <v-icon class="mr-2">mdi-wrench</v-icon>
            Детальная информация о компании
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="$router.push(`/admin/maintenance_companies/${id}/edit`)">
              <v-icon left>mdi-pencil</v-icon>
              Редактировать
            </v-btn>
          </v-card-title>

          <v-card-text v-if="loading">
            <v-progress-linear indeterminate></v-progress-linear>
            <div class="text-center mt-4">Загрузка данных компании...</div>
          </v-card-text>

          <v-card-text v-else-if="error">
            <v-alert type="error">
              {{ errorMessage }}
            </v-alert>
            <v-btn @click="$router.back()" color="secondary" class="mt-4">
              <v-icon left>mdi-arrow-left</v-icon>
              Назад
            </v-btn>
          </v-card-text>

          <v-card-text v-else>
            <v-row>
              <v-col cols="12" md="6">
                <v-card variant="outlined">
                  <v-card-title>Основная информация</v-card-title>
                  <v-card-text>
                    <div class="mb-4">
                      <strong>ID:</strong>
                      <div class="mt-1">{{ company.id }}</div>
                    </div>

                    <div class="mb-4">
                      <strong>Название компании:</strong>
                      <div class="mt-1">{{ company.name }}</div>
                    </div>

                    <div class="mb-4">
                      <strong>Телефон:</strong>
                      <div class="mt-1">{{ company.phone || 'Не указан' }}</div>
                    </div>

                    <div class="mb-4">
                      <strong>Адрес:</strong>
                      <div class="mt-1">{{ company.address || 'Не указан' }}</div>
                    </div>

                    <div class="mb-4">
                      <strong>Дата создания:</strong>
                      <div class="mt-1">{{ formatDateTime(company.created_at) }}</div>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>

              <v-col cols="12" md="6">
                <v-card variant="outlined">
                  <v-card-title>Действия</v-card-title>
                  <v-card-text>
                    <div class="d-flex flex-column gap-3">
                      <v-btn color="primary" @click="$router.push(`/admin/maintenance_companies/${id}/edit`)">
                        <v-icon left>mdi-pencil</v-icon>
                        Редактировать компанию
                      </v-btn>

                      <v-btn color="error" @click="deleteCompany" :loading="deleteLoading">
                        <v-icon left>mdi-delete</v-icon>
                        Удалить компанию
                      </v-btn>

                      <v-btn @click="$router.back()" color="secondary">
                        <v-icon left>mdi-arrow-left</v-icon>
                        Назад к списку
                      </v-btn>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Диалог подтверждения удаления -->
    <v-dialog v-model="deleteDialog" max-width="500">
      <v-card>
        <v-card-title class="headline">Подтверждение удаления</v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить компанию "{{ company.name }}"?
          <v-alert type="warning" class="mt-4">
            Это действие нельзя отменить. Все связанные записи об обслуживании останутся без ссылки на компанию.
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="deleteDialog = false" color="secondary">Отмена</v-btn>
          <v-btn @click="confirmDelete" color="error" :loading="deleteLoading">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminMaintenanceCompanyDetail',
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      company: {},
      loading: true,
      error: false,
      errorMessage: '',
      deleteDialog: false,
      deleteLoading: false
    }
  },
  methods: {
    async fetchCompany() {
      try {
        this.loading = true
        const response = await axios.get(`admin/maintenance_companies/${this.id}/`)
        this.company = response.data.company
        console.log('Компания загружена:', this.company)
      } catch (error) {
        console.error('Ошибка загрузки компании:', error)
        this.error = true
        this.errorMessage = 'Не удалось загрузить данные компании'
      } finally {
        this.loading = false
      }
    },

    formatDateTime(dateTimeString) {
      if (!dateTimeString) return '—'
      return new Date(dateTimeString).toLocaleString('ru-RU')
    },

    deleteCompany() {
      this.deleteDialog = true
    },

    async confirmDelete() {
      this.deleteLoading = true

      try {
        await axios.delete(`admin/maintenance_companies/${this.id}/`)

        // Успешное удаление
        this.deleteDialog = false

        // Перейти обратно к списку через 1 секунду
        setTimeout(() => {
          this.$router.push('/admin/maintenance_companies')
        }, 1000)

      } catch (error) {
        console.error('Ошибка удаления компании:', error)
        this.error = true

        if (error.response?.status === 400 && error.response?.data?.error) {
          this.errorMessage = error.response.data.error
        } else if (error.response?.data?.detail) {
          this.errorMessage = error.response.data.detail
        } else {
          this.errorMessage = 'Ошибка при удалении компании'
        }
      } finally {
        this.deleteLoading = false
      }
    }
  },
  mounted() {
    this.fetchCompany()
  }
}
</script>

<style scoped>
.gap-3 {
  gap: 12px;
}
</style>