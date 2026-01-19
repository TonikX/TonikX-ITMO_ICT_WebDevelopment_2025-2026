<template>
  <v-dialog v-model="showModal" width="500" @click:outside="$emit('close')">
    <v-card>
      <v-card-title>
        {{ editingAssignment ? "Edit" : "Add" }} Worker Assignment
        <v-spacer></v-spacer>
        <v-btn icon @click="$emit('close')">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-form @submit.prevent="submit" class="pa-4">
        <v-select
          v-model="form.worker"
          :items="objectWorkers"
          item-title="name"
          item-value="id"
          label="Worker"
          required
          :loading="loadingWorkers"
          :disabled="loadingWorkers"
        >
          <template v-slot:item="{ props, item }">
            <v-list-item v-bind="props">
              <v-list-item-title>{{ item.title }}</v-list-item-title>
              <v-list-item-subtitle v-if="item.raw.phone">
                {{ item.raw.phone }}
              </v-list-item-subtitle>
            </v-list-item>
          </template>
        </v-select>

        <v-text-field
          v-model="form.date"
          type="date"
          label="Date"
          required
          class="mt-4"
        ></v-text-field>

        <div class="d-flex justify-space-between mt-6">
          <v-btn @click="$emit('close')" :disabled="saving">Cancel</v-btn>
          <v-btn
            type="submit"
            color="primary"
            :loading="saving"
            :disabled="!form.worker || !form.date"
          >
            {{ editingAssignment ? "Update" : "Assign" }}
          </v-btn>
        </div>

        <v-btn
          v-if="editingAssignment"
          @click="deleteAssignment"
          color="error"
          :loading="saving"
          class="mt-2"
        >
          Delete
        </v-btn>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from "vue";
import { useAuthStore } from "@/store/auth";
import {
  createPlantWorkerAssignment,
  updatePlantWorkerAssignment,
  deletePlantWorkerAssignment,
  getObjectWorkers,
} from "@/services/plantWorkerService";

const props = defineProps({
  plantId: {
    type: Number,
    required: true,
  },
  objectId: {
    type: Number,
    required: true,
  },
  assignment: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(["close", "updated"]);
const auth = useAuthStore();

const saving = ref(false);
const loadingWorkers = ref(false);
const objectWorkers = ref([]);
const showModal = ref(true);

const form = reactive({
  worker: "",
  date: new Date().toISOString().split("T")[0],
});

const editingAssignment = computed(
  () => props.assignment && props.assignment.id
);

const initForm = () => {
  if (props.assignment) {
    form.worker = props.assignment.worker?.id || "";
    form.date = props.assignment.date || new Date().toISOString().split("T")[0];
  } else {
    form.worker = "";
    form.date = new Date().toISOString().split("T")[0];
  }
};

const loadObjectWorkers = async () => {
  loadingWorkers.value = true;
  try {
    const workers = await getObjectWorkers(props.objectId, auth.token);

    if (Array.isArray(workers)) {
      objectWorkers.value = workers.map((worker) => ({
        id: worker.id,
        name: formatWorkerName(worker),
        phone: worker.phone_number || worker.worker?.phone_number || "",
      }));
    } else if (workers.results && Array.isArray(workers.results)) {
      objectWorkers.value = workers.results.map((worker) => ({
        id: worker.id,
        name: formatWorkerName(worker),
        phone: worker.phone_number || worker.worker?.phone_number || "",
      }));
    } else {
      objectWorkers.value = [];
    }
  } catch (error) {
    console.error("Error loading object workers:", error);
    objectWorkers.value = [];
  } finally {
    loadingWorkers.value = false;
  }
};

const formatWorkerName = (worker) => {
  const lastName = worker.last_name || worker.worker?.last_name || "";
  const firstName = worker.first_name || worker.worker?.first_name || "";
  const fullName = worker.full_name || worker.worker?.full_name || "";

  if (fullName) return fullName;
  if (lastName && firstName) return `${lastName} ${firstName}`;
  if (lastName) return lastName;
  if (firstName) return firstName;

  return `Worker #${worker.id || worker.worker?.id || "Unknown"}`;
};

const submit = async () => {
  if (!form.worker || !form.date) {
    alert("Please select a worker and date");
    return;
  }

  saving.value = true;
  try {
    const assignmentData = {
      plant_id: props.plantId,
      worker_id: parseInt(form.worker),
      date: form.date,
    };

    if (editingAssignment.value) {
      await updatePlantWorkerAssignment(
        props.assignment.id,
        assignmentData,
        auth.token
      );
    } else {
      await createPlantWorkerAssignment(assignmentData, auth.token);
    }

    emit("updated");
    emit("close");
  } catch (error) {
    console.error("Error saving worker assignment:", error);
    alert(
      `Failed to save: ${
        error.response?.data?.detail || error.message || "Unknown error"
      }`
    );
  } finally {
    saving.value = false;
  }
};

const deleteAssignment = async () => {
  if (
    !props.assignment?.id ||
    !confirm("Are you sure you want to delete this assignment?")
  ) {
    return;
  }

  saving.value = true;
  try {
    await deletePlantWorkerAssignment(props.assignment.id, auth.token);
    emit("updated");
    emit("close");
  } catch (error) {
    console.error("Error deleting assignment:", error);
    alert(
      `Failed to delete: ${
        error.response?.data?.detail || error.message || "Unknown error"
      }`
    );
  } finally {
    saving.value = false;
  }
};

onMounted(async () => {
  initForm();
  await loadObjectWorkers();
});
</script>
