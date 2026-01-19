<template>
  <v-card>
    <v-card-title>Who cleaned client room</v-card-title>
    <v-card-text>
      <v-form @submit.prevent="run">
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field v-model="clientId" label="Client ID" type="number" />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field v-model="date" label="Date (YYYY-MM-DD)" />
          </v-col>
        </v-row>

        <v-btn type="submit" :loading="loading">Run</v-btn>
      </v-form>

      <v-alert v-if="error" type="error" class="mt-3">{{ error }}</v-alert>

      <v-card v-if="result" variant="tonal" class="mt-3">
        <v-card-text>
          <pre>{{ result }}</pre>
        </v-card-text>
      </v-card>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref } from "vue";
import { http } from "@/api/http";
import { endpoints } from "@/api/endpoints";

const clientId = ref("");
const date = ref("");

const loading = ref(false);
const error = ref("");
const result = ref(null);

async function run() {
  loading.value = true;
  error.value = "";
  result.value = null;

  try {
    const res = await http.get(endpoints.analytics.whoCleaned, {
      params: { client_id: clientId.value, date: date.value },
    });
    result.value = JSON.stringify(res.data, null, 2);
  } catch (e) {
    error.value = JSON.stringify(e.response?.data || e.message);
  } finally {
    loading.value = false;
  }
}
</script>