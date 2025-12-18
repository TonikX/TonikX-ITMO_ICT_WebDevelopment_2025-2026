import React, { useState } from 'react'
import { Outlet, useNavigate, useLocation } from 'react-router-dom'
import {
  Box,
  Drawer,
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
  Collapse,
  Avatar,
  Fade,
} from '@mui/material' // импортируем компоненты интерфейса из mui
import {
  Menu as MenuIcon,
  Logout as LogoutIcon,
  Book as BookIcon,
  Inventory as InventoryIcon,
  People as PeopleIcon,
  Assignment as AssignmentIcon,
  Analytics as AnalyticsIcon,
  Assessment as AssessmentIcon,
  Category as CategoryIcon,
  Person as PersonIcon,
  ExpandLess,
  ExpandMore,
  PersonAdd as PersonAddIcon,
  Home as HomeIcon,
} from '@mui/icons-material'
import { useAuth } from '../auth/AuthContext' // импортируем кастомный хук авторизации

const drawerWidth = 280

export const AppLayout: React.FC = () => { // основной layout-компонент приложения, обертка для внутренних страниц
  const [mobileOpen, setMobileOpen] = useState(false)
  const [openBooks, setOpenBooks] = useState(false)
  const [openCopies, setOpenCopies] = useState(false)
  const [openReaders, setOpenReaders] = useState(false)
  const [openIssues, setOpenIssues] = useState(false)
  const [openAnalytics, setOpenAnalytics] = useState(false)
  const [openReports, setOpenReports] = useState(false)
  const [openDictionaries, setOpenDictionaries] = useState(false)

  const navigate = useNavigate() // хук для программной навигации между страницами
  const location = useLocation() // хук для получения информации о текущем url
  const { logout } = useAuth()

  const handleDrawerToggle = () => { // обработчик переключения состояния боковой панели на мобильных
    setMobileOpen(!mobileOpen)
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const isActive = (path: string) => location.pathname === path // функция проверяет, совпадает ли текущий путь с заданным

  const menuItems = [ // массив конфигураций для групп пунктов меню боковой панели
    {
      title: 'Книги',
      icon: <BookIcon />,
      open: openBooks,
      setOpen: setOpenBooks,
      items: [
        { text: 'Каталог книг', path: '/books', icon: <BookIcon /> },
      ],
    },
    {
      title: 'Фонд и экземпляры',
      icon: <InventoryIcon />,
      open: openCopies,
      setOpen: setOpenCopies,
      items: [
        { text: 'Экземпляры книг', path: '/copies', icon: <InventoryIcon /> },
        { text: 'Принять книгу', path: '/accept-book', icon: <HomeIcon /> },
        { text: 'Списать книгу', path: '/writeoff-book', icon: <LogoutIcon /> },
      ],
    },
    {
      title: 'Читатели',
      icon: <PeopleIcon />,
      open: openReaders,
      setOpen: setOpenReaders,
      items: [
        { text: 'Список читателей', path: '/readers', icon: <PeopleIcon /> },
        { text: 'Регистрация читателя', path: '/register-reader', icon: <PersonAddIcon /> },
        { text: 'Деактивация читателей', path: '/deactivate-readers', icon: <PersonIcon /> },
      ],
    },
    {
      title: 'Выдачи',
      icon: <AssignmentIcon />,
      open: openIssues,
      setOpen: setOpenIssues,
      items: [
        { text: 'Список выдач', path: '/issues', icon: <AssignmentIcon /> },
        { text: 'Выдать книгу', path: '/issue-book', icon: <BookIcon /> },
      ],
    },
    {
      title: 'Аналитика',
      icon: <AnalyticsIcon />,
      open: openAnalytics,
      setOpen: setOpenAnalytics,
      items: [
        { text: 'Просроченные выдачи', path: '/analytics/overdue', icon: <AssignmentIcon /> }, // аналитика по просроченным книгам
        { text: 'Редкие книги', path: '/analytics/rare-books', icon: <BookIcon /> }, // аналитика по редким книгам
        { text: 'Статистика по возрасту', path: '/analytics/age', icon: <AnalyticsIcon /> }, // статистика по возрасту читателей
        { text: 'Статистика по образованию', path: '/analytics/education', icon: <AnalyticsIcon /> }, // статистика по образованию читателей
      ],
    },
    {
      title: 'Отчёты',
      icon: <AssessmentIcon />,
      open: openReports,
      setOpen: setOpenReports,
      items: [
        { text: 'Ежемесячный отчёт', path: '/reports/monthly', icon: <AssessmentIcon /> }, // страница с ежемесячным отчётом
      ],
    },
    {
      title: 'Справочники',
      icon: <CategoryIcon />,
      open: openDictionaries,
      setOpen: setOpenDictionaries,
      items: [
        { text: 'Авторы', path: '/authors', icon: <PersonIcon /> }, // справочник авторов
        { text: 'Издательства', path: '/publishers', icon: <CategoryIcon /> }, // справочник издательств
        { text: 'Разделы', path: '/sections', icon: <CategoryIcon /> }, // справочник разделов
        { text: 'Залы', path: '/halls', icon: <HomeIcon /> }, // справочник залов
      ],
    },
  ]

  const drawer = ( // jsx-разметка для боковой панели навигации
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* верхняя часть боковой панели с логотипом и фоном */}
      <Box
        sx={{
          p: 3,
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          background: '#6366f1',
          color: 'white',
          height: '90px',
        }}
      >
        {/* аватар с иконкой книги, создаёт логотип приложения */}
        <Avatar
          sx={{
            width: 56,
            height: 56,
            background: 'rgba(255, 255, 255, 0.2)',
            backdropFilter: 'blur(10px)',
            transition: 'all 0.3s ease-in-out',
            '&:hover': {
              transform: 'scale(1.1) rotate(5deg)',
              boxShadow: '0 8px 16px rgba(0, 0, 0, 0.2)',
            },
          }}
        >
          <BookIcon sx={{ fontSize: 32 }} />
        </Avatar>
      </Box>

      {/* основная область меню, может прокручиваться по вертикали */}
      <Box sx={{ flex: 1, overflowY: 'auto', py: 2 }}>
        <List>
          {menuItems.map((menu, index) => (
            <React.Fragment key={index}>
              <ListItem disablePadding sx={{ px: 2 }}>
                <ListItemButton
                  onClick={() => menu.setOpen(!menu.open)}
                  sx={{
                    borderRadius: 2,
                    mb: 0.5,
                    '&:hover': {
                      bgcolor: 'rgba(99, 102, 241, 0.08)',
                    },
                  }}
                >
                  <ListItemIcon sx={{ color: '#6366f1', minWidth: 40 }}>
                    {menu.icon}
                  </ListItemIcon>
                  <ListItemText
                    primary={menu.title}
                    primaryTypographyProps={{
                      fontWeight: 600,
                      fontSize: '0.9375rem',
                    }}
                  />
                  {menu.open ? <ExpandLess /> : <ExpandMore />}
                </ListItemButton>
              </ListItem>
              <Collapse in={menu.open} timeout="auto" unmountOnExit>
                <List component="div" disablePadding> {/* вложенный список подпунктов */}
                  {menu.items.map((item, idx) => ( // проходим по пунктам внутри группы
                    <Fade
                      in={menu.open}
                      key={idx}
                      timeout={300 + idx * 50}
                    >
                      <ListItemButton
                        sx={{
                          pl: 6,
                          pr: 2,
                          py: 1,
                          mx: 2,
                          mb: 0.5,
                          borderRadius: 2,
                          bgcolor: isActive(item.path)
                            ? 'rgba(99, 102, 241, 0.12)'
                            : 'transparent',
                          borderLeft: isActive(item.path)
                            ? '3px solid #6366f1'
                            : '3px solid transparent',
                          '&:hover': {
                            bgcolor: 'rgba(99, 102, 241, 0.08)',
                          },
                          transition: 'all 0.2s ease-in-out',
                        }}
                        onClick={() => {
                          navigate(item.path)
                          if (mobileOpen) setMobileOpen(false)
                        }}
                      >
                        <ListItemText
                          primary={item.text}
                          primaryTypographyProps={{
                            fontSize: '0.875rem',
                            fontWeight: isActive(item.path) ? 600 : 400,
                            color: isActive(item.path) ? '#6366f1' : 'text.secondary',
                          }}
                        />
                      </ListItemButton>
                    </Fade>
                  ))}
                </List>
              </Collapse>
            </React.Fragment>
          ))}
        </List>
      </Box>

      <Divider />
      <List sx={{ px: 2, py: 2 }}> {/* нижний блок меню с пунктами профиля и выхода */}
        <ListItem disablePadding sx={{ mb: 1 }}>
          <ListItemButton
            onClick={() => navigate('/profile')}
            sx={{
              borderRadius: 2,
              bgcolor: isActive('/profile') ? 'rgba(99, 102, 241, 0.12)' : 'transparent',
              '&:hover': {
                bgcolor: 'rgba(99, 102, 241, 0.08)',
              },
            }}
          >
            <ListItemIcon sx={{ color: '#6366f1', minWidth: 40 }}> {/* иконка пользователя слева */}
              <PersonIcon />
            </ListItemIcon>
            <ListItemText
              primary="Профиль"
              primaryTypographyProps={{
                fontWeight: isActive('/profile') ? 600 : 400,
                fontSize: '0.9375rem',
              }}
            />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding sx={{ mb: 1 }}> {/* пункт списка для регистрации сотрудника */}
          <ListItemButton
            onClick={() => navigate('/register-staff')} // по клику переходим на страницу регистрации сотрудника
            sx={{
              borderRadius: 2, // скругляем углы
              bgcolor: isActive('/register-staff') ? 'rgba(99, 102, 241, 0.12)' : 'transparent', //
              '&:hover': {
                bgcolor: 'rgba(99, 102, 241, 0.08)',
              },
            }}
          >
            <ListItemIcon sx={{ color: '#6366f1', minWidth: 40 }}>
              <PersonAddIcon />
            </ListItemIcon>
            <ListItemText
              primary="Регистрация сотрудника"
              primaryTypographyProps={{
                fontWeight: isActive('/register-staff') ? 600 : 400,
                fontSize: '0.9375rem',
              }}
            />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding> {/* пункт списка для выхода пользователя */}
          <ListItemButton
            onClick={handleLogout}
            sx={{
              borderRadius: 2,
              color: 'error.main',
              '&:hover': {
                bgcolor: 'rgba(239, 68, 68, 0.08)',
              },
            }}
          >
            <ListItemIcon sx={{ color: 'error.main', minWidth: 40 }}>
              <LogoutIcon />
            </ListItemIcon>
            <ListItemText
              primary="Выход"
              primaryTypographyProps={{
                fontWeight: 600,
                fontSize: '0.9375rem',
              }}
            />
          </ListItemButton>
        </ListItem>
      </List>
    </Box>
  ) // конец разметки боковой панели

  return ( // основной jsx-рендер layout-а
    <Box sx={{ display: 'flex', minHeight: '100vh' }}> {/* корневой контейнер, располагающий боковую панель и контент рядом */}
      {/* верхняя панель - фиксированная позиция поверх контента */}
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
          background: '#6366f1',
          color: 'white',
          boxShadow: 'none',
          borderRadius: 0,
        }}
        elevation={0}
      >
        <Toolbar sx={{ minHeight: '90px !important', height: '90px' }}> {/* тулбар с заданной высотой, совпадает с высотой верхнего блока drawer */}
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ 
              mr: 2,
              display: { sm: 'none' },
            }}
          >
            <MenuIcon /> {/* иконка  для открытия меню */}
          </IconButton>
          <Typography 
            variant="body1" 
            noWrap 
            component="div" 
            sx={{ 
              flexGrow: 1,
              fontWeight: 500,
              fontSize: '1.5rem',
            }}
          >
            Система управления библиотекой {/* текст заголовка в appbar */}
          </Typography>
        </Toolbar>
      </AppBar>
      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }} // контейнер для боковой панели навигации
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true, // оставляем компонент смонтированным для лучшей производительности на мобильных
          }}
          sx={{
            display: { xs: 'block', sm: 'none' }, // показываем этот drawer только на маленьких экранах
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer} {/* вставляем ранее описанную разметку drawer внутрь временного drawer */}
        </Drawer>
        <Drawer
          variant="permanent" // постоянный drawer для больших экранов
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          {drawer} {/* та же разметка боковой панели для десктопной версии */}
        </Drawer>
      </Box>
      {/* основная область контента - с отступом сверху под верхнюю панель */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          minHeight: '100vh',
          mt: '104px',
        }}
      >
        <Fade in timeout={300}>
          <Box>
            <Outlet />
          </Box>
        </Fade>
      </Box>
    </Box>
  )
}
