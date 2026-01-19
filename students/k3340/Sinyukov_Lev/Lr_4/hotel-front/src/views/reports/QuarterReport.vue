<template>
  <v-card>
    <v-card-title>Quarter report</v-card-title>
    <v-card-text>
      <v-form @submit.prevent="run" class="d-flex ga-2 align-end">
        <v-select v-model="q" :items="[1,2,3,4]" label="Quarter" />
        <v-btn type="submit" :loading="loading">Run</v-btn>
      </v-form>

      <v-alert v-if="error" type="error" class="mt-3">{{ error }}</v-alert>

      <v-card v-if="result" variant="tonal" class="mt-3">
        <v-card-text><pre>{{ result }}</pre></v-card-text>
      </v-card>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref } from "vue";
import { http } from "@/api/http";
import { endpoints } from "@/api/endpoints";

const q = ref(1);
const loading = ref(false);
const error = ref("");
const result = ref(null);

async function run() {
  loading.value = true;
  error.value = "";
  result.value = null;

  try {
    const res = await http.get(endpoints.reports.quarter, { params: { q: q.value } });
    result.value = JSON.stringify(res.data, null, 2);
  } catch (e) {
    error.value = JSON.stringify(e.response?.data || e.message);
  } finally {
    loading.value = false;
  }
}
</script>