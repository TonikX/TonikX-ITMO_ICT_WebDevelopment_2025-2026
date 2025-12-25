import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { login } from "../api/auth";
import { setToken } from "../utils/token";

export default function Login() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const data = await login(username, password);
      setToken(data.access_token);
      navigate("/");
    } catch (err) {
      const msg =
        err?.response?.data?.detail ||
        err?.message ||
        "Не удалось войти. Проверь логин/пароль.";
      setError(typeof msg === "string" ? msg : "Ошибка входа");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-wrap">
      <div className="card pad auth-card">
        <div className="stack" style={{ gap: 14 }}>
          <div className="stack" style={{ gap: 6 }}>
            <h2 className="auth-title">Вход</h2>
            <div className="auth-sub">Войди в систему</div>
          </div>

          <form className="form" onSubmit={onSubmit}>
            <label>
              Логин
              <input
                className="input"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                autoComplete="username"
                required
              />
            </label>

            <label>
              Пароль
              <input
                className="input"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="current-password"
                type="password"
                required
              />
            </label>

            {error ? <div className="alert error">{error}</div> : null}

            <div className="actions between">
              <button className="btn primary" type="submit" disabled={loading}>
                {loading ? "Входим..." : "Войти"}
              </button>

              <Link className="btn ghost" to="/register">
                Регистрация →
              </Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
