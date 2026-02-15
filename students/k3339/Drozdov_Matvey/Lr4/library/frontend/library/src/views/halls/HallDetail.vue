<template>
  <div>
    <div style="display:flex; align-items:center; gap:10px;">
      <h2 style="margin:0;">Зал</h2>
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
      <div v-if="hall" class="card" style="margin-top:10px;">
        <div><b>Номер:</b> {{ hallNumber(hall) }}</div>
        <div><b>Название:</b> {{ hallName(hall) }}</div>
        <div><b>Вместимость:</b> {{ hall.capacity ?? "-" }}</div>
        <div style="margin-top:8px;">
          <b>Закреплено читателей:</b> {{ readers.length }}
        </div>
        <div>
          <b>Свободно мест:</b> {{ freeSeats }}
        </div>
      </div>

      <div class="card" style="margin-top:12px;">
        <div style="display:flex; align-items:center; justify-content:space-between; gap:10px;">
          <h3 style="margin:0;">Читатели зала</h3>
          <input
            class="input"
            v-model="readersSearch"
            placeholder="Поиск по читателям..."
            style="max-width: 320px;"
          />
        </div>

        <table v-if="filteredReaders.length" class="table" style="margin-top:10px;">
          <thead>
            <tr>
              <th>#</th>
              <th>ФИО</th>
              <th>Билет</th>
              <th>Телефон</th>
              <th style="width:120px;">Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(r, idx) in filteredReaders" :key="r.id">
              <td>{{ idx + 1 }}</td>
              <td>{{ r.full_name || r.fio || "-" }}</td>
              <td>{{ r.active_ticket_number || r.ticket || "-" }}</td>
              <td>{{ r.phone || "-" }}</td>
              <td>
                <router-link class="btn link" :to="`/readers/${r.id}`">Открыть</router-link>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-else style="margin-top:10px;">
          В этом зале пока нет читателей.
        </div>
      </div>

      <div class="card" style="margin-top:12px;">
        <div style="display:flex; align-items:center; justify-content:space-between; gap:10px;">
          <h3 style="margin:0;">Фонд зала (экземпляры)</h3>
          <input
            class="input"
            v-model="stockSearch"
            placeholder="Поиск по книгам..."
            style="max-width: 320px;"
          />
        </div>

        <table v-if="filteredStock.length" class="table" style="margin-top:10px;">
          <thead>
            <tr>
              <th>#</th>
              <th>Книга</th>
              <th>Шифр</th>
              <th>Экземпляров</th>
              <th style="width:120px;">Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(s, idx) in filteredStock" :key="s.id">
              <td>{{ idx + 1 }}</td>

              <td>
                <router-link class="link" :to="`/books/${bookId(s)}`">
                  {{ bookTitle(s) }}
                </router-link>
              </td>

              <td>{{ bookCode(s) }}</td>
              <td>{{ stockCount(s) }}</td>

              <td>
                <router-link class="btn link" :to="`/books/${bookId(s)}`">К книге</router-link>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-else style="margin-top:10px;">
          В этом зале пока нет книг (или фонд не загружен).
        </div>

        <div style="margin-top:10px; font-size: 14px;">
          <b>Всего экземпляров в зале:</b> {{ totalCopies }}
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

const hall = ref(null);
const readers = ref([]);
const stock = ref([]);

const loading = ref(false);
const error = ref("");

const readersSearch = ref("");
const stockSearch = ref("");

function hallName(h) {
  return h.name || h.title || `Зал ${hallNumber(h)}`;
}

function hallNumber(h) {
  return h.number ?? h.hall_number ?? h.room_number ?? h.id ?? "-";
}


const booksMap = ref({});
const codesMap = ref({}); 

function bookId(s) {
  return Number(s.book);
}

function bookTitle(s) {
  const b = booksMap.value[bookId(s)];
  return b?.title || `Книга #${bookId(s)}`;
}

function bookCode(s) {
  return codesMap.value[bookId(s)] || booksMap.value[bookId(s)]?.current_code || "—";
}

function stockCount(s) {
  return s.copies ?? 0;
}



async function loadBooksMap() {
  const res = await http.get("/api/books/");
  const data = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
  const map = {};
  for (const b of data) map[b.id] = b;
  booksMap.value = map;
}

async function loadCodesMap() {
  const res = await http.get("/api/book-codes/");
  const data = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
  const map = {};

  for (const row of data) {
    if (row.valid_to == null) {
      map[Number(row.book)] = row.code;
    }
  }
  codesMap.value = map;
}

async function loadHall() {
  const id = route.params.id;
  const res = await http.get(`/api/halls/${id}/`);
  hall.value = res.data;
}

async function loadReaders() {
  const hallId = Number(route.params.id);

  const histRes = await http.get("/api/reader-hall-history/");
  const currentLinks = histRes.data.filter(
    (x) => Number(x.hall) === hallId && x.valid_to == null
  );

  const readerIds = currentLinks.map((x) => x.reader);

  const readersRes = await http.get("/api/readers/");
  const allReaders = readersRes.data;

  const set = new Set(readerIds);
  readers.value = allReaders.filter((r) => set.has(r.id));
}

async function loadStock() {
  const hallId = Number(route.params.id);
  const res = await http.get("/api/stock/");
  const data = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
  stock.value = data.filter(s => Number(s.hall) === hallId);
}


async function loadAll() {
  error.value = "";
  loading.value = true;

  try {
    await Promise.all([
      loadHall(),
      loadReaders(),
      loadStock(),
      loadBooksMap(),
      loadCodesMap(),
    ]);
  } catch (e) {
    console.log("HALL DETAIL ERROR:", e);
    error.value = "Не удалось загрузить данные зала.";
  } finally {
    loading.value = false;
  }
}

function goBack() {
  router.push("/halls");
}

const freeSeats = computed(() => {
  if (!hall.value) return "-";
  const cap = Number(hall.value.capacity ?? 0);
  if (!cap) return "-";
  const free = cap - readers.value.length;
  return free < 0 ? 0 : free;
});

const totalCopies = computed(() => {
  return stock.value.reduce((sum, s) => sum + Number(s.copies ?? 0), 0);
});

// ---- фильтры ----
const filteredReaders = computed(() => {
  const q = readersSearch.value.trim().toLowerCase();
  if (!q) return readers.value;

  return readers.value.filter(r => {
    const fio = String(r.full_name || r.fio || "").toLowerCase();
    const ticket = String(r.ticket_number || r.ticket || "").toLowerCase();
    const phone = String(r.phone || "").toLowerCase();
    return fio.includes(q) || ticket.includes(q) || phone.includes(q);
  });
});

const filteredStock = computed(() => {
  const q = stockSearch.value.trim().toLowerCase();
  if (!q) return stock.value;

  return stock.value.filter(s => {
    const t = String(bookTitle(s)).toLowerCase();
    const c = String(bookCode(s)).toLowerCase();
    return t.includes(q) || c.includes(q);
  });
});


onMounted(loadAll);

watch(() => route.params.id, loadAll);
</script>

<style scoped>
.card {
  border: 1px solid #ddd;
  padding: 12px;
}

.input {
  padding: 10px;
  border: 1px solid teal;
  width: 100%;
}

.btn {
  padding: 8px 12px;
  border: 1px solid teal;
  background: white;
  cursor: pointer;
}

.link {
  text-decoration: none;
  display: inline-block;
}

.table {
  border-collapse: collapse;
  width: 100%;
}

.table th,
.table td {
  border: 1px solid #ddd;
  padding: 8px;
  vertical-align: top;
}

.table th {
  background: #f6f6f6;
}
</style>