export const endpoints = {
  auth: {
    login: "/auth/jwt/create/",
    refresh: "/auth/jwt/refresh/",
    me: "/auth/users/me/",
    register: "/auth/users/",
    setPassword: "/auth/users/set_password/",
  },

  crud: {
    rooms: "/api/rooms/",
    clients: "/api/clients/",
    stays: "/api/stays/",
    employees: "/api/employees/",
    schedules: "/api/schedules/",
  },

  analytics: {
    freeRooms: "/api/analytics/free-rooms/",
    clientsFromCity: "/api/analytics/clients-from-city/",
    clientsInRoom: "/api/analytics/clients-in-room/",
    whoCleaned: "/api/analytics/who-cleaned-client-room/",
    clientsOverlap: "/api/analytics/clients-overlap/",
  },

  reports: {
    quarter: "/api/reports/quarter/",
  },
};