<template>
  <div>
    <div style="display:flex; align-items:center; justify-content:space-between; gap:12px; flex-wrap:wrap;">
      <h2 style="margin:0;">Книги</h2>
      <button class="btn" @click="goHome">На главную</button>
    </div>

    <div style="display:flex; gap:10px; align-items:center; margin: 10px 0; flex-wrap: wrap;">
      <input
        class="input"
        v-model="search"
        placeholder="Поиск: название, автор, шифр..."
      />

      <button class="btn" @click="loadBooks" :disabled="loading">
        {{ loading ? "Загружаю..." : "Обновить" }}
      </button>

      <router-link class="btn link" to="/books/new">+ Добавить книгу</router-link>
    </div>

    <div v-if="error" style="color:red; white-space:pre-line; margin: 10px 0;">
      {{ error }}
    </div>

    <table v-if="filteredBooks.length" class="table">
      <thead>
        <tr>
          <th>#</th>
          <th>Название</th>
          <th>Автор(ы)</th>
          <th>Год</th>
          <th>Издательство</th>
          <th>Раздел</th>
          <th>Шифр</th>
          <th style="width: 160px;">Действия</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(b, index) in filteredBooks" :key="b.id">
          <td>{{ index + 1 }}</td>

          <td>
            <router-link :to="`/books/${b.id}`">
              {{ b.title || b.name || "Без названия" }}
            </router-link>
          </td>

          <td>{{ formatAuthors(b) }}</td>
          <td>{{ b.publication_year || "-" }}</td>
          <td>{{ b.publisher || "-" }}</td>
          <td>{{ b.section || "-" }}</td>
          <td>{{ b.current_code || "-" }}</td>

          <td>
            <router-link class="btn link" :to="`/books/${b.id}`">Открыть</router-link>
            <button class="btn danger" @click="deleteBook(b.id)">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-else-if="!loading" style="margin-top: 10px;">
      Книг пока нет (или ничего не найдено).
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { http } from "@/api/http";

const router = useRouter();

const books = ref([]);
const loading = ref(false);
const error = ref("");
const search = ref("");

function goHome() {
  router.push("/");
}

function formatAuthors(b) {
  if (Array.isArray(b.authors) && b.authors.length) {
    return b.authors.map(a => a.full_name).join(", ");
  }
  return "-";
}

async function loadBooks() {
  error.value = "";
  loading.value = true;

  try {
    const res = await http.get("/api/books/");
    books.value = res.data;
  } catch (e) {
    error.value = "Не удалось загрузить книги.\n";
  } finally {
    loading.value = false;
  }
}

const filteredBooks = computed(() => {
  const q = search.value.trim().toLowerCase();
  if (!q) return books.value;

  return books.value.filter((b) => {
    const title = String(b.title || b.name || "").toLowerCase();
    const authors = String(formatAuthors(b) || "").toLowerCase();
    const cipher = String(b.current_code || "").toLowerCase();
    return title.includes(q) || authors.includes(q) || cipher.includes(q);
  });
});

async function deleteBook(id) {
  if (!confirm("Точно удалить книгу?")) return;

  try {
    await http.delete(`/api/books/${id}/`);
    books.value = books.value.filter((b) => b.id !== id);
  } catch (e) {
    alert("Не получилось удалить.");
  }
}

onMounted(loadBooks);
</script>

<style scoped>
.input {
  width: 340px;
  padding: 10px;
  border: 1px solid teal;
}

.btn {
  padding: 3px 12px;
  border: 2px solid teal;
  background: white;
  cursor: pointer;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.link {
  text-decoration: none;
  display: inline-block;
}

.danger {
  border-color: #cc0000;
  width: 88px;
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