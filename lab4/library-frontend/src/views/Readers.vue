<template>
  <v-container>
    <v-row class="mb-4">
      <v-col><h2>Читатели</h2></v-col>
      <v-col class="d-flex justify-end"
        ><v-btn color="primary" @click="$router.push({ name: 'reader-create' })"
          >Добавить читателя</v-btn
        ></v-col
      >
    </v-row>
    <v-simple-table>
      <thead>
        <tr>
          <th>Билет</th>
          <th>ФИО</th>
          <th>Зал</th>
          <th>Зарегистрирован</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in readers" :key="r.id">
          <td>{{ r.ticket_number }}</td>
          <td>{{ r.full_name }}</td>
          <td>{{ r.hall_name || r.hall }}</td>
          <td>{{ formatDate(r.registration_date) }}</td>
          <td>
            <v-btn small @click="$router.push({ name: 'reader-edit', params: { id: r.id } })"
              >Редактировать</v-btn
            >
            <v-btn small color="error" @click="remove(r.id)">Удалить</v-btn>
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
    return { readers: [] };
  },
  methods: {
    async load() {
      try {
        const res = await api.getReaders();
        this.readers = res.data;
      } catch (e) {
        console.error(e);
      }
    },
    formatDate(value) {
      if (!value) return "";
      return String(value).slice(0, 10);
    },
    async remove(id) {
      if (!confirm("Delete reader?")) return;
      try {
        await api.deleteReader(id);
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
