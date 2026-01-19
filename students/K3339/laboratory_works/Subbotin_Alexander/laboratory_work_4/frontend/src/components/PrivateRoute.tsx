import { ReactNode } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '@/store';

interface PrivateRouteProps {
  children: ReactNode;
}

export function PrivateRoute({ children }: PrivateRouteProps) {
  const location = useLocation();
  const { isAuthenticated, token } = useAuthStore();

  // Проверяем и токен, и состояние аутентификации
  if (!isAuthenticated && !token) {
    // Сохраняем текущий URL для редиректа после логина
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <>{children}</>;
}
