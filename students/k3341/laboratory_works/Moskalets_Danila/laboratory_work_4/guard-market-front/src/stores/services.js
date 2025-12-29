import { defineStore } from 'pinia'
import apiClient from '@/api'

export const useServicesStore = defineStore('services', {
    state: () => ({
        services: [],
        currentService: null,
        isLoading: false,
        error: null,
        totalPages: 1,
        currentPage: 1
    }),

    actions: {
        async fetchServices(params = {}) {
            this.isLoading = true
            this.error = null

            try {
                const response = await apiClient.get('services/', { params })
                this.services = response.data.results || response.data
                this.totalPages = Math.ceil(response.data.count / 10) || 1
                this.currentPage = params.page || 1
            } catch (error) {
                this.error = error.response?.data?.detail || 'Ошибка загрузки услуг'
                console.error('Fetch services error:', error)
            } finally {
                this.isLoading = false
            }
        },

        async fetchServiceById(id) {
            this.isLoading = true
            this.error = null

            try {
                const response = await apiClient.get(`services/${id}/`)
                this.currentService = response.data
                return response.data
            } catch (error) {
                this.error = error.response?.data?.detail || 'Ошибка загрузки услуги'
                console.error('Fetch service error:', error)
                throw error
            } finally {
                this.isLoading = false
            }
        },

        async createService(serviceData) {
            this.isLoading = true
            this.error = null

            try {
                const response = await apiClient.post('services/', serviceData)
                return response.data
            } catch (error) {
                this.error = error.response?.data?.detail || 'Ошибка создания услуги'
                console.error('Create service error:', error)
                throw error
            } finally {
                this.isLoading = false
            }
        },

        async updateService(id, serviceData) {
            this.isLoading = true
            this.error = null

            try {
                const response = await apiClient.put(`services/${id}/`, serviceData)
                this.currentService = response.data
                return response.data
            } catch (error) {
                this.error = error.response?.data?.detail || 'Ошибка обновления услуги'
                console.error('Update service error:', error)
                throw error
            } finally {
                this.isLoading = false
            }
        },

        async deleteService(id) {
            this.isLoading = true
            this.error = null

            try {
                await apiClient.delete(`services/${id}/`)
            } catch (error) {
                this.error = error.response?.data?.detail || 'Ошибка удаления услуги'
                console.error('Delete service error:', error)
                throw error
            } finally {
                this.isLoading = false
            }
        }
    },

    getters: {
        getServiceById: (state) => (id) => {
            return state.services.find(service => service.id === id)
        }
    }
})