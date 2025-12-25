import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { getCageWithChickens } from "../api/cages";
import { clearToken } from "../utils/token";

export default function CageDetail() {
  const { cageId } = useParams();
  const navigate = useNavigate();

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function load() {
    setError("");
    setLoading(true);
    try {
      const res = await getCageWithChickens(cageId);
      setData(res);
    } catch (err) {
      if (err?.response?.status === 401) {
        clearToken();
        navigate("/login", { replace: true });
        return;
      }
      const msg =
        err?.response?.data?.detail || err?.message || "Не удалось загрузить клетку";
      setError(typeof msg === "string" ? msg : "Ошибка");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [cageId]);

  const title = data?.name ?? `Клетка #${data?.cage_no ?? data?.cage_id ?? cageId}`;
  const chickens = data?.chickens ?? [];
  const cageIdShown = data?.cage_id ?? cageId;

  return (
    <div className="container">
      <div className="card">
        <div className="card-header">
          <div className="stack" style={{ gap: 6 }}>
            <div className="page-title">{title}</div>
            <div className="subtitle">
              id: {cageIdShown}
              {data?.cage_no != null ? ` • № ${data.cage_no}` : ""}
            </div>
          </div>

          <div className="actions right">
            <button className="btn" onClick={load} disabled={loading}>
              {loading ? "Загрузка..." : "Обновить"}
            </button>
            <Link className="btn ghost" to="/workshops">
              ← к цехам
            </Link>
          </div>
        </div>

        <div className="card-content">
          {error ? <div className="alert error">{error}</div> : null}
          {loading ? <div className="alert">Загрузка...</div> : null}

          {!loading && !error ? (
            <>
              <div className="row" style={{ marginBottom: 12 }}>
                <span className="badge">🐔 Кур: {chickens.length}</span>
              </div>

              <div className="card-title" style={{ marginBottom: 10 }}>
                Куры
              </div>

              {chickens.length === 0 ? (
                <div className="alert">В клетке нет кур.</div>
              ) : (
                <div className="list-grid">
                  {chickens.map((ch) => {
                    const id = ch.chicken_id ?? ch.id;
                    const name = ch.name ?? `Курица #${id ?? "?"}`;

                    return (
                      <div key={id ?? name} className="list-card">
                        <div className="row wrap" style={{ justifyContent: "space-between" }}>
                          <Link className="list-link" to={`/chickens/${id}`}>
                            <div className="list-title">{name}</div>
                            <div className="list-meta">id: {id ?? "—"}</div>
                          </Link>

                          <button
                            className="btn sm"
                            onClick={() =>
                              navigate(`/chickens/${id}/move?fromCage=${cageIdShown}`)
                            }
                          >
                            Переместить
                          </button>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </>
          ) : null}
        </div>
      </div>
    </div>
  );
}
