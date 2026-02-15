<template>
  <div>
    <div style="display:flex; align-items:center; gap:10px;">
      <h2 style="margin:0;">Отчёты</h2>
      <button class="btn" @click="goBack">Назад</button>
      <button class="btn" @click="reloadCurrent" :disabled="loading">
        {{ loading ? "Загружаю..." : "Обновить" }}
      </button>
    </div>

    <div v-if="error" style="margin-top:10px; color:red; white-space:pre-line;">
      {{ error }}
    </div>

    <div class="tabs" style="margin-top:12px;">
      <button class="tab" :class="{active: tab==='reader_books'}" @click="switchTab('reader_books')">Книги у читателя</button>
      <button class="tab" :class="{active: tab==='overdue'}" @click="switchTab('overdue')">Просрочки</button>
      <button class="tab" :class="{active: tab==='rare'}" @click="switchTab('rare')">Редкие книги (на руках)</button>
      <button class="tab" :class="{active: tab==='under20'}" @click="switchTab('under20')">Читатели до 20</button>
      <button class="tab" :class="{active: tab==='education'}" @click="switchTab('education')">Статистика образования</button>
      <button class="tab" :class="{active: tab==='monthly'}" @click="switchTab('monthly')">Месячный отчёт</button>
    </div>

    <div v-if="loading" style="margin-top:10px;">Загружаю...</div>

    <!-- 1) ReaderBooks -->
    <div v-else-if="tab==='reader_books'" class="card" style="margin-top:12px;">
      <div style="display:flex; justify-content:space-between; gap:10px; align-items:flex-end; flex-wrap:wrap;">
        <div>
          <div class="label">Reader ID</div>
          <input class="input" type="number" min="1" v-model.number="readerId" placeholder="например 19" />
        </div>
        <button class="btn" @click="loadReaderBooks" :disabled="!readerId">Показать</button>
      </div>

      <div style="margin-top:10px;">
        <b>Активные выдачи:</b> {{ readerBooks.active_loans?.length ?? 0 }}
      </div>

      <table v-if="(readerBooks.active_loans||[]).length" class="table" style="margin-top:10px;">
        <thead>
          <tr>
            <th>#</th>
            <th>Книга</th>
            <th>Автор(ы)</th>
            <th>Зал</th>
            <th>Выдано</th>
            <th>qty</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(x, i) in readerBooks.active_loans" :key="x.loan_id">
            <td>{{ i+1 }}</td>
            <td>
              <router-link class="link" :to="`/books/${x.book.id}`">{{ x.book.title }}</router-link>
            </td>
            <td>{{ (x.book.authors||[]).map(a=>a.full_name).join(', ') || "—" }}</td>
            <td>
              <router-link class="link" :to="`/halls/${x.hall.id}`">{{ x.hall.name }}</router-link>
            </td>
            <td>{{ x.assigned_at }}</td>
            <td>{{ x.qty }}</td>
          </tr>
        </tbody>
      </table>

      <div v-else style="margin-top:10px;">Нет активных выдач.</div>
    </div>

    <!-- 2) Overdue -->
    <div v-else-if="tab==='overdue'" class="card" style="margin-top:12px;">
      <div style="display:flex; gap:10px; align-items:flex-end; flex-wrap:wrap;">
        <div>
          <div class="label">Порог (дней)</div>
          <input class="input" type="number" min="1" v-model.number="overdueDays" />
        </div>
        <button class="btn" @click="loadOverdue">Показать</button>
      </div>

      <div style="margin-top:10px;">
        <b>Найдено:</b> {{ overdue.results?.length ?? 0 }}
        <span v-if="overdue.cutoff"> (cutoff: {{ overdue.cutoff }})</span>
      </div>

      <table v-if="(overdue.results||[]).length" class="table" style="margin-top:10px;">
        <thead>
          <tr>
            <th>#</th>
            <th>Читатель</th>
            <th>Книга</th>
            <th>Зал</th>
            <th>Выдано</th>
            <th>qty</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(x, i) in overdue.results" :key="x.loan_id">
            <td>{{ i+1 }}</td>
            <td><router-link class="link" :to="`/readers/${x.reader.id}`">{{ x.reader.full_name }}</router-link></td>
            <td><router-link class="link" :to="`/books/${x.book.id}`">{{ x.book.title }}</router-link></td>
            <td><router-link class="link" :to="`/halls/${x.hall.id}`">{{ x.hall.name }}</router-link></td>
            <td>{{ x.assigned_at }}</td>
            <td>{{ x.qty }}</td>
          </tr>
        </tbody>
      </table>

      <div v-else style="margin-top:10px;">Просрочек нет.</div>
    </div>

    <!-- 3) Rare books loans -->
    <div v-else-if="tab==='rare'" class="card" style="margin-top:12px;">
      <button class="btn" @click="loadRare">Показать</button>

      <div style="margin-top:10px;">
        <b>Найдено:</b> {{ rare.results?.length ?? 0 }}
      </div>

      <table v-if="(rare.results||[]).length" class="table" style="margin-top:10px;">
        <thead>
          <tr>
            <th>#</th>
            <th>Читатель</th>
            <th>Книга</th>
            <th>Зал</th>
            <th>Выдано</th>
            <th>qty</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(x, i) in rare.results" :key="x.loan_id">
            <td>{{ i+1 }}</td>
            <td><router-link class="link" :to="`/readers/${x.reader.id}`">{{ x.reader.full_name }}</router-link></td>
            <td><router-link class="link" :to="`/books/${x.book.id}`">{{ x.book.title }}</router-link></td>
            <td><router-link class="link" :to="`/halls/${x.hall.id}`">{{ x.hall.name }}</router-link></td>
            <td>{{ x.assigned_at }}</td>
            <td>{{ x.qty }}</td>
          </tr>
        </tbody>
      </table>

      <div v-else style="margin-top:10px;">Нет активных выдач редких книг.</div>
    </div>

    <!-- 4) Under 20 -->
    <div v-else-if="tab==='under20'" class="card" style="margin-top:12px;">
      <button class="btn" @click="loadUnder20">Посчитать</button>
      <div style="margin-top:10px; font-size:18px;">
        <b>Читателей младше 20:</b> {{ under20.under_20_count ?? "—" }}
      </div>
    </div>

    <!-- 5) Education stats -->
    <div v-else-if="tab==='education'" class="card" style="margin-top:12px;">
      <button class="btn" @click="loadEducation">Показать</button>

      <div style="margin-top:10px;">
        <div><b>Всего читателей:</b> {{ education.total ?? 0 }}</div>
        <div><b>Учёная степень:</b> {{ education.degree_count ?? 0 }} ({{ education.degree_percent ?? 0 }}%)</div>
      </div>

      <table v-if="educationRows.length" class="table" style="margin-top:10px;">
        <thead>
          <tr>
            <th>Уровень</th>
            <th>Кол-во</th>
            <th>%</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in educationRows" :key="r.lvl">
            <td>{{ r.lvl }}</td>
            <td>{{ r.cnt }}</td>
            <td>{{ r.pct }}</td>
          </tr>
        </tbody>
      </table>

      <div v-else style="margin-top:10px;">Нет данных.</div>
    </div>

    <div v-else-if="tab==='monthly'" class="card" style="margin-top:12px;">
      <div style="display:flex; gap:10px; align-items:flex-end; flex-wrap:wrap;">
        <div>
          <div class="label">Год</div>
          <input class="input" type="number" min="2000" v-model.number="monthYear" />
        </div>
        <div>
          <div class="label">Месяц</div>
          <input class="input" type="number" min="1" max="12" v-model.number="monthNum" />
        </div>
        <button class="btn" @click="loadMonthly">Показать</button>
      </div>

      <div v-if="monthly.period" style="margin-top:10px;">
        <b>Период:</b> {{ monthly.period.from }} — {{ monthly.period.to }}
      </div>

      <div v-if="monthly.enrollments_month" style="margin-top:10px;">
        <b>Записались за месяц:</b> {{ monthly.enrollments_month.total ?? 0 }}
      </div>

      <details v-if="(monthly.enrollments_month?.by_hall||[]).length" style="margin-top:10px;">
        <summary style="cursor:pointer;">Записались по залам</summary>
        <table class="table" style="margin-top:10px;">
          <thead><tr><th>Зал</th><th>Кол-во</th></tr></thead>
          <tbody>
            <tr v-for="h in monthly.enrollments_month.by_hall" :key="h.hall_id">
              <td>Зал {{ h.hall_number }}: {{ h.name }}</td>
              <td>{{ h.enroll_count }}</td>
            </tr>
          </tbody>
        </table>
      </details>

      <details v-if="(monthly.daily||[]).length" style="margin-top:10px;">
        <summary style="cursor:pointer;">Помесячно по дням (итог по библиотеке)</summary>
        <table class="table" style="margin-top:10px;">
          <thead><tr><th>Дата</th><th>Экземпляров</th><th>Читателей</th></tr></thead>
          <tbody>
            <tr v-for="d in monthly.daily" :key="d.date">
              <td>{{ d.date }}</td>
              <td>{{ d.total?.books_copies ?? 0 }}</td>
              <td>{{ d.total?.readers ?? 0 }}</td>
            </tr>
          </tbody>
        </table>
      </details>

      <div v-if="monthlyErrorHint" style="margin-top:10px; opacity:.85;">
        {{ monthlyErrorHint }}
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { http } from "@/api/http";

const router = useRouter();
function goBack(){ router.push("/"); } 


const tab = ref("monthly");
const loading = ref(false);
const error = ref("");

function parseDrfError(e) {
  const data = e.response?.data;
  if (!data) return `Ошибка (${e.response?.status ?? "?"}). Проверь сервер/эндпоинты.`;
  if (typeof data === "object") {
    const lines = [];
    for (const k in data) {
      const v = data[k];
      lines.push(`${k}: ${Array.isArray(v) ? v.join(", ") : String(v)}`);
    }
    return lines.join("\n");
  }
  return String(data);
}

function switchTab(t){
  tab.value = t;
  error.value = "";
}

async function reloadCurrent(){
  if (tab.value === "reader_books") return loadReaderBooks();
  if (tab.value === "overdue") return loadOverdue();
  if (tab.value === "rare") return loadRare();
  if (tab.value === "under20") return loadUnder20();
  if (tab.value === "education") return loadEducation();
  if (tab.value === "monthly") return loadMonthly();
}


const readerId = ref(null);
const readerBooks = ref({ reader_id: null, active_loans: [] });

async function loadReaderBooks(){
  if (!readerId.value) return;
  error.value = "";
  loading.value = true;
  try{
    const res = await http.get("api/analytics/readers/<int:reader_id>/books/");
    readerBooks.value = res.data;
  }catch(e){
    error.value = parseDrfError(e);
  }finally{
    loading.value = false;
  }
}

// -------- overdue --------
const overdueDays = ref(30);
const overdue = ref({ cutoff: null, results: [] });

async function loadOverdue(){
  error.value = "";
  loading.value = true;
  try{
    const res = await http.get("api/analytics/loans/overdue/");
    overdue.value = res.data;
  }catch(e){
    error.value = parseDrfError(e);
  }finally{
    loading.value = false;
  }
}

const rare = ref({ results: [] });

async function loadRare(){
  error.value = "";
  loading.value = true;
  try{
    const res = await http.get("api/analytics/loans/rare/");
    rare.value = res.data;
  }catch(e){
    error.value = parseDrfError(e);
  }finally{
    loading.value = false;
  }
}

const under20 = ref({ under_20_count: null });

async function loadUnder20(){
  error.value = "";
  loading.value = true;
  try{
    const res = await http.get("api/analytics/readers/under20/");
    under20.value = res.data;
  }catch(e){
    error.value = parseDrfError(e);
  }finally{
    loading.value = false;
  }
}

const education = ref({});
const educationRows = computed(() => {
  const edu = education.value?.education || {};
  const pct = education.value?.education_percent || {};
  return Object.keys(edu).map(lvl => ({
    lvl,
    cnt: edu[lvl],
    pct: (pct[lvl] ?? 0) + "%",
  }));
});

async function loadEducation(){
  error.value = "";
  loading.value = true;
  try{
    const res = await http.get("api/analytics/readers/education-stats/");
    education.value = res.data;
  }catch(e){
    error.value = parseDrfError(e);
  }finally{
    loading.value = false;
  }
}

function todayParts(){
  const d = new Date();
  return { y: d.getFullYear(), m: d.getMonth()+1 };
}
const { y, m } = todayParts();
const monthYear = ref(y);
const monthNum = ref(m);
const monthly = ref({});
const monthlyErrorHint = ref("");

async function loadMonthly(){
  error.value = "";
  monthlyErrorHint.value = "";
  loading.value = true;
  try{
    const res = await http.get("api/analytics/monthly-report/");
    monthly.value = res.data;
  }catch(e){
    error.value = parseDrfError(e);
    monthlyErrorHint.value = "Если 404 — проверь, что эндпоинт MonthlyReportAPIView подключён в urls.py и путь совпадает с API.monthly().";
  }finally{
    loading.value = false;
  }
}

</script>

<style scoped>
.card { border: 1px solid #ddd; padding: 12px; margin-top: 10px; }
.label { font-weight: 600; margin-bottom: 6px; }
.input { padding: 10px; border: 1px solid teal; min-width: 240px; }
.btn { padding: 8px 12px; border: 1px solid teal; background: white; cursor: pointer; }
.btn:disabled { opacity: .6; cursor: not-allowed; }
.link { text-decoration: none; display: inline-block; }
.table { border-collapse: collapse; width: 100%; }
.table th, .table td { border: 1px solid #ddd; padding: 8px; vertical-align: top; }
.table th { background: #f6f6f6; }
.tabs { display:flex; gap:8px; flex-wrap:wrap; }
.tab { padding: 8px 10px; border: 1px solid #ddd; background: #fff; cursor:pointer; }
.tab.active { border-color: teal; font-weight: 700; }
.tab.danger { border-color: #c00; }
.btn.danger { border-color: #c00; }
</style>