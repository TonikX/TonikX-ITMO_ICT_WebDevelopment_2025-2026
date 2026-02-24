<template>
  <v-container class="my-8">
    <!-- Кнопка назад -->
    <v-btn
        @click="$router.push('/admin/services')"
        color="primary"
        variant="text"
        class="mb-4"
    >
      <v-icon start>mdi-arrow-left</v-icon>
      Назад к услугам
    </v-btn>

    <!-- Загрузка -->
    <div v-if="loading" class="text-center">
      <v-progress-circular
          indeterminate
          color="primary"
          size="64"
      ></v-progress-circular>
    </div>

    <!-- Ошибка -->
    <div v-else-if="error" class="text-center">
      <v-alert type="error">{{ error }}</v-alert>
    </div>

    <!-- Контент услуги -->
    <div v-else-if="service" class="service-detail">
      <v-row>
        <!-- Изображения -->
        <v-col cols="12" md="6">
          <v-card class="pa-4">
            <img
                :src="getMainImage()"
                :alt="service.name"
                style="width: 100%; height: 400px; object-fit: cover; border-radius: 8px;"
                class="mb-4"
            />


            <v-btn color="primary" block @click="showUploadDialog = true">
              <v-icon start>mdi-upload</v-icon>
              Добавить изображение
            </v-btn>
          </v-card>
        </v-col>

        <!-- Информация -->
        <v-col cols="12" md="6">
          <v-card class="pa-4 h-100">
            <v-card-title class="text-h4 mb-4">
              {{ service.name }}
              <v-chip :color="service.is_active ? 'success' : 'error'" class="ml-2">
                {{ service.is_active ? 'Активна' : 'Неактивна' }}
              </v-chip>
            </v-card-title>

            <v-card-subtitle class="text-h6 mb-4">
              {{ service.category }}
            </v-card-subtitle>

            <v-divider class="my-4"></v-divider>

            <v-card-text>
              <div class="mb-4">
                <h3 class="text-h6 mb-2">Описание:</h3>
                <p class="text-body-1">{{ service.description }}</p>
              </div>

              <div class="mb-4">
                <h3 class="text-h6 mb-2">Детали:</h3>
                <v-list>
                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon color="primary">mdi-cash</v-icon>
                    </template>
                    <v-list-item-title>Цена: <strong class="text-h5 text-primary">{{ service.price }} руб.</strong></v-list-item-title>
                  </v-list-item>

                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon color="primary">mdi-clock</v-icon>
                    </template>
                    <v-list-item-title>Длительность: {{ service.duration }} минут</v-list-item-title>
                  </v-list-item>

                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon color="primary">mdi-account</v-icon>
                    </template>
                    <v-list-item-title>Создал: {{ service.created_by_email }}</v-list-item-title>
                  </v-list-item>

                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon color="primary">mdi-calendar</v-icon>
                    </template>
                    <v-list-item-title>Создано: {{ formatDate(service.created_at) }}</v-list-item-title>
                  </v-list-item>

                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon color="primary">mdi-update</v-icon>
                    </template>
                    <v-list-item-title>Обновлено: {{ formatDate(service.updated_at) }}</v-list-item-title>
                  </v-list-item>
                </v-list>
              </div>
            </v-card-text>

            <v-card-actions class="px-4 pb-4">
              <v-btn
                  color="primary"
                  @click="editService"
                  class="mr-2"
              >
                <v-icon start>mdi-pencil</v-icon>
                Редактировать
              </v-btn>

              <v-btn
                  color="error"
                  @click="toggleActivation"
                  class="mr-2"
              >
                <v-icon start>{{ service.is_active ? 'mdi-close' : 'mdi-check' }}</v-icon>
                {{ service.is_active ? 'Деактивировать' : 'Активировать' }}
              </v-btn>

              <v-btn
                  color="error"
                  variant="outlined"
                  @click="deleteService"
              >
                <v-icon start>mdi-delete</v-icon>
                Удалить
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </v-container>

  <!-- Загрузка изображения -->
  <v-dialog v-model="showUploadDialog" max-width="500">
    <v-card class="pa-4">
      <h3 class="mb-4">Загрузка изображения</h3>

      <v-file-input
          label="Файл"
          accept="image/*"
          v-model="uploadFile"
          show-size
      />

      <v-text-field
          label="Alt текст"
          v-model="uploadAltText"
      />

      <v-checkbox
          label="Основное изображение"
          v-model="uploadIsPrimary"
      />

      <v-text-field
          label="Порядок отображения"
          type="number"
          v-model.number="uploadDisplayOrder"
      />

      <v-btn
          color="primary"
          class="mt-4"
          :disabled="!uploadFile"
          @click="uploadImage"
      >
        Загрузить
      </v-btn>
    </v-card>
  </v-dialog>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminServiceDetailView',

  data() {
    return {
      service: null,
      loading: true,
      error: null,

      showUploadDialog: false,

      uploadFile: null,
      uploadAltText: '',
      uploadIsPrimary: false,
      uploadDisplayOrder: 0
    }
  },

  async mounted() {
    await this.loadService()
  },

  methods: {
    async loadService() {
      this.loading = true
      this.error = null

      const serviceId = this.$route.params.id

      try {

        const response = await axios.get(`/api/admin/services/${serviceId}/`)
        this.service = response.data

      } catch (error) {
        console.error('Ошибка загрузки услуги:', error)
        this.error = 'Не удалось загрузить информацию об услуге'
      } finally {
        this.loading = false
      }
    },

    async uploadImage() {
      if (!this.uploadFile) return

      const formData = new FormData()
      formData.append('service', this.service.id)
      formData.append('file', this.uploadFile)
      formData.append('alt_text', this.uploadAltText)
      formData.append('is_primary', this.uploadIsPrimary)
      formData.append('display_order', this.uploadDisplayOrder)

      try {
        await axios.post(
            '/api/admin/files/upload/',
            formData

        )

        alert('Изображение загружено')
        this.showUploadDialog = false


        await this.loadService()

      } catch (error) {
        console.error('Ошибка загрузки:', error)
        alert('Ошибка при загрузке изображения')
      }
    },

    getImageUrl(imagePath) {
      if (!imagePath) {
        return 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200" viewBox="0 0 400 200"><rect width="400" height="200" fill="%23f5f5f5"/><text x="50%" y="50%" font-family="Arial" font-size="16" fill="%23999" text-anchor="middle" dy=".3em">Нет изображения</text></svg>'
      }

      if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {

        const parts = imagePath.split('/')
        const filename = parts[parts.length - 1]
        return `../../../../media/services/${this.service.id}/${filename}`
      }

      return imagePath
    },

    getMainImage() {
      if (this.service && this.service.primary_image) {
        return this.getImageUrl(this.service.primary_image)
      }
      return 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="%23f5f5f5"/><text x="50%" y="50%" font-family="Arial" font-size="16" fill="%23999" text-anchor="middle" dy=".3em">Нет изображения</text></svg>'
    },

    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    // Редактирование услуги
    editService() {
      this.$router.push(`/admin/services/${this.service.id}/edit`)
    },

    // Переключение активности
    async toggleActivation() {
      const action = this.service.is_active ? 'деактивировать' : 'активировать'
      if (!confirm(`Вы уверены, что хотите ${action} эту услугу?`)) return

      try {
        if (this.service.is_active) {
          await axios.post(`/api/admin/services/${this.service.id}/deactivate/`)
          this.service.is_active = false
          alert('Услуга деактивирована')
        } else {
          const response = await axios.patch(`/api/admin/services/${this.service.id}/`, {
            is_active: true
          })
          this.service = response.data
          alert('Услуга активирована')
        }
      } catch (error) {
        console.error('Ошибка:', error)
        alert(`Ошибка при ${action} услуги`)
      }
    },

    async deleteService() {
      if (!confirm(`Удалить услугу "${this.service.name}"?`)) return

      try {
        await axios.delete(`/api/admin/services/${this.service.id}/`)
        alert('Услуга удалена')
        this.$router.push('/admin/services')
      } catch (error) {
        console.error('Ошибка удаления:', error)
        alert('Ошибка при удалении услуги')
      }
    }
  }
}
</script>