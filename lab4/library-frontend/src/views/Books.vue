<template>
  <v-container>
    <v-row class="mb-4">
      <v-col>
        <h2>Книги</h2>
      </v-col>
      <v-col class="d-flex justify-end">
        <v-btn color="primary" @click="$router.push({ name: 'book-create' })">Добавить книгу</v-btn>
      </v-col>
    </v-row>

    <v-simple-table>
      <thead>
        <tr>
          <th>Название</th>
          <th>Авторы</th>
          <th>Зал</th>
          <th>Копий</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in booksInHalls" :key="item.id">
          <td>{{ item.book_title }}</td>
          <td>{{ item.authors || "-" }}</td>
          <td>{{ item.hall_name }}</td>
          <td>{{ item.copies }}</td>
          <td>
            <v-btn small @click="$router.push({ name: 'book-edit', params: { id: item.book } })"
              >Редактировать книгу</v-btn
            >
            <v-btn small @click="$router.push({ name: 'book-in-hall-edit', params: { id: item.id } })"
              >Зал / копии</v-btn
            >
            <v-btn small color="error" @click="remove(item.id)">Удалить</v-btn>
          </td>
        </tr>
      </tbody>
    </v-simple-table>
  </v-container>
</template>

<script>
import api from "../api/index.js";

export default {
  data() {
    return { booksInHalls: [] };
  },
  methods: {
    async load() {
      try {
        const res = await api.getBooksInHalls();
        this.booksInHalls = res.data;
      } catch (e) {
        console.error(e);
      }
    },
    async remove(id) {
      if (!confirm("Удалить запись о книге в зале?")) return;
      try {
        await api.deleteBookInHall(id);
        this.load();
      } catch (e) {
        console.error(e);
      }
    },
  },
  mounted() {
    this.load();
  },
};
</script>
