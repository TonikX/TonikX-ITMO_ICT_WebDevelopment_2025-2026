import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/layout.css';

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const navItems = [
    { to: '/', label: 'Главная', icon: '📊' },
    { to: '/subjects', label: 'Предметы', icon: '📚' },
    { to: '/classrooms', label: 'Кабинеты', icon: '🚪' },
    { to: '/teachers', label: 'Учителя', icon: '👨‍🏫' },
    { to: '/classes', label: 'Классы', icon: '👥' },
    { to: '/students', label: 'Ученики', icon: '🎓' },
    { to: '/quarters', label: 'Четверти', icon: '📅' },
    { to: '/assignments', label: 'Назначения', icon: '📝' },
    { to: '/schedule', label: 'Расписание', icon: '🕐' },
    { to: '/grades', label: 'Оценки', icon: '⭐' },
  ];

  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="sidebar-header">
          <span className="logo-icon">🏫</span>
          <h1>Школа</h1>
        </div>

        <nav className="sidebar-nav">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `nav-link ${isActive ? 'active' : ''}`
              }
              end={item.to === '/'}
            >
              <span className="nav-icon">{item.icon}</span>
              <span className="nav-label">{item.label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="user-info">
            <span className="user-icon">👤</span>
            <span className="user-name">{user?.username}</span>
          </div>
          <button onClick={handleLogout} className="logout-btn">
            Выйти
          </button>
        </div>
      </aside>

      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}

