<template>
  <v-container class="my-8">
    <h1 class="text-h4 text-center mb-6">Услуги</h1>

    <v-row v-if="services.length > 0">
      <v-col
          v-for="service in services"
          :key="service.id"
          cols="12"
          md="6"
          lg="4"
      >
        <v-card class="pa-4 h-100 d-flex flex-column">
          <div class="mb-3 flex-grow-0" style="height: 200px; overflow: hidden; cursor: pointer;"
               @click="goToServiceDetail(service)">
            <img
                :src="getImagePath(service)"
                :alt="service.name"
                style="width: 100%; height: 100%; object-fit: cover; border-radius: 8px;"
            />
          </div>

          <div class="flex-grow-1">
            <v-card-title
                class="text-h6 mb-2 pa-0"
                style="cursor: pointer;"
                @click="goToServiceDetail(service)"
            >
              {{ service.name }}
            </v-card-title>

            <v-card-subtitle class="mb-2 pa-0">
              {{ service.category }}
            </v-card-subtitle>

            <v-card-text class="text-grey mb-3 pa-0">
              {{ truncateDescription(service.description, 100) }}
            </v-card-text>
          </div>

          <v-card-text class="mb-3 pa-0 flex-grow-0">
            <div class="mb-1">
              <span class="text-h6 text-primary font-weight-bold">{{ service.price }} руб.</span>
            </div>
            <div v-if="service.duration" class="text-caption text-grey">
              Длительность: {{ service.duration }} мин
            </div>
          </v-card-text>

          <v-card-actions class="pa-0 mt-2 flex-grow-0">
            <v-btn
                color="primary"
                block
                @click="createOrder(service)"
                size="large"
            >
              Выбрать
            </v-btn>
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
  name: 'ServicesView',

  data() {
    return {
      services: [],
      loading: false
    }
  },

  async mounted() {
    await this.loadServices()
  },

  computed: {
    isAuthenticated() {
      return this.$store.getters.isAuthenticated
    }
  },

  methods: {
    async loadServices() {
      this.loading = true
      try {
        const response = await axios.get('/api/services/')
        this.services = response.data
      } catch (error) {
        console.error('Ошибка загрузки услуг:', error)
        this.services = []
      } finally {
        this.loading = false
      }
    },

    goToServiceDetail(service) {
      this.$router.push(`/services/${service.id}`)
    },

    createOrder(service) {
      if (!this.isAuthenticated) {
        this.$router.push('/login')
      } else {
        this.$router.push(`/orders/new?service_id=${service.id}`)
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