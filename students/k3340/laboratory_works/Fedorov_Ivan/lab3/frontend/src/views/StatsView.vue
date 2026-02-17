<template>
  <v-container>
    <h2 class="mb-4">Статистика</h2>

    <div class="d-flex mb-4">
      <v-btn color="primary" class="mr-2" :loading="loadingHotel" @click="loadHotel">
        Stats (Hotel)
      </v-btn>
      <v-btn color="primary" variant="outlined" :loading="loadingClient" @click="loadClient">
        Stats (Client)
      </v-btn>
    </div>

    <v-alert v-if="error" type="error" class="mb-3">{{ error }}</v-alert>

    <pre v-if="hotel" class="pa-4 mb-4" style="background:#111;color:#eee;border-radius:8px;overflow:auto;">
{{ hotel }}
</pre>

    <pre v-if="client" class="pa-4" style="background:#111;color:#eee;border-radius:8px;overflow:auto;">
{{ client }}
</pre>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import http from "../services/http";
import { EP } from "../services/endpoints";

const loadingHotel = ref(false);
const loadingClient = ref(false);
const error = ref("");
const hotel = ref(null);
const client = ref(null);

async function loadHotel() {
  loadingHotel.value = true;
  error.value = "";
  try {
    const res = await http.get(EP.statsHotel);
    hotel.value = res.data;
  } catch (e) {
    error.value = "Не удалось загрузить stats hotel (проверь EP.statsHotel)";
  } finally {
    loadingHotel.value = false;
  }
}

async function loadClient() {
  loadingClient.value = true;
  error.value = "";
  try {
    const res = await http.get(EP.statsClient);
    client.value = res.data;
  } catch (e) {
    error.value = "Не удалось загрузить stats client (проверь EP.statsClient)";
  } finally {
    loadingClient.value = false;
  }
}
</script>
