import { Component, ReactNode } from 'react'
import { Container, Paper, Typography, Button, Box } from '@mui/material'
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline'

// интерфейс для пропсов компонента ErrorBoundary
interface Props {
  children: ReactNode // дочерние компоненты, которые нужно защитить от ошибок
}

// интерфейс для состояния компонента ErrorBoundary
interface State {
  hasError: boolean // флаг наличия ошибки
  error: Error | null // объект ошибки или null
}

// компонент-класс для перехвата ошибок
export class ErrorBoundary extends Component<Props, State> {
  // начальное состояние компонента
  public state: State = {
    hasError: false,
    error: null,
  }

  // статический метод, вызываемый при возникновении ошибки в дочерних компонентах
  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }


  // обработчик клика на кнопку перезагрузки страницы
  private handleReload = () => {
    window.location.reload()
  }

  // метод рендеринга компонента
  public render() {
    // если произошла ошибка, отображаем UI ошибки
    if (this.state.hasError) {
      return (
        <Container maxWidth="md" sx={{ mt: 4 }}>
          {/* бумажная карточка */}
          <Paper sx={{ p: 4, textAlign: 'center' }}>
            <ErrorOutlineIcon color="error" sx={{ fontSize: 64, mb: 2 }} />
            <Typography variant="h4" gutterBottom>
              Что-то пошло не так
            </Typography>
            <Typography variant="body1" color="text.secondary" paragraph>
              Произошла ошибка при загрузке страницы.
            </Typography>
            {this.state.error && (
              <Box sx={{ my: 2, p: 2, bgcolor: 'grey.100', borderRadius: 1 }}>
                <Typography variant="body2" color="error" sx={{ fontFamily: 'monospace' }}>
                  {this.state.error.toString()}
                </Typography>
              </Box>
            )}
            {/* контейнер с кнопками действий */}
            <Box sx={{ mt: 3, display: 'flex', gap: 2, justifyContent: 'center' }}>
              <Button variant="contained" onClick={this.handleReload}>
                Перезагрузить страницу
              </Button>
              <Button variant="outlined" onClick={() => window.history.back()}>
                Вернуться назад
              </Button>
            </Box>
          </Paper>
        </Container>
      )
    }

    // если ошибки нет, отображаем дочерние компоненты как обычно
    return this.props.children
  }
}

