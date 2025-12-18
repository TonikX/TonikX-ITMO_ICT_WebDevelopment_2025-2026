import { Navigate } from 'react-router-dom'
import { useAuth } from './AuthContext'
import { CircularProgress, Box } from '@mui/material'

// интерфейс для пропсов компонента RequireAuth
interface RequireAuthProps {
  children: JSX.Element // дочерний компонент, который нужно защитить
}

// компонент-обертка для защищенных маршрутов (требует аутентификации)
export const RequireAuth: React.FC<RequireAuthProps> = ({ children }) => {
  // получаем состояние аутентификации и флаг загрузки из контекста
  const { isAuthenticated, loading } = useAuth()

  // если идет проверка токенов, показываем индикатор загрузки
  if (loading) {
    return (
      // контейнер с центрированным индикатором загрузки
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        {/* круговой индикатор загрузки из MUI */}
        <CircularProgress />
      </Box>
    )
  }

  // если пользователь не аутентифицирован, перенаправляем на страницу входа
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  // если пользователь аутентифицирован, отображаем защищенный контент
  return children
}


