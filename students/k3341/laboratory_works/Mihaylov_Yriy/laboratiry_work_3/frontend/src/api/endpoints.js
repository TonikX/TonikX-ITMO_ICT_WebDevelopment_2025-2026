export const API_BASE = 'http://localhost:8000/api/'
export const AUTH_BASE = 'http://localhost:8000/'

export const ENDPOINTS = {
    // Авторизация
    LOGIN: 'auth/jwt/create/',
    REGISTER: 'auth/users/',
    USER_ME: 'auth/users/me/',

    // API endpoints
    CARS_LIST: 'cars/',
    CAR_DETAIL: (id) => `cars/${id}/`,
    CAR_APPLICATION: (id) => `cars/${id}/application/`,

    // Клиенты (если есть endpoint)
    CLIENTS_LIST: 'clients/',

    // Договоры
    LEASES_LIST: 'leases/',

    // Заявки
    APPLICATIONS_LIST: 'lease_applications/',

    // Обслуживание
    MAINTENANCE_LIST: 'maintenance/',

    // Отчеты
    REPORTS_REVENUE: 'reports/revenue/',
    REPORTS_UTILIZATION: 'reports/utilization/',
}