import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getWorkshops } from "../api/workshops";
import { clearToken } from "../utils/token";

export default function Workshops() {
  const navigate = useNavigate();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function load() {
    setError("");
    setLoading(true);
    try {
      const data = await getWorkshops({ countChickens: true });
      setItems(Array.isArray(data) ? data : []);
    } catch (err) {
      if (err?.response?.status === 401) {
        clearToken();
        navigate("/login", { replace: true });
        return;
      }
      const msg =
        err?.response?.data?.detail || err?.message || "Не удалось загрузить цеха";
      setError(typeof msg === "string" ? msg : "Ошибка");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="container">
      <div className="card">
        <div className="card-header">
          <div className="stack" style={{ gap: 6 }}>
            <div className="page-title">Цеха</div>
            <div className="subtitle">Список цехов и количество кур в каждом</div>
          </div>

          <div className="actions right">
            <button className="btn" onClick={load} disabled={loading}>
              {loading ? "Загрузка..." : "Обновить"}
            </button>
            <Link className="btn ghost" to="/">
              ← На панель
            </Link>
          </div>
        </div>

        <div className="card-content">
          {error ? <div className="alert error">{error}</div> : null}

          {!loading && !error && items.length === 0 ? (
            <div className="alert">Цехов нет.</div>
          ) : null}

          <div className="list-grid">
            {items.map((w) => {
              const id = w.workshop_id ?? w.id;
              const title = w.name ?? w.title ?? `Цех #${id ?? "?"}`;

              return (
                <Link key={id ?? title} to={`/workshops/${id}`} className="list-link">
                  <div className="list-card">
                    <div className="list-title">{title}</div>

                    <div className="list-meta">
                      id: {id ?? "—"}
                      {w.workshop_no != null ? ` • № ${w.workshop_no}` : ""}
                    </div>

                    <div className="list-meta" style={{ marginTop: 8 }}>
                      🐔 Кур в цехе: <b>{w.chicken_count ?? 0}</b>
                    </div>
                  </div>
                </Link>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
