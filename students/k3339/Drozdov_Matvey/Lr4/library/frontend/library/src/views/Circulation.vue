<template>
  <div>
    <div>
      <h2 style="margin:0;">Выдача / Возврат</h2>
      <button class="btn" @click="goHome">На главную</button>
    </div>

    <div v-if="error" style="color:red; white-space:pre-line; margin: 10px 0;">
      {{ error }}
    </div>

    <div class="card">
      <h3 style="margin-top:0;">Выдать книгу</h3>

      <div class="row">
        <div class="col">
          <label class="label">Читатель (поиск)</label>
          <input class="input" v-model="readerQuery" @input="searchReaders" placeholder="ФИО/паспорт/телефон/билет..." />
          <div v-if="readerResults.length" class="dropdown">
            <div
              v-for="r in readerResults"
              :key="r.id"
              class="dropdown-item"
              @click="selectReader(r)"
            >
              <b>{{ r.full_name }}</b>
              <span style="opacity:.7"> · билет: {{ r.active_ticket_number || "—" }}</span>
            </div>
          </div>

          <div v-if="selectedReader" class="hint">
            Выбран: <b>{{ selectedReader.full_name }}</b>,
            билет: <b>{{ selectedReader.active_ticket_number || "—" }}</b>
          </div>
        </div>

        <div class="col">
          <label class="label">Книга (поиск)</label>
          <input class="input" v-model="bookQuery" @input="searchBooks" placeholder="Название/шифр/автор..." />
          <div v-if="bookResults.length" class="dropdown">
            <div
              v-for="b in bookResults"
              :key="b.id"
              class="dropdown-item"
              @click="selectBook(b)"
            >
              <b>{{ b.title }}</b>
              <span style="opacity:.7"> · шифр: {{ b.current_code || "—" }}</span>
            </div>
          </div>

          <div v-if="selectedBook" class="hint">
            Выбрана: <b>{{ selectedBook.title }}</b>,
            шифр: <b>{{ selectedBook.current_code || "—" }}</b>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col">
          <label class="label">Зал</label>
          <select class="input" v-model.number="hallId" @change="recalcAvailability">
            <option :value="null">— выбрать зал —</option>
            <option v-for="h in halls" :key="h.id" :value="h.id">
              Зал {{ h.hall_number }}: {{ h.name || "—" }}
            </option>
          </select>
        </div>

        <div class="col">
          <label class="label">Кол-во</label>
          <input class="input" type="number" min="1" v-model.number="qty" @input="recalcAvailability" />
        </div>

        <div class="col">
          <label class="label">Дата выдачи</label>
          <input class="input" type="date" v-model="assignedAt" @change="recalcAvailability" />
        </div>
      </div>

      <div class="hint" v-if="availabilityText">
        {{ availabilityText }}
      </div>

      <button class="btn" @click="createLoan" :disabled="busyCreate || !canCreate">
        {{ busyCreate ? "Выдаю..." : "Выдать" }}
      </button>
    </div>

    <div class="card" style="margin-top:12px;">
      <div style="display:flex; justify-content:space-between; gap:10px; align-items:center;">
        <h3 style="margin:0;">Активные выдачи</h3>
        <button class="btn" @click="loadLoans" :disabled="busyLoans">
          {{ busyLoans ? "..." : "Обновить" }}
        </button>
      </div>

      <table v-if="activeLoans.length" class="table" style="margin-top:10px;">
        <thead>
          <tr>
            <th>#</th>
            <th>Читатель</th>
            <th>Книга</th>
            <th>Зал</th>
            <th>Выдано</th>
            <th>qty</th>
            <th style="width:140px;">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(l, i) in activeLoans" :key="l.id">
            <td>{{ i + 1 }}</td>
            <td>
              <router-link class="link" :to="`/readers/${l.reader}`">Reader #{{ l.reader }}</router-link>
            </td>
            <td>
              <router-link class="link" :to="`/books/${l.book}`">Book #{{ l.book }}</router-link>
            </td>
            <td>
              <router-link class="link" :to="`/halls/${l.hall}`">Hall #{{ l.hall }}</router-link>
            </td>
            <td>{{ l.assigned_at }}</td>
            <td>{{ l.qty }}</td>
            <td>
              <button class="btn" @click="returnLoan(l)" :disabled="busyReturnId === l.id">
                {{ busyReturnId === l.id ? "..." : "Принять" }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-else style="margin-top:10px;">
        Активных выдач нет.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { http } from "@/api/http";
import { useRouter } from "vue-router";

const router = useRouter();
const error = ref("");

const halls = ref([]);

const readerQuery = ref("");
const readerResults = ref([]);
const selectedReader = ref(null);

const bookQuery = ref("");
const bookResults = ref([]);
const selectedBook = ref(null);

const hallId = ref(null);
const qty = ref(1);
const assignedAt = ref(today());

const availabilityText = ref("");
const canCreate = computed(() => {
  return selectedReader.value && selectedBook.value && hallId.value && qty.value >= 1;
});

const busyCreate = ref(false);

const loans = ref([]);
const busyLoans = ref(false);
const busyReturnId = ref(null);

function goHome() {
  router.push("/");
}

function today() {
  const d = new Date();
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, "0");
  const dd = String(d.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

function parseDrfError(e) {
  const data = e.response?.data;
  if (!data) return "Ошибка";
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

async function loadHalls() {
  const res = await http.get("/api/halls/");
  halls.value = res.data;
}

let readersTimer = null;
async function searchReaders() {
  clearTimeout(readersTimer);
  const q = readerQuery.value.trim();
  if (!q) {
    readerResults.value = [];
    return;
  }
  readersTimer = setTimeout(async () => {
    try {
      const res = await http.get(`/api/readers/?search=${encodeURIComponent(q)}`);
      readerResults.value = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
    } catch {
      readerResults.value = [];
    }
  }, 250);
}

function selectReader(r) {
  selectedReader.value = r;
  readerQuery.value = r.full_name;
  readerResults.value = [];
  recalcAvailability();
}

let booksTimer = null;
async function searchBooks() {
  clearTimeout(booksTimer);
  const q = bookQuery.value.trim();
  if (!q) {
    bookResults.value = [];
    return;
  }
  booksTimer = setTimeout(async () => {
    try {
      const res = await http.get(`/api/books/?search=${encodeURIComponent(q)}`);
      bookResults.value = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
    } catch {
      bookResults.value = [];
    }
  }, 250);
}

function selectBook(b) {
  selectedBook.value = b;
  bookQuery.value = b.title;
  bookResults.value = [];
  recalcAvailability();
}

async function recalcAvailability() {
  availabilityText.value = "";
  if (!selectedBook.value || !hallId.value) return;

  try {
    const stockRes = await http.get("/api/stock/");
    const stockRows = Array.isArray(stockRes.data) ? stockRes.data : (stockRes.data.results ?? []);
    const row = stockRows.find(s => Number(s.book) === Number(selectedBook.value.id) && Number(s.hall) === Number(hallId.value));
    if (!row) {
      availabilityText.value = "В этом зале нет строки BookStock для этой книги (выдача не пройдёт).";
      return;
    }

    const total = Number(row.copies ?? 0);

    const loansRes = await http.get("/api/loans/");
    const allLoans = Array.isArray(loansRes.data) ? loansRes.data : (loansRes.data.results ?? []);
    const activeQty = allLoans
      .filter(l => Number(l.book) === Number(selectedBook.value.id) && Number(l.hall) === Number(hallId.value) && l.returned_at == null)
      .reduce((sum, l) => sum + Number(l.qty ?? 0), 0);

    const available = total - activeQty;

    availabilityText.value = `В зале всего: ${total}. На руках: ${activeQty}. Доступно: ${available}.`;

    if (available < Number(qty.value ?? 1)) {
      availabilityText.value += ` Недостаточно для qty=${qty.value}.`;
    }
  } catch {
  }
}

async function createLoan() {
  error.value = "";
  if (!canCreate.value) return;

  busyCreate.value = true;
  try {
    await http.post("/api/loans/", {
      reader: selectedReader.value.id,
      book: selectedBook.value.id,
      hall: Number(hallId.value),
      qty: Number(qty.value ?? 1),
      assigned_at: assignedAt.value || today(),
      returned_at: null,
    });

    await loadLoans();
    await recalcAvailability();
  } catch (e) {
    error.value = parseDrfError(e);
  } finally {
    busyCreate.value = false;
  }
}

async function loadLoans() {
  busyLoans.value = true;
  try {
    const res = await http.get("/api/loans/");
    loans.value = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
  } catch (e) {
    error.value = parseDrfError(e);
  } finally {
    busyLoans.value = false;
  }
}

const activeLoans = computed(() => loans.value.filter(l => l.returned_at == null));

async function returnLoan(loan) {
  busyReturnId.value = loan.id;
  try {
    await http.patch(`/api/loans/${loan.id}/`, { returned_at: today() });
    await loadLoans();
    await recalcAvailability();
  } catch (e) {
    error.value = parseDrfError(e);
  } finally {
    busyReturnId.value = null;
  }
}

onMounted(async () => {
  await loadHalls();
  await loadLoans();
});
</script>

<style scoped>
.card { border: 1px solid #ddd; padding: 12px; margin-top: 10px; }
.row { display:flex; gap:12px; margin-bottom: 10px; flex-wrap: wrap; }
.col { flex: 1; min-width: 240px; }
.label { display:block; margin-bottom:6px; font-weight:600; }
.input { width:95%; padding:10px; border:1px solid teal; }
.btn { padding:8px 12px; border:1px solid teal; background:white; cursor:pointer; }
.table { border-collapse: collapse; width: 100%; }
.table th, .table td { border:1px solid #ddd; padding:8px; vertical-align: top; }
.table th { background:#f6f6f6; }
.link { text-decoration:none; display:inline-block; }
.hint { margin-top:8px; font-size: 14px; opacity: .9; }
.dropdown { border:1px solid #ddd; margin-top:6px; max-height: 220px; overflow:auto; }
.dropdown-item { padding:8px; cursor:pointer; }
.dropdown-item:hover { background:#f6f6f6; }
</style>