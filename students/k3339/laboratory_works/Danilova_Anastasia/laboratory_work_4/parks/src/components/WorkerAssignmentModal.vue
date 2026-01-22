<template>
  <v-dialog
    :model-value="true"
    @update:model-value="$emit('close')"
    max-width="500"
  >
    <v-card>
      <v-card-title class="d-flex justify-space-between align-center">
        <span>{{ editingAssignment ? "Edit" : "Add" }} Worker Assignment</span>
        <v-btn icon @click="$emit('close')">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text>
        <v-form @submit.prevent="submit">
          <v-select
            v-model="form.worker"
            label="Worker *"
            :items="processedWorkers"
            item-title="displayText"
            item-value="id"
            :loading="loadingWorkers"
            required
            class="mb-4"
          >
            <template v-if="loadingWorkers" #progress>
              Loading workers...
            </template>
            <template
              v-if="objectWorkers.length === 0 && !loadingWorkers"
              #details
            >
              No workers assigned to this object. Please add workers through
              Object settings first.
            </template>
            <template v-else-if="objectWorkers.length > 0" #details>
              Showing {{ objectWorkers.length }} worker(s) assigned to this
              object
            </template>
          </v-select>

          <v-text-field
            v-model="form.date"
            label="Date *"
            type="date"
            required
            class="mb-4"
          ></v-text-field>

          <v-card-actions class="px-0">
            <v-btn
              type="submit"
              :disabled="saving || !form.worker || !form.date"
              color="primary"
            >
              {{
                saving ? "Saving..." : editingAssignment ? "Update" : "Assign"
              }}
            </v-btn>
            <v-btn @click="$emit('close')" :disabled="saving"> Cancel </v-btn>
            <v-btn
              v-if="editingAssignment"
              @click="deleteAssignment"
              :disabled="saving"
              color="error"
            >
              Delete
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card-text>
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

const form = reactive({
  worker: "",
  date: new Date().toISOString().split("T")[0],
});

const editingAssignment = computed(
  () => props.assignment && props.assignment.id
);

const processedWorkers = computed(() => {
  return objectWorkers.value.map((item) => {
    const worker = item.worker || item;
    const lastName = worker.last_name || "";
    const firstName = worker.first_name || "";
    const fullName = worker.full_name || `${lastName} ${firstName}`.trim();
    const phone = worker.phone_number || "";
    const startDate = item.start_date || "";

    let displayText = fullName;
    if (phone) displayText += ` (${phone})`;
    if (startDate) {
      const date = new Date(startDate);
      displayText += ` - Assigned: ${date.toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
      })}`;
    }

    return {
      id: worker.id || item.id,
      displayText: displayText,
    };
  });
});

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
      objectWorkers.value = workers;
    } else if (workers.results && Array.isArray(workers.results)) {
      objectWorkers.value = workers.results;
    } else if (workers && typeof workers === "object") {
      objectWorkers.value = [workers];
    } else {
      objectWorkers.value = [];
    }
  } catch (error) {
    objectWorkers.value = [];
  } finally {
    loadingWorkers.value = false;
  }
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
    if (error.response && error.response.status === 400) {
      let errorMessage = "Validation errors:\n";
      for (const [field, errors] of Object.entries(error.response.data)) {
        errorMessage += `- ${field}: ${
          Array.isArray(errors) ? errors.join(", ") : errors
        }\n`;
      }
      alert(errorMessage);
    } else {
      alert(
        `Failed to save: ${
          error.response?.data?.detail || error.message || "Unknown error"
        }`
      );
    }
  } finally {
    saving.value = false;
  }
};

const deleteAssignment = async () => {
  if (!props.assignment?.id) return;

  if (!confirm("Are you sure you want to delete this assignment?")) return;

  saving.value = true;
  try {
    await deletePlantWorkerAssignment(props.assignment.id, auth.token);
    emit("updated");
    emit("close");
  } catch (error) {
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

<style scoped></style>
