import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { register } from "../api/auth";

export default function Register() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function onSubmit(e) {
    e.preventDefault();
    setError("");

    if (password !== password2) {
      setError("Пароли не совпадают");
      return;
    }

    setLoading(true);
    try {
      await register(username, password);
      navigate("/login");
    } catch (err) {
      const msg =
        err?.response?.data?.detail || err?.message || "Не удалось зарегистрироваться";
      setError(typeof msg === "string" ? msg : "Ошибка регистрации");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-wrap">
      <div className="card pad auth-card">
        <div className="stack" style={{ gap: 14 }}>
          <div className="stack" style={{ gap: 6 }}>
            <h2 className="auth-title">Регистрация</h2>
            <div className="auth-sub">Создай аккаунт сотрудника</div>
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
                autoComplete="new-password"
                type="password"
                required
              />
            </label>

            <label>
              Повтори пароль
              <input
                className="input"
                value={password2}
                onChange={(e) => setPassword2(e.target.value)}
                autoComplete="new-password"
                type="password"
                required
              />
            </label>

            {error ? <div className="alert error">{error}</div> : null}

            <div className="actions between">
              <button className="btn primary" type="submit" disabled={loading}>
                {loading ? "Создаём..." : "Зарегистрироваться"}
              </button>

              <Link className="btn ghost" to="/login">
                ← Войти
              </Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
