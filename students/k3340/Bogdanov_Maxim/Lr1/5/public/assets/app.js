// Простая утилита для селекторов
const $ = (s) => document.querySelector(s);

const form = $("#grade-form");
const subjectEl = $("#subject");
const gradeEl = $("#grade");
const hintEl = $("#hint");
const tbody = $("#grades-body");

// ------- Рендер таблицы -------
function renderTable(data) {
    // data: { [subject]: { grades: number[], updated: string } }
    const subjects = Object.keys(data).sort((a,b)=>a.localeCompare(b, "ru"));
    if (subjects.length === 0) {
        tbody.innerHTML = `<tr><td colspan="3"><em>Пока пусто. Добавьте первую оценку.</em></td></tr>`;
        return;
    }
    const rows = subjects.map(subj => {
        const rec = data[subj] || { grades: [], updated: null };
        const grades = (rec.grades || []).join(", ");
        const updated = rec.updated ? new Date(rec.updated).toLocaleString() : "—";
        return `<tr>
      <td>${escapeHTML(subj)}</td>
      <td>${escapeHTML(grades)}</td>
      <td>${escapeHTML(updated)}</td>
    </tr>`;
    });
    tbody.innerHTML = rows.join("");
}

function escapeHTML(s){
    return String(s)
        .replaceAll("&","&amp;").replaceAll("<","&lt;")
        .replaceAll(">","&gt;").replaceAll('"',"&quot;").replaceAll("'","&#39;");
}

// ------- API -------
async function apiGetGrades(){
    const res = await fetch("/api/grades", { headers: { "Accept": "application/json" }, cache: "no-store" });
    if (!res.ok) throw new Error("Не удалось загрузить данные");
    const json = await res.json();
    return json.data || {};
}

async function apiPostGrade(subject, grade){
    const res = await fetch("/api/grades", {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify({ subject, grade })
    });
    const json = await res.json().catch(()=> ({}));
    if (!res.ok) {
        throw new Error(json?.error || "Ошибка сохранения");
    }
    return json;
}

// ------- Клиентская валидация (дополняет серверную) -------
function validate(subject, gradeStr){
    const s = subject.trim();
    if (!s) return "Дисциплина не должна быть пустой";
    if ([...s].length > 100) return "Слишком длинное название (макс 100)";
    if (!/^\d+$/.test(gradeStr.trim())) return "Оценка должна быть числом";
    const g = Number(gradeStr);
    if (g < 2 || g > 5) return "Оценка должна быть в диапазоне 2–5";
    return null;
}

// ------- Submit -------
form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const subject = subjectEl.value;
    const gradeStr = gradeEl.value;

    const err = validate(subject, gradeStr);
    if (err) {
        hintEl.textContent = err;
        hintEl.style.color = "var(--err)";
        return;
    }
    hintEl.textContent = "Сохраняем…";
    hintEl.style.color = "var(--muted)";

    try{
        await apiPostGrade(subject, Number(gradeStr));
        subjectEl.value = "";
        gradeEl.value = "";
        hintEl.textContent = "Готово!";
        hintEl.style.color = "var(--ok)";
        const data = await apiGetGrades();
        renderTable(data);
    }catch(ex){
        hintEl.textContent = ex.message || "Ошибка";
        hintEl.style.color = "var(--err)";
    }
});

// ------- Инициализация -------
(async function init(){
    try{
        const data = await apiGetGrades();
        renderTable(data);
    }catch{
        tbody.innerHTML = `<tr><td colspan="3"><em>Не удалось загрузить данные</em></td></tr>`;
    }
})();
