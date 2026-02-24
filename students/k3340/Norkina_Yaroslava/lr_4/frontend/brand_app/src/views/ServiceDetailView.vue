<template>
  <v-container class="my-8">
    <!-- Кнопка назад -->
    <v-btn
        @click="$router.push('/services')"
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

            <!-- Галерея дополнительных изображений -->
            <div v-if="service.images && service.images.length > 1" class="d-flex flex-wrap gap-2">
              <img
                  v-for="(img, index) in service.images"
                  :key="img.id"
                  :src="getImageUrl(img.url)"
                  :alt="img.alt_text"
                  style="width: 80px; height: 80px; object-fit: cover; border-radius: 4px; cursor: pointer;"
                  @click="setMainImage(img.url)"
              />
            </div>
          </v-card>
        </v-col>

        <!-- Информация -->
        <v-col cols="12" md="6">
          <v-card class="pa-4 h-100">
            <v-card-title class="text-h4 mb-4">
              {{ service.name }}
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
                      <v-icon color="primary">mdi-calendar</v-icon>
                    </template>
                    <v-list-item-title>Добавлено: {{ formatDate(service.created_at) }}</v-list-item-title>
                  </v-list-item>
                </v-list>
              </div>

              <!-- Для админа дополнительная информация -->
              <div v-if="isAdminView" class="mb-4">
                <h3 class="text-h6 mb-2">Административная информация:</h3>
                <v-list>
                  <v-list-item>
                    <v-list-item-title>Статус:
                      <v-chip :color="service.is_active ? 'success' : 'error'" size="small">
                        {{ service.is_active ? 'Активна' : 'Неактивна' }}
                      </v-chip>
                    </v-list-item-title>
                  </v-list-item>

                  <v-list-item>
                    <v-list-item-title>Создал: {{ service.created_by_email }}</v-list-item-title>
                  </v-list-item>

                  <v-list-item>
                    <v-list-item-title>Обновлено: {{ formatDate(service.updated_at) }}</v-list-item-title>
                  </v-list-item>
                </v-list>
              </div>
            </v-card-text>

            <v-card-actions class="px-4 pb-4">
              <!-- Для обычного пользователя -->
              <template v-if="!isAdminView">
                <v-btn
                    color="primary"
                    size="large"
                    @click="createOrder"
                    block
                >
                  <v-icon start>mdi-cart</v-icon>
                  Оставить заявку
                </v-btn>
              </template>

              <!-- Для админа -->
              <template v-else>
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
                    @click="deactivateService"
                    v-if="service.is_active"
                >
                  <v-icon start>mdi-close</v-icon>
                  Деактивировать
                </v-btn>

                <v-btn
                    color="success"
                    @click="activateService"
                    v-else
                >
                  <v-icon start>mdi-check</v-icon>
                  Активировать
                </v-btn>
              </template>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>


      <div
          v-if="reviewsData && reviewsData.statistics.total_reviews > 0"
          class="mt-8"
      >
        <h2 class="text-h5 mb-4">Отзывы</h2>

        <!-- Рейтинг -->
        <v-card class="pa-4 mb-4">
          <p>
            <b>Средний рейтинг:</b>
            {{ reviewsData.statistics.average_rating }}
          </p>
          <p>
            <b>Всего отзывов:</b>
            {{ reviewsData.statistics.total_reviews }}
          </p>
        </v-card>

        <!-- Список отзывов -->
        <v-row>
          <v-col
              v-for="review in reviewsData.reviews"
              :key="review.id"
              cols="12"
              md="6"
          >
            <v-card class="pa-4 h-100">
              <p class="mb-1"><b>{{ review.title }}</b></p>
              <p class="text-caption mb-2">
                {{ review.user_full_name }} • {{ formatDate(review.created_at) }}
              </p>

              <p><b>Оценка:</b> {{ review.rating }}</p>
              <p>{{ review.content }}</p>

              <v-chip
                  v-if="review.is_verified"
                  size="small"
                  color="success"
                  class="mt-2"
              >
                Проверен
              </v-chip>
            </v-card>
          </v-col>
        </v-row>
      </div>
    </div>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ServiceDetailView',

  data() {
    return {
      service: null,
      loading: true,
      error: null,
      mainImage: null,
      isAdminView: false,
      reviewsData: null,
      reviewsLoading: false
    }
  },

  computed: {
    isAuthenticated() {
      return this.$store.getters.isAuthenticated
    },
    isAdmin() {
      return this.$store.getters.isAdmin
    }
  },

  async mounted() {
    await this.loadService()
    await this.loadReviews()
  },

  methods: {
    async loadService() {
      this.loading = true
      this.error = null

      const serviceId = this.$route.params.id

      try {
        this.isAdminView = this.isAdmin

        let url = `/api/services/${serviceId}/`
        if (this.isAdminView) {
          url = `/api/admin/services/${serviceId}/`
        }

        const response = await axios.get(url)
        this.service = response.data

        if (this.service.primary_image) {
          this.mainImage = this.getImageUrl(this.service.primary_image)
        } else if (this.service.images && this.service.images.length > 0) {
          this.mainImage = this.getImageUrl(this.service.images[0].url)
        }

      } catch (error) {
        console.error('Ошибка загрузки услуги:', error)
        this.error = 'Не удалось загрузить информацию об услуге'
      } finally {
        this.loading = false
      }
    },

    async loadReviews() {
      const serviceId = this.$route.params.id
      this.reviewsLoading = true

      try {
        const res = await axios.get(`/api/services/${serviceId}/reviews/`)
        this.reviewsData = res.data
      } catch (e) {
        this.reviewsData = null
      } finally {
        this.reviewsLoading = false
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
      return this.mainImage || 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="%23f5f5f5"/><text x="50%" y="50%" font-family="Arial" font-size="16" fill="%23999" text-anchor="middle" dy=".3em">Нет изображения</text></svg>'
    },

    setMainImage(url) {
      this.mainImage = this.getImageUrl(url)
    },

    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    },

    // Создание заявки
    createOrder() {
      if (!this.isAuthenticated) {
        this.$router.push('/login')
      } else {
        this.$router.push(`/orders/new?service_id=${this.service.id}`)
      }
    },

    // Редактирование услуги (для админа)
    editService() {
      this.$router.push(`/admin/services/${this.service.id}/edit`)
    },

    // Деактивация услуги (для админа)
    async deactivateService() {
      if (!confirm('Вы уверены, что хотите деактивировать эту услугу?')) return

      try {
        await axios.post(`/api/admin/services/${this.service.id}/deactivate/`)
        this.service.is_active = false
        alert('Услуга деактивирована')
      } catch (error) {
        console.error('Ошибка деактивации:', error)
        alert('Ошибка при деактивации услуги')
      }
    },

    async activateService() {
      try {
        const response = await axios.patch(`/api/admin/services/${this.service.id}/`, {
          is_active: true
        })
        this.service = response.data
        alert('Услуга активирована')
      } catch (error) {
        console.error('Ошибка активации:', error)
        alert('Ошибка при активации услуги')
      }
    }
  }
}
</script>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}

.gap-2 > * {
  margin: 4px;
}
</style>