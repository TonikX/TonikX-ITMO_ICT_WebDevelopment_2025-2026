<template>
  <v-container class="my-8">
    <h1 class="text-h4 text-center mb-6">Управление услугами</h1>

    <!-- Кнопка создания новой услуги -->
    <div class="mb-6 text-right">
      <v-btn color="primary" to="/admin/services/new">
        <v-icon start>mdi-plus</v-icon>
        Добавить услугу
      </v-btn>
    </div>

    <v-row v-if="services.length > 0">
      <v-col
          v-for="service in services"
          :key="service.id"
          cols="12"
          md="6"
          lg="4"
      >
        <v-card class="pa-4 h-100 d-flex flex-column">
          <!-- Картинка -->
          <div class="mb-3 flex-grow-0" style="height: 200px; overflow: hidden; cursor: pointer;"
               @click="goToServiceDetail(service)">
            <img
                :src="getImagePath(service)"
                :alt="service.name"
                style="width: 100%; height: 100%; object-fit: cover; border-radius: 8px;"
            />
          </div>

          <!-- Информация об услуге -->
          <div class="flex-grow-1">
            <v-card-title
                class="text-h6 mb-2 pa-0"
                style="cursor: pointer;"
                @click="goToServiceDetail(service)"
            >
              {{ service.name }}
              <v-chip :color="service.is_active ? 'success' : 'error'" size="small" class="ml-2">
                {{ service.is_active ? 'Активна' : 'Неактивна' }}
              </v-chip>
            </v-card-title>

            <v-card-subtitle class="mb-2 pa-0">
              {{ service.category }}
            </v-card-subtitle>

            <v-card-text class="text-grey mb-3 pa-0">
              {{ truncateDescription(service.description, 100) }}
            </v-card-text>
          </div>

          <!-- Цена и детали -->
          <v-card-text class="mb-3 pa-0 flex-grow-0">
            <div class="mb-1">
              <span class="text-h6 text-primary font-weight-bold">{{ service.price }} руб.</span>
            </div>
            <div v-if="service.duration" class="text-caption text-grey">
              Длительность: {{ service.duration }} мин
            </div>
            <div class="text-caption text-grey">
              Создал: {{ service.created_by_email }}
            </div>
          </v-card-text>

          <!-- Админские кнопки -->
          <v-card-actions class="pa-0 mt-2 flex-grow-0">
            <v-btn-group class="d-flex" style="width: 100%;">
              <v-btn
                  color="primary"
                  @click="goToServiceDetail(service)"
                  style="flex: 1;"
              >
                <v-icon>mdi-eye</v-icon>
              </v-btn>

              <v-btn
                  color="secondary"
                  @click="editService(service)"
                  style="flex: 1;"
              >
                <v-icon>mdi-pencil</v-icon>
              </v-btn>

              <v-btn
                  color="error"
                  @click="deleteService(service)"
                  style="flex: 1;"
                  :loading="deletingId === service.id"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </v-btn-group>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-else-if="loading">
      <v-col cols="12" class="text-center">
        <v-progress-circular
            indeterminate
            color="primary"
            size="64"
        ></v-progress-circular>
      </v-col>
    </v-row>

    <v-row v-else>
      <v-col cols="12" class="text-center">
        <p>Услуги не найдены</p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminServicesView',

  data() {
    return {
      services: [],
      loading: false,
      deletingId: null
    }
  },

  async mounted() {
    await this.loadServices()
  },

  methods: {
    async loadServices() {
      this.loading = true
      try {
        // Админский endpoint
        const response = await axios.get('/api/admin/services/')
        this.services = response.data
      } catch (error) {
        console.error('Ошибка загрузки услуг:', error)
        this.services = []
      } finally {
        this.loading = false
      }
    },

    // Переход на детальную страницу услуги (админскую)
    goToServiceDetail(service) {
      this.$router.push(`/admin/services/${service.id}`)
    },

    // Редактирование услуги
    editService(service) {
      this.$router.push(`/admin/services/${service.id}/edit`)
    },

    // Удаление услуги
    async deleteService(service) {
      if (!confirm(`Удалить услугу "${service.name}"?`)) return

      this.deletingId = service.id
      try {
        await axios.delete(`/api/admin/services/${service.id}/`)
        this.services = this.services.filter(s => s.id !== service.id)
        alert('Услуга удалена')
      } catch (error) {
        console.error('Ошибка удаления:', error)
        alert('Ошибка при удалении услуги')
      } finally {
        this.deletingId = null
      }
    },

    truncateDescription(text, length) {
      if (!text) return ''
      if (text.length <= length) return text
      return text.substring(0, length) + '...'
    },

    getImagePath(service) {
      if (service.primary_image) {
        const parts = service.primary_image.split('/')
        const filename = parts[parts.length - 1]

        return `../../../../media/services/${service.id}/${filename}`
      }

      return 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200" viewBox="0 0 400 200"><rect width="400" height="200" fill="%23f5f5f5"/><text x="50%" y="50%" font-family="Arial" font-size="16" fill="%23999" text-anchor="middle" dy=".3em">Нет изображения</text></svg>'
    }
  }
}
</script>