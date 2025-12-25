import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { getWorkshopWithCages } from "../api/workshops";
import { getCageWithChickens } from "../api/cages";
import { clearToken } from "../utils/token";

export default function WorkshopDetail() {
  const { workshopId } = useParams();
  const navigate = useNavigate();

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function load() {
    setError("");
    setLoading(true);

    try {
      // 1) Загружаем цех + список клеток (обычно без кур)
      const res = await getWorkshopWithCages(workshopId);

      // 2) Для каждой клетки подтягиваем её кур и считаем chickens.length
      const cages = res?.cages ?? [];

      const cagesWithCounts = await Promise.all(
        cages.map(async (c) => {
          const cageId = c.cage_id ?? c.id;
          if (!cageId) return { ...c, chicken_count: 0 };

          try {
            const cageFull = await getCageWithChickens(cageId);
            const count = (cageFull?.chickens ?? []).length;
            return { ...c, chicken_count: count };
          } catch {
            return { ...c, chicken_count: 0 };
          }
        })
      );

      setData({ ...res, cages: cagesWithCounts });
    } catch (err) {
      if (err?.response?.status === 401) {
        clearToken();
        navigate("/login", { replace: true });
        return;
      }

      const msg =
        err?.response?.data?.detail || err?.message || "Не удалось загрузить цех";
      setError(typeof msg === "string" ? msg : "Ошибка");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [workshopId]);

  const workshopName =
    data?.name ?? `Цех #${data?.workshop_no ?? data?.workshop_id ?? workshopId}`;

  const workshopIdShown = data?.workshop_id ?? workshopId;

  return (
    <div className="container">
      <div className="card">
        <div className="card-header">
          <div className="stack" style={{ gap: 6 }}>
            <div className="page-title">{workshopName}</div>
            <div className="subtitle">id: {workshopIdShown}</div>
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
              <div className="row" style={{ marginBottom: 10 }}>
                <div className="card-title">Клетки</div>
              </div>

              {!data?.cages || data.cages.length === 0 ? (
                <div className="alert">Клеток нет.</div>
              ) : (
                <div className="list-grid">
                  {data.cages.map((c) => {
                    const cageId = c.cage_id ?? c.id;
                    const cageTitle = c.name ?? `Клетка #${c.cage_no ?? cageId ?? "?"}`;

                    return (
                      <Link key={cageId ?? cageTitle} to={`/cages/${cageId}`} className="list-link">
                        <div className="list-card">
                          <div className="row" style={{ justifyContent: "space-between" }}>
                            <div className="list-title">{cageTitle}</div>
                            <span className="badge">
                              🐔 {c.chicken_count ?? 0}
                            </span>
                          </div>

                          <div className="list-meta">
                            id: {cageId ?? "—"}
                            {c.cage_no != null ? ` • № ${c.cage_no}` : ""}
                          </div>
                        </div>
                      </Link>
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
