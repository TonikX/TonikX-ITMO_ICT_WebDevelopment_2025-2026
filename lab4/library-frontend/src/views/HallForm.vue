<template>
  <v-container>
    <h2>{{ isEdit ? "Редактировать зал" : "Добавить зал" }}</h2>
    <v-form @submit.prevent="submit">
      <v-row>
        <v-col cols="12" md="4"><v-text-field v-model.number="hall.number" label="Номер" /></v-col>
        <v-col cols="12" md="4"><v-text-field v-model="hall.name" label="Название" /></v-col>
        <v-col cols="12" md="4"
          ><v-text-field v-model.number="hall.capacity" label="Вместимость"
        /></v-col>
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
    return { hall: { number: null, name: "", capacity: null }, isEdit: false };
  },
  async mounted() {
    const id = this.$route.params.id;
    if (id) {
      this.isEdit = true;
      const res = await api.getHall(id);
      this.hall = res.data;
    }
  },
  methods: {
    async submit() {
      try {
        if (this.isEdit) await api.updateHall(this.$route.params.id, this.hall);
        else await api.createHall(this.hall);
        this.$router.push({ name: "halls" });
      } catch (e) {
        console.error(e);
      }
    },
  },
};
</script>
