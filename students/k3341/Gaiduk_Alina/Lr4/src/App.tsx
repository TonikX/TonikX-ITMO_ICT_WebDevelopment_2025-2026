import { AppRoutes } from './routes'
import { ErrorBoundary } from './components/ErrorBoundary'

// Основной компонент приложения
function App() {
  return (
    // ErrorBoundary - компонент для перехвата ошибок в дочерних компонентах
    <ErrorBoundary>
      {/* AppRoutes - компонент с определением всех маршрутов приложения */}
      <AppRoutes />
    </ErrorBoundary>
  )
}

// Экспортируем компонент App как экспорт по умолчанию
export default App


