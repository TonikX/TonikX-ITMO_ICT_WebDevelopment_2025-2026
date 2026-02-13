<template>
  <div>
    <h1>Vehicle models</h1>
    <div v-if="loading">Loading...</div>
    <ul v-else>
      <li v-for="vm in models" :key="vm.id">
        <strong>{{ vm.manufacturer }}</strong> — {{ vm.model }} <small v-if="vm.segment">({{ vm.segment }})</small>
      </li>
    </ul>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "VehicleModels",
  data() {
    return {
      models: [],
      loading: true,
    };
  },
  async created() {
    try {
      const res = await api.get("api/vehicle-models/");
      this.models = res.data.results || res.data;
    } catch (e) {
      console.error(e);
    } finally {
      this.loading = false;
    }
  },
};
</script>