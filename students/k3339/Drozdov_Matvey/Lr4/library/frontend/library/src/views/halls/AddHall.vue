<template>
  <div>
    <h2>Добавить читальный зал</h2>

    <form @submit.prevent="onSubmit" class="card">
      <label class="label">Номер зала</label>
      <input
        class="input"
        type="number"
        v-model.number="number"
        placeholder="Например: 1"
        min="1"
      />

      <label class="label">Название</label>
      <input
        class="input"
        type="text"
        v-model="name"
        placeholder="Например: Гуманитарный зал"
      />

      <label class="label">Вместимость</label>
      <input
        class="input"
        type="number"
        v-model.number="capacity"
        placeholder="Например: 40"
        min="1"
      />

      <div style="display:flex; gap:10px; margin-top:12px;">
        <button class="btn" type="submit" :disabled="loading">
          {{ loading ? "Сохраняю..." : "Сохранить" }}
        </button>

        <button class="btn" type="button" @click="goBack">
          Отмена
        </button>
      </div>

      <div v-if="success" style="color: green; margin-top: 10px;">
        Зал создан!
      </div>

      <div v-if="error" style="color: red; margin-top: 10px; white-space: pre-line;">
        {{ error }}
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { http } from "@/api/http";

const router = useRouter();

const number = ref(null);
const name = ref("");
const capacity = ref(null);

const loading = ref(false);
const error = ref("");
const success = ref(false);

function goBack() {
  router.push("/halls");
}

function parseDrfError(e) {
  const data = e.response?.data;
  if (!data) return "Не удалось сохранить";

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

async function onSubmit() {
  error.value = "";
  success.value = false;

  if (!number.value || number.value < 1) {
    error.value = "Укажи номер зала (число >= 1).";
    return;
  }
  if (!name.value.trim()) {
    error.value = "Укажи название зала.";
    return;
  }
  if (!capacity.value || capacity.value < 1) {
    error.value = "Укажи вместимость (число >= 1).";
    return;
  }

  loading.value = true;
  try {
    await http.post("/api/halls/", {
      hall_number: number.value,
      name: name.value.trim(),
      capacity: capacity.value,
    });

    success.value = true;

    setTimeout(() => router.push("/halls"), 500);
  } catch (e) {
    console.log("ADD HALL ERROR:", e);
    error.value = parseDrfError(e);
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.card {
  max-width: 520px;
  border: 1px solid #ddd;
  padding: 12px;
  margin-top: 10px;
}

.label {
  display: block;
  margin-top: 10px;
  margin-bottom: 6px;
  font-weight: 600;
}

.input {
  width: 90%;
  padding: 10px;
  border: 1px solid teal;
}

.btn {
  padding: 8px 12px;
  border: 1px solid teal;
  background: white;
  cursor: pointer;
}
.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>