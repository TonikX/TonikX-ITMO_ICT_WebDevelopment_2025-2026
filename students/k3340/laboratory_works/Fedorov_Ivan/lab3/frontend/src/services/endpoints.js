export const EP = {
  // auth
  login: "/auth/token/login/",
  register: "/auth/users/",
  me: "/auth/users/me/",
  setPassword: "/auth/users/set_password/",
  resetPassword: "/auth/users/reset_password/",

  // core CRUD
  rooms: "/api/rooms/",
  roomsAvailable: "/api/rooms/available/",
  clients: "/api/clients/",
  employees: "/api/employees/",
  cleaning: "/api/cleaning/",

  // custom
  clientsInPeriod: "/api/clients_in_period/",          // (9)
  whoCleaned: "/api/who_cleaned_client_room/",         // (10)
  samePeriodClients: "/api/same_period_clients/",      // (11)
  unjobEmployees: "/api/unjob_employees/",             // (12)
  getjobEmployees: "/api/getjob_employees/",           // (13)

  report: "/api/report/?quarter=4&year=2024",                               // (6)
  statsHotel: "/api/statistics/hotel/",                            // (15)
  statsClient: "/api/statistics/clients/",                    // (16)
  schedule: "/api/employee-schedule/",                           // (17)
};
