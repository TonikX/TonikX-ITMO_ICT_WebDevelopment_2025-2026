<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal">
      <div class="modal-header">
        <h3>{{ editingAssignment ? "Edit" : "Add" }} Worker Assignment</h3>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>

      <form @submit.prevent="submit">
        <div class="form-group">
          <label>Worker *</label>
          <select
            v-model="form.worker"
            class="form-control"
            required
            :disabled="loadingWorkers"
          >
            <option value="">Select worker</option>
            <option
              v-for="workerItem in objectWorkers"
              :key="workerItem.id"
              :value="workerItem.worker?.id || workerItem.id"
            >
              {{ formatWorkerName(workerItem) }}
              <template v-if="getWorkerPhone(workerItem)">
                ({{ getWorkerPhone(workerItem) }})
              </template>
              <template v-if="workerItem.start_date">
                - Assigned: {{ formatDateShort(workerItem.start_date) }}
              </template>
            </option>
          </select>
          <div v-if="loadingWorkers" class="loading-small">
            Loading workers...
          </div>
          <div
            v-if="objectWorkers.length === 0 && !loadingWorkers"
            class="hint"
          >
            No workers assigned to this object. Please add workers through
            Object settings first.
          </div>
          <div v-else-if="objectWorkers.length > 0" class="hint">
            Showing {{ objectWorkers.length }} worker(s) assigned to this object
          </div>
        </div>

        <div class="form-group">
          <label>Date *</label>
          <input
            v-model="form.date"
            type="date"
            class="form-control"
            required
          />
        </div>

        <div class="actions">
          <button
            type="submit"
            :disabled="saving || !form.worker || !form.date"
            class="primary-btn"
          >
            {{ saving ? "Saving..." : editingAssignment ? "Update" : "Assign" }}
          </button>
          <button
            type="button"
            @click="$emit('close')"
            :disabled="saving"
            class="secondary-btn"
          >
            Cancel
          </button>
          <button
            v-if="editingAssignment"
            type="button"
            @click="deleteAssignment"
            :disabled="saving"
            class="danger-btn"
          >
            Delete
          </button>
        </div>
      </form>
    </div>
  </div>
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
  notes: "",
});

const editingAssignment = computed(
  () => props.assignment && props.assignment.id
);

const formatWorkerName = (worker) => {
  if (!worker) return "Unknown Worker";

  const lastName = worker.last_name || worker.worker?.last_name || "";
  const firstName = worker.first_name || worker.worker?.first_name || "";
  const fullName = worker.full_name || worker.worker?.full_name || "";

  if (fullName) return fullName;

  if (lastName && firstName) {
    return `${lastName} ${firstName}`;
  } else if (lastName) {
    return lastName;
  } else if (firstName) {
    return firstName;
  }

  return `Worker #${worker.id || worker.worker?.id || "Unknown"}`;
};

const getWorkerPhone = (worker) => {
  return worker.phone_number || worker.worker?.phone_number || "";
};

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
    console.log(`Loading workers for object ${props.objectId}...`);
    const workers = await getObjectWorkers(props.objectId, auth.token);

    console.log("=== API RESPONSE STRUCTURE ===");
    console.log("Full response:", workers);
    console.log("Is array?", Array.isArray(workers));
    console.log("Has results?", workers.results);
    console.log("First item structure:", workers[0] || workers.results?.[0]);

    if (Array.isArray(workers)) {
      objectWorkers.value = workers;
    } else if (workers.results && Array.isArray(workers.results)) {
      objectWorkers.value = workers.results;
    } else if (workers && typeof workers === "object") {
      objectWorkers.value = [workers];
    } else {
      objectWorkers.value = [];
    }

    console.log("=== PROCESSED WORKERS ===");
    console.log("Count:", objectWorkers.value.length);
    objectWorkers.value.forEach((worker, index) => {
      console.log(`Worker ${index}:`, worker);
      console.log(`  - ID: ${worker.id}`);
      console.log(`  - Worker object:`, worker.worker);
      console.log(`  - Last name: ${worker.worker?.last_name}`);
      console.log(`  - First name: ${worker.worker?.first_name}`);
    });
  } catch (error) {
    console.error("Error loading object workers:", error);
    console.error("Error response:", error.response?.data);
    objectWorkers.value = [];
  } finally {
    loadingWorkers.value = false;
  }
};

const submit = async () => {
  console.log("=== SUBMIT START ===");
  console.log("Plant ID from props:", props.plantId);
  console.log("Plant ID type:", typeof props.plantId);
  console.log("Form worker:", form.worker);
  console.log("Form date:", form.date);

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

    console.log("Assignment data to send:", assignmentData);
    console.log("Plant ID in assignment data:", assignmentData.plant_id);
    console.log("Worker ID in assignment data:", assignmentData.worker_id);

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

    if (error.response && error.response.status === 400) {
      console.error("Validation errors:", error.response.data);

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

const formatDateShort = (dateString) => {
  if (!dateString) return "";
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  } catch (error) {
    console.error("Error formatting date:", error);
    return dateString;
  }
};

onMounted(async () => {
  initForm();
  await loadObjectWorkers();
});
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

form {
  padding: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #333;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-control:focus {
  outline: none;
  border-color: #4dabf7;
  box-shadow: 0 0 0 2px rgba(77, 171, 247, 0.1);
}

.form-control:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.hint {
  font-size: 12px;
  color: #666;
  margin-top: 5px;
  padding: 8px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.loading-small {
  font-size: 12px;
  color: #666;
  margin-top: 5px;
}

.actions {
  display: flex;
  gap: 10px;
  margin-top: 30px;
}

.primary-btn {
  background-color: #4dabf7;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.primary-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.secondary-btn {
  background-color: #f0f0f0;
  color: #333;
  border: 1px solid #ddd;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.danger-btn {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.danger-btn:hover {
  background-color: #c82333;
}

textarea.form-control {
  resize: vertical;
  min-height: 80px;
}
</style>
