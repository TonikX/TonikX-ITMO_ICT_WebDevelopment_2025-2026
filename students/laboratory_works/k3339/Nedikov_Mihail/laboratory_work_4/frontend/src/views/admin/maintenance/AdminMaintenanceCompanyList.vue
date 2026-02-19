<template>
  <div>
    <v-row class="mb-4">
      <v-col cols="12">
        <v-card>
          <v-card-title class="headline">
            <v-icon class="mr-2">mdi-wrench</v-icon>
            Компании по обслуживанию
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="$router.push('/admin/maintenance_companies/new')">
              <v-icon left>mdi-plus</v-icon>
              Добавить компанию
            </v-btn>
          </v-card-title>

          <v-card-subtitle>
            Всего компаний: {{ maintenanceCompanies.length }} (Показано: {{ paginatedCompanies.length }})
          </v-card-subtitle>

          <v-card-text v-if="loading">
            <v-progress-linear indeterminate></v-progress-linear>
            <div class="text-center mt-4">Загрузка компаний...</div>
          </v-card-text>

          <v-card-text v-else>
            <!-- Таблица компаний -->
            <table class="elevation-1" style="width: 100%; border-collapse: collapse; background-color: white;">
              <thead>
              <tr style="background-color: #f5f5f5;">
                <th style="width: 10%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">ID</th>
                <th style="width: 30%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Название</th>
                <th style="width: 20%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Телефон</th>
                <th style="width: 30%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Адрес</th>
                <th style="width: 10%; padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">Действия</th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="item in paginatedCompanies" :key="item.id" style="border-bottom: 1px solid #e0e0e0;">
                <td style="width: 10%; padding: 12px; text-align: center;">{{ item.id || '-' }}</td>
                <td style="width: 30%; padding: 12px; text-align: center;">{{ item.name || '-' }}</td>
                <td style="width: 20%; padding: 12px; text-align: center;">{{ item.phone || '-' }}</td>
                <td style="width: 30%; padding: 12px; text-align: center;">{{ item.address || '-' }}</td>
                <td style="width: 10%; padding: 12px; text-align: center;">
                  <v-btn
                      color="primary"
                      small
                      @click="$router.push(`/admin/maintenance_companies/${item.id}`)"
                      style="margin-right: 4px;"
                  >
                    <v-icon small>mdi-eye</v-icon>
                  </v-btn>

                  <v-btn
                      color="warning"
                      small
                      @click="$router.push(`/admin/maintenance_companies/${item.id}/edit`)"
                  >
                    <v-icon small>mdi-pencil</v-icon>
                  </v-btn>
                </td>
              </tr>
              <tr v-if="paginatedCompanies.length === 0">
                <td colspan="5" style="padding: 16px; text-align: center; color: #9E9E9E;">
                  Нет компаний для отображения
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
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminMaintenanceCompanyList',
  data() {
    return {
      maintenanceCompanies: [],
      loading: true,
      currentPage: 1,
      itemsPerPage: 5,
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.maintenanceCompanies.length / this.itemsPerPage)
    },

    paginatedCompanies() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.maintenanceCompanies.slice(start, end)
    }
  },
  methods: {
    async fetchMaintenanceCompanies() {
      try {
        this.loading = true
        const response = await axios.get('admin/maintenance_companies/')
        this.maintenanceCompanies = response.data.maintenance_companies
        console.log('Компании по обслуживанию загружены:', this.maintenanceCompanies.length)
      } catch (error) {
        console.error('Ошибка загрузки компаний:', error)
      } finally {
        this.loading = false
      }
    }
  },
  mounted() {
    this.fetchMaintenanceCompanies()
  }
}
</script>