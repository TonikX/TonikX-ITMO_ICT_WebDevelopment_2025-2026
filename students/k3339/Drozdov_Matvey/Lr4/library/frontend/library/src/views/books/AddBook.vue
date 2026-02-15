<template>
  <div>
    <h2>Добавить книгу</h2>

    <form @submit.prevent="onSubmit">
      <div style="display:flex; flex-direction:column; gap:8px; max-width:520px;">
        <input class="input" v-model="title" placeholder="Название" />
        <input class="input" v-model="publisher" placeholder="Издательство" />
        <input class="input" v-model.number="publicationYear" type="number" placeholder="Год издания" />
        <input class="input" v-model="section" placeholder="Раздел" />

        <input class="input" v-model="code" placeholder="Шифр (текущий)" />

        <div style="margin-top:10px;">
          <div style="font-weight:600; margin-bottom:6px;">Авторы</div>

          <select class="input" v-model.number="selectedAuthorId">
            <option :value="0">-- выбрать автора --</option>
            <option v-for="a in authors" :key="a.id" :value="a.id">
              {{ a.full_name }}
            </option>
          </select>

          <button class="btn" type="button" @click="addAuthorToBook" style="margin-top:6px;">
            Добавить автора
          </button>

          <div v-if="authorIds.length" style="margin-top:10px;">
            <div>Выбрано:</div>
            <ul>
              <li v-for="id in authorIds" :key="id">
                {{ authorNameById(id) }}
                <button type="button" class="btn danger" @click="removeAuthor(id)">x</button>
              </li>
            </ul>
          </div>

          <div style="margin-top:10px;">
            <input class="input" v-model="newAuthorName" placeholder="Новый автор (ФИО)"/>
            <button class="btn" type="button" @click="createAuthor" :disabled="creatingAuthor">
              {{ creatingAuthor ? "Создаю..." : "Создать автора" }}
            </button>
          </div>
        </div>

        <button class="btn" type="submit" :disabled="loading">
          {{ loading ? "Сохраняю..." : "Сохранить книгу" }}
        </button>

        <div v-if="error" style="color:red; white-space:pre-line;">{{ error }}</div>
        <div v-if="success" style="color:green;">Книга создана!</div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { http } from "@/api/http";

const router = useRouter();

const title = ref("");
const publisher = ref("");
const publicationYear = ref(null);
const section = ref("");
const code = ref("");

const authors = ref([]);
const selectedAuthorId = ref(0);
const authorIds = ref([]);

const newAuthorName = ref("");
const creatingAuthor = ref(false);

const loading = ref(false);
const error = ref("");
const success = ref(false);

async function loadAuthors() {
  const res = await http.get("/api/authors/");
  authors.value = res.data;
}

function authorNameById(id) {
  const a = authors.value.find(x => x.id === id);
  return a ? a.full_name : `Автор #${id}`;
}

function addAuthorToBook() {
  const id = Number(selectedAuthorId.value);
  if (!id) return;
  if (!authorIds.value.includes(id)) authorIds.value.push(id);
  selectedAuthorId.value = 0;
}

function removeAuthor(id) {
  authorIds.value = authorIds.value.filter(x => x !== id);
}

async function createAuthor() {
  const name = newAuthorName.value.trim();
  if (!name) return;

  creatingAuthor.value = true;
  try {
    const res = await http.post("/api/authors/", { full_name: name });
    // добавляем в список и сразу выбираем
    authors.value.push(res.data);
    authorIds.value.push(res.data.id);
    newAuthorName.value = "";
  } catch (e) {
    console.log(e);
    alert("Не получилось создать автора.");
  } finally {
    creatingAuthor.value = false;
  }
}

async function onSubmit() {
  error.value = "";
  success.value = false;
  loading.value = true;

  try {
    // 1) создать книгу
    const bookRes = await http.post("/api/books/", {
      title: title.value,
      publisher: publisher.value,
      publication_year: publicationYear.value,
      section: section.value,
      author_ids: authorIds.value,
    });

    const bookId = bookRes.data.id;

    // 2) создать шифр 
    const c = code.value.trim();
    if (c) {
      await http.post("/api/book-codes/", {
        book: bookId,
        code: c,
      });
    }

    success.value = true;

    // можно перейти в карточку книги
    router.push(`/books/${bookId}`);
  } catch (e) {
    const data = e.response?.data;
    error.value = data ? JSON.stringify(data, null, 2) : "Не удалось создать книгу.";
  } finally {
    loading.value = false;
  }
}

onMounted(loadAuthors);
</script>

<style scoped>
.input { padding:10px; border:1px solid teal; width: 100%; }
.btn { padding:8px 12px; border:1px solid teal; background:#fff; cursor:pointer; margin-top:6px; }
.danger { border-color:#c00; margin-left:8px; }
</style>