import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { clearToken } from "../utils/token";
import { getMe, updateMe } from "../api/auth";

export default function Profile() {
  const navigate = useNavigate();

  const [me, setMe] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const [newUsername, setNewUsername] = useState("");
  const [newPassword, setNewPassword] = useState("");

  async function loadMe() {
    setError("");
    setLoading(true);
    try {
      const data = await getMe();
      setMe(data);
      setNewUsername(data?.username ?? "");
    } catch (err) {
      if (err?.response?.status === 401) {
        clearToken();
        navigate("/login", { replace: true });
        return;
      }
      const msg =
        err?.response?.data?.detail || err?.message || "Не удалось загрузить профиль";
      setError(typeof msg === "string" ? msg : "Ошибка профиля");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadMe();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function onSave(e) {
    e.preventDefault();
    setError("");
    setSaving(true);

    try {
      const payload = {};
      if (newUsername && newUsername !== me?.username) payload.username = newUsername;
      if (newPassword) payload.password = newPassword;

      if (Object.keys(payload).length === 0) {
        setError("Нечего сохранять (не было изменений)");
        return;
      }

      const updated = await updateMe(payload);
      setMe(updated);
      setNewPassword("");
      alert("Сохранено ✅");
    } catch (err) {
      const msg =
        err?.response?.data?.detail || err?.message || "Не удалось сохранить изменения";
      setError(typeof msg === "string" ? msg : "Ошибка сохранения");
    } finally {
      setSaving(false);
    }
  }

  function onLogout() {
    clearToken();
    navigate("/login");
  }

  return (
    <div className="container">
      <div className="card">
        <div className="card-header">
          <div className="stack" style={{ gap: 6 }}>
            <div className="page-title">Профиль</div>
            <div className="subtitle">Учётные данные пользователя</div>
          </div>

          <div className="actions right">
            <button className="btn" onClick={loadMe} disabled={loading || saving}>
              Обновить
            </button>
            <button className="btn danger" onClick={onLogout}>
              Выйти
            </button>
            <Link className="btn ghost" to="/">
              ← На панель
            </Link>
          </div>
        </div>

        <div className="card-content">
          {loading ? <div className="alert">Загрузка...</div> : null}
          {error ? <div className="alert error">{error}</div> : null}

          {!loading && me ? (
            <div className="card pad" style={{ boxShadow: "none" }}>
              <div className="card-title" style={{ marginBottom: 10 }}>
                Информация
              </div>
              <div className="kv">
                <div>
                  <b>ID:</b> {me.user_id ?? "—"}
                </div>
                <div>
                  <b>Username:</b> {me.username ?? "—"}
                </div>
                <div>
                  <b>Role:</b> {me.role ?? "—"}
                </div>
              </div>
            </div>
          ) : null}

          <div className="divider" />

          <form className="form" onSubmit={onSave}>
            <div className="card-title">Изменить данные</div>

            <div className="form-grid">
              <label>
                Новый username
                <input
                  className="input"
                  value={newUsername}
                  onChange={(e) => setNewUsername(e.target.value)}
                  autoComplete="username"
                />
              </label>

              <label>
                Новый пароль
                <input
                  className="input"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  autoComplete="new-password"
                  type="password"
                  placeholder="Оставь пустым, если не меняешь"
                />
              </label>
            </div>

            <div className="actions">
              <button className="btn primary" type="submit" disabled={saving}>
                {saving ? "Сохраняю..." : "Сохранить"}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
