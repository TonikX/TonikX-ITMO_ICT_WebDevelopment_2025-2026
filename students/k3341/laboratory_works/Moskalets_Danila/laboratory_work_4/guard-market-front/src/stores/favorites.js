import { defineStore } from 'pinia'
import apiClient from '@/api'

export const useFavoritesStore = defineStore('favorites', {
    state: () => ({
        favorites: [],
        isLoading: false,
        error: null
    }),

    actions: {
        async fetchFavorites() {
            this.isLoading = true
            this.error = null

            try {
                // Всегда используем эндпоинт /my/ для получения своих избранных
                const response = await apiClient.get('favorites/my/')
                this.favorites = response.data || []
                console.log('Favorites loaded:', this.favorites)
                return this.favorites
            } catch (error) {
                console.error('Error loading favorites:', error)
                this.error = error.response?.data?.detail || 'Ошибка загрузки избранного'
                this.favorites = [] // Сбрасываем на пустой массив при ошибке
                throw error
            } finally {
                this.isLoading = false
            }
        },

        async addToFavorites(serviceId) {
            this.isLoading = true
            this.error = null

            try {
                const response = await apiClient.post('favorites/', { service_id: serviceId })
                console.log('Added to favorites:', response.data)

                // После добавления перезагружаем список избранного
                await this.fetchFavorites()
                return response.data
            } catch (error) {
                console.error('Error adding to favorites:', error)
                this.error = error.response?.data?.detail || 'Ошибка добавления в избранное'
                throw error
            } finally {
                this.isLoading = false
            }
        },

        async removeFromFavorites(favoriteId) {
            this.isLoading = true
            this.error = null

            try {
                await apiClient.delete(`favorites/${favoriteId}/`)
                console.log('Removed from favorites:', favoriteId)

                // Удаляем из локального списка
                const index = this.favorites.findIndex(fav => fav.id === favoriteId)
                if (index !== -1) {
                    this.favorites.splice(index, 1)
                }
            } catch (error) {
                console.error('Error removing from favorites:', error)
                this.error = error.response?.data?.detail || 'Ошибка удаления из избранного'
                throw error
            } finally {
                this.isLoading = false
            }
        },

        isServiceInFavorites(serviceId) {
            return this.favorites.some(fav => {
                // Проверяем разные форматы ответа
                if (fav.service_info && fav.service_info.id === serviceId) return true
                if (fav.service_id === serviceId) return true
                return false
            })
        },

        getFavoriteIdByServiceId(serviceId) {
            const favorite = this.favorites.find(fav => {
                if (fav.service_info && fav.service_info.id === serviceId) return true
                if (fav.service_id === serviceId) return true
                return false
            })
            console.log('Finding favorite for service', serviceId, 'found:', favorite)
            return favorite ? favorite.id : null
        }
    }
})