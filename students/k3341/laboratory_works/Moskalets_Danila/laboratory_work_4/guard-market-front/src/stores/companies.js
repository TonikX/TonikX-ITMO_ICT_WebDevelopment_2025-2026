import { defineStore } from 'pinia'
import apiClient from '@/api'

export const useCompaniesStore = defineStore('companies', {
    state: () => ({
        companies: [],
        currentCompany: null,
        isLoading: false,
        error: null,
        totalPages: 1,
        currentPage: 1,
        // Новые состояния для управления компанией
        companyDiscounts: [],
        companyServices: []
    }),

    actions: {
        async fetchCompanies(params = {}) {
            this.isLoading = true
            this.error = null

            try {
                const response = await apiClient.get('companies/', { params })
                this.companies = response.data.results || response.data
                this.totalPages = Math.ceil(response.data.count / 10) || 1
                this.currentPage = params.page || 1
            } catch (error) {
                this.error = error.response?.data?.detail || 'Ошибка загрузки компаний'
                console.error('Fetch companies error:', error)
            } finally {
                this.isLoading = false
            }
        },

        async fetchCompanyById(id) {
            this.isLoading = true
            this.error = null

            try {
                const response = await apiClient.get(`companies/${id}/`)
                this.currentCompany = response.data
                return response.data
            } catch (error) {
                this.error = error.response?.data?.detail || 'Ошибка загрузки компании'
                console.error('Fetch company error:', error)
                throw error
            } finally {
                this.isLoading = false
            }
        },

        async fetchMyCompany() {
            this.isLoading = true
            this.error = null

            try {
                const response = await apiClient.get('companies/my/')
                this.currentCompany = response.data
                return response.data
            } catch (error) {
                if (error.response?.status === 404) {
                    // У пользователя нет компании - это нормально
                    this.currentCompany = null
                    return null
                }
                this.error = error.response?.data?.detail || 'Ошибка загрузки компании'
                console.error('Fetch my company error:', error)
                throw error
            } finally {
                this.isLoading = false
            }
        },

        async createCompany(companyData) {
            this.isLoading = true
            this.error = null

            try {
                const response = await apiClient.post('companies/', companyData)
                this.currentCompany = response.data
                return response.data
            } catch (error) {
                this.error = error.response?.data?.detail || 'Ошибка создания компании'
                console.error('Create company error:', error)
                throw error
            } finally {
                this.isLoading = false
            }
        },

        async updateCompany(companyData) {
            this.isLoading = true
            this.error = null

            try {
                const response = await apiClient.put('companies/update_my/', companyData)
                this.currentCompany = response.data
                return response.data
            } catch (error) {
                this.error = error.response?.data?.detail || 'Ошибка обновления компании'
                console.error('Update company error:', error)
                throw error
            } finally {
                this.isLoading = false
            }
        },

        async deleteCompany() {
            this.isLoading = true
            this.error = null

            try {
                await apiClient.delete('companies/destroy_my/')
                this.currentCompany = null
            } catch (error) {
                this.error = error.response?.data?.detail || 'Ошибка удаления компании'
                console.error('Delete company error:', error)
                throw error
            } finally {
                this.isLoading = false
            }
        },

        async fetchCompanyDiscounts(companyId) {
            this.isLoading = true
            this.error = null

            try {
                const response = await apiClient.get('discounts/', {
                    params: { security_company: companyId }
                })
                this.companyDiscounts = response.data
                return response.data
            } catch (error) {
                this.error = error.response?.data?.detail || 'Ошибка загрузки скидок'
                throw error
            } finally {
                this.isLoading = false
            }
        },

        async fetchCompanyServices() {
            this.isLoading = true
            this.error = null

            try {
                const response = await apiClient.get('services/', {
                    params: { company_only: true }
                })
                this.companyServices = response.data.results || response.data
                return this.companyServices
            } catch (error) {
                this.error = error.response?.data?.detail || 'Ошибка загрузки услуг компании'
                throw error
            } finally {
                this.isLoading = false
            }
        },

        clearCurrentCompany() {
            this.currentCompany = null
        }
    },

    getters: {
        getCompanyById: (state) => (id) => {
            return state.companies.find(company => company.id === id)
        },

        // Новые геттеры для управления компанией
        activeDiscounts: (state) => {
            const now = new Date()
            return state.companyDiscounts.filter(discount => {
                const start = new Date(discount.start_date)
                const end = new Date(discount.end_date)
                return now >= start && now <= end
            })
        }
    }
})