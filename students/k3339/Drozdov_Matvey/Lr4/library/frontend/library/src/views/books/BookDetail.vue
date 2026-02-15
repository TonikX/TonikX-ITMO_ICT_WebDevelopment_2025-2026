<template>
  <div>
    <div style="display:flex; align-items:center; gap:10px;">
      <h2 style="margin:0;">Книга</h2>
      <button class="btn" @click="goBack">Назад</button>
      <button class="btn" @click="loadAll" :disabled="loading">
        {{ loading ? "Обновляю..." : "Обновить" }}
      </button>
    </div>

    <div v-if="error" style="margin-top:10px; color:red; white-space:pre-line;">
      {{ error }}
    </div>

    <div v-if="loading" style="margin-top:10px;">
      Загружаю...
    </div>

    <div v-else>
      <div v-if="book" class="card" style="margin-top:10px;">
        <div style="display:flex; justify-content:space-between; gap:10px; align-items:flex-start;">
          <div>
            <div style="font-size:20px; font-weight:700;">
              {{ book.title || `Книга #${book.id}` }}
            </div>

            <div style="margin-top:6px;">
              <b>Автор(ы):</b> {{ authorsText }}
            </div>

            <div style="margin-top:6px;">
              <b>Издательство:</b> {{ book.publisher || "-" }}
              &nbsp; | &nbsp;
              <b>Год:</b> {{ book.publication_year ?? "-" }}
            </div>

            <div style="margin-top:6px;">
              <b>Раздел:</b> {{ book.section || "-" }}
            </div>

            <div style="margin-top:6px;">
              <b>Текущий шифр:</b> {{ currentCode || "—" }}
            </div>
          </div>

          <div style="display:flex; gap:10px;">
            <button class="btn danger" @click="deleteBook" :disabled="busyDelete">
              {{ busyDelete ? "Удаляю..." : "Удалить" }}
            </button>
          </div>
        </div>
      </div>

      <div class="card" style="margin-top:12px;">
        <div style="display:flex; align-items:center; justify-content:space-between; gap:10px;">
          <h3 style="margin:0;">Шифры (история)</h3>

          <div style="display:flex; gap:10px; align-items:center;">
            <input class="input" v-model="newCode" placeholder="Новый шифр..." style="max-width:260px;" />
            <button class="btn" @click="addCode" :disabled="busyCode || !newCode.trim()">
              {{ busyCode ? "Сохраняю..." : "Добавить шифр" }}
            </button>
          </div>
        </div>

        <table v-if="codeHistorySorted.length" class="table" style="margin-top:10px;">
          <thead>
            <tr>
              <th>#</th>
              <th>Шифр</th>
              <th>Действует с</th>
              <th>Действует до</th>
              <th>Статус</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(c, idx) in codeHistorySorted" :key="c.id || idx">
              <td>{{ idx + 1 }}</td>
              <td>{{ c.code }}</td>
              <td>{{ c.valid_from || "-" }}</td>
              <td>{{ c.valid_to || "—" }}</td>
              <td>
                <span v-if="c.valid_to == null"><b>Действует</b></span>
                <span v-else>Закрыт</span>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-else style="margin-top:10px;">
          Пока нет шифров.
        </div>
      </div>

      <div class="card" style="margin-top:12px;">
        <div style="display:flex; align-items:center; justify-content:space-between; gap:10px;">
          <h3 style="margin:0;">Фонд по залам</h3>

          <div style="display:flex; gap:10px; align-items:center;">
            <select class="input" v-model.number="stockHallId" style="max-width:260px;">
              <option :value="null">— выбрать зал —</option>
              <option v-for="h in halls" :key="h.id" :value="h.id">
                {{ hallLabel(h) }}
              </option>
            </select>

            <input
              class="input"
              type="number"
              min="0"
              v-model.number="stockCopies"
              placeholder="Экземпляров"
              style="max-width:160px;"
            />

            <button class="btn" @click="upsertStock" :disabled="busyStock || !stockHallId">
              {{ busyStock ? "Сохраняю..." : "Сохранить" }}
            </button>
          </div>
        </div>

        <table v-if="stockRowsSorted.length" class="table" style="margin-top:10px;">
          <thead>
            <tr>
              <th>#</th>
              <th>Зал</th>
              <th>Экземпляров</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(s, idx) in stockRowsSorted" :key="s.id || idx">
              <td>{{ idx + 1 }}</td>
              <td>
                <router-link class="link" :to="`/halls/${hallIdOfStock(s)}`">
                  {{ hallNameById(hallIdOfStock(s)) }}
                </router-link>
              </td>
              <td>{{ s.copies ?? 0 }}</td>
            </tr>
          </tbody>
        </table>

        <div v-else style="margin-top:10px;">
          В фонде пока нет записей по залам.
        </div>

        <div style="margin-top:10px;">
          <b>Всего экземпляров в библиотеке:</b> {{ totalCopies }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { http } from "@/api/http";

const route = useRoute();
const router = useRouter();

const loading = ref(false);
const error = ref("");

const book = ref(null);

const codeHistory = ref([]);
const newCode = ref("");
const busyCode = ref(false);

const halls = ref([]);
const authors = ref([]);

const stockRows = ref([]);
const stockHallId = ref(null);
const stockCopies = ref(0);
const busyStock = ref(false);

const busyDelete = ref(false);

function goBack() {
  router.push("/books");
}

function todayDateString() {
  const d = new Date();
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, "0");
  const dd = String(d.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

function parseDrfError(e) {
  const data = e.response?.data;
  if (!data) return "Ошибка. Проверь сервер и эндпоинты.";
  if (typeof data === "object") {
    const lines = [];
    for (const key in data) {
      const val = data[key];
      lines.push(`${key}: ${Array.isArray(val) ? val.join(", ") : String(val)}`);
    }
    return lines.join("\n");
  }
  return String(data);
}

function hallNumber(h) {
  return h.hall_number ?? h.number ?? h.id ?? "-";
}
function hallName(h) {
  return h.name || `Зал ${hallNumber(h)}`;
}
function hallLabel(h) {
  return `Зал ${hallNumber(h)}: ${hallName(h)}`;
}
function hallNameById(id) {
  const h = halls.value.find(x => x.id === Number(id));
  return h ? hallLabel(h) : `Зал #${id}`;
}
function hallIdOfStock(s) {
  return Number(s.hall_id ?? s.hall);
}

async function loadHalls() {
  try {
    const res = await http.get("/api/halls/");
    halls.value = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
  } catch {
    halls.value = [];
  }
}

async function loadAuthors() {
  try {
    const res = await http.get("/api/authors/");
    authors.value = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
  } catch {
    authors.value = [];
  }
}

async function loadBook() {
  const id = route.params.id;
  const res = await http.get(`/api/books/${id}/`);
  book.value = res.data;
}

async function loadCodeHistory() {
  const id = Number(route.params.id);

  try {
    const res = await http.get(`/api/book-codes/?book=${id}`);
    const data = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
    codeHistory.value = data.filter(x => Number(x.book) === id);
    return;
  } catch {}

  const resAll = await http.get("/api/book-codes/");
  const dataAll = Array.isArray(resAll.data) ? resAll.data : (resAll.data.results ?? []);
  codeHistory.value = dataAll.filter(x => Number(x.book) === id);
}

async function loadStock() {
  const bookId = Number(route.params.id);

  try {
    const res = await http.get(`/api/stock/?book=${bookId}`);
    const data = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
    stockRows.value = data;
    return;
  } catch {}

  const resAll = await http.get("/api/stock/");
  const dataAll = Array.isArray(resAll.data) ? resAll.data : (resAll.data.results ?? []);
  stockRows.value = dataAll.filter(s => Number(s.book) === bookId);
}

async function loadAll() {
  error.value = "";
  loading.value = true;

  try {
    await Promise.all([
      loadHalls(),
      loadAuthors(),
      loadBook(),
      loadCodeHistory(),
      loadStock(),
    ]);
  } catch (e) {
    console.log("BOOK DETAIL ERROR:", e);
    error.value =
      "Не удалось загрузить страницу книги.\n" +
      "Проверь эндпоинты: /api/books/<id>/, /api/book-codes/, /api/stock/.";
  } finally {
    loading.value = false;
  }
}

const codeHistorySorted = computed(() => {
  return [...codeHistory.value].sort((a, b) => {
    const aOpen = a.valid_to == null ? 1 : 0;
    const bOpen = b.valid_to == null ? 1 : 0;
    if (aOpen !== bOpen) return bOpen - aOpen;
    return String(b.valid_from || "").localeCompare(String(a.valid_from || ""));
  });
});

const currentCode = computed(() => {
  const cur = codeHistory.value.find(x => x.valid_to == null);
  return cur?.code ?? (book.value?.current_code ?? null);
});

const totalCopies = computed(() => {
  return stockRows.value.reduce((sum, s) => sum + Number(s.copies ?? 0), 0);
});

const stockRowsSorted = computed(() => {
  return [...stockRows.value].sort((a, b) => hallIdOfStock(a) - hallIdOfStock(b));
});

const authorsText = computed(() => {
  const a = book.value?.authors;
  if (!a) return "—";

  if (Array.isArray(a) && a.length && typeof a[0] === "number") {
    if (!authors.value.length) return a.join(", ");
    const map = new Map(authors.value.map(x => [x.id, x.full_name]));
    return a.map(id => map.get(id) || `#${id}`).join(", ");
  }

  if (Array.isArray(a) && a.length && typeof a[0] === "object") {
    return a.map(x => x.full_name || x.name || `#${x.id}`).join(", ");
  }

  return "—";
});

async function addCode() {
  if (!book.value) return;
  busyCode.value = true;

  try {
    const today = todayDateString();

    const cur = codeHistory.value.find(x => x.valid_to == null);
    if (cur?.id) {
      await http.patch(`/api/book-codes/${cur.id}/`, { valid_to: today });
    }

    await http.post("/api/book-codes/", {
      book: book.value.id,
      code: newCode.value.trim(),
      valid_from: today,
      valid_to: null,
    });

    newCode.value = "";
    await loadCodeHistory();
  } catch (e) {
    console.log("ADD CODE ERROR:", e);
    alert(parseDrfError(e));
  } finally {
    busyCode.value = false;
  }
}

async function upsertStock() {
  if (!book.value || !stockHallId.value) return;
  busyStock.value = true;

  try {
    const hallId = Number(stockHallId.value);
    const existing = stockRows.value.find(s =>
      Number(s.book) === Number(book.value.id) && hallIdOfStock(s) === hallId
    );

    if (existing?.id) {
      await http.patch(`/api/stock/${existing.id}/`, { copies: Number(stockCopies.value ?? 0) });
    } else {
      await http.post("/api/stock/", {
        book: book.value.id,
        hall: hallId,
        copies: Number(stockCopies.value ?? 0),
      });
    }

    await loadStock();
  } catch (e) {
    console.log("UPSERT STOCK ERROR:", e);
    alert(parseDrfError(e));
  } finally {
    busyStock.value = false;
  }
}

async function deleteBook() {
  if (!book.value) return;
  if (!confirm("Точно удалить книгу?")) return;

  busyDelete.value = true;
  try {
    await http.delete(`/api/books/${book.value.id}/`);
    router.push("/books");
  } catch (e) {
    console.log("DELETE BOOK ERROR:", e);
    alert(parseDrfError(e));
  } finally {
    busyDelete.value = false;
  }
}

onMounted(loadAll);
watch(() => route.params.id, loadAll);
</script>

<style scoped>
.card { border: 1px solid #ddd; padding: 12px; }
.input { padding: 10px; border: 1px solid teal; width: 100%; }
.btn { padding: 8px 12px; border: 1px solid teal; background: white; cursor: pointer; }
.btn:disabled { opacity: 0.6; cursor: not-allowed; }
.danger { border-color: #c00; }
.link { text-decoration: none; display: inline-block; }
.table { border-collapse: collapse; width: 100%; }
.table th, .table td { border: 1px solid #ddd; padding: 8px; vertical-align: top; }
.table th { background: #f6f6f6; }
</style>