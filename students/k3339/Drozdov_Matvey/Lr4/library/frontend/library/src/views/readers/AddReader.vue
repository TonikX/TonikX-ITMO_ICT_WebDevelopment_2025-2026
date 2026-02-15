<template>
  <div>
    <h2>Добавить читателя</h2>

    <form @submit.prevent="onSubmit" class="card">
      <label class="label">ФИО</label>
      <input class="input" v-model="full_name" placeholder="Иванов Иван Иванович" />

      <label class="label">Телефон</label>
      <input class="input" v-model="phone" placeholder="+7..." />

      <label class="label">Паспорт</label>
      <input class="input" v-model="passport_number" placeholder="Серия и номер" />

      <label class="label">Дата рождения</label>
      <input class="input" type="date" v-model="birth_date" />

      <label class="label">Образование</label>
      <input class="input" v-model="education_lvl" placeholder="например: высшее" />

      <label class="label">
      <input type="checkbox" v-model="degree" />
        Есть учёная степень
      </label>
      <hr style="margin: 14px 0;" />

      <label class="label">Номер читательского билета (активный)</label>
      <input class="input" v-model="ticket_number" placeholder="Например: A-123" />

      <label class="label">Закрепить за залом (необязательно)</label>
      <select class="input" v-model.number="hall_id">
        <option :value="null">— не выбирать —</option>
        <option v-for="h in halls" :key="h.id" :value="h.id">
          {{ hallLabel(h) }}
        </option>
      </select>

      <div style="display:flex; gap:10px; margin-top:12px;">
        <button class="btn" type="submit" :disabled="loading">
          {{ loading ? "Сохраняю..." : "Создать" }}
        </button>
        <button class="btn" type="button" @click="goBack">Отмена</button>
      </div>

      <div v-if="error" style="color:red; margin-top:10px; white-space:pre-line;">
        {{ error }}
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { http } from "@/api/http";

const router = useRouter();

const loading = ref(false);
const error = ref("");

const halls = ref([]);
const hall_id = ref(null);

const full_name = ref("");
const phone = ref("");
const passport_number = ref("");
const birth_date = ref("");
const education_lvl = ref("");
const degree = ref(false);
const ticket_number = ref("");

function goBack() {
  router.push("/readers");
}

function hallLabel(h) {
  const name = h.name || h.title || "";
  const num = h.number ?? h.id;
  return name ? `Зал ${num}: ${name}` : `Зал ${num}`;
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

async function loadHalls() {
  try {
    const res = await http.get("/api/halls/");
    halls.value = res.data;
  } catch {
    halls.value = [];
  }
}

async function onSubmit() {
  loading.value = true;
  error.value = "";

  let createdReaderId = null;

  try {
    const readerRes = await http.post("/api/readers/", {
      full_name: full_name.value.trim(),
      phone: phone.value.trim() || null,
      passport_number: passport_number.value.trim() || null,
      birth_date: birth_date.value || null,
      education_lvl: education_lvl.value.trim() || null,
      degree: degree.value,
    });

    createdReaderId = readerRes.data.id;

    const today = todayDateString();

    await http.post("/api/ticket-history/", {
        reader: createdReaderId,
        ticket_number: ticket_number.value.trim(),
        valid_to: null,
        });

    if (hall_id.value) {
        await http.post("/api/reader-hall-history/", {
        reader: createdReaderId,
        hall: hall_id.value,
        valid_to: null,
  });
}

    router.push("/readers");
  } catch (e) {
    if (createdReaderId) {
      try {
        await http.delete(`/api/readers/${createdReaderId}/`);
      } catch (rollbackErr) {
        console.log("ROLLBACK DELETE FAILED:", rollbackErr);
      }
    }

    error.value = parseDrfError(e);
  } finally {
    loading.value = false;
  }
}

onMounted(loadHalls);
</script>

<style scoped>
.card { max-width: 640px; border: 1px solid #ddd; padding: 12px; margin-top: 10px; }
.label { display:block; margin-top:10px; margin-bottom:6px; font-weight:600; }
.input { width:90%; padding:10px; border:1px solid teal; }
.btn { padding:8px 12px; border:1px solid teal; background:white; cursor:pointer; }
.btn:disabled { opacity:0.6; cursor:not-allowed; }
</style>