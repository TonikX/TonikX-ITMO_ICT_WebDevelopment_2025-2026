import { createTheme } from '@mui/material/styles'

// Основная тема приложения - цвета, шрифты, стили компонентов
const theme = createTheme({
  // Палитра цветов приложения
  palette: {
    mode: 'light', // Светлая тема
    // Основной цвет (primary) - используется для основных действий и акцентов
    primary: {
      main: '#6366f1', // Индиго - основной оттенок
      light: '#818cf8', // Светлый оттенок
      dark: '#4f46e5', // Темный оттенок
      contrastText: '#ffffff', // Цвет текста для контраста с основным цветом
    },
    // Вторичный цвет (secondary) - используется для дополнительных действий
    secondary: {
      main: '#ec4899', // Розовый - основной оттенок
      light: '#f472b6', // Светлый оттенок
      dark: '#db2777', // Темный оттенок
      contrastText: '#ffffff', // Цвет текста для контраста с вторичным цветом
    },
    // Цвет успеха (для успешных операций)
    success: {
      main: '#10b981', // Зеленый - основной оттенок
      light: '#34d399', // Светлый оттенок
      dark: '#059669', // Темный оттенок
    },
    // Цвет ошибки (для ошибок и предупреждений об опасных действиях)
    error: {
      main: '#ef4444', // Красный - основной оттенок
      light: '#f87171', // Светлый оттенок
      dark: '#dc2626', // Темный оттенок
    },
    // Цвет предупреждения (для предупреждений)
    warning: {
      main: '#f59e0b', // Оранжевый - основной оттенок
      light: '#fbbf24', // Светлый оттенок
      dark: '#d97706', // Темный оттенок
    },
    // Цвет информации (для информационных сообщений)
    info: {
      main: '#3b82f6', // Синий - основной оттенок
      light: '#60a5fa', // Светлый оттенок
      dark: '#2563eb', // Темный оттенок
    },
    // Цвета фона
    background: {
      default: '#f8fafc', // Цвет фона по умолчанию (светло-серый)
      paper: '#ffffff', // Цвет фона для карточек и панелей (белый)
    },
    // Цвета текста
    text: {
      primary: '#0f172a', // Основной цвет текста (темно-синий)
      secondary: '#64748b', // Вторичный цвет текста (серый)
    },
  },
  // Настройки типографики (шрифты, размеры, веса)
  typography: {
    // Семейство шрифтов (приоритет: Inter, затем Roboto, затем системные)
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    // Стили для заголовка первого уровня (H1)
    h1: {
      fontSize: '2.5rem', // Размер шрифта 2.5rem
      fontWeight: 700, // Жирный шрифт
      letterSpacing: '-0.02em', // Уменьшенный межбуквенный интервал
    },
    // Стили для заголовка второго уровня (H2)
    h2: {
      fontSize: '2rem', // Размер шрифта 2rem
      fontWeight: 700, // Жирный шрифт
      letterSpacing: '-0.01em', // Уменьшенный межбуквенный интервал
    },
    // Стили для заголовка третьего уровня (H3)
    h3: {
      fontSize: '1.75rem', // Размер шрифта 1.75rem
      fontWeight: 600, // Полужирный шрифт
      letterSpacing: '-0.01em', // Уменьшенный межбуквенный интервал
    },
    // Стили для заголовка четвертого уровня (H4)
    h4: {
      fontSize: '1.5rem', // Размер шрифта 1.5rem
      fontWeight: 600, // Полужирный шрифт
      letterSpacing: '-0.01em', // Уменьшенный межбуквенный интервал
    },
    // Стили для заголовка пятого уровня (H5)
    h5: {
      fontSize: '1.25rem', // Размер шрифта 1.25rem
      fontWeight: 600, // Полужирный шрифт
    },
    // Стили для заголовка шестого уровня (H6)
    h6: {
      fontSize: '1rem', // Размер шрифта 1rem
      fontWeight: 600, // Полужирный шрифт
    },
    // Стили для текста кнопок
    button: {
      textTransform: 'none', // Без преобразования текста в верхний регистр
      fontWeight: 600, // Полужирный шрифт
    },
  },
  // Настройки формы элементов (скругление углов)
  shape: {
    borderRadius: 12, // Скругление углов по умолчанию (12px)
  },
  // Массив теней для различных уровней elevation (0-24)
  shadows: [
    'none', // Уровень 0 - без тени
    '0 1px 2px 0 rgb(0 0 0 / 0.05)', // Уровень 1 - очень легкая тень
    '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)', // Уровень 2 - легкая тень
    '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)', // Уровень 3 - средняя тень
    '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)', // Уровень 4 - заметная тень
    '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)', // Уровень 5 - выраженная тень
    '0 25px 50px -12px rgb(0 0 0 / 0.25)', // Уровень 6+ - сильная тень для модальных окон
    '0 25px 50px -12px rgb(0 0 0 / 0.25)',
    '0 25px 50px -12px rgb(0 0 0 / 0.25)',
    '0 25px 50px -12px rgb(0 0 0 / 0.25)',
    '0 25px 50px -12px rgb(0 0 0 / 0.25)',
    '0 25px 50px -12px rgb(0 0 0 / 0.25)',
    '0 25px 50px -12px rgb(0 0 0 / 0.25)',
    '0 25px 50px -12px rgb(0 0 0 / 0.25)',
    '0 25px 50px -12px rgb(0 0 0 / 0.25)',
    '0 25px 50px -12px rgb(0 0 0 / 0.25)',
    '0 25px 50px -12px rgb(0 0 0 / 0.25)',
    '0 25px 50px -12px rgb(0 0 0 / 0.25)',
    '0 25px 50px -12px rgb(0 0 0 / 0.25)',
    '0 25px 50px -12px rgb(0 0 0 / 0.25)',
    '0 25px 50px -12px rgb(0 0 0 / 0.25)',
    '0 25px 50px -12px rgb(0 0 0 / 0.25)',
    '0 25px 50px -12px rgb(0 0 0 / 0.25)',
    '0 25px 50px -12px rgb(0 0 0 / 0.25)',
    '0 25px 50px -12px rgb(0 0 0 / 0.25)',
  ],
  components: {
    // Стили для кнопок
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 10, // Скругление углов
          padding: '10px 24px', // Внутренние отступы
          fontSize: '0.9375rem', // Размер шрифта
          boxShadow: 'none', // Без тени по умолчанию
          transition: 'all 0.2s ease-in-out', // Плавная анимация
          '&:hover': {
            boxShadow: '0 4px 12px rgba(99, 102, 241, 0.3)', // Тень при наведении
            transform: 'translateY(-1px)', // Легкий подъем
          },
        },
        contained: {
          // Градиентный фон для основных кнопок
          background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
          '&:hover': {
            // Более темный градиент при наведении
            background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)',
          },
        },
      },
    },
    // Стили для карточек и панелей
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 16, // Скругление углов
          boxShadow: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)', // Легкая тень
        },
        elevation1: {
          // Легкая тень для первого уровня
          boxShadow: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
        },
        elevation2: {
          // Средняя тень для второго уровня
          boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
        },
        elevation3: {
          // Более выраженная тень для третьего уровня
          boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
        },
      },
    },
    // Стили для карточек - с эффектом подъема при наведении
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 16, // Скругление углов
          boxShadow: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)', // Легкая тень
          transition: 'all 0.3s ease-in-out', // Плавная анимация
          '&:hover': {
            boxShadow: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)', // Усиленная тень
            transform: 'translateY(-4px)', // Подъем карточки
          },
        },
      },
    },
    // Стили для полей ввода
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 10, // Скругление углов
            transition: 'all 0.2s ease-in-out', // Плавная анимация
            '&:hover': {
              // Фиолетовая рамка при наведении
              '& .MuiOutlinedInput-notchedOutline': {
                borderColor: '#6366f1',
              },
            },
            '&.Mui-focused': {
              // Более толстая рамка при фокусе
              '& .MuiOutlinedInput-notchedOutline': {
                borderWidth: 2,
              },
            },
          },
        },
      },
    },
    // Стили для меток (чипсов)
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 8, // Скругление углов
          fontWeight: 500, // Средняя жирность шрифта
        },
      },
    },
    // Стили для боковой панели
    MuiDrawer: {
      styleOverrides: {
        paper: {
          borderRadius: 0, // Без скругления
          borderRight: 'none', // Без правой границы
          boxShadow: '4px 0 24px rgba(0, 0, 0, 0.06)', // Тень справа
        },
      },
    },
    // Стили для верхней панели (AppBar)
    MuiAppBar: {
      styleOverrides: {
        root: {
          boxShadow: 'none', // Без тени для плоского вида
          borderRadius: 0, // Без скругления углов
        },
      },
    },
    // Стили для контейнера - боковые отступы
    MuiContainer: {
      styleOverrides: {
        root: {
          paddingLeft: '24px', // Отступ слева 24px
          paddingRight: '24px', // Отступ справа 24px
        },
      },
    },
  },
})

// Экспортируем тему для использования в приложении
export default theme

