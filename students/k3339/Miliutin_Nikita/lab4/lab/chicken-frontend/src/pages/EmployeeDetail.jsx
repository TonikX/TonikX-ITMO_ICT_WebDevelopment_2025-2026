import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { clearToken } from "../utils/token";
import {
  getEmployeeWithAssignments,
  getEmployee,
  assignEmployeeToCage,
  unassignEmployeeFromCage,
} from "../api/employees";
import { getWorkshops, getWorkshopWithCages } from "../api/workshops";
import { getEmployeeDisplayName } from "../utils/employeeNames";

function field(v) {
  if (v === null || v === undefined || v === "") return "—";
  return String(v);
}

function todayYmd() {
  return new Date().toISOString().slice(0, 10); // YYYY-MM-DD
}

export default function EmployeeDetail() {
  const { employeeId } = useParams();
  const navigate = useNavigate();

  const employeeIdNum = useMemo(() => Number(employeeId), [employeeId]);

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [showAssign, setShowAssign] = useState(false);
  const [workshops, setWorkshops] = useState([]);
  const [cages, setCages] = useState([]);
  const [wsId, setWsId] = useState("");
  const [cageId, setCageId] = useState("");
  const [assigning, setAssigning] = useState(false);
  const [loadingCages, setLoadingCages] = useState(false);

  async function load() {
    setError("");
    setLoading(true);
    try {
      try {
        const res = await getEmployeeWithAssignments(employeeId);
        setData(res);
        return;
      } catch {
        // fallback
      }

      const res = await getEmployee(employeeId);
      setData(res);
    } catch (err) {
      if (err?.response?.status === 401) {
        clearToken();
        navigate("/login", { replace: true });
        return;
      }
      if (err?.response?.status === 404) {
        setError("Работник не найден");
        return;
      }
      const msg =
        err?.response?.data?.detail || err?.message || "Не удалось загрузить работника";
      setError(typeof msg === "string" ? msg : "Ошибка");
    } finally {
      setLoading(false);
    }
  }

  async function loadWorkshops() {
    try {
      const res = await getWorkshops();
      setWorkshops(res ?? []);
    } catch {
      setWorkshops([]);
    }
  }

  async function loadCagesForWorkshop(workshopId) {
    if (!workshopId) {
      setCages([]);
      return;
    }
    setLoadingCages(true);
    try {
      const res = await getWorkshopWithCages(workshopId);
      setCages(res?.cages ?? []);
    } catch {
      setCages([]);
    } finally {
      setLoadingCages(false);
    }
  }

  async function onAssign() {
    setError("");
    const targetCageId = Number(cageId);

    if (!wsId) return setError("Выбери цех");
    if (!targetCageId || Number.isNaN(targetCageId)) return setError("Выбери клетку");

    setAssigning(true);
    try {
      await assignEmployeeToCage(employeeIdNum, targetCageId, {
        assigned_from: todayYmd(),
        assigned_to: null,
      });

      await load();

      setShowAssign(false);
      setWsId("");
      setCageId("");
      setCages([]);
    } catch (err) {
      if (err?.response?.status === 401) {
        clearToken();
        navigate("/login", { replace: true });
        return;
      }
      const msg =
        err?.response?.data?.detail || err?.message || "Не удалось назначить на клетку";
      setError(typeof msg === "string" ? msg : "Ошибка");
    } finally {
      setAssigning(false);
    }
  }

  async function onUnassign(targetCageId) {
    setError("");
    try {
      await unassignEmployeeFromCage(employeeIdNum, targetCageId, {
        assigned_to: todayYmd(),
      });
      await load();
    } catch (err) {
      if (err?.response?.status === 401) {
        clearToken();
        navigate("/login", { replace: true });
        return;
      }

      const detail =
        err?.response?.data?.detail || err?.message || "Не удалось завершить назначение";

      const text = typeof detail === "string" ? detail.toLowerCase() : "";
      const looksLikeLast =
        text.includes("послед") || text.includes("last") || text.includes("никого") || text.includes("cannot");

      if (looksLikeLast) {
        alert("Нельзя снять работника с клетки: он последний (в клетке должен остаться хотя бы один).");
        return;
      }

      setError(typeof detail === "string" ? detail : "Ошибка");
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [employeeId]);

  useEffect(() => {
    if (showAssign) loadWorkshops();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [showAssign]);

  useEffect(() => {
    loadCagesForWorkshop(wsId);
    setCageId("");
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [wsId]);

  const id = data?.employee_id ?? data?.id ?? employeeId;
  const title = getEmployeeDisplayName(id);
  const assignments = data?.cage_assignments ?? data?.assignments ?? [];

  return (
    <div className="container">
      <div className="card">
        <div className="card-header">
          <div className="stack" style={{ gap: 6 }}>
            <div className="page-title">{title}</div>
            <div className="subtitle">id: {field(id)}</div>
          </div>

          <div className="actions right">
            <button className="btn" onClick={load} disabled={loading}>
              {loading ? "Загрузка..." : "Обновить"}
            </button>
            <Link className="btn ghost" to="/employees">
              ← к работникам
            </Link>
          </div>
        </div>

        <div className="card-content">
          {loading ? <div className="alert">Загрузка...</div> : null}
          {error ? <div className="alert error">{error}</div> : null}

          {!loading && !error && data ? (
            <div className="stack">
              <div className="card pad" style={{ boxShadow: "none" }}>
                <div className="card-title" style={{ marginBottom: 10 }}>
                  Информация
                </div>
                <div className="kv">
                  <div><b>ФИО:</b> {getEmployeeDisplayName(id)}</div>
                  <div><b>passport:</b> {field(data.passport)}</div>
                  <div><b>contract_no:</b> {field(data.contract_no)}</div>
                  <div><b>salary:</b> {field(data.salary)}</div>
                  <div><b>fire_date:</b> {field(data.fire_date)}</div>
                  <div><b>fire_reason:</b> {field(data.fire_reason)}</div>
                </div>
              </div>

              <div className="card pad" style={{ boxShadow: "none" }}>
                <div className="actions between">
                  <div className="card-title">Назначить на клетку</div>
                  <button className="btn" onClick={() => setShowAssign((v) => !v)}>
                    {showAssign ? "Скрыть" : "Назначить"}
                  </button>
                </div>

                {showAssign ? (
                  <div className="stack" style={{ marginTop: 12 }}>
                    <label>
                      1) Цех
                      <select
                        className="select"
                        value={wsId}
                        onChange={(e) => setWsId(e.target.value)}
                      >
                        <option value="">— выбери цех —</option>
                        {workshops.map((w) => {
                          const wid = w.workshop_id ?? w.id;
                          const t = w.name ?? `Цех #${w.workshop_no ?? wid ?? "?"}`;
                          return (
                            <option key={wid ?? t} value={wid}>
                              {t}
                            </option>
                          );
                        })}
                      </select>
                    </label>

                    <label>
                      2) Клетка
                      <select
                        className="select"
                        value={cageId}
                        onChange={(e) => setCageId(e.target.value)}
                        disabled={!wsId || loadingCages}
                      >
                        <option value="">— выбери клетку —</option>
                        {cages.map((c) => {
                          const cid = c.cage_id ?? c.id;
                          const t = c.name ?? `Клетка #${c.cage_no ?? cid ?? "?"}`;
                          return (
                            <option key={cid ?? t} value={cid}>
                              {t}
                            </option>
                          );
                        })}
                      </select>

                      {loadingCages ? <div className="help">Загрузка клеток...</div> : null}
                    </label>

                    <div className="actions">
                      <button className="btn primary" onClick={onAssign} disabled={assigning || !cageId}>
                        {assigning ? "Назначаю..." : "Назначить"}
                      </button>
                    </div>
                  </div>
                ) : null}
              </div>

              <div className="card pad" style={{ boxShadow: "none" }}>
                <div className="card-title" style={{ marginBottom: 10 }}>
                  Назначения по клеткам
                </div>

                {assignments.length === 0 ? (
                  <div className="alert">Назначений нет.</div>
                ) : (
                  <div className="list-grid">
                    {assignments.map((a, idx) => {
                      const targetCageId = a?.cage_id ?? a?.cage?.cage_id ?? a?.cage?.id;
                      const isActive = !a?.assigned_to;

                      return (
                        <div key={`${targetCageId ?? "c"}-${idx}`} className="list-card">
                          <div className="row wrap" style={{ justifyContent: "space-between" }}>
                            <div>
                              <div className="list-title">cage_id: {field(targetCageId)}</div>
                              {a?.assigned_from ? <div className="list-meta">assigned_from: {field(a.assigned_from)}</div> : null}
                              {a?.assigned_to ? <div className="list-meta">assigned_to: {field(a.assigned_to)}</div> : null}
                            </div>

                            <div className="actions">
                              {targetCageId ? (
                                <Link className="btn sm" to={`/cages/${targetCageId}`}>
                                  Открыть
                                </Link>
                              ) : null}

                              {isActive && targetCageId ? (
                                <button className="btn sm danger" onClick={() => onUnassign(targetCageId)}>
                                  Завершить
                                </button>
                              ) : null}
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
}
