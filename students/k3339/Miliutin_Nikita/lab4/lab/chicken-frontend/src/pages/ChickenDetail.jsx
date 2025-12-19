import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { clearToken } from "../utils/token";
import { getChicken } from "../api/chickens";

export default function ChickenDetail() {
  const { chickenId } = useParams();
  const navigate = useNavigate();

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function load() {
    setError("");
    setLoading(true);
    try {
      const ch = await getChicken(chickenId);
      setData(ch);
    } catch (err) {
      if (err?.response?.status === 401) {
        clearToken();
        navigate("/login", { replace: true });
        return;
      }
      if (err?.response?.status === 404) {
        setError("Курица не найдена");
        return;
      }
      const msg =
        err?.response?.data?.detail || err?.message || "Не удалось загрузить курицу";
      setError(typeof msg === "string" ? msg : "Ошибка");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [chickenId]);

  const id = data?.chicken_id ?? chickenId;
  const title = `Курица #${id}`;
  const cageId = data?.cage_id ?? null;

  return (
    <div className="container">
      <div className="card">
        <div className="card-header">
          <div className="stack" style={{ gap: 6 }}>
            <div className="page-title">{title}</div>
            <div className="subtitle">id: {id}</div>
          </div>

          <div className="actions right">
            <button className="btn" onClick={load} disabled={loading}>
              {loading ? "Загрузка..." : "Обновить"}
            </button>
            <Link className="btn ghost" to={cageId ? `/cages/${cageId}` : "/workshops"}>
              ← назад
            </Link>
          </div>
        </div>

        <div className="card-content">
          {loading ? <div className="alert">Загрузка...</div> : null}
          {error ? <div className="alert error">{error}</div> : null}

          {!loading && !error && data ? (
            <>
              <div className="card pad" style={{ boxShadow: "none" }}>
                <div className="card-title" style={{ marginBottom: 10 }}>
                  Информация
                </div>

                <div className="kv">
                  <div><b>breed_id:</b> {data.breed_id}</div>
                  <div><b>cage_id:</b> {String(data.cage_id)}</div>
                  <div><b>weight_kg:</b> {String(data.weight_kg)}</div>
                  <div><b>age_months:</b> {String(data.age_months)}</div>
                  <div><b>eggs_per_month:</b> {String(data.eggs_per_month)}</div>
                </div>
              </div>

              <div className="actions" style={{ marginTop: 12 }}>
                <button
                  className="btn primary"
                  onClick={() =>
                    navigate(`/chickens/${id}/move${cageId ? `?fromCage=${cageId}` : ""}`)
                  }
                >
                  Переместить
                </button>

                {cageId ? (
                  <Link className="btn ghost" to={`/cages/${cageId}`}>
                    Открыть клетку
                  </Link>
                ) : null}
              </div>
            </>
          ) : null}
        </div>
      </div>
    </div>
  );
}
