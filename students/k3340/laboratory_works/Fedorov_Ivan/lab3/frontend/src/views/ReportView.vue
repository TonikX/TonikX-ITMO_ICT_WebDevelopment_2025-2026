<template>
  <v-container>
    <h2 class="mb-4">Отчет за квартал</h2>

    <v-row>
      <v-col cols="12" sm="4">
        <v-text-field v-model.number="quarter" label="Квартал (1-4)" type="number" />
      </v-col>
      <v-col cols="12" sm="4">
        <v-text-field v-model.number="year" label="Год" type="number" />
      </v-col>
      <v-col cols="12" sm="4" class="d-flex align-end">
        <v-btn color="primary" :loading="loading" @click="loadReport">Сформировать</v-btn>
      </v-col>
    </v-row>

    <v-alert v-if="error" type="error" class="my-3">{{ error }}</v-alert>

    <pre v-if="report" class="pa-4" style="background:#111;color:#eee;border-radius:8px;overflow:auto;">
{{ report }}
</pre>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import http from "../services/http";
import { EP } from "../services/endpoints";

const quarter = ref(4);
const year = ref(new Date().getFullYear());
const loading = ref(false);
const error = ref("");
const report = ref(null);

async function loadReport() {
  loading.value = true;
  error.value = "";
  report.value = null;
  try {
    const res = await http.get(EP.report, { params: { quarter: quarter.value, year: year.value } });
    report.value = res.data;
  } catch (e) {
    error.value = "Не удалось получить отчет (проверь EP.report)";
  } finally {
    loading.value = false;
  }
}
</script>
