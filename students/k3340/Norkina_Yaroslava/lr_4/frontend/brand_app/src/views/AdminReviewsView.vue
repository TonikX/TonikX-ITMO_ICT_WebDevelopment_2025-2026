<template>
  <v-container class="my-8">
    <h1 class="text-h4 text-center mb-6">Отзывы (админ)</h1>

    <v-row v-if="reviews.length">
      <v-col
          v-for="review in reviews"
          :key="review.id"
          cols="12"
          md="6"
      >
        <v-card class="pa-4">
          <p><b>ID отзыва:</b> {{ review.id }}</p>
          <p><b>Пользователь:</b> {{ review.user_email }}</p>
          <p><b>ID заявки:</b> {{ review.order_id }}</p>
          <p><b>Услуга:</b> {{ review.service_name }}</p>

          <p><b>Рейтинг:</b> {{ review.rating }}</p>

          <p class="mt-2"><b>{{ review.title }}</b></p>
          <p>{{ review.content }}</p>

          <p class="text-caption mt-2">
            Проверен: {{ review.is_verified ? 'да' : 'нет' }} |
            Опубликован: {{ review.is_published ? 'да' : 'нет' }}
          </p>

          <v-btn
              v-if="!review.is_published"
              size="small"
              color="primary"
              class="mt-2"
              @click="publishReview(review)"
          >
            Опубликовать
          </v-btn>

          <p class="text-caption">
            Создан: {{ review.created_at }}
          </p>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-else>
      <v-col cols="12" class="text-center">
        <p>Отзывы недоступны</p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminReviewsView',

  data() {
    return {
      reviews: []
    }
  },

  async mounted() {
    try {
      const res = await axios.get('/api/admin/reviews/')
      this.reviews = res.data
    } catch (error) {
      console.error('Ошибка загрузки отзывов:', error)
      this.reviews = []
    }
  },

  methods: {
    async publishReview(review) {
      try {
        await axios.patch(`/api/admin/reviews/${review.id}/`, {
          rating: review.rating,
          title: review.title,
          content: review.content,
          is_verified: true,
          is_published: true
        })

        // локально обновляем состояние
        review.is_verified = true
        review.is_published = true
      } catch (error) {
        console.error('Ошибка публикации отзыва:', error)
      }
    }
  }
}
</script>
