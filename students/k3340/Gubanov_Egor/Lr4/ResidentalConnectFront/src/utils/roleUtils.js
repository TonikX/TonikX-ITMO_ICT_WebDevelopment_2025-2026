export const ROLES = {
  RESIDENT: 'resident',
  MASTER: 'master',
  DISPATCHER: 'dispatcher',
}

export const ROLE_LABELS = {
  [ROLES.RESIDENT]: 'Жилец',
  [ROLES.MASTER]: 'Мастер',
  [ROLES.DISPATCHER]: 'Диспетчер',
}

export function isResident(user) {
  return user?.role === ROLES.RESIDENT
}

export function isMaster(user) {
  return user?.role === ROLES.MASTER
}

export function isDispatcher(user) {
  return user?.role === ROLES.DISPATCHER
}

export function getRoleLabel(role) {
  return ROLE_LABELS[role] || role
}

export function hasAccess(user, requiredRole) {
  if (!user) return false
  
  if (requiredRole === ROLES.DISPATCHER) {
    return isDispatcher(user)
  }
  
  if (requiredRole === ROLES.MASTER) {
    return isMaster(user) || isDispatcher(user)
  }
  
  return true
}

