import { Link, useNavigate } from 'react-router-dom';
import { Plane, User, LogOut, Menu, Shield } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { useAuthStore } from '@/store';

export function Header() {
  const navigate = useNavigate();
  const { user, isAuthenticated, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center">
        <div className="mr-4 flex">
          <Link to="/" className="mr-6 flex items-center space-x-2">
            <Plane className="h-6 w-6" />
            <span className="font-bold">Hokkaido Tours</span>
          </Link>
          <nav className="hidden md:flex items-center space-x-6 text-sm font-medium">
            <Link
              to="/tours"
              className="transition-colors hover:text-foreground/80 text-foreground/60"
            >
              Туры
            </Link>
            {isAuthenticated && (
              <Link
                to="/reservations"
                className="transition-colors hover:text-foreground/80 text-foreground/60"
              >
                Мои бронирования
              </Link>
            )}
            {user?.is_admin && (
              <Link
                to="/admin/reservations"
                className="transition-colors hover:text-foreground/80 text-foreground/60"
              >
                Админ-панель
              </Link>
            )}
          </nav>
        </div>
        <div className="flex flex-1 items-center justify-end space-x-2">
          {isAuthenticated ? (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                  <Avatar className="h-8 w-8">
                    <AvatarFallback>
                      {user?.username?.charAt(0).toUpperCase() || 'U'}
                    </AvatarFallback>
                  </Avatar>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-56" align="end" forceMount>
                <DropdownMenuLabel className="font-normal">
                  <div className="flex flex-col space-y-1">
                    <p className="text-sm font-medium leading-none">{user?.username}</p>
                    <p className="text-xs leading-none text-muted-foreground">
                      {user?.email}
                    </p>
                  </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={() => navigate('/profile')}>
                  <User className="mr-2 h-4 w-4" />
                  <span>Профиль</span>
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => navigate('/reservations')}>
                  <Menu className="mr-2 h-4 w-4" />
                  <span>Мои бронирования</span>
                </DropdownMenuItem>
                {user?.is_admin && (
                  <DropdownMenuItem onClick={() => navigate('/admin/reservations')}>
                    <Shield className="mr-2 h-4 w-4" />
                    <span>Админ-панель</span>
                  </DropdownMenuItem>
                )}
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={handleLogout}>
                  <LogOut className="mr-2 h-4 w-4" />
                  <span>Выйти</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          ) : (
            <div className="flex items-center space-x-2">
              <Button variant="ghost" onClick={() => navigate('/login')}>
                Войти
              </Button>
              <Button onClick={() => navigate('/register')}>
                Регистрация
              </Button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
