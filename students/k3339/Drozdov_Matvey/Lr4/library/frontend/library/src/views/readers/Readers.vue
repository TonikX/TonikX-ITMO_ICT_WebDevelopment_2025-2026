<template>
  <div>
    <div>
      <h2 style="margin:0;">Читатели</h2>
      <button class="btn" @click="goHome">На главную</button>
    </div>

    <div style="display:flex; gap:10px; align-items:center; margin: 10px 0;">
      <input
        class="input"
        v-model="search"
        placeholder="Поиск: ФИО, билет, паспорт, телефон..."
      />

      <button class="btn" @click="loadAll" :disabled="loading">
        {{ loading ? "Загружаю..." : "Обновить" }}
      </button>

      <router-link class="btn link" to="/readers/new">+ Добавить читателя</router-link>
    </div>

    <div v-if="error" style="color:red; white-space:pre-line; margin: 10px 0;">
      {{ error }}
    </div>

    <table v-if="filteredReaders.length" class="table">
      <thead>
        <tr>
          <th>#</th>
          <th>ФИО</th>
          <th>Билет</th>
          <th>Паспорт</th>
          <th>Дата рождения</th>
          <th>Телефон</th>
          <th>Текущий зал</th>
          <th style="width: 150px;">Действия</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(r, index) in filteredReaders" :key="r.id">
          <td>{{ index + 1 }}</td>

          <td>
            <router-link :to="`/readers/${r.id}`" class="link">
              {{ r.full_name || r.fio || "-" }}
            </router-link>
          </td>

          <td>{{ r.active_ticket_number || "-" }}</td>
          <td>{{ r.passport_number ||  "-" }}</td>
          <td>{{ r.birth_date || "-" }}</td>
          <td>{{ r.phone || "-" }}</td>

          <td>{{ hallNameByReader(r.id) }}</td>

          <td>
            <router-link class="btn link" :to="`/readers/${r.id}`">Открыть</router-link>
            <button class="btn danger" @click="deleteReader(r.id)">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-else-if="!loading" style="margin-top: 10px;">
      Читателей пока нет (или ничего не найдено).
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { http } from "@/api/http";
import { useRouter } from "vue-router";

const router = useRouter();

const readers = ref([]);
const hallHistory = ref([]); 
const halls = ref([]);      

const loading = ref(false);
const error = ref("");
const search = ref("");

const currentHallByReaderId = ref({}); 
const hallsMap = ref({});          


function goHome() {
  router.push("/");
}

async function deleteReader(id) {
  if (!confirm("Точно удалить читателя?")) return;

  try {
    await http.delete(`/api/readers/${id}/`);
    readers.value = readers.value.filter(r => r.id !== id);
  } catch (e) {
    console.log("DELETE READER ERROR:", e);
    alert("Не получилось удалить читателя. Проверь права/эндпоинт.");
  }
}

function buildMaps() {
  const map = {};
  for (const rec of hallHistory.value) {
    const isCurrent = rec.valid_to === null || rec.valid_to === "" || rec.valid_to === undefined;
    if (isCurrent) {
      map[rec.reader] = rec.hall;
    }
  }
  currentHallByReaderId.value = map;

  const hmap = {};
  for (const h of halls.value) {
    const name = h.name || h.title || `Зал ${h.number ?? h.id}`;
    hmap[h.id] = name;
  }
  hallsMap.value = hmap;
}

function hallNameByReader(readerId) {
  const hallId = currentHallByReaderId.value[readerId];
  if (!hallId) return "-";
  return hallsMap.value[hallId] || `Зал #${hallId}`;
}

async function loadReaders() {
  const res = await http.get("/api/readers/");
  readers.value = res.data;
}

async function loadHallHistory() {
  const res = await http.get("/api/reader-hall-history/");
  hallHistory.value = res.data;
}

async function loadHalls() {
  const res = await http.get("/api/halls/");
  halls.value = res.data;
}

async function loadAll() {
  error.value = "";
  loading.value = true;

  try {
    await Promise.all([loadReaders(), loadHallHistory(), loadHalls()]);
    buildMaps();
  } catch (e) {
    console.log("READERS PAGE ERROR:", e);
    error.value =
      "Не удалось загрузить читателей.\n" +
      "Проверь эндпоинты /api/readers/, /api/reader-hall-history/, /api/halls/ и авторизацию.";
  } finally {
    loading.value = false;
  }
}

const filteredReaders = computed(() => {
  const q = search.value.trim().toLowerCase();
  if (!q) return readers.value;

  return readers.value.filter((r) => {
    const fio = String(r.full_name || r.fio || "").toLowerCase();
    const ticket = String(r.ticket_number || r.ticket || "").toLowerCase();
    const passport = String(r.passport_number || r.passport || "").toLowerCase();
    const phone = String(r.phone || "").toLowerCase();

    const hallText = String(hallNameByReader(r.id)).toLowerCase();

    return fio.includes(q) || ticket.includes(q) || passport.includes(q) || phone.includes(q) || hallText.includes(q);
  });
});

onMounted(loadAll);
</script>

<style scoped>
.input {
  width: 440px;
  padding: 10px;
  border: 1px solid teal;
}

.btn {
  padding: 8px 7px;
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
  margin-top: 10px;
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

.danger {
  border-color: #cc0000;
  width: 77px;
}

</style>