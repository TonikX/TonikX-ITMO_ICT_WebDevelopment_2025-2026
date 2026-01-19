export const endpoints = {
  companies: '/companies/',
  aircrafts: '/aircrafts/',
  airports: '/airports/',
  employees: '/employees/',
  crews: '/crews/',
  crewMembers: '/crew-members/',
  flights: '/flights/',
  transitStops: '/transit-stops/',

  // Djoser (authtoken)
  register: '/auth/users/',            // POST create user
  tokenLogin: '/auth/token/login/',    // POST {username,password} -> {auth_token}
  tokenLogout: '/auth/token/logout/',  // POST logout (optional)
  currentUser: '/current-user/',       // GET custom endpoint
}
