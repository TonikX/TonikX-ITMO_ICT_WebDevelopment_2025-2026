<template>
  <v-container>
    <h2>{{ isEdit ? "Редактировать читателя" : "Добавить читателя" }}</h2>
    <v-form @submit.prevent="submit">
      <v-row>
        <v-col cols="12" md="6"
          ><v-text-field v-model="reader.ticket_number" label="Номер билета"
        /></v-col>
        <v-col cols="12" md="6"
          ><v-text-field v-model="reader.full_name" label="Полное имя"
        /></v-col>
        <v-col cols="12" md="6"
          ><v-text-field v-model="reader.passport_number" label="Номер паспорта"
        /></v-col>
        <v-col cols="12" md="6"><v-text-field v-model="reader.phone" label="Телефон" /></v-col>
        <v-col cols="12" md="6"><v-text-field v-model="reader.address" label="Адрес" /></v-col>
        <v-col cols="12" md="6">
          <v-text-field
            v-model="reader.birth_date"
            label="Дата рождения"
            type="date"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-select
            :items="halls"
            item-title="name"
            item-value="id"
            v-model="reader.hall"
            label="Hall"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-select
            v-model="reader.education"
            :items="educationOptions"
            item-title="label"
            item-value="value"
            label="Образование"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-switch
            v-model="reader.academic_degree"
            label="Имеет ученую степень"
          />
        </v-col>
      </v-row>
      <v-row class="mt-4"
        ><v-col
          ><v-btn color="primary" @click="submit">Save</v-btn
          ><v-btn text @click="$router.back()">Cancel</v-btn></v-col
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
      reader: {
        ticket_number: "",
        full_name: "",
        passport_number: "",
        birth_date: "",
        address: "",
        phone: "",
        education: "",
        academic_degree: false,
        hall: null,
      },
      halls: [],
      isEdit: false,
      menu: false,
      educationOptions: [
        { label: "Начальное", value: "primary" },
        { label: "Среднее", value: "secondary" },
        { label: "Высшее", value: "higher" },
      ],
    };
  },
  async mounted() {
    await this.loadHalls();
    const id = this.$route.params.id;
    if (id) {
      this.isEdit = true;
      const res = await api.getReader(id);
      this.reader = res.data;
      if (this.reader.birth_date) {
        this.reader.birth_date = this.reader.birth_date.slice(0, 10);
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
        if (this.isEdit) await api.updateReader(this.$route.params.id, this.reader);
        else await api.createReader(this.reader);
        this.$router.push({ name: "readers" });
      } catch (e) {
        console.error(e);
      }
    },
  },
};
</script>
