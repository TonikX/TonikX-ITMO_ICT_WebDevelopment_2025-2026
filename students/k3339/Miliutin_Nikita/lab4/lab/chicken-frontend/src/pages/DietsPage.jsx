import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { clearToken } from "../utils/token";
import { getDiets } from "../api/diets";

function field(v) {
  if (v === null || v === undefined || v === "") return "—";
  return String(v);
}

export default function DietsPage() {
  const navigate = useNavigate();

  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function load() {
    setError("");
    setLoading(true);
    try {
      const res = await getDiets({ limit: 200 });
      setData(res ?? []);
    } catch (err) {
      if (err?.response?.status === 401) {
        clearToken();
        navigate("/login", { replace: true });
        return;
      }
      const msg =
        err?.response?.data?.detail || err?.message || "Не удалось загрузить диеты";
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
            <div className="page-title">🥣 Диеты</div>
            <div className="subtitle">Всего: {data.length}</div>
          </div>

          <div className="actions right">
            <button className="btn" onClick={load} disabled={loading}>
              {loading ? "Загрузка..." : "Обновить"}
            </button>
            <Link className="btn primary" to="/diets/new">
              ➕ Добавить
            </Link>
            <Link className="btn ghost" to="/">
              ← на главную
            </Link>
          </div>
        </div>

        <div className="card-content">
          {error ? <div className="alert error">{error}</div> : null}
          {loading ? <div className="alert">Загрузка...</div> : null}

          {!loading && !error ? (
            data.length === 0 ? (
              <div className="alert">Диет нет.</div>
            ) : (
              <div className="list-grid">
                {data.map((d) => {
                  const id = d?.diet_id ?? d?.id;
                  const title = d?.diet_no != null ? `Диета №${d.diet_no}` : `Диета #${id}`;
                  const content = d?.content ?? d?.description ?? "";

                  return (
                    <Link key={id ?? title} to={`/diets/${id}`} className="list-link">
                      <div className="list-card">
                        <div className="row" style={{ justifyContent: "space-between" }}>
                          <div className="list-title">{title}</div>
                          <span className="badge">id: {field(id)}</span>
                        </div>

                        <div className="list-meta" style={{ marginTop: 8 }}>
                          {content
                            ? content.slice(0, 140) + (content.length > 140 ? "…" : "")
                            : "—"}
                        </div>
                      </div>
                    </Link>
                  );
                })}
              </div>
            )
          ) : null}
        </div>
      </div>
    </div>
  );
}
