<template>
  <div>
    <div>
      <h2 style="margin:0;">Читальные залы</h2>
      <button class="btn" @click="goHome">На главную</button>
    </div>

    <div style="display:flex; gap:10px; align-items:center; margin: 10px 0;">
      <input
        class="input"
        v-model="search"
        placeholder="Поиск: номер, название..."
      />

      <button class="btn" @click="loadHalls" :disabled="loading">
        {{ loading ? "Загружаю..." : "Обновить" }}
      </button>

      <router-link class="btn link" to="/halls/new">+ Добавить зал</router-link>
    </div>

    <div v-if="error" style="color:red; white-space:pre-line; margin: 10px 0;">
      {{ error }}
    </div>

    <table v-if="filteredHalls.length" class="table">
      <thead>
        <tr>
          <th>#</th>
          <th>Номер</th>
          <th>Название</th>
          <th>Вместимость</th>
          <th>Читателей</th>
          <th>Экземпляров</th>
          <th style="width: 180px;">Действия</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(h, index) in filteredHalls" :key="h.id">
          <td>{{ index + 1 }}</td>

          <td>{{ hallNumber(h) }}</td>

          <td>
            <router-link :to="`/halls/${h.id}`">
              {{ hallName(h) }}
            </router-link>
          </td>

          <td>{{ h.capacity ?? "-" }}</td>

          <td>{{ hallReadersCount(h.id) }}</td>
          <td>{{ hallCopiesCount(h.id) }}</td>

          <td>
            <router-link class="btn link" :to="`/halls/${h.id}`">Открыть</router-link>
            <button class="btn danger" @click="deleteHall(h.id)">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-else-if="!loading" style="margin-top: 10px;">
      Залов пока нет (или ничего не найдено).
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { http } from "@/api/http";
import { useRouter } from "vue-router";
const router = useRouter();

function goHome() {
  router.push("/");
}
const halls = ref([]);
const loading = ref(false);
const error = ref("");
const search = ref("");

const readersByHall = ref(null); 
const copiesByHall = ref(null);  

function hallName(h) {
  return h.name || h.title || `Зал ${h.number ?? h.id}`;
}

function hallNumber(h) {
  return h.number ?? h.hall_number ?? h.room_number ?? h.id ?? "-";
}

async function loadHalls() {
  error.value = "";
  loading.value = true;

  try {
    const res = await http.get("/api/halls/");
    halls.value = res.data;

    await loadReadersCountByHall();
    await loadCopiesCountByHall();
  } catch (e) {
    console.log("HALLS ERROR:", e);
    error.value =
      "Не удалось загрузить залы.\n";
  } finally {
    loading.value = false;
  }
}

async function loadReadersCountByHall() {
  readersByHall.value = null;

  try {
    const res = await http.get("/api/reader-hall-history/");
    const map = {};

    for (const x of res.data) {
      if (x.valid_to != null) continue;

      const hallId = Number(x.hall);
      if (!hallId) continue;

      map[hallId] = (map[hallId] || 0) + 1;
    }

    readersByHall.value = map;
  } catch (e) {
    console.log("READERS COUNT ERROR:", e);
    readersByHall.value = null;
  }
}


async function loadCopiesCountByHall() {
  copiesByHall.value = null;
  try {
    const res = await http.get("/api/stock/");
    const map = {};
    for (const s of res.data) {
      const hallId = s.hall;
      const cnt = Number(s.copies ?? 0);
      if (!hallId) continue;
      map[hallId] = (map[hallId] || 0) + cnt;
    }
    copiesByHall.value = map;
  } catch {
    copiesByHall.value = null;
  }
}

function hallReadersCount(hallId) {
  if (!readersByHall.value) return "—";
  return readersByHall.value[hallId] ?? 0;
}

function hallCopiesCount(hallId) {
  if (!copiesByHall.value) return "—";
  return copiesByHall.value[hallId] ?? 0;
}

async function deleteHall(id) {
  if (!confirm("Точно удалить зал?")) return;

  try {
    await http.delete(`/api/halls/${id}/`);
    halls.value = halls.value.filter((h) => h.id !== id);
  } catch (e) {
    console.log("DELETE HALL ERROR:", e);
    alert("Не получилось удалить. Возможно, у тебя нет прав или эндпоинт другой.");
  }
}

const filteredHalls = computed(() => {
  const q = search.value.trim().toLowerCase();
  if (!q) return halls.value;

  return halls.value.filter((h) => {
    const name = String(hallName(h)).toLowerCase();
    const num = String(hallNumber(h)).toLowerCase();
    return name.includes(q) || num.includes(q);
  });
});

onMounted(loadHalls);
</script>

<style scoped>
.input {
  width: 360px;
  padding: 10px;
  border: 1px solid teal;
}

.btn {
  padding: 3px 12px;
  border: 2px solid teal;
  background: white;
  height: 20px;
  cursor: pointer;
}


.link {
  text-decoration: none;
  display: inline-block;
}

.danger {
  border-color: #cc0000;
  height: 30px;
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
</style>