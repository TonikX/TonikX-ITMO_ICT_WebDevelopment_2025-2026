import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { CssBaseline, ThemeProvider } from '@mui/material'
import App from './App'
import { AuthProvider } from './auth/AuthContext'
import theme from './theme/theme'
import './index.css'

// Точка входа в приложение - монтирование React приложения в DOM
ReactDOM.createRoot(document.getElementById('root')!).render(
  // React.StrictMode - режим строгого соответствия для выявления проблем
  <React.StrictMode>
    {/* ThemeProvider - провайдер темы Material-UI для всего приложения */}
    <ThemeProvider theme={theme}>
      {/* BrowserRouter - провайдер маршрутизации (HTML5 History API) */}
      <BrowserRouter>
        {/* AuthProvider - провайдер контекста аутентификации */}
        <AuthProvider>
          {/* CssBaseline - базовые стили Material-UI для единообразного отображения */}
          <CssBaseline />
          {/* Основной компонент приложения */}
          <App />
        </AuthProvider>
      </BrowserRouter>
    </ThemeProvider>
  </React.StrictMode>,
)


