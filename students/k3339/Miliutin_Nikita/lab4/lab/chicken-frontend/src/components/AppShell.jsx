import { Link, useLocation, useNavigate } from "react-router-dom";
import { clearToken } from "../utils/token";

export default function AppShell({ children, hideTopActions = false }) {
  const navigate = useNavigate();
  const location = useLocation();

  function onLogout() {
    clearToken();
    navigate("/login");
  }

  // на логине/регистрации обычно не надо показывать кнопки
  const isAuthPage =
    location.pathname === "/login" || location.pathname === "/register";

  const shouldShow = !hideTopActions && !isAuthPage;

  return (
    <div className="app-shell">
      {shouldShow ? (
        <div className="top-actions">
          <Link to="/profile" className="icon-btn" title="Профиль" aria-label="Профиль">
            👤
          </Link>
          <button
            onClick={onLogout}
            className="icon-btn danger"
            title="Выйти"
            aria-label="Выйти"
          >
            🚪
          </button>
        </div>
      ) : null}

      {children}
    </div>
  );
}
