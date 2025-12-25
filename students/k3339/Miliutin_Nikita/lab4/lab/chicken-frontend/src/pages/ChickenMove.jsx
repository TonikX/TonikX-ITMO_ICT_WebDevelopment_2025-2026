import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useParams, useSearchParams } from "react-router-dom";
import { clearToken } from "../utils/token";
import { getWorkshops, getWorkshopWithCages } from "../api/workshops";
import { moveChicken } from "../api/chickens";

export default function ChickenMove() {
  const { chickenId } = useParams();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const fromCage = searchParams.get("fromCage");
  const fromCageId = fromCage ? Number(fromCage) : null;

  const [workshops, setWorkshops] = useState([]);
  const [cages, setCages] = useState([]);

  const [selectedWorkshopId, setSelectedWorkshopId] = useState("");
  const [selectedCageId, setSelectedCageId] = useState("");

  const [loading, setLoading] = useState(true);
  const [loadingCages, setLoadingCages] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const chickenIdNum = useMemo(() => Number(chickenId), [chickenId]);

  async function loadWorkshops() {
    setError("");
    setLoading(true);
    try {
      const res = await getWorkshops();
      setWorkshops(res ?? []);
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

  async function loadCagesForWorkshop(wsId) {
    if (!wsId) {
      setCages([]);
      return;
    }

    setError("");
    setLoadingCages(true);
    try {
      const res = await getWorkshopWithCages(wsId);
      setCages(res?.cages ?? []);
    } catch (err) {
      if (err?.response?.status === 401) {
        clearToken();
        navigate("/login", { replace: true });
        return;
      }
      const msg =
        err?.response?.data?.detail || err?.message || "Не удалось загрузить клетки";
      setError(typeof msg === "string" ? msg : "Ошибка");
      setCages([]);
    } finally {
      setLoadingCages(false);
    }
  }

  async function submit() {
    setError("");
    const target = Number(selectedCageId);

    if (!target || Number.isNaN(target)) {
      setError("Выбери клетку назначения");
      return;
    }
    if (fromCageId != null && target === fromCageId) {
      setError("Курица уже в этой клетке");
      return;
    }

    setSaving(true);
    try {
      await moveChicken(chickenIdNum, { to_cage_id: target });
      navigate(`/cages/${target}`, { replace: true });
    } catch (err) {
      if (err?.response?.status === 401) {
        clearToken();
        navigate("/login", { replace: true });
        return;
      }
      const msg =
        err?.response?.data?.detail || err?.message || "Не удалось переместить курицу";
      setError(typeof msg === "string" ? msg : "Ошибка");
    } finally {
      setSaving(false);
    }
  }

  useEffect(() => {
    loadWorkshops();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    loadCagesForWorkshop(selectedWorkshopId);
    setSelectedCageId("");
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedWorkshopId]);

  const backTo = fromCageId != null ? `/cages/${fromCageId}` : "/workshops";

  return (
    <div className="container">
      <div className="card">
        <div className="card-header">
          <div className="stack" style={{ gap: 6 }}>
            <div className="page-title">Перемещение курицы</div>
            <div className="subtitle">
              Курица id: {chickenId}
              {fromCageId != null ? ` • из клетки: ${fromCageId}` : ""}
            </div>
          </div>

          <div className="actions right">
            <Link className="btn ghost" to={backTo}>
              ← назад
            </Link>
          </div>
        </div>

        <div className="card-content">
          {loading ? <div className="alert">Загрузка...</div> : null}
          {error ? <div className="alert error">{error}</div> : null}

          {!loading ? (
            <div className="stack" style={{ gap: 12 }}>
              <div className="card pad" style={{ boxShadow: "none" }}>
                <div className="card-title" style={{ marginBottom: 10 }}>
                  1) Выбери цех
                </div>

                <select
                  className="select"
                  value={selectedWorkshopId}
                  onChange={(e) => setSelectedWorkshopId(e.target.value)}
                >
                  <option value="">— выбери цех —</option>
                  {workshops.map((w) => {
                    const id = w.workshop_id ?? w.id;
                    const title = w.name ?? `Цех #${w.workshop_no ?? id ?? "?"}`;
                    return (
                      <option key={id ?? title} value={id}>
                        {title}
                      </option>
                    );
                  })}
                </select>
              </div>

              <div className="card pad" style={{ boxShadow: "none" }}>
                <div className="card-title" style={{ marginBottom: 10 }}>
                  2) Выбери клетку
                </div>

                {loadingCages ? <div className="alert">Загрузка клеток...</div> : null}

                <select
                  className="select"
                  value={selectedCageId}
                  onChange={(e) => setSelectedCageId(e.target.value)}
                  disabled={!selectedWorkshopId || loadingCages}
                >
                  <option value="">— выбери клетку —</option>
                  {cages.map((c) => {
                    const id = c.cage_id ?? c.id;
                    const title = c.name ?? `Клетка #${c.cage_no ?? id ?? "?"}`;
                    return (
                      <option key={id ?? title} value={id}>
                        {title}
                      </option>
                    );
                  })}
                </select>

                <div className="actions" style={{ marginTop: 12 }}>
                  <button className="btn primary" onClick={submit} disabled={saving || !selectedCageId}>
                    {saving ? "Перемещаю..." : "Переместить"}
                  </button>
                </div>
              </div>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
}
