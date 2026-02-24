<template>
  <v-container class="my-8">
    <!-- Кнопка назад -->
    <v-btn
        @click="$router.go(-1)"
        color="primary"
        variant="text"
        class="mb-4"
    >
      <v-icon start>mdi-arrow-left</v-icon>
      Назад
    </v-btn>

    <v-card class="pa-6" max-width="800" style="margin: 0 auto;">
      <v-card-title class="text-h4 mb-6">
        Оформление заявки
      </v-card-title>

      <v-form @submit.prevent="submitOrder">
        <v-card-text>
          <!-- Информация об услуге -->
          <div v-if="service" class="mb-8">
            <h3 class="text-h6 mb-4">Выбранная услуга:</h3>
            <v-card variant="outlined" class="pa-4">
              <v-row align="center">
                <v-col cols="auto">
                  <v-img
                      :src="getServiceImage()"
                      :alt="service.name"
                      width="80"
                      height="80"
                      cover
                      class="rounded"
                  ></v-img>
                </v-col>
                <v-col>
                  <div class="text-h6">{{ service.name }}</div>
                  <div class="text-grey">{{ service.category }}</div>
                  <div class="text-h5 text-primary mt-2">{{ service.price }} руб.</div>
                </v-col>
              </v-row>
            </v-card>
          </div>

          <!-- Поле для комментария -->
          <v-textarea
              v-model="form.notes"
              label="Комментарий к заявке"
              variant="outlined"
              rows="4"
              :rules="[v => v.length <= 1000 || 'Максимум 1000 символов']"
              counter="1000"
              class="mb-6"
              placeholder="Укажите дополнительные пожелания или требования..."
          ></v-textarea>

          <!-- Ошибки -->
          <v-alert
              v-if="error"
              type="error"
              class="mb-4"
          >
            {{ error }}
          </v-alert>

          <!-- Кнопки -->
          <div class="d-flex justify-end gap-4">
            <v-btn
                @click="$router.go(-1)"
                variant="outlined"
                color="primary"
            >
              Отмена
            </v-btn>

            <v-btn
                type="submit"
                color="primary"
                :loading="loading"
                :disabled="loading"
            >
              Отправить заявку
            </v-btn>
          </div>
        </v-card-text>
      </v-form>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CreateOrderView',

  data() {
    return {
      service: null,
      loading: false,
      error: null,
      form: {
        service: null,
        notes: ''
      }
    }
  },

  async mounted() {
    const serviceId = this.$route.query.service_id
    if (serviceId) {
      await this.loadService(serviceId)
      this.form.service = serviceId
    } else {
      this.error = 'Не выбрана услуга'
    }
  },

  methods: {
    async loadService(serviceId) {
      try {
        const response = await axios.get(`/api/services/${serviceId}/`)
        this.service = response.data
      } catch (error) {
        console.error('Ошибка загрузки услуги:', error)
        this.error = 'Не удалось загрузить информацию об услуге'
      }
    },

    getServiceImage() {
      if (this.service && this.service.primary_image) {
        // Используем ту же логику что и в ServicesView
        const parts = this.service.primary_image.split('/')
        const filename = parts[parts.length - 1]
        return `../../../../media/services/${this.service.id}/${filename}`
      }
      return 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 80 80"><rect width="80" height="80" fill="%23f5f5f5"/></svg>'
    },

    async submitOrder() {
      this.loading = true
      this.error = null

      try {
        const response = await axios.post('/api/orders/', this.form)
        const createdOrder = response.data

        if (this.form.notes && this.form.notes.trim() !== '') {
          try {
            await axios.post('/api/admin/comments/', {
              order: createdOrder.id,
              content: this.form.notes,
              is_visible_to_user: true
            })
          } catch (commentError) {
            console.error('Ошибка создания комментария:', commentError)

          }
        }

        alert('Заявка успешно создана!')
        this.$router.push('/profile/orders')

      } catch (error) {
        console.error('Ошибка создания заявки:', error)
        this.error = error.response?.data?.detail || 'Ошибка при создании заявки'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.gap-4 > * {
  margin-right: 16px;
}

.gap-4 > *:last-child {
  margin-right: 0;
}
</style>