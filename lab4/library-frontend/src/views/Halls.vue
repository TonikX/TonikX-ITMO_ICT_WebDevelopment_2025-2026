<template>
  <v-container>
    <v-row class="mb-4">
      <v-col><h2>Залы</h2></v-col>
      <v-col class="d-flex justify-end">
        <v-btn color="primary" @click="$router.push({ name: 'hall-create' })">Добавить зал</v-btn>
      </v-col>
    </v-row>

    <v-simple-table>
      <thead>
        <tr>
          <th>Номер</th>
          <th>Название</th>
          <th>Вместимость (разных книг)</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="h in halls" :key="h.id">
          <td>{{ h.number }}</td>
          <td>
            <v-btn text @click="$router.push({ name: 'hall-detail', params: { id: h.id } })">
              {{ h.name }}
            </v-btn>
          </td>
          <td>{{ h.capacity }}</td>
          <td>
            <v-btn small @click="$router.push({ name: 'hall-detail', params: { id: h.id } })">
              Открыть
            </v-btn>
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
    return { halls: [] };
  },
  methods: {
    async load() {
      try {
        const res = await api.getHalls();
        this.halls = res.data;
      } catch (e) {
        console.error(e);
      }
    },
    async remove(id) {
      if (!confirm("Удалить зал?")) return;
      try {
        await api.deleteHall(id);
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
