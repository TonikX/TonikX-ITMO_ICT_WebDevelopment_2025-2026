import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { clearToken } from "../utils/token";

import { getDiet, deleteDiet } from "../api/diets";
import { getBreeds } from "../api/breeds";
import {
  getBreedDietSeasons,
  upsertBreedDietForSeason,
  deleteBreedDietSeason,
} from "../api/breedDietSeasons";

function field(v) {
  if (v === null || v === undefined || v === "") return "—";
  return String(v);
}

// ⚠️ если у тебя enum Season другой — поменяй тут
const SEASONS = ["WINTER", "SPRING", "SUMMER", "AUTUMN"];

export default function DietDetail() {
  const { dietId } = useParams();
  const navigate = useNavigate();

  const dietIdNum = useMemo(() => Number(dietId), [dietId]);

  const [diet, setDiet] = useState(null);
  const [breeds, setBreeds] = useState([]);
  const [links, setLinks] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [breedId, setBreedId] = useState("");
  const [season, setSeason] = useState(SEASONS[0]);
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const breedNameById = useMemo(() => {
    const m = new Map();
    (breeds ?? []).forEach((b) => {
      const id = b?.breed_id ?? b?.id;
      const name = b?.name ?? `Порода #${id ?? "?"}`;
      if (id != null) m.set(Number(id), name);
    });
    return m;
  }, [breeds]);

  async function load() {
    setError("");
    setLoading(true);
    try {
      const [d, b, l] = await Promise.all([
        getDiet(dietId),
        getBreeds({ limit: 500 }),
        getBreedDietSeasons({ diet_id: dietIdNum, limit: 500 }),
      ]);

      setDiet(d);
      setBreeds(b ?? []);
      setLinks(l ?? []);
    } catch (err) {
      if (err?.response?.status === 401) {
        clearToken();
        navigate("/login", { replace: true });
        return;
      }
      const msg =
        err?.response?.data?.detail || err?.message || "Не удалось загрузить диету";
      setError(typeof msg === "string" ? msg : "Ошибка");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [dietId]);

  const title =
    diet?.diet_no != null ? `Диета №${diet.diet_no}` : `Диета #${diet?.diet_id ?? dietId}`;

  async function onApply() {
    setError("");
    const bId = Number(breedId);
    if (!bId || Number.isNaN(bId)) return setError("Выбери породу");
    if (!season) return setError("Выбери сезон");

    setSaving(true);
    try {
      await upsertBreedDietForSeason(bId, season, dietIdNum);
      await load();
      setBreedId("");
    } catch (err) {
      if (err?.response?.status === 401) {
        clearToken();
        navigate("/login", { replace: true });
        return;
      }
      const msg =
        err?.response?.data?.detail ||
        err?.message ||
        "Не удалось применить диету (проверь season/enum на сервере)";
      setError(typeof msg === "string" ? msg : "Ошибка");
    } finally {
      setSaving(false);
    }
  }

  async function onDeleteLink(bId, s) {
    setError("");
    try {
      await deleteBreedDietSeason(bId, s);
      await load();
    } catch (err) {
      if (err?.response?.status === 401) {
        clearToken();
        navigate("/login", { replace: true });
        return;
      }
      const msg =
        err?.response?.data?.detail || err?.message || "Не удалось удалить привязку";
      setError(typeof msg === "string" ? msg : "Ошибка");
    }
  }

  async function onDeleteDiet() {
    const ok = window.confirm(
      "Удалить диету? Это действие нельзя отменить.\n\n(Если диета где-то назначена, сервер может не дать удалить.)"
    );
    if (!ok) return;

    setDeleting(true);
    setError("");
    try {
      await deleteDiet(dietId);
      navigate("/diets", { replace: true });
    } catch (err) {
      if (err?.response?.status === 401) {
        clearToken();
        navigate("/login", { replace: true });
        return;
      }
      const msg =
        err?.response?.data?.detail || err?.message || "Не удалось удалить диету";
      alert(typeof msg === "string" ? msg : "Ошибка");
    } finally {
      setDeleting(false);
    }
  }

  return (
    <div className="container">
      <div className="card">
        <div className="card-header">
          <div className="stack" style={{ gap: 6 }}>
            <div className="page-title">{title}</div>
            <div className="subtitle">id: {field(diet?.diet_id ?? dietId)}</div>
          </div>

          <div className="actions right">
            <button className="btn" onClick={load} disabled={loading}>
              {loading ? "Загрузка..." : "Обновить"}
            </button>
            <Link className="btn primary" to="/diets/new">
              ➕ Добавить
            </Link>
            <button className="btn danger" onClick={onDeleteDiet} disabled={deleting || loading}>
              {deleting ? "Удаляю..." : "🗑 Удалить"}
            </button>
            <Link className="btn ghost" to="/diets">
              ← к диетам
            </Link>
          </div>
        </div>

        <div className="card-content">
          {loading ? <div className="alert">Загрузка...</div> : null}
          {error ? <div className="alert error">{error}</div> : null}

          {!loading && !error && diet ? (
            <div className="stack">
              <div className="card pad" style={{ boxShadow: "none" }}>
                <div className="card-title" style={{ marginBottom: 10 }}>
                  Описание
                </div>
                <div className="list-meta" style={{ color: "var(--text)" }}>
                  {diet?.content ?? diet?.description ?? "—"}
                </div>
              </div>

              <div className="card pad" style={{ boxShadow: "none" }}>
                <div className="card-title" style={{ marginBottom: 10 }}>
                  Применить диету к породе и сезону
                </div>

                <div className="form-grid">
                  <label>
                    Порода
                    <select
                      className="select"
                      value={breedId}
                      onChange={(e) => setBreedId(e.target.value)}
                    >
                      <option value="">— выбери породу —</option>
                      {breeds.map((b) => {
                        const id = b?.breed_id ?? b?.id;
                        const name = b?.name ?? `Порода #${id ?? "?"}`;
                        return (
                          <option key={id ?? name} value={id}>
                            {name}
                          </option>
                        );
                      })}
                    </select>
                  </label>

                  <label>
                    Сезон
                    <select
                      className="select"
                      value={season}
                      onChange={(e) => setSeason(e.target.value)}
                    >
                      {SEASONS.map((s) => (
                        <option key={s} value={s}>
                          {s}
                        </option>
                      ))}
                    </select>
                    <div className="help">
                      Если сервер ругается 422 — значения Season у тебя другие. Поменяй массив SEASONS вверху файла.
                    </div>
                  </label>
                </div>

                <div className="actions" style={{ marginTop: 12 }}>
                  <button className="btn primary" onClick={onApply} disabled={saving || !breedId}>
                    {saving ? "Сохраняю..." : "Применить"}
                  </button>
                </div>
              </div>

              <div className="card pad" style={{ boxShadow: "none" }}>
                <div className="card-title" style={{ marginBottom: 10 }}>
                  Где эта диета применяется (порода + сезон)
                </div>

                {links.length === 0 ? (
                  <div className="alert">Пока нигде не назначена.</div>
                ) : (
                  <div className="list-grid">
                    {links.map((x, idx) => {
                      const bId = x?.breed_id ?? x?.breed?.breed_id ?? x?.breed?.id;
                      const s = x?.season;
                      const dietAssigned = x?.diet_id ?? x?.diet?.diet_id;

                      return (
                        <div key={`${bId ?? "b"}-${s ?? "s"}-${idx}`} className="list-card">
                          <div className="row wrap" style={{ justifyContent: "space-between" }}>
                            <div>
                              <div className="list-title">
                                Порода: {field(bId)}
                                {bId != null ? ` • ${breedNameById.get(Number(bId)) ?? ""}` : ""}
                              </div>
                              <div className="list-meta">Сезон: {field(s)}</div>
                              <div className="list-meta">diet_id: {field(dietAssigned)}</div>
                            </div>

                            <button className="btn sm danger" onClick={() => onDeleteLink(bId, s)}>
                              Убрать
                            </button>
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
