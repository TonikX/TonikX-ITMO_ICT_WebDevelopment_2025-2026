<template>
  <v-container>
    <h2>{{ isEdit ? "Редактировать выдачу" : "Добавить выдачу" }}</h2>
    <v-form @submit.prevent="submit">
      <v-row>
        <v-col cols="12" md="6">
          <v-select
            :items="booksInHalls"
            :item-title="bookInHallLabel"
            item-value="id"
            v-model="issue.book_in_hall"
            label="Книга в зале"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-select
            :items="readers"
            item-title="full_name"
            item-value="id"
            v-model="issue.reader"
            label="Читатель"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
            v-model="issue.issue_date"
            label="Дата выдачи"
            type="date"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
            v-model="issue.return_date"
            label="Дата возврата (опционально)"
            type="date"
          />
        </v-col>
      </v-row>
      <v-row class="mt-4"
        ><v-col
          ><v-btn color="primary" @click="submit">Сохранить</v-btn
          ><v-btn text @click="$router.back()">Отмена</v-btn></v-col
        ></v-row
      >
    </v-form>
  </v-container>
</template>

<script>
import api from "../api/index.js";

export default {
  data() {
    return {
      issue: {
        book_in_hall: null,
        reader: null,
        issue_date: new Date().toISOString().slice(0, 10),
        return_date: null,
      },
      booksInHalls: [],
      readers: [],
      isEdit: false,
      menu: false,
    };
  },
  async mounted() {
    const id = this.$route.params.id;
    if (id) {
      this.isEdit = true;
      const res = await api.getIssue(id);
      this.issue = {
        book_in_hall: res.data.book_in_hall,
        reader: res.data.reader,
        issue_date: res.data.issue_date
          ? res.data.issue_date.slice(0, 10)
          : new Date().toISOString().slice(0, 10),
        return_date: res.data.return_date
          ? res.data.return_date.slice(0, 10)
          : null,
      };
    }
    await this.loadLists();
  },
  methods: {
    bookInHallLabel(item) {
      return item ? `${item.book_title} — ${item.hall_name} (${item.copies} шт.)` : "";
    },
    async loadLists() {
      try {
        const bh = await api.getBooksInHalls();
        this.booksInHalls = bh.data.filter(
          (x) => x.copies > 0 || x.id === this.issue.book_in_hall,
        );
        const r = await api.getReaders();
        this.readers = r.data;
      } catch (e) {
        console.error(e);
      }
    },
    async submit() {
      try {
        if (this.isEdit) await api.updateIssue(this.$route.params.id, this.issue);
        else await api.createIssue(this.issue);
        this.$router.push({ name: "issues" });
      } catch (e) {
        console.error(e);
      }
    },
  },
};
</script>
