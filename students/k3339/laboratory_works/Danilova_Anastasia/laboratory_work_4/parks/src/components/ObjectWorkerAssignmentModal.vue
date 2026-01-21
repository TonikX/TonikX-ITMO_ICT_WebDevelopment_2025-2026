<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal">
      <div class="modal-header">
        <h3>{{ editingAssignment ? "Edit" : "Add" }} Worker to Object</h3>
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
              v-for="worker in availableWorkers"
              :key="worker.id"
              :value="worker.id"
            >
              {{ worker.last_name }} {{ worker.first_name }}
            </option>
          </select>
          <div v-if="loadingWorkers" class="loading-small">
            Loading workers...
          </div>
          <div
            v-if="availableWorkers.length === 0 && !loadingWorkers"
            class="hint"
          >
            No workers available to assign
          </div>
        </div>

        <div class="form-group">
          <label>Start Date *</label>
          <input
            v-model="form.start_date"
            type="date"
            class="form-control"
            required
          />
        </div>

        <div class="form-group">
          <label>End Date (Optional)</label>
          <input
            v-model="form.end_date"
            type="date"
            class="form-control"
            :class="{ 'has-end-date': form.end_date }"
          />
          <div class="hint">
            Leave empty if the worker is currently assigned
          </div>
        </div>

        <div class="form-group" v-if="editingAssignment && !form.end_date">
          <div class="warning">
            <strong>Note:</strong> This worker is currently active. Setting an
            end date will deactivate them.
          </div>
        </div>

        <div class="actions">
          <button
            type="submit"
            :disabled="saving || !form.worker || !form.start_date"
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
            {{ form.end_date ? "Delete" : "End Assignment" }}
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
  getAllWorkers,
  createObjectWorkerAssignment,
  updateObjectWorkerAssignment,
  deleteObjectWorkerAssignment,
} from "@/services/plantWorkerService";

const props = defineProps({
  objectId: {
    type: Number,
    required: true,
  },
  assignment: {
    type: Object,
    default: null,
  },
  existingAssignments: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits(["close", "updated"]);
const auth = useAuthStore();

const saving = ref(false);
const loadingWorkers = ref(false);
const allWorkers = ref([]);

const form = reactive({
  worker: "",
  start_date: new Date().toISOString().split("T")[0],
  end_date: "",
});

const editingAssignment = computed(
  () => props.assignment && props.assignment.id
);

const availableWorkers = computed(() => {
  const assignedWorkerIds = props.existingAssignments
    .map((a) => a.worker?.id)
    .filter((id) => id !== (props.assignment?.worker?.id || null));

  return allWorkers.value.filter(
    (worker) => worker && worker.id && !assignedWorkerIds.includes(worker.id)
  );
});

const initForm = () => {
  if (props.assignment) {
    form.worker = props.assignment.worker?.id || "";
    form.start_date =
      props.assignment.start_date || new Date().toISOString().split("T")[0];
    form.end_date = props.assignment.end_date || "";
  } else {
    form.worker = "";
    form.start_date = new Date().toISOString().split("T")[0];
    form.end_date = "";
  }
};

const loadAllWorkers = async () => {
  loadingWorkers.value = true;
  try {
    const workers = await getAllWorkers(auth.token);
    console.log("All workers:", workers);
    allWorkers.value = workers;
  } catch (error) {
    console.error("Error loading workers:", error);
    allWorkers.value = [];
  } finally {
    loadingWorkers.value = false;
  }
};

const submit = async () => {
  if (!form.worker || !form.start_date) {
    alert("Please select a worker and start date");
    return;
  }

  saving.value = true;
  try {
    const assignmentData = {
      object: props.objectId,
      worker_id: form.worker,
      start_date: form.start_date,
      end_date: form.end_date || null,
    };

    console.log("Submitting object worker assignment:", assignmentData);
    console.log("Using token:", auth.token ? "Token exists" : "No token");
    console.log(
      "API URL would be:",
      "http://127.0.0.1:8000/parks/objectworkers/"
    );

    if (editingAssignment.value) {
      console.log("Updating assignment ID:", props.assignment.id);
      await updateObjectWorkerAssignment(
        props.assignment.id,
        assignmentData,
        auth.token
      );
      console.log("Update successful");
    } else {
      console.log("Creating new assignment");
      await createObjectWorkerAssignment(assignmentData, auth.token);
      console.log("Create successful");
    }

    emit("updated");
    emit("close");
  } catch (error) {
    console.error("Error saving object worker assignment:", error);
    console.error("Error details:", {
      message: error.message,
      response: error.response,
      status: error.response?.status,
      data: error.response?.data,
    });

    const errorMessage =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      "Unknown error";
    alert(`Failed to save: ${errorMessage}`);
  } finally {
    saving.value = false;
  }
};

const deleteAssignment = async () => {
  if (!props.assignment?.id) return;

  const message = form.end_date
    ? "Are you sure you want to delete this assignment?"
    : "Are you sure you want to end this assignment? (This will set the end date to today)";

  if (!confirm(message)) return;

  saving.value = true;
  try {
    if (!form.end_date) {
      const today = new Date().toISOString().split("T")[0];
      await updateObjectWorkerAssignment(
        props.assignment.id,
        { end_date: today },
        auth.token
      );
    } else {
      await deleteObjectWorkerAssignment(props.assignment.id, auth.token);
    }

    emit("updated");
    emit("close");
  } catch (error) {
    console.error("Error updating/deleting assignment:", error);
    const errorMessage =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      "Unknown error";
    alert(`Failed to update/delete: ${errorMessage}`);
  } finally {
    saving.value = false;
  }
};

onMounted(async () => {
  initForm();
  await loadAllWorkers();
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

.has-end-date {
  border-color: #ff6b6b;
  background-color: #fff5f5;
}

.hint {
  font-size: 12px;
  color: #666;
  margin-top: 5px;
  font-style: italic;
}

.warning {
  padding: 10px;
  background-color: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 4px;
  color: #856404;
  font-size: 14px;
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

.danger-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
