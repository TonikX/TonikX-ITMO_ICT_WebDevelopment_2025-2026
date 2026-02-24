<template>
  <v-container class="my-8">
    <h1 class="text-h4 text-center mb-6">Мои заявки</h1>

    <v-row v-if="orders.length">
      <v-col
          v-for="order in orders"
          :key="order.id"
          cols="12"
          md="6"
      >
        <v-card class="pa-4">
          <p><b>Услуга:</b> {{ order.service_name }}</p>
          <p><b>Цена:</b> {{ order.service_price }} руб.</p>
          <p><b>Статус:</b> {{ order.status }}</p>

          <v-btn size="small" class="mr-2" @click="openDetails(order.id)">
            Детали
          </v-btn>

          <v-btn size="small" class="mr-2" @click="openComments(order.id)">
            Комментарии
          </v-btn>

          <v-btn
              v-if="order.status !== 'completed'"
              size="small"
              color="error"
              class="mr-2"
              @click="cancelOrder(order.id)"
          >
            Отклонить
          </v-btn>

          <v-btn
              v-if="order.status === 'completed' && !reviewedServices.has(order.service)"
              size="small"
              color="primary"
              @click="openReview(order)"
          >
            Оставить отзыв
          </v-btn>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-else>
      <v-col cols="12" class="text-center">
        <p>Заявки недоступны</p>
      </v-col>
    </v-row>

    <!-- Детали -->
    <v-dialog v-model="detailsDialog" max-width="600">
      <v-card class="pa-4">
        <h3>Детали заявки</h3>

        <div class="mb-2">
          <strong>Комментарий:</strong>
          <p>{{ orderDetails && orderDetails.notes ? orderDetails.notes : '—' }}</p>
        </div>

        <div class="mb-2">
          <strong>Дата создания:</strong>
          <p>{{ orderDetails && orderDetails.created_at ? orderDetails.created_at : '—' }}</p>
        </div>

        <div class="mb-2">
          <strong>Название услуги:</strong>
          <p>{{ orderDetails && orderDetails.service_details ? orderDetails.service_details.name : '—' }}</p>
        </div>

        <div class="mb-2">
          <strong>Описание услуги:</strong>
          <p>{{ orderDetails && orderDetails.service_details ? orderDetails.service_details.description : '—' }}</p>
        </div>

        <v-btn color="primary" @click="detailsDialog = false">Закрыть</v-btn>
      </v-card>
    </v-dialog>


    <!-- Комментарии -->
    <v-dialog v-model="commentsDialog" max-width="600">
      <v-card class="pa-4">
        <h3>Комментарии</h3>
        <div v-for="c in comments" :key="c.id">
          <p>{{ c.content }}</p>
        </div>
        <v-btn @click="commentsDialog = false">Закрыть</v-btn>
      </v-card>
    </v-dialog>

    <!-- Отзыв -->
    <v-dialog v-model="reviewDialog" max-width="500">
      <v-card class="pa-4">
        <v-text-field label="Оценка" v-model="review.rating" />
        <v-text-field label="Заголовок" v-model="review.title" />
        <v-textarea label="Текст" v-model="review.content" />
        <v-btn color="primary" @click="sendReview">
          Отправить
        </v-btn>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'OrdersView',

  data() {
    return {
      orders: [],
      orderDetailsDialog: false,
      reviewedServices: new Set(),

      orderDetails: null,
      comments: [],
      selectedOrder: null,

      detailsDialog: false,
      commentsDialog: false,
      reviewDialog: false,

      review: {
        rating: 5,
        title: '',
        content: ''
      }
    }
  },

  async mounted() {
    try {
      const res = await axios.get('/api/orders/')
      this.orders = res.data.filter(o => o.status !== 'cancelled')

      const completedOrders = this.orders.filter(o => o.status === 'completed')

      for (const order of completedOrders) {
        const reviewsRes = await axios.get(
            `/api/services/${order.service}/reviews/`
        )

        const hasMyReview = reviewsRes.data.reviews.some(
            r => r.user_full_name
        )

        if (hasMyReview) {
          this.reviewedServices.add(order.service)
        }
      }
    } catch {
      this.orders = []
    }
  },

  methods: {
    async openDetails(id) {
      const res = await axios.get(`/api/orders/${id}/`)
      this.orderDetails = res.data
      this.detailsDialog = true
    },

    async openComments(id) {
      const res = await axios.get(`/api/orders/${id}/comments/`)
      this.comments = res.data
      this.commentsDialog = true
    },

    async cancelOrder(id) {
      await axios.post(`/api/orders/${id}/cancel/`)
      this.orders = this.orders.filter(o => o.id !== id)
    },

    openReview(order) {
      this.selectedOrder = order
      this.reviewDialog = true
    },

    async sendReview() {
      await axios.post('/api/reviews/', {
        order: this.selectedOrder.id,
        service: this.selectedOrder.service,
        rating: this.review.rating,
        title: this.review.title,
        content: this.review.content
      })

      this.reviewedServices.add(this.selectedOrder.service)
      this.reviewDialog = false
    }
  }
}
</script>
