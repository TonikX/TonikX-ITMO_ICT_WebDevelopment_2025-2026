<template>
  <v-container>
    <h2>Редактировать книгу в зале</h2>
    <v-form @submit.prevent="submit">
      <v-row>
        <v-col cols="12" md="6">
          <v-text-field :model-value="bookTitle" label="Книга" readonly />
        </v-col>
        <v-col cols="12" md="6">
          <v-select
            v-model="form.hall"
            :items="halls"
            item-title="name"
            item-value="id"
            label="Зал"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
            v-model.number="form.copies"
            label="Количество копий"
            type="number"
            min="0"
          />
        </v-col>
      </v-row>
      <v-row class="mt-4">
        <v-col>
          <v-btn color="primary" @click="submit">Сохранить</v-btn>
          <v-btn text @click="$router.push({ name: 'books' })">Отмена</v-btn>
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
      form: { hall: null, copies: 0 },
      halls: [],
      bookTitle: "",
    };
  },
  async mounted() {
    const id = this.$route.params.id;
    try {
      const res = await api.getBookInHall(id);
      this.form = {
        hall: res.data.hall,
        copies: res.data.copies,
      };
      this.bookTitle = res.data.book_title;
      const h = await api.getHalls();
      this.halls = h.data;
    } catch (e) {
      console.error(e);
    }
  },
  methods: {
    async submit() {
      try {
        await api.updateBookInHall(this.$route.params.id, this.form);
        this.$router.push({ name: "books" });
      } catch (e) {
        console.error(e);
      }
    },
  },
};
</script>
