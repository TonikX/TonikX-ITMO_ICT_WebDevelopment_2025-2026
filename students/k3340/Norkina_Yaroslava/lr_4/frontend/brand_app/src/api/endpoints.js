const API_BASE = 'http://localhost:8000'

export const ENDPOINTS = {
    // Аутентификация (Djoser)
    AUTH: {
        LOGIN: `${API_BASE}/auth/jwt/create/`,
        REGISTER: `${API_BASE}/auth/users/`,
        LOGOUT: `${API_BASE}/auth/jwt/logout/`,
        REFRESH: `${API_BASE}/auth/jwt/refresh/`,
        VERIFY: `${API_BASE}/auth/jwt/verify/`,
        USER_INFO: `${API_BASE}/auth/users/me/`,
    },

    // Услуги
    SERVICES: {
        LIST: `${API_BASE}/api/services/`,
        DETAIL: (id) => `${API_BASE}/api/services/${id}/`,
        CATEGORIES: `${API_BASE}/api/services/categories/`,
    },

    // Заказы (Orders)
    ORDERS: {
        LIST: `${API_BASE}/api/orders/`,
        CREATE: `${API_BASE}/api/orders/`,
        DETAIL: (id) => `${API_BASE}/api/orders/${id}/`,
        CANCEL: (id) => `${API_BASE}/api/orders/${id}/cancel/`,
        COMMENTS: (orderId) => `${API_BASE}/api/orders/${orderId}/comments/`,
    },

    // Админские endpoints
    ADMIN: {
        SERVICES: {
            LIST: `${API_BASE}/api/admin/services/`,
            DETAIL: (id) => `${API_BASE}/api/admin/services/${id}/`,
            DEACTIVATE: (id) => `${API_BASE}/api/admin/services/${id}/deactivate/`,
        },
        ORDERS: {
            LIST: `${API_BASE}/api/admin/orders/`,
            DETAIL: (id) => `${API_BASE}/api/admin/orders/${id}/`,
            STATUS: (id) => `${API_BASE}/api/admin/orders/${id}/status/`,
            HISTORY: (id) => `${API_BASE}/api/admin/orders/${id}/history/`,
        },
        USERS: {
            LIST: `${API_BASE}/api/admin/users/`,
            DETAIL: (id) => `${API_BASE}/api/admin/users/${id}/`,
            ROLE: (id) => `${API_BASE}/api/admin/users/${id}/role/`,
        },
    },
}

export const API_BASE_URL = API_BASE