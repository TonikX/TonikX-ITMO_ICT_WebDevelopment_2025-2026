import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { clearToken } from "../utils/token";
import { createEmployee } from "../api/employees";

export default function EmployeeCreate() {
  const navigate = useNavigate();

  const [passport, setPassport] = useState("");
  const [contractNo, setContractNo] = useState("");
  const [salary, setSalary] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function onSubmit(e) {
    e.preventDefault();
    setError("");

    if (!passport.trim()) return setError("Заполни паспорт");
    if (!contractNo.trim()) return setError("Заполни номер договора");
    if (salary === "" || Number.isNaN(Number(salary))) return setError("Заполни зарплату числом");

    setLoading(true);
    try {
      const created = await createEmployee({
        passport: passport.trim(),
        contract_no: contractNo.trim(),
        salary: Number(salary),
        fire_date: null,
        fire_reason: null,
      });

      const id = created?.employee_id ?? created?.id;
      navigate(`/employees/${id}`, { replace: true });
    } catch (err) {
      if (err?.response?.status === 401) {
        clearToken();
        navigate("/login", { replace: true });
        return;
      }
      const msg =
        err?.response?.data?.detail || err?.message || "Не удалось создать работника";
      setError(typeof msg === "string" ? msg : "Ошибка");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container">
      <div className="card">
        <div className="card-header">
          <div className="stack" style={{ gap: 6 }}>
            <div className="page-title">➕ Добавить работника</div>
            <div className="subtitle">Паспорт, договор, зарплата</div>
          </div>

          <div className="actions right">
            <Link className="btn ghost" to="/employees">
              ← к работникам
            </Link>
          </div>
        </div>

        <div className="card-content">
          {error ? <div className="alert error">{error}</div> : null}

          <form className="form" onSubmit={onSubmit}>
            <div className="form-grid">
              <label>
                Паспорт
                <input
                  className="input"
                  value={passport}
                  onChange={(e) => setPassport(e.target.value)}
                  placeholder="Напр. 1234 567890"
                />
              </label>

              <label>
                Номер договора
                <input
                  className="input"
                  value={contractNo}
                  onChange={(e) => setContractNo(e.target.value)}
                  placeholder="Напр. DOG-2025-001"
                />
              </label>
            </div>

            <label>
              Зарплата
              <input
                className="input"
                value={salary}
                onChange={(e) => setSalary(e.target.value)}
                placeholder="Напр. 65000"
                inputMode="decimal"
              />
            </label>

            <div className="actions">
              <button className="btn primary" type="submit" disabled={loading}>
                {loading ? "Создаю..." : "Создать"}
              </button>
              <Link className="btn ghost" to="/employees">
                Отмена
              </Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
