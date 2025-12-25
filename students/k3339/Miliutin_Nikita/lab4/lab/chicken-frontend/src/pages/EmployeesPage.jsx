import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { clearToken } from "../utils/token";
import { getEmployees } from "../api/employees";
import { getEmployeeDisplayName } from "../utils/employeeNames";

function fieldOrDash(v) {
  if (v === null || v === undefined || v === "") return "—";
  return String(v);
}

export default function EmployeesPage() {
  const navigate = useNavigate();

  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function load() {
    setError("");
    setLoading(true);
    try {
      const res = await getEmployees({ limit: 200 });
      setData(res ?? []);
    } catch (err) {
      if (err?.response?.status === 401) {
        clearToken();
        navigate("/login", { replace: true });
        return;
      }
      const msg =
        err?.response?.data?.detail ||
        err?.message ||
        "Не удалось загрузить работников";
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
            <div className="page-title">Работники</div>
            <div className="subtitle">Всего: {data?.length ?? 0}</div>
          </div>

          <div className="actions right">
            <button className="btn" onClick={load} disabled={loading}>
              {loading ? "Загрузка..." : "Обновить"}
            </button>

            <Link className="btn primary" to="/employees/new">
              ➕ Добавить
            </Link>

            <Link className="btn ghost" to="/">
              ← на главную
            </Link>
          </div>
        </div>

        <div className="card-content">
          {loading ? <div className="alert">Загрузка...</div> : null}
          {error ? <div className="alert error">{error}</div> : null}

          {!loading && !error ? (
            data.length === 0 ? (
              <div className="alert">Работников нет.</div>
            ) : (
              <div className="list-grid">
                {data.map((e) => {
                  const id = e?.employee_id ?? e?.id;
                  return (
                    <Link key={id ?? `emp-${Math.random()}`} to={`/employees/${id}`} className="list-link">
                      <div className="list-card">
                        <div className="row wrap" style={{ justifyContent: "space-between" }}>
                          <div>
                            <div className="list-title">{getEmployeeDisplayName(id)}</div>
                            <div className="list-meta">
                              id: {fieldOrDash(id)} • паспорт: {fieldOrDash(e?.passport)} • договор:{" "}
                              {fieldOrDash(e?.contract_no)}
                            </div>
                          </div>

                          <span className="badge">
                            💰 {fieldOrDash(e?.salary)}
                          </span>
                        </div>

                        {e?.fire_date ? (
                          <div className="list-meta" style={{ marginTop: 8 }}>
                            ⚠️ уволен: {fieldOrDash(e.fire_date)}
                          </div>
                        ) : null}
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
