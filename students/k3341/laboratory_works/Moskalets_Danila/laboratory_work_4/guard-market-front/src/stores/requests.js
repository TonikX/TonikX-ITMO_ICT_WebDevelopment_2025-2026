import { defineStore } from 'pinia'
import apiClient from '@/api'

export const useRequestsStore = defineStore('requests', {
    state: () => ({
        // Все заявки (для администратора)
        allRequests: [],
        // Мои заявки (для обычного пользователя)
        myRequests: [],
        // Заявки на мою компанию (для владельца компании)
        companyRequests: [],
        // Текущая выбранная заявка
        currentRequest: null,
        isLoading: false,
        error: null
    }),

    actions: {
        // Получить все заявки (только для администратора)
        async fetchAllRequests(params = {}) {
            this.isLoading = true
            this.error = null

            try {
                const response = await apiClient.get('requests/', { params })
                this.allRequests = response.data || []
                return this.allRequests
            } catch (error) {
                this.error = error.response?.data?.detail || 'Ошибка загрузки заявок'
                throw error
            } finally {
                this.isLoading = false
            }
        },

        // Получить мои заявки
        async fetchMyRequests(params = {}) {
            this.isLoading = true
            this.error = null

            try {
                const response = await apiClient.get('requests/my/')
                this.myRequests = response.data || []
                return this.myRequests
            } catch (error) {
                this.error = error.response?.data?.detail || 'Ошибка загрузки ваших заявок'
                throw error
            } finally {
                this.isLoading = false
            }
        },

        // Получить заявки на мою компанию
        async fetchCompanyRequests(params = {}) {
            this.isLoading = true
            this.error = null

            try {
                const response = await apiClient.get('requests/company/')
                this.companyRequests = response.data || []
                return this.companyRequests
            } catch (error) {
                this.error = error.response?.data?.detail || 'Ошибка загрузки заявок компании'
                throw error
            } finally {
                this.isLoading = false
            }
        },

        // Получить конкретную заявку по ID
        async fetchRequestById(id) {
            this.isLoading = true
            this.error = null

            try {
                const response = await apiClient.get(`requests/${id}/`)
                this.currentRequest = response.data
                return this.currentRequest
            } catch (error) {
                this.error = error.response?.data?.detail || 'Ошибка загрузки заявки'
                throw error
            } finally {
                this.isLoading = false
            }
        },

        // Создать новую заявку
        async createRequest(requestData) {
            this.isLoading = true
            this.error = null

            try {
                const response = await apiClient.post('requests/', requestData)
                // Добавляем в список моих заявок
                this.myRequests.unshift(response.data)
                return response.data
            } catch (error) {
                this.error = error.response?.data?.detail || 'Ошибка создания заявки'
                throw error
            } finally {
                this.isLoading = false
            }
        },

        // Обновить заявку (частичное обновление - PATCH)
        async updateRequest(id, requestData) {
            this.isLoading = true
            this.error = null

            try {
                console.log('Updating request:', id, 'with data:', requestData)

                const response = await apiClient.patch(`requests/${id}/`, requestData)
                console.log('Update response:', response.data)

                // Обновляем в соответствующих списках с сохранением всех данных
                this.updateRequestInLists(id, response.data)

                // Обновляем текущую заявку если она открыта
                if (this.currentRequest && this.currentRequest.id === id) {
                    this.currentRequest = response.data
                }

                return response.data
            } catch (error) {
                console.error('Error updating request:', error)
                this.error = error.response?.data?.detail || 'Ошибка обновления заявки'
                throw error
            } finally {
                this.isLoading = false
            }
        },

        // Удалить заявку
        async deleteRequest(id) {
            this.isLoading = true
            this.error = null

            try {
                console.log('Deleting request:', id)
                await apiClient.delete(`requests/${id}/`)
                console.log('Delete successful for request:', id)

                // Удаляем из всех списков
                this.removeRequestFromLists(id)

                // Очищаем текущую заявку если она удалена
                if (this.currentRequest && this.currentRequest.id === id) {
                    this.currentRequest = null
                }
            } catch (error) {
                console.error('Error deleting request:', error)
                this.error = error.response?.data?.detail || 'Ошибка удаления заявки'
                throw error
            } finally {
                this.isLoading = false
            }
        },

        // Вспомогательные методы для обновления списков
        updateRequestInLists(requestId, updatedRequest) {
            console.log('Updating request in lists:', requestId, 'with:', updatedRequest)

            // Обновляем заявку с сохранением всех полей
            const updateRequestData = (request) => {
                if (request.id === requestId) {
                    // Сохраняем все существующие данные и добавляем обновленные
                    return {
                        ...request,           // Сохраняем все старые данные
                        ...updatedRequest,    // Добавляем обновленные поля
                        // Убедимся, что id не перезаписан
                        id: requestId
                    }
                }
                return request
            }

            // Обновляем во всех списках
            this.allRequests = this.allRequests.map(updateRequestData)
            this.myRequests = this.myRequests.map(updateRequestData)
            this.companyRequests = this.companyRequests.map(updateRequestData)
        },

        removeRequestFromLists(requestId) {
            console.log('Removing request from lists:', requestId)
            this.allRequests = this.allRequests.filter(r => r.id !== requestId)
            this.myRequests = this.myRequests.filter(r => r.id !== requestId)
            this.companyRequests = this.companyRequests.filter(r => r.id !== requestId)
        },

        // Очистить текущую заявку
        clearCurrentRequest() {
            this.currentRequest = null
        },

        // Получить заявку по ID из кэша
        getRequestById(id) {
            // Ищем во всех списках
            const allRequest = this.allRequests.find(r => r.id === id)
            if (allRequest) return allRequest

            const myRequest = this.myRequests.find(r => r.id === id)
            if (myRequest) return myRequest

            const companyRequest = this.companyRequests.find(r => r.id === id)
            if (companyRequest) return companyRequest

            return null
        }
    },

    getters: {
        // Фильтрованные мои заявки для таблицы
        filteredMyRequestsTable: (state) => (statusFilter = null, searchTerm = '') => {
            let requests = [...state.myRequests]

            // Фильтрация по статусу
            if (statusFilter && statusFilter !== 'all') {
                requests = requests.filter(request => request.status === statusFilter)
            }

            // Поиск по названию услуги или описанию
            if (searchTerm) {
                const term = searchTerm.toLowerCase()
                requests = requests.filter(request =>
                    request.service_info?.name?.toLowerCase().includes(term) ||
                    request.description?.toLowerCase().includes(term) ||
                    request.service_info?.company?.name?.toLowerCase().includes(term) ||
                    request.user_info?.name?.toLowerCase().includes(term) ||
                    request.user_info?.email?.toLowerCase().includes(term)
                )
            }

            return requests
        },

        // Фильтрованные заявки компании
        filteredCompanyRequests: (state) => (statusFilter = null, searchTerm = '') => {
            let requests = [...state.companyRequests]

            // Фильтрация по статусу
            if (statusFilter && statusFilter !== 'all') {
                requests = requests.filter(request => request.status === statusFilter)
            }

            // Поиск по названию услуги, описанию или пользователю
            if (searchTerm) {
                const term = searchTerm.toLowerCase()
                requests = requests.filter(request =>
                    request.service_info?.name?.toLowerCase().includes(term) ||
                    request.description?.toLowerCase().includes(term) ||
                    request.user_info?.name?.toLowerCase().includes(term) ||
                    request.user_info?.email?.toLowerCase().includes(term)
                )
            }

            return requests
        },

        // Статистика по статусам для моих заявок
        myRequestsStats: (state) => {
            const stats = {
                pending: 0,
                confirmed: 0,
                in_progress: 0,
                completed: 0,
                cancelled: 0,
                total: state.myRequests.length
            }

            state.myRequests.forEach(request => {
                if (request.status && stats.hasOwnProperty(request.status)) {
                    stats[request.status]++
                }
            })

            return stats
        },

        // Статистика по статусам для заявок компании
        companyRequestsStats: (state) => {
            const stats = {
                pending: 0,
                confirmed: 0,
                in_progress: 0,
                completed: 0,
                cancelled: 0,
                total: state.companyRequests.length
            }

            state.companyRequests.forEach(request => {
                if (request.status && stats.hasOwnProperty(request.status)) {
                    stats[request.status]++
                }
            })

            return stats
        },

        // Перевод статуса на русский
        statusTranslation: () => {
            return {
                pending: 'Ожидание',
                confirmed: 'Подтверждено',
                in_progress: 'В работе',
                completed: 'Завершено',
                cancelled: 'Отменено'
            }
        },

        // Цвета для статусов
        statusColors: () => {
            return {
                pending: 'warning',
                confirmed: 'info',
                in_progress: 'primary',
                completed: 'success',
                cancelled: 'error'
            }
        },

        // Порядок сортировки статусов для отображения
        statusOrder: () => {
            return {
                pending: 1,
                confirmed: 2,
                in_progress: 3,
                completed: 4,
                cancelled: 5
            }
        },

        // Получить все статусы как массив
        allStatuses: () => {
            return [
                { value: 'pending', label: 'Ожидание', color: 'warning' },
                { value: 'confirmed', label: 'Подтверждено', color: 'info' },
                { value: 'in_progress', label: 'В работе', color: 'primary' },
                { value: 'completed', label: 'Завершено', color: 'success' },
                { value: 'cancelled', label: 'Отменено', color: 'error' }
            ]
        }
    }
})