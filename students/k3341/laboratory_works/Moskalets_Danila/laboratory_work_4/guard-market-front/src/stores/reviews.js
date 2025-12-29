import { defineStore } from 'pinia'
import apiClient from '@/api'

export const useReviewsStore = defineStore('reviews', {
    state: () => ({
        reviews: [],
        companyReviews: [], // Отзывы для конкретной компании
        userReviews: [], // Отзывы текущего пользователя
        isLoading: false,
        error: null,
        currentPage: 1,
        totalPages: 1
    }),

    actions: {
        // Получить все отзывы (для администраторов)
        async fetchReviews(params = {}) {
            this.isLoading = true
            this.error = null

            try {
                const response = await apiClient.get('reviews/', { params })
                this.reviews = response.data.results || response.data
                this.totalPages = Math.ceil(response.data.count / 10) || 1
                this.currentPage = params.page || 1
                return this.reviews
            } catch (error) {
                this.error = error.response?.data?.detail || 'Ошибка загрузки отзывов'
                console.error('Fetch reviews error:', error)
                throw error
            } finally {
                this.isLoading = false
            }
        },

        // Получить отзывы для конкретной компании
        async fetchCompanyReviews(companyId) {
            this.isLoading = true
            this.error = null

            try {
                const response = await apiClient.get('reviews/', {
                    params: {
                        security_company_id: companyId,
                        page_size: 50 // Большое число чтобы получить все отзывы
                    }
                })
                this.companyReviews = response.data.results || response.data
                return this.companyReviews
            } catch (error) {
                this.error = error.response?.data?.detail || 'Ошибка загрузки отзывов компании'
                console.error('Fetch company reviews error:', error)
                throw error
            } finally {
                this.isLoading = false
            }
        },

        // Получить отзывы текущего пользователя
        async fetchMyReviews() {
            this.isLoading = true
            this.error = null

            try {
                const response = await apiClient.get('reviews/my/')
                this.userReviews = response.data.results || response.data
                return this.userReviews
            } catch (error) {
                this.error = error.response?.data?.detail || 'Ошибка загрузки ваших отзывов'
                console.error('Fetch my reviews error:', error)
                throw error
            } finally {
                this.isLoading = false
            }
        },

        // Создать отзыв
        async createReview(reviewData) {
            this.isLoading = true
            this.error = null

            try {
                const response = await apiClient.post('reviews/', reviewData)

                // Добавляем в локальные списки
                this.reviews.unshift(response.data)
                this.companyReviews.unshift(response.data)

                return response.data
            } catch (error) {
                this.error = error.response?.data?.detail || 'Ошибка создания отзыва'
                console.error('Create review error:', error)
                throw error
            } finally {
                this.isLoading = false
            }
        },

        // Обновить отзыв
        async updateReview(reviewId, reviewData) {
            this.isLoading = true
            this.error = null

            try {
                const response = await apiClient.put(`reviews/${reviewId}/`, reviewData)

                // Обновляем в локальных списках
                this.updateReviewInLists(reviewId, response.data)

                return response.data
            } catch (error) {
                this.error = error.response?.data?.detail || 'Ошибка обновления отзыва'
                console.error('Update review error:', error)
                throw error
            } finally {
                this.isLoading = false
            }
        },

        // Удалить отзыв
        async deleteReview(reviewId) {
            this.isLoading = true
            this.error = null

            try {
                await apiClient.delete(`reviews/${reviewId}/`)

                // Удаляем из локальных списков
                this.removeReviewFromLists(reviewId)
            } catch (error) {
                this.error = error.response?.data?.detail || 'Ошибка удаления отзыва'
                console.error('Delete review error:', error)
                throw error
            } finally {
                this.isLoading = false
            }
        },

        // Вспомогательные методы для обновления локальных списков
        updateReviewInLists(reviewId, updatedReview) {
            // Обновляем в общем списке
            const reviewIndex = this.reviews.findIndex(r => r.id === reviewId)
            if (reviewIndex !== -1) {
                this.reviews[reviewIndex] = updatedReview
            }

            // Обновляем в списке компании
            const companyReviewIndex = this.companyReviews.findIndex(r => r.id === reviewId)
            if (companyReviewIndex !== -1) {
                this.companyReviews[companyReviewIndex] = updatedReview
            }

            // Обновляем в списке пользователя
            const userReviewIndex = this.userReviews.findIndex(r => r.id === reviewId)
            if (userReviewIndex !== -1) {
                this.userReviews[userReviewIndex] = updatedReview
            }
        },

        removeReviewFromLists(reviewId) {
            this.reviews = this.reviews.filter(r => r.id !== reviewId)
            this.companyReviews = this.companyReviews.filter(r => r.id !== reviewId)
            this.userReviews = this.userReviews.filter(r => r.id !== reviewId)
        },

        // Очистить отзывы компании
        clearCompanyReviews() {
            this.companyReviews = []
        }
    },

    getters: {
        // Найти отзыв пользователя для компании
        getUserReviewForCompany: (state) => (companyId, userId) => {
            return state.companyReviews.find(review =>
                review.security_company === companyId &&
                review.user?.id === userId
            )
        },

        // Получить средний рейтинг компании
        getCompanyAverageRating: (state) => {
            if (state.companyReviews.length === 0) return 0

            const total = state.companyReviews.reduce((sum, review) => sum + review.rating, 0)
            return total / state.companyReviews.length
        },

        // Проверить, оставил ли пользователь отзыв для компании
        hasUserReviewedCompany: (state) => (companyId, userId) => {
            return state.companyReviews.some(review =>
                review.security_company === companyId &&
                review.user?.id === userId
            )
        }
    }
})