<template>
  <v-container>
    <v-row class="mb-4">
      <v-col><h2>Выдачи книг</h2></v-col>
      <v-col class="d-flex justify-end"
        ><v-btn color="primary" @click="$router.push({ name: 'issue-create' })"
          >Добавить выдачу</v-btn
        ></v-col
      >
    </v-row>
    <v-simple-table>
      <thead>
        <tr>
          <th>Книга</th>
          <th>Читатель</th>
          <th>Дата выдачи</th>
          <th>Дата возврата</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="i in issues" :key="i.id">
          <td>{{ i.book_title || (i.book && i.book.title) }}</td>
          <td>{{ i.reader_name || (i.reader && i.reader.full_name) }}</td>
          <td>{{ formatDate(i.issue_date) }}</td>
          <td>{{ formatDate(i.return_date) }}</td>
          <td>
            <v-btn small @click="$router.push({ name: 'issue-edit', params: { id: i.id } })"
              >Редактировать</v-btn
            >
            <v-btn small color="error" @click="remove(i.id)">Удалить</v-btn>
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
    return { issues: [] };
  },
  methods: {
    async load() {
      try {
        const res = await api.getIssues();
        this.issues = res.data;
      } catch (e) {
        console.error(e);
      }
    },
    formatDate(value) {
      if (!value) return "";
      return String(value).slice(0, 10);
    },
    async remove(id) {
      if (!confirm("Delete issue?")) return;
      try {
        await api.deleteIssue(id);
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
