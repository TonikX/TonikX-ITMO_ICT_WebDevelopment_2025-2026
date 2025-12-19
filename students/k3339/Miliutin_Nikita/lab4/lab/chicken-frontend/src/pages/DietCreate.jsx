import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { clearToken } from "../utils/token";
import { createDiet } from "../api/diets";

export default function DietCreate() {
  const navigate = useNavigate();

  const [dietNo, setDietNo] = useState("");
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function onSubmit(e) {
    e.preventDefault();
    setError("");

    const no = Number(dietNo);
    if (!no || Number.isNaN(no)) return setError("diet_no должен быть числом (>= 1)");
    if (!content.trim()) return setError("Заполни описание (content)");

    setLoading(true);
    try {
      const created = await createDiet({
        diet_no: no,
        content: content.trim(),
      });

      const id = created?.diet_id ?? created?.id;
      navigate(`/diets/${id}`, { replace: true });
    } catch (err) {
      if (err?.response?.status === 401) {
        clearToken();
        navigate("/login", { replace: true });
        return;
      }
      const msg =
        err?.response?.data?.detail || err?.message || "Не удалось создать диету";
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
            <div className="page-title">➕ Добавить диету</div>
            <div className="subtitle">diet_no + content</div>
          </div>

          <div className="actions right">
            <Link className="btn ghost" to="/diets">
              ← к диетам
            </Link>
          </div>
        </div>

        <div className="card-content">
          {error ? <div className="alert error">{error}</div> : null}

          <form className="form" onSubmit={onSubmit}>
            <label>
              Номер диеты (diet_no)
              <input
                className="input"
                value={dietNo}
                onChange={(e) => setDietNo(e.target.value)}
                placeholder="Напр. 1"
                inputMode="numeric"
              />
            </label>

            <label>
              Описание (content)
              <textarea
                className="textarea"
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Что входит в диету..."
                rows={6}
              />
            </label>

            <div className="actions">
              <button className="btn primary" type="submit" disabled={loading}>
                {loading ? "Создаю..." : "Создать"}
              </button>
              <Link className="btn ghost" to="/diets">
                Отмена
              </Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
