import {
  AppBar,
  Box,
  CssBaseline,
  Divider,
  Drawer,
  IconButton,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
} from '@mui/material';
import {
  Assessment,
  Assignment,
  Dashboard,
  Group,
  Hotel,
  People,
} from '@mui/icons-material';
import MenuIcon from '@mui/icons-material/Menu';
import { useMemo, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';

const drawerWidth = 240;

const navItems = [
  { label: 'Обзор', icon: <Dashboard />, path: '/' },
  { label: 'Номера', icon: <Hotel />, path: '/rooms' },
  { label: 'Клиенты', icon: <People />, path: '/clients' },
  { label: 'Проживания', icon: <Assignment />, path: '/stays' },
  { label: 'Сотрудники', icon: <Group />, path: '/employees' },
  { label: 'Отчёты', icon: <Assessment />, path: '/reports' },
];

interface Props {
  children: React.ReactNode;
}

export function DashboardLayout({ children }: Props) {
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation();

  const drawer = useMemo(
    () => (
      <div>
        <Toolbar>
          <Typography variant="h6" noWrap>
            Hotel Admin
          </Typography>
        </Toolbar>
        <Divider />
        <List>
          {navItems.map((item) => (
            <ListItem key={item.path} disablePadding>
              <ListItemButton
                component={Link}
                to={item.path}
                selected={location.pathname === item.path}
                onClick={() => setMobileOpen(false)}
              >
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.label} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </div>
    ),
    [location.pathname],
  );

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        sx={{ width: { sm: `calc(100% - ${drawerWidth}px)` }, ml: { sm: `${drawerWidth}px` } }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            edge="start"
            onClick={() => setMobileOpen(true)}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div">
            Панель администратора гостиницы
          </Typography>
        </Toolbar>
      </AppBar>
      <Box component="nav" sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}>
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={() => setMobileOpen(false)}
          ModalProps={{ keepMounted: true }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          minHeight: '100vh',
          bgcolor: 'background.default',
        }}
      >
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
}

