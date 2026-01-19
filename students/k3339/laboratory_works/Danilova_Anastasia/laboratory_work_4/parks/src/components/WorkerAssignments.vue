<template>
  <v-card class="mb-6">
    <v-card-title>Worker Assignments</v-card-title>

    <div v-if="loading" class="text-center pa-4">Loading...</div>

    <v-table v-else-if="assignments.length">
      <thead>
        <tr>
          <th>Worker</th>
          <th>Start Date</th>
          <th>End Date</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="assignment in assignments" :key="assignment.id">
          <td>{{ assignment.worker.full_name }}</td>
          <td>{{ assignment.start_date }}</td>
          <td>{{ assignment.end_date || "Present" }}</td>
        </tr>
      </tbody>
    </v-table>

    <p v-else class="text-center pa-4">No assignments yet.</p>

    <div
      v-if="count > pageSize"
      class="d-flex justify-center align-center pa-4"
    >
      <v-btn @click="prevPage" :disabled="page === 1" class="mr-2">Prev</v-btn>
      <span>Page {{ page }}</span>
      <v-btn @click="nextPage" :disabled="page * pageSize >= count" class="ml-2"
        >Next</v-btn
      >
    </div>
  </v-card>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useAuthStore } from "@/store/auth";
import { getObjectWorkerAssignments } from "@/services/workerService";

const props = defineProps({
  objectId: {
    type: Number,
    required: true,
  },
});

const auth = useAuthStore();

const assignments = ref([]);
const count = ref(0);
const page = ref(1);
const pageSize = 15;
const loading = ref(false);

const loadAssignments = async () => {
  if (!props.objectId) return;

  loading.value = true;
  const data = await getObjectWorkerAssignments(
    props.objectId,
    auth.token,
    page.value
  );
  assignments.value = data.results;
  count.value = data.count;
  loading.value = false;
};

onMounted(loadAssignments);

watch(
  () => props.objectId,
  () => {
    page.value = 1;
    loadAssignments();
  }
);

const nextPage = () => {
  page.value++;
  loadAssignments();
};

const prevPage = () => {
  if (page.value > 1) {
    page.value--;
    loadAssignments();
  }
};
</script>
