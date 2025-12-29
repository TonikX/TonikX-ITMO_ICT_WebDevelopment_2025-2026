<template>
  <div>
    <!-- Уведомление об успехе -->
    <v-snackbar
        v-model="successSnackbar.show"
        :color="successSnackbar.color"
        :timeout="3000"
        location="top"
        elevation="24"
        class="success-notification"
        :z-index="9999"
    >
      <div class="d-flex align-center">
        <v-icon :color="successSnackbar.color" class="mr-3">
          {{ successSnackbar.icon }}
        </v-icon>
        <span class="text-body-1">{{ successSnackbar.text }}</span>
      </div>
      <template v-slot:actions>
        <v-btn
            variant="text"
            :color="successSnackbar.color === 'success' ? 'white' : 'white'"
            @click="successSnackbar.show = false"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </template>
    </v-snackbar>

    <!-- Форма для создания нового отзыва -->
    <v-card
        v-if="authStore.isAuthenticated && !hasUserReview && !isCompanyOwner"
        class="mb-6"
    >
      <v-card-title class="text-h6">
        <v-icon start icon="mdi-pencil-outline"></v-icon>
        Оставить отзыв
      </v-card-title>
      <v-card-text>
        <v-alert
            v-if="reviewError"
            type="error"
            class="mb-4"
            closable
            @click:close="reviewError = null"
        >
          {{ formatReviewError(reviewError) }}
        </v-alert>

        <v-form @submit.prevent="submitReview" ref="reviewForm">
          <!-- Рейтинг (только целые числа) -->
          <div class="text-center mb-4">
            <div class="d-flex justify-center mb-2">
              <v-rating
                  v-model="newReview.rating"
                  color="amber"
                  size="34"
                  hover
                  clearable
                  :disabled="reviewLoading"
                  :half-increments="false"
              />
            </div>
            <div class="text-caption text-grey">
              {{ getRatingHint(newReview.rating) }}
            </div>
          </div>

          <v-textarea
              v-model="newReview.comment"
              label="Ваш отзыв"
              :rules="[rules.required]"
              rows="3"
              placeholder="Поделитесь вашим опытом сотрудничества с компанией..."
              class="mb-4"
              :disabled="reviewLoading"
          ></v-textarea>

          <div class="d-flex justify-end">
            <v-btn
                type="submit"
                color="primary"
                :loading="reviewLoading"
                :disabled="!isNewReviewValid"
                prepend-icon="mdi-send"
            >
              Отправить отзыв
            </v-btn>
          </div>
        </v-form>
      </v-card-text>
    </v-card>

    <!-- Список отзывов -->
    <div v-if="isLoading && reviews.length === 0" class="text-center py-10">
      <v-progress-circular indeterminate></v-progress-circular>
      <p class="mt-4">Загрузка отзывов...</p>
    </div>

    <v-alert
        v-else-if="reviewsError"
        type="error"
        @close="reviewsError = null"
        closable
    >
      {{ reviewsError }}
    </v-alert>

    <div v-else-if="reviews.length === 0">
      <v-alert type="info">
        У этой компании пока нет отзывов.
        <span v-if="authStore.isAuthenticated && !isCompanyOwner">
          Будьте первым, кто оставит отзыв!
        </span>
      </v-alert>
    </div>

    <div v-else>
      <!-- Средний рейтинг и сортировка -->
      <v-card class="mb-6 average-rating-card">
        <v-card-text class="text-center">
          <div class="text-h3 font-weight-bold average-rating-value">
            {{ companyAverageRating.toFixed(1) }}
          </div>
          <v-rating
              :model-value="companyAverageRating"
              readonly
              color="amber"
              size="large"
              class="my-2 average-rating-stars"
              density="comfortable"
              :half-increments="false"
          />
          <div class="text-body-2 text-grey average-rating-count">
            На основе {{ reviews.length }} {{ getReviewCountText(reviews.length) }}
          </div>

          <!-- Сортировка отзывов -->
          <div class="d-flex justify-center mt-4">
            <v-chip-group v-model="sortOption" mandatory @update:model-value="changeSorting">
              <v-chip variant="outlined" size="small" value="-rating">
                <v-icon start icon="mdi-sort-descending"></v-icon>
                Высокий рейтинг
              </v-chip>
              <v-chip variant="outlined" size="small" value="rating">
                <v-icon start icon="mdi-sort-ascending"></v-icon>
                Низкий рейтинг
              </v-chip>
              <v-chip variant="outlined" size="small" value="-created_at">
                <v-icon start icon="mdi-clock-outline"></v-icon>
                Сначала новые
              </v-chip>
            </v-chip-group>
          </div>
        </v-card-text>
      </v-card>

      <!-- Карточки отзывов -->
      <v-card
          v-for="review in sortedReviews"
          :key="review.id"
          class="mb-4 review-card"
      >
        <v-card-text>
          <div class="d-flex align-start mb-2">
            <div class="flex-grow-1">
              <div class="text-h6">
                {{ review.user_info.name || 'Анонимный пользователь' }}
              </div>
              <div class="text-caption text-grey">
                {{ formatDate(review.created_at) }}
              </div>
            </div>

            <div class="d-flex align-center">
              <v-rating
                  :model-value="review.rating"
                  readonly
                  color="amber"
                  density="compact"
                  size="small"
                  class="mr-2"
                  :half-increments="false"
              />
              <span class="text-h6 font-weight-bold">{{ review.rating }}</span>
            </div>
          </div>

          <p class="text-body-1 review-comment">
            {{ review.comment }}
          </p>

          <!-- Кнопки управления для своих отзывов -->
          <div v-if="isCurrentUserReview(review)" class="text-right">
            <v-btn
                @click="openEditDialog(review)"
                size="small"
                variant="text"
                class="mr-2"
                :loading="reviewLoading"
            >
              Редактировать
            </v-btn>
            <v-btn
                @click="initiateDeleteReview(review.id)"
                size="small"
                variant="text"
                color="error"
                :loading="reviewLoading"
            >
              Удалить
            </v-btn>
          </div>
        </v-card-text>
      </v-card>
    </div>

    <!-- Диалог редактирования отзыва -->
    <v-dialog v-model="editDialog.show" max-width="500" persistent>
      <v-card>
        <v-card-title>Редактировать отзыв</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="updateReview" ref="editReviewForm">
            <div class="text-center mb-4">
              <v-rating
                  v-model="editDialog.form.rating"
                  color="amber"
                  size="large"
                  class="mb-2 rating-stars"
                  hover
                  clearable
                  :readonly="reviewLoading"
                  :half-increments="false"
              />
              <div v-if="editDialog.form.rating > 0" class="text-body-2 text-amber">
                Выбрано: {{ editDialog.form.rating }} {{ getRatingText(editDialog.form.rating) }}
              </div>
              <div v-else class="text-body-2 text-grey">
                Нажмите на звезду для оценки
              </div>
            </div>

            <v-textarea
                v-model="editDialog.form.comment"
                label="Ваш отзыв"
                :rules="[rules.required]"
                rows="3"
                class="mb-4"
                :disabled="reviewLoading"
            ></v-textarea>

            <div class="d-flex justify-end">
              <v-btn
                  @click="editDialog.show = false"
                  class="mr-2"
                  :disabled="reviewLoading"
              >
                Отмена
              </v-btn>
              <v-btn
                  type="submit"
                  color="primary"
                  :loading="reviewLoading"
                  :disabled="!editDialog.form.rating || !editDialog.form.comment.trim()"
              >
                Сохранить
              </v-btn>
            </div>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Диалог подтверждения удаления -->
    <v-dialog v-model="deleteDialog.show" max-width="400">
      <v-card>
        <v-card-title class="d-flex align-center">
          <v-icon icon="mdi-alert-circle-outline" color="error" class="mr-2"></v-icon>
          Подтвердите удаление
        </v-card-title>
        <v-card-text>
          <p class="text-body-1 mb-4">
            Вы уверены, что хотите удалить свой отзыв? Это действие нельзя отменить.
          </p>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn
              @click="deleteDialog.show = false"
              variant="text"
              :disabled="reviewLoading"
          >
            Отмена
          </v-btn>
          <v-btn
              @click="confirmDeleteReview"
              color="error"
              :loading="reviewLoading"
              prepend-icon="mdi-delete"
          >
            Удалить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, reactive, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/api'

const props = defineProps({
  company: {
    type: Object,
    required: true
  },
  reviews: {
    type: Array,
    default: () => []
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  onReviewSubmitted: {
    type: Function,
    default: () => {}
  }
})

const authStore = useAuthStore()

// Состояния
const reviewsError = ref(null)
const reviewLoading = ref(false)
const reviewError = ref(null)
const sortOption = ref('-created_at') // По умолчанию: сначала новые
const companyReviews = ref([]) // Отзывы, загруженные с сервера с сортировкой

const newReview = reactive({
  rating: 0,
  comment: ''
})

const editDialog = reactive({
  show: false,
  form: {
    id: null,
    rating: 0,
    comment: ''
  }
})

const deleteDialog = reactive({
  show: false,
  reviewId: null
})

const successSnackbar = reactive({
  show: false,
  text: '',
  color: 'success'
})

// Computed свойства
const companyAverageRating = computed(() => {
  if (!props.company) return 0
  return props.company.average_rating || 0
})

const isCompanyOwner = computed(() => {
  if (!authStore.user || !props.company) return false
  return authStore.user.id === props.company.user?.id
})

const hasUserReview = computed(() => {
  if (!authStore.user || !companyReviews.value?.length) return false
  return companyReviews.value.some(review => isCurrentUserReview(review))
})

const isNewReviewValid = computed(() => {
  return newReview.rating > 0 && newReview.comment.trim().length > 0
})

// Сортируем отзывы локально (если нужно, можно и серверную сортировку)
const sortedReviews = computed(() => {
  if (!companyReviews.value.length) return []

  const reviews = [...companyReviews.value]

  switch (sortOption.value) {
    case '-rating': // Высокий рейтинг
      return reviews.sort((a, b) => b.rating - a.rating)
    case 'rating': // Низкий рейтинг
      return reviews.sort((a, b) => a.rating - b.rating)
    case '-created_at': // Сначала новые
      return reviews.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    default:
      return reviews
  }
})

// Правила валидации
const rules = {
  required: value => !!value?.trim() || 'Обязательное поле'
}

// Вспомогательные методы
const isCurrentUserReview = (review) => {
  if (!authStore.user) return false
  console.log(review)
  return review.user_info.id === authStore.user.id
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const getRatingHint = (rating) => {
  if (!rating || rating === 0) return 'Нажмите на звезду для оценки'
  const hints = {
    1: '★ - Плохо',
    2: '★★ - Удовлетворительно',
    3: '★★★ - Хорошо',
    4: '★★★★ - Отлично',
    5: '★★★★★ - Превосходно'
  }
  return hints[rating] || ''
}

const getRatingText = (rating) => {
  const texts = {
    1: '★ - Плохо',
    2: '★★ - Удовлетворительно',
    3: '★★★ - Хорошо',
    4: '★★★★ - Отлично',
    5: '★★★★★ - Превосходно'
  }
  return texts[rating] || ''
}

const getReviewCountText = (count) => {
  if (count % 10 === 1 && count % 100 !== 11) return 'отзыва'
  if (count % 10 >= 2 && count % 10 <= 4 && (count % 100 < 10 || count % 100 >= 20)) return 'отзыва'
  return 'отзывов'
}

const formatReviewError = (errorData) => {
  if (typeof errorData === 'string') return errorData
  if (errorData.detail) return errorData.detail

  if (errorData.security_company_id) {
    const msg = Array.isArray(errorData.security_company_id)
        ? errorData.security_company_id[0]
        : errorData.security_company_id
    if (msg.includes('already exists')) return 'Вы уже оставляли отзыв для этой компании'
    return msg
  }

  return 'Ошибка при отправке отзыва'
}

const showSuccessMessage = (message, type = 'success') => {
  successSnackbar.text = message
  successSnackbar.color = type
  successSnackbar.icon = type === 'success' ? 'mdi-check-circle' : 'mdi-alert-circle'
  successSnackbar.show = true

  // Гарантируем, что уведомление будет наверху
  setTimeout(() => {
    const snackbar = document.querySelector('.success-notification')
    if (snackbar) {
      snackbar.style.zIndex = '9999'
    }
  }, 100)
}

// Загрузка отзывов с сервера с сортировкой
const loadCompanyReviews = async () => {
  if (!props.company?.id) return

  try {
    // Используем эндпоинт company_reviews_by_id
    const response = await apiClient.get(`reviews/company/${props.company.id}/`, {
      params: {
        ordering: sortOption.value
      }
    })

    companyReviews.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки отзывов компании:', error)
    // Если не работает эндпоинт, используем данные из props
    companyReviews.value = props.reviews
  }
}

// Изменение сортировки
const changeSorting = async () => {
  await loadCompanyReviews()
}

// Основные методы
const submitReview = async () => {
  if (!props.company || reviewLoading.value) return

  reviewLoading.value = true
  reviewError.value = null

  try {
    await apiClient.post('reviews/', {
      security_company_id: props.company.id,
      rating: newReview.rating,
      comment: newReview.comment.trim()
    })

    showSuccessMessage('Ваш отзыв успешно опубликован!')

    // Очищаем форму
    newReview.rating = 0
    newReview.comment = ''

    // Обновляем данные
    if (props.onReviewSubmitted) {
      await props.onReviewSubmitted()
    }

    // Перезагружаем отзывы с сервера
    await loadCompanyReviews()
  } catch (error) {
    console.error('Ошибка при отправке отзыва:', error)
    reviewError.value = error.response?.data || 'Ошибка при отправке отзыва'
  } finally {
    reviewLoading.value = false
  }
}

const openEditDialog = (review) => {
  editDialog.form.id = review.id
  editDialog.form.rating = review.rating
  editDialog.form.comment = review.comment
  editDialog.show = true
}

const updateReview = async () => {
  if (!editDialog.form.id) return

  reviewLoading.value = true

  try {
    await apiClient.put(`reviews/${editDialog.form.id}/`, {
      rating: editDialog.form.rating,
      comment: editDialog.form.comment.trim(),
      security_company_id: props.company.id
    })

    showSuccessMessage('Отзыв успешно обновлен!')
    editDialog.show = false

    if (props.onReviewSubmitted) {
      await props.onReviewSubmitted()
    }

    // Перезагружаем отзывы с сервера
    await loadCompanyReviews()
  } catch (error) {
    console.error('Ошибка при обновлении отзыва:', error)
    reviewError.value = error.response?.data?.detail || 'Ошибка обновления отзыва'
  } finally {
    reviewLoading.value = false
  }
}

const initiateDeleteReview = (reviewId) => {
  deleteDialog.reviewId = reviewId
  deleteDialog.show = true
}

const confirmDeleteReview = async () => {
  if (!deleteDialog.reviewId) return

  reviewLoading.value = true

  try {
    await apiClient.delete(`reviews/${deleteDialog.reviewId}/`)

    showSuccessMessage('Отзыв успешно удален!')
    deleteDialog.show = false

    if (props.onReviewSubmitted) {
      await props.onReviewSubmitted()
    }

    // Перезагружаем отзывы с сервера
    await loadCompanyReviews()
  } catch (error) {
    console.error('Ошибка при удалении отзыва:', error)
    reviewsError.value = error.response?.data?.detail || 'Ошибка удаления отзыва'
  } finally {
    reviewLoading.value = false
  }
}

// Загрузка отзывов при монтировании или изменении компании
watch(() => props.company, async (newCompany) => {
  if (newCompany?.id) {
    await loadCompanyReviews()
  }
  reviewsError.value = null
  reviewError.value = null
}, { immediate: true })

// Используем локальные отзывы для отображения
const displayReviews = computed(() => {
  return companyReviews.value.length ? companyReviews.value : props.reviews
})
</script>

<style scoped>
/* Сохраняем ваши оригинальные стили */

.average-rating-card {
  background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
  border: 1px solid #ffd54f;
}

.average-rating-value {
  color: #ff9800;
}

.average-rating-stars {
  display: inline-block;
}

.average-rating-count {
  margin-top: 8px;
}

:deep(.average-rating-stars .v-icon) {
  opacity: 1;
}

:deep(.average-rating-stars .v-icon.v-icon--selected) {
  color: #FF9800 !important;
}

:deep(.average-rating-stars .v-icon:not(.v-icon--selected)) {
  color: #ffcc80 !important;
}

.review-card {
  border-left: 4px solid #FFC107;
  transition: all 0.3s ease;
}

.review-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.review-comment {
  line-height: 1.6;
  color: #333;
}

/* Стили для чипов сортировки */
:deep(.v-chip-group .v-chip) {
  margin: 4px;
}

:deep(.v-chip-group .v-chip--selected) {
  background-color: rgba(25, 118, 210, 0.1);
  border-color: #1976d2;
}
</style>