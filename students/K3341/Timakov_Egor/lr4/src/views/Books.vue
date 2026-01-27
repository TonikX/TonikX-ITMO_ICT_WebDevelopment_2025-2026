<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span class="text-h5">Книги</span>
            <v-btn color="primary" @click="openDialog()">
              <v-icon start>mdi-plus</v-icon>
              Добавить книгу
            </v-btn>
          </v-card-title>

          <v-card-text>
            <v-text-field
                v-model="search"
                label="Поиск по названию книги"
                prepend-inner-icon="mdi-magnify"
                variant="outlined"
                class="mb-4"
                @input="loadBooks"
            />

            <v-data-table
                :headers="headers"
                :items="books"
                :loading="loading"
                no-data-text="Нет доступных книг."
                item-key="id"
            >
              <template #item.title="{ item }">{{ item.title }}</template>

              <template #item.status_display="{ item }">
                <v-chip :color="getStatusColor(item.status)" small>
                  {{ item.status_display }}
                </v-chip>
              </template>

              <template #item.actions="{ item }">
                <v-btn icon="mdi-pencil" size="small" @click="openDialog(item)">
                  Редактировать
                </v-btn>
                <v-btn
                    icon="mdi-delete"
                    size="small"
                    color="error"
                    @click="deleteBook(item)"
                >
                  Удалить
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Диалог добавления/редактирования -->
    <v-dialog v-model="dialog" max-width="800">
      <v-card>
        <v-card-title>
          <span>{{ editingItem ? "Редактировать книгу" : "Добавить книгу" }}</span>
        </v-card-title>

        <v-card-text>
          <v-form ref="formRef">
            <v-text-field v-model="form.title" label="Название книги" outlined required />
            <v-text-field v-model="form.isbn" label="ISBN" outlined />

            <v-select
                v-model="form.author_ids"
                :items="authors"
                item-title="full_name"
                item-value="id"
                label="Авторы книги"
                multiple
                outlined
                required
            />

            <v-select
                v-model="form.editor_id"
                :items="editors"
                item-title="user?.username"
                item-value="id"
                label="Редактор (необязательно)"
                outlined
            />

            <v-text-field
                v-model="form.pages"
                label="Количество страниц"
                type="number"
                outlined
                required
            />
            <v-text-field
                v-model="form.publication_date"
                label="Дата публикации"
                type="date"
                outlined
            />
            <v-text-field
                v-model="form.print_date"
                label="Дата печати"
                type="date"
                outlined
            />
            <v-text-field
                v-model="form.print_run"
                label="Тираж"
                type="number"
                outlined
                required
            />
            <v-text-field
                v-model="form.price"
                label="Цена"
                type="number"
                outlined
                required
            />
            <v-text-field
                v-model="form.cost"
                label="Себестоимость"
                type="number"
                outlined
                required
            />
            <v-select
                v-model="form.status"
                :items="statuses"
                item-title="title"
                item-value="value"
                label="Статус"
                outlined
                required
            />

            <v-textarea v-model="form.description" label="Описание" outlined />
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-btn color="error" text @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" text @click="saveBook">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { ref, reactive, onMounted } from "vue";
import { booksApi } from "@/services/api";

export default {
  setup() {
    const books = ref([]);
    const authors = ref([]);
    const editors = ref([]); // при необходимости подгрузите, сейчас опционально
    const dialog = ref(false);
    const loading = ref(false);
    const editingItem = ref(null);
    const search = ref("");

    // Поля, ожидаемые сериализатором BookDetailSerializer
    const form = reactive({
      title: "",
      isbn: "",
      author_ids: [],
      editor_id: null,
      pages: 1,
      publication_date: "", // YYYY-MM-DD или пусто -> null
      print_date: "",
      print_run: 1,
      price: "0.00", // Decimal как строка
      cost: "0.00",  // Decimal как строка
      status: "draft",
      description: "",
    });

    const statuses = [
      { title: "Черновик", value: "draft" },
      { title: "Редактирование", value: "editing" },
      { title: "Дизайн", value: "design" },
      { title: "Печать", value: "printing" },
      { title: "Опубликована", value: "published" },
      { title: "Архив", value: "archived" },
    ];

    const headers = [
      { text: "Название", value: "title" },
      { text: "Статус", value: "status_display" },
      { text: "Действия", value: "actions", align: "center", sortable: false },
    ];

    const getStatusColor = (status) => {
      const colors = {
        draft: "grey",
        editing: "blue",
        design: "purple",
        printing: "orange",
        published: "green",
        archived: "red",
      };
      return colors[status] || "grey";
    };

    const loadBooks = async () => {
      loading.value = true;
      try {
        const response = await booksApi.getAll({ search: search.value });
        books.value = response.data?.results ?? response.data ?? [];

        // Уникальные авторы из всех книг
        const map = new Map();
        books.value.forEach((b) => {
          (b.authors || []).forEach((a) => {
            if (!map.has(a.id)) map.set(a.id, a);
          });
        });
        authors.value = Array.from(map.values());
      } catch (e) {
        console.error("Ошибка загрузки книг:", e?.response?.data ?? e);
      } finally {
        loading.value = false;
      }
    };

    const openDialog = (item = null) => {
      resetForm();
      editingItem.value = item || null;
      if (item) {
        Object.assign(form, {
          title: item.title ?? "",
          isbn: item.isbn ?? "",
          author_ids: (item.authors || []).map((a) => a.id),
          editor_id: item.editor?.id ?? null,
          pages: item.pages ?? 1,
          publication_date: item.publication_date ?? "",
          print_date: item.print_date ?? "",
          print_run: item.print_run ?? 1,
          price: item.price != null ? String(item.price) : "0.00",
          cost: item.cost != null ? String(item.cost) : "0.00",
          status: item.status ?? "draft",
          description: item.description ?? "",
        });
      }
      dialog.value = true;
    };

    const closeDialog = () => {
      dialog.value = false;
      resetForm();
    };

    const resetForm = () => {
      editingItem.value = null;
      Object.assign(form, {
        title: "",
        isbn: "",
        author_ids: [],
        editor_id: null,
        pages: 1,
        publication_date: "",
        print_date: "",
        print_run: 1,
        price: "0.00",
        cost: "0.00",
        status: "draft",
        description: "",
      });
    };

    const normalizeDate = (d) => (d && d.trim() ? d : null);

    const saveBook = async () => {
      try {
        // Клиентская проверка минимально необходимых полей
        if (!form.title.trim()) {
          alert("Название обязательно");
          return;
        }
        if (!form.author_ids.length) {
          alert("Укажите хотя бы одного автора");
          return;
        }
        if (Number(form.pages) < 1 || Number(form.print_run) < 1) {
          alert("Страницы и тираж должны быть >= 1");
          return;
        }

        const payload = {
          title: form.title.trim(),
          isbn: form.isbn?.trim() || null,
          author_ids: form.author_ids,         // write_only -> authors
          editor_id: form.editor_id || null,   // optional
          pages: Number(form.pages),
          publication_date: normalizeDate(form.publication_date), // null если пусто
          print_date: normalizeDate(form.print_date),
          print_run: Number(form.print_run),
          price: String(form.price ?? "0.00"),
          cost: String(form.cost ?? "0.00"),
          status: form.status,
          description: form.description || "",
        };

        console.log("Отправка в API:", payload);

        if (editingItem.value) {
          await booksApi.update(editingItem.value.id, payload);
        } else {
          await booksApi.create(payload);
        }

        dialog.value = false;
        await loadBooks();
      } catch (e) {
        console.error("Ошибка сохранения:", e?.response?.data ?? e);
        const msg = e?.response?.data
            ? JSON.stringify(e.response.data, null, 2)
            : "Сервер недоступен или неверный формат данных.";
        alert(`Ошибка сохранения:\n${msg}`);
      }
    };

    const deleteBook = async (item) => {
      if (!confirm("Удалить книгу?")) return;
      try {
        await booksApi.delete(item.id);
        await loadBooks();
      } catch (e) {
        console.error("Ошибка удаления:", e?.response?.data ?? e);
        alert("Ошибка удаления книги.");
      }
    };

    onMounted(loadBooks);

    return {
      books,
      authors,
      editors,
      dialog,
      loading,
      editingItem,
      search,
      form,
      headers,
      statuses,
      getStatusColor,
      loadBooks,
      openDialog,
      closeDialog,
      saveBook,
      deleteBook,
    };
  },
};
</script>