<template>
  <v-container>
    <h2>Зал: {{ hall?.name }}</h2>
    <p>
      <strong>Номер:</strong> {{ hall?.number }}<br />
      <strong>Вместимость (разных книг):</strong> {{ hall?.capacity }}<br />
      <strong>Сейчас книг в зале:</strong> {{ booksInHall.length }}
    </p>

    <v-row class="mb-4">
      <v-col>
        <v-btn color="primary" @click="$router.push({ name: 'hall-edit', params: { id: hallId } })">
          Редактировать зал
        </v-btn>
        <v-btn color="error" class="ml-2" @click="removeHall">Удалить зал</v-btn>
        <v-btn text class="ml-2" @click="$router.push({ name: 'halls' })">Назад к списку залов</v-btn>
      </v-col>
    </v-row>

    <h3>Книги в этом зале</h3>
    <v-simple-table>
      <thead>
        <tr>
          <th>Название</th>
          <th>Авторы</th>
          <th>Копий</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="b in booksInHall" :key="b.id">
          <td>{{ b.book_title }}</td>
          <td>{{ b.authors }}</td>
          <td>{{ b.copies }}</td>
          <td>
            <v-btn
              small
              @click="$router.push({ name: 'book-in-hall-edit', params: { id: b.id } })"
            >
              Зал / копии
            </v-btn>
            <v-btn small color="error" @click="removeBookInHall(b.id)">Удалить</v-btn>
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
    return {
      hallId: Number(this.$route.params.id),
      hall: null,
      booksInHall: [],
    };
  },
  async mounted() {
    await this.load();
  },
  methods: {
    async load() {
      try {
        const hallRes = await api.getHall(this.hallId);
        this.hall = hallRes.data;
        const booksRes = await api.getBooksInHalls();
        this.booksInHall = booksRes.data.filter((b) => b.hall === this.hallId);
      } catch (e) {
        console.error(e);
      }
    },
    async removeBookInHall(id) {
      if (!confirm("Удалить книгу из зала?")) return;
      try {
        await api.deleteBookInHall(id);
        this.load();
      } catch (e) {
        console.error(e);
      }
    },
    async removeHall() {
      if (!confirm("Удалить зал? Все записи книг в этом зале также будут удалены.")) return;
      try {
        await api.deleteHall(this.hallId);
        this.$router.push({ name: "halls" });
      } catch (e) {
        console.error(e);
      }
    },
  },
};
</script>

