<template>
  <div>
    <div style="display:flex; align-items:center; gap:10px;">
      <h2 style="margin:0;">Читатель</h2>
      <button class="btn" @click="goBack">Назад</button>
      <button class="btn" @click="loadAll" :disabled="loading">
        {{ loading ? "Обновляю..." : "Обновить" }}
      </button>
    </div>

    <div v-if="error" style="margin-top:10px; color:red; white-space:pre-line;">
      {{ error }}
    </div>

    <div v-if="loading" style="margin-top:10px;">Загружаю...</div>

    <div v-else>
      <div v-if="reader" class="card" style="margin-top:10px;">
        <div style="display:flex; justify-content:space-between; gap:10px; align-items:flex-start;">
          <div>
            <div style="font-size:20px; font-weight:700;">
              {{ reader.full_name || `Reader #${reader.id}` }}
            </div>

            <div style="margin-top:6px;">
              <b>Билет (активный):</b> {{ reader.active_ticket_number || "—" }}
            </div>

            <div style="margin-top:6px;">
              <b>Дата рождения:</b> {{ reader.birth_date || "—" }}
              &nbsp; | &nbsp;
              <b>Телефон:</b> {{ reader.phone || "—" }}
            </div>

            <div style="margin-top:6px;">
              <b>Паспорт:</b> {{ reader.passport_number || "—" }}
            </div>

            <div style="margin-top:6px;">
              <b>Образование:</b> {{ reader.education_lvl || "—" }}
              &nbsp; | &nbsp;
              <b>Учёная степень:</b> {{ reader.degree ? "да" : "нет" }}
            </div>

            <div style="margin-top:10px;">
              <b>Текущий зал:</b> {{ currentHallText }}
              <span v-if="currentHallLinkId">
                &nbsp;(<router-link class="link" :to="`/halls/${currentHallLinkId}`">открыть</router-link>)
              </span>
            </div>
          </div>

          <div style="display:flex; gap:10px;">
            <button class="btn danger" @click="deleteReader" :disabled="busyDelete">
              {{ busyDelete ? "Удаляю..." : "Удалить" }}
            </button>
          </div>
        </div>
      </div>

      <div class="card" style="margin-top:12px;">
        <div style="display:flex; align-items:center; justify-content:space-between; gap:10px;">
          <h3 style="margin:0;">Членство</h3>

          <div style="display:flex; gap:10px; align-items:center;">
            <select class="input" v-model="newMembershipType" style="max-width:220px;">
              <option value="enroll">enroll (вступил)</option>
              <option value="reregister">reregister (перерег.)</option>
              <option value="unregister">unregister (выбыл)</option>
            </select>

            <input class="input" v-model="newMembershipComment" placeholder="Комментарий (необязательно)" style="max-width:260px;" />

            <button class="btn" @click="addMembershipEvent" :disabled="busyMembership || !reader">
              {{ busyMembership ? "..." : "Добавить событие" }}
            </button>
          </div>
        </div>

        <div style="margin-top:10px;">
          <b>Текущий статус:</b> {{ membershipStatus }}
        </div>

        <table v-if="membershipEventsSorted.length" class="table" style="margin-top:10px;">
          <thead>
            <tr>
              <th>#</th>
              <th>Дата</th>
              <th>Тип</th>
              <th>Комментарий</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(m, idx) in membershipEventsSorted" :key="m.id || idx">
              <td>{{ idx + 1 }}</td>
              <td>{{ m.event_date || "-" }}</td>
              <td>{{ m.event_type }}</td>
              <td>{{ m.comment || "—" }}</td>
            </tr>
          </tbody>
        </table>

        <div v-else style="margin-top:10px;">
          Нет событий членства.
        </div>
      </div>

      <div class="card" style="margin-top:12px;">
        <div style="display:flex; align-items:center; justify-content:space-between; gap:10px;">
          <h3 style="margin:0;">Читательские билеты</h3>

          <div style="display:flex; gap:10px; align-items:center;">
            <input class="input" v-model="newTicketNumber" placeholder="Новый номер билета..." style="max-width:240px;" />
            <button class="btn" @click="addTicket" :disabled="busyTicket || !newTicketNumber.trim() || !reader">
              {{ busyTicket ? "..." : "Добавить билет" }}
            </button>
          </div>
        </div>

        <table v-if="ticketHistorySorted.length" class="table" style="margin-top:10px;">
          <thead>
            <tr>
              <th>#</th>
              <th>Номер</th>
              <th>Действует с</th>
              <th>Действует до</th>
              <th>Статус</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(t, idx) in ticketHistorySorted" :key="t.id || idx">
              <td>{{ idx + 1 }}</td>
              <td>{{ t.ticket_number }}</td>
              <td>{{ t.valid_from || "-" }}</td>
              <td>{{ t.valid_to || "—" }}</td>
              <td>
                <b v-if="t.valid_to == null">активен</b>
                <span v-else>закрыт</span>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-else style="margin-top:10px;">
          История билетов пустая.
        </div>
      </div>

      <div class="card" style="margin-top:12px;">
        <div style="display:flex; align-items:center; justify-content:space-between; gap:10px;">
          <h3 style="margin:0;">Закрепление за залами</h3>

          <div style="display:flex; gap:10px; align-items:center;">
            <select class="input" v-model.number="newHallId" style="max-width:280px;">
              <option :value="null">— выбрать зал —</option>
              <option v-for="h in halls" :key="h.id" :value="h.id">
                {{ hallLabel(h) }}
              </option>
            </select>

            <button class="btn" @click="assignHall" :disabled="busyHall || !newHallId || !reader">
              {{ busyHall ? "..." : "Закрепить" }}
            </button>
          </div>
        </div>

        <table v-if="hallHistorySorted.length" class="table" style="margin-top:10px;">
          <thead>
            <tr>
              <th>#</th>
              <th>Зал</th>
              <th>С</th>
              <th>До</th>
              <th>Статус</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(h, idx) in hallHistorySorted" :key="h.id || idx">
              <td>{{ idx + 1 }}</td>
              <td>
                <router-link class="link" :to="`/halls/${h.hall}`">
                  {{ hallNameById(h.hall) }}
                </router-link>
              </td>
              <td>{{ h.valid_from || "-" }}</td>
              <td>{{ h.valid_to || "—" }}</td>
              <td>
                <b v-if="h.valid_to == null">активно</b>
                <span v-else>закрыто</span>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-else style="margin-top:10px;">
          История залов пустая.
        </div>
      </div>

      <div class="card" style="margin-top:12px;">
        <div style="display:flex; align-items:center; justify-content:space-between; gap:10px;">
          <h3 style="margin:0;">Выдачи</h3>
          <input class="input" v-model="loanSearch" placeholder="Поиск по книге/залу..." style="max-width:320px;" />
        </div>

        <div style="margin-top:10px;">
          <b>Активные выдачи:</b> {{ activeLoans.length }}
        </div>

        <table v-if="filteredActiveLoans.length" class="table" style="margin-top:10px;">
          <thead>
            <tr>
              <th>#</th>
              <th>Книга</th>
              <th>Зал</th>
              <th>Выдано</th>
              <th>Кол-во</th>
              <th style="width:140px;">Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(l, idx) in filteredActiveLoans" :key="l.id || idx">
              <td>{{ idx + 1 }}</td>
              <td>
                <router-link class="link" :to="`/books/${l.book}`">
                  {{ bookTitleById(l.book) }}
                </router-link>
              </td>
              <td>
                <router-link class="link" :to="`/halls/${l.hall}`">
                  {{ hallNameById(l.hall) }}
                </router-link>
              </td>
              <td>{{ l.assigned_at || "-" }}</td>
              <td>{{ l.qty ?? 1 }}</td>
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

        <details style="margin-top:12px;">
          <summary style="cursor:pointer;">Показать историю возвратов</summary>

          <table v-if="closedLoans.length" class="table" style="margin-top:10px;">
            <thead>
              <tr>
                <th>#</th>
                <th>Книга</th>
                <th>Зал</th>
                <th>Выдано</th>
                <th>Возврат</th>
                <th>Кол-во</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(l, idx) in closedLoans" :key="l.id || idx">
                <td>{{ idx + 1 }}</td>
                <td>{{ bookTitleById(l.book) }}</td>
                <td>{{ hallNameById(l.hall) }}</td>
                <td>{{ l.assigned_at || "-" }}</td>
                <td>{{ l.returned_at || "-" }}</td>
                <td>{{ l.qty ?? 1 }}</td>
              </tr>
            </tbody>
          </table>

          <div v-else style="margin-top:10px;">История пустая.</div>
        </details>
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

const reader = ref(null);

const halls = ref([]);
const books = ref([]); 

const membershipEvents = ref([]);
const ticketHistory = ref([]);
const hallHistory = ref([]);
const loans = ref([]);

const busyDelete = ref(false);
const busyMembership = ref(false);
const busyTicket = ref(false);
const busyHall = ref(false);
const busyReturnId = ref(null);

const newMembershipType = ref("enroll");
const newMembershipComment = ref("");

const newTicketNumber = ref("");

const newHallId = ref(null);

const loanSearch = ref("");

function goBack() {
  router.push("/readers");
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

function bookTitleById(id) {
  const b = books.value.find(x => x.id === Number(id));
  return b ? (b.title || `Книга #${b.id}`) : `Книга #${id}`;
}

async function loadReader() {
  const id = route.params.id;
  const res = await http.get(`/api/readers/${id}/`);
  reader.value = res.data;
}

async function loadHalls() {
  try {
    const res = await http.get("/api/halls/");
    halls.value = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
  } catch {
    halls.value = [];
  }
}

async function loadBooks() {
  try {
    const res = await http.get("/api/books/");
    books.value = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
  } catch {
    books.value = [];
  }
}

async function loadMembershipEvents() {
  const rid = Number(route.params.id);
  const res = await http.get("/api/membership-events/");
  const data = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
  membershipEvents.value = data.filter(x => Number(x.reader) === rid);
}

async function loadTicketHistory() {
  const rid = Number(route.params.id);

  const res = await http.get("/api/ticket-history/");
  const data = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
  ticketHistory.value = data.filter(x => Number(x.reader) === rid);
}

async function loadHallHistory() {
  const rid = Number(route.params.id);

  const res = await http.get("/api/reader-hall-history/");
  const data = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
  hallHistory.value = data.filter(x => Number(x.reader) === rid);
}

async function loadLoans() {
  const rid = Number(route.params.id);

  const res = await http.get("/api/loans/");
  const data = Array.isArray(res.data) ? res.data : (res.data.results ?? []);
  loans.value = data.filter(x => Number(x.reader) === rid);
}

async function loadAll() {
  error.value = "";
  loading.value = true;

  try {
    await Promise.all([
      loadReader(),
      loadHalls(),
      loadBooks(),
      loadMembershipEvents(),
      loadTicketHistory(),
      loadHallHistory(),
      loadLoans(),
    ]);
  } catch (e) {
    console.log("READER DETAIL ERROR:", e);
    error.value =
      "Не удалось загрузить страницу читателя.\n" +
      "Проверь эндпоинты: /api/readers/<id>/, /api/membership-events/, /api/ticket-history/, /api/reader-hall-history/, /api/loans/.";
  } finally {
    loading.value = false;
  }
}

const membershipEventsSorted = computed(() => {
  return [...membershipEvents.value].sort((a, b) => {
    const ad = a.event_date || "";
    const bd = b.event_date || "";
    if (bd !== ad) return bd.localeCompare(ad);
    return Number(b.id ?? 0) - Number(a.id ?? 0);
  });
});

const membershipStatus = computed(() => {
  const last = membershipEventsSorted.value[0];
  if (!last) return "нет данных";
  const t = last.event_type;
  if (t === "enroll" || t === "reregister") return `состоит (посл.: ${t} ${last.event_date || ""})`;
  if (t === "unregister") return `не состоит (посл.: unregister ${last.event_date || ""})`;
  return `неизвестно (${t})`;
});

const ticketHistorySorted = computed(() => {
  return [...ticketHistory.value].sort((a, b) => {
    const aOpen = a.valid_to == null ? 1 : 0;
    const bOpen = b.valid_to == null ? 1 : 0;
    if (aOpen !== bOpen) return bOpen - aOpen;
    const af = a.valid_from || "";
    const bf = b.valid_from || "";
    return bf.localeCompare(af);
  });
});

const hallHistorySorted = computed(() => {
  return [...hallHistory.value].sort((a, b) => {
    const aOpen = a.valid_to == null ? 1 : 0;
    const bOpen = b.valid_to == null ? 1 : 0;
    if (aOpen !== bOpen) return bOpen - aOpen;
    const af = a.valid_from || "";
    const bf = b.valid_from || "";
    return bf.localeCompare(af);
  });
});

const currentHall = computed(() => hallHistory.value.find(x => x.valid_to == null) || null);

const currentHallText = computed(() => {
  if (!currentHall.value) return "—";
  return hallNameById(currentHall.value.hall);
});

const currentHallLinkId = computed(() => currentHall.value?.hall ?? null);

const activeLoans = computed(() => loans.value.filter(l => l.returned_at == null));
const closedLoans = computed(() => loans.value.filter(l => l.returned_at != null));

const filteredActiveLoans = computed(() => {
  const q = loanSearch.value.trim().toLowerCase();
  if (!q) return activeLoans.value;
  return activeLoans.value.filter(l => {
    const bt = String(bookTitleById(l.book)).toLowerCase();
    const ht = String(hallNameById(l.hall)).toLowerCase();
    return bt.includes(q) || ht.includes(q);
  });
});

async function addMembershipEvent() {
  if (!reader.value) return;
  busyMembership.value = true;
  try {
    await http.post("/api/membership-events/", {
      reader: reader.value.id,
      event_type: newMembershipType.value,
      event_date: todayDateString(),
      comment: newMembershipComment.value.trim() || null,
    });
    newMembershipComment.value = "";
    await loadMembershipEvents();
  } catch (e) {
    alert(parseDrfError(e));
  } finally {
    busyMembership.value = false;
  }
}

async function addTicket() {
  if (!reader.value) return;
  busyTicket.value = true;

  try {
    const today = todayDateString();

    const cur = ticketHistory.value.find(x => x.valid_to == null);
    if (cur?.id) {
      await http.patch(`/api/ticket-history/${cur.id}/`, { valid_to: today });
    }

    await http.post("/api/ticket-history/", {
      reader: reader.value.id,
      ticket_number: newTicketNumber.value.trim(),
      valid_from: today,
      valid_to: null,
    });

    newTicketNumber.value = "";
    await Promise.all([loadTicketHistory(), loadReader()]);
  } catch (e) {
    alert(parseDrfError(e));
  } finally {
    busyTicket.value = false;
  }
}

async function assignHall() {
  if (!reader.value || !newHallId.value) return;
  busyHall.value = true;

  try {
    const today = todayDateString();
    const cur = hallHistory.value.find(x => x.valid_to == null);
    if (cur?.id) {
      await http.patch(`/api/reader-hall-history/${cur.id}/`, { valid_to: today });
    }

    await http.post("/api/reader-hall-history/", {
      reader: reader.value.id,
      hall: Number(newHallId.value),
      valid_from: today,
      valid_to: null,
    });

    await loadHallHistory();
  } catch (e) {
    alert(parseDrfError(e));
  } finally {
    busyHall.value = false;
  }
}

async function returnLoan(loan) {
  if (!loan?.id) return;
  busyReturnId.value = loan.id;

  try {
    await http.patch(`/api/loans/${loan.id}/`, { returned_at: todayDateString() });
    await loadLoans();
  } catch (e) {
    alert(parseDrfError(e));
  } finally {
    busyReturnId.value = null;
  }
}

async function deleteReader() {
  if (!reader.value) return;
  if (!confirm("Точно удалить читателя?")) return;

  busyDelete.value = true;
  try {
    await http.delete(`/api/readers/${reader.value.id}/`);
    router.push("/readers");
  } catch (e) {
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