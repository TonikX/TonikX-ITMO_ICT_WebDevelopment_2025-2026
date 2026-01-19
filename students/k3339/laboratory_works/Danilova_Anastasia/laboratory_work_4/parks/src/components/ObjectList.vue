<template>
  <v-card>
    <v-card-title>
      Objects
      <v-spacer></v-spacer>
      <span v-if="!loading">Total: {{ count }}</span>
    </v-card-title>

    <div v-if="loading" class="text-center pa-4">
      <v-progress-circular indeterminate></v-progress-circular>
      <p>Loading parks...</p>
    </div>

    <v-table v-else-if="objects.length">
      <thead>
        <tr>
          <th>#</th>
          <th>Name</th>
          <th>Address</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="object in objects" :key="object.id">
          <td>
            <v-chip>{{ object.id }}</v-chip>
          </td>
          <td>
            <v-btn @click="emit('select', object)" variant="text">
              {{ object.name }}
            </v-btn>
          </td>
          <td>{{ object.address }}</td>
          <td>
            <v-btn @click="handleDelete(object)" color="error" size="small">
              Delete
            </v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>

    <div v-else class="text-center pa-4">
      <p>No parks found</p>
    </div>

    <div v-if="objects.length" class="d-flex justify-center align-center pa-4">
      <v-btn @click="prevPage" :disabled="page === 1">Previous</v-btn>
      <span class="mx-4">Page {{ page }} of {{ Math.ceil(count / 15) }}</span>
      <v-btn @click="nextPage" :disabled="page * 15 >= count">Next</v-btn>
    </div>
  </v-card>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useAuthStore } from "@/store/auth";
import { getObjects, deleteObject } from "@/services/objectsService";

const emit = defineEmits(["select", "deleted"]);
const auth = useAuthStore();

const objects = ref([]);
const page = ref(1);
const count = ref(0);
const loading = ref(false);

const loadObjects = async () => {
  loading.value = true;
  try {
    const data = await getObjects(auth.token, page.value);
    objects.value = data.results;
    count.value = data.count;
  } catch (error) {
    console.error("Error loading objects:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(loadObjects);

const nextPage = () => {
  page.value++;
  loadObjects();
};

const prevPage = () => {
  if (page.value > 1) {
    page.value--;
    loadObjects();
  }
};

const handleDelete = async (object) => {
  if (!confirm(`Are you sure you want to delete "${object.name}"?`)) {
    return;
  }

  try {
    await deleteObject(object.id, auth.token);
    objects.value = objects.value.filter((obj) => obj.id !== object.id);
    count.value -= 1;
    emit("deleted", object.id);

    if (objects.value.length === 0 && page.value > 1) {
      page.value--;
      loadObjects();
    }
  } catch (error) {
    console.error("Error deleting object:", error);
    alert("Failed to delete object");
  }
};
</script>
