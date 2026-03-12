<template>
  <v-container>
    <h2>{{ isEdit ? "Edit Book" : "Create Book" }}</h2>

    <v-form ref="form" @submit.prevent="submit">
      <v-row>
        <v-col cols="12" md="6">
          <v-text-field v-model="book.title" label="Название" required />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field v-model="book.authors" label="Авторы" />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field v-model="book.publisher" label="Издатель" />
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field v-model.number="book.year" label="Год" type="number" />
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field v-model="book.code" label="Код" />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field v-model="book.section" label="Раздел" />
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field v-model.number="book.copies" label="Копий" type="number" />
        </v-col>
        <v-col cols="12" md="6">
          <v-select
            :items="halls"
            item-title="name"
            item-value="id"
            v-model="book.hall"
            label="Зал"
          />
        </v-col>
      </v-row>

      <v-row class="mt-4">
        <v-col>
          <v-btn color="primary" @click="submit">Сохранить</v-btn>
          <v-btn text @click="$router.back()">Отмена</v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script>
import api from "../api/index.js";

export default {
  data() {
    return {
      book: {
        title: "",
        authors: "",
        publisher: "",
        year: null,
        section: "",
        code: "",
        copies: 1,
        hall: null,
      },
      halls: [],
      isEdit: false,
    };
  },
  async mounted() {
    const id = this.$route.params.id;
    await this.loadHalls();
    if (id) {
      this.isEdit = true;
      try {
        const res = await api.getBook(id);
        this.book = {
          title: res.data.title,
          authors: res.data.authors,
          publisher: res.data.publisher,
          year: res.data.year,
          section: res.data.section,
          code: res.data.code,
          copies: res.data.copies,
          hall: res.data.hall,
        };
      } catch (e) {
        console.error(e);
      }
    }
  },
  methods: {
    async loadHalls() {
      try {
        const res = await api.getHalls();
        this.halls = res.data;
      } catch (e) {
        console.error(e);
      }
    },
    async submit() {
      try {
        if (this.isEdit) {
          await api.updateBook(this.$route.params.id, this.book);
        } else {
          const bookRes = await api.createBook({
            title: this.book.title,
            authors: this.book.authors,
            publisher: this.book.publisher,
            year: this.book.year,
            section: this.book.section,
            code: this.book.code,
          });
          const bookId = bookRes.data.id;
          if (this.book.hall && bookId) {
            await api.createBookInHall({
              book: bookId,
              hall: this.book.hall,
              copies: this.book.copies ?? 1,
            });
          }
        }
        this.$router.push({ name: "books" });
      } catch (e) {
        console.error(e);
      }
    },
  },
};
</script>
