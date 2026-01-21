<template>
  <v-dialog
    :model-value="true"
    @update:model-value="$emit('close')"
    max-width="600"
  >
    <v-card>
      <v-card-title class="d-flex justify-space-between">
        <span>{{ editingAssignment ? "Edit" : "Add" }} Worker to Object</span>
        <v-btn icon @click="$emit('close')">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text>
        <v-form @submit.prevent="submit">
          <v-select
            v-model="form.worker"
            label="Worker *"
            :items="availableWorkers"
            item-title="name"
            item-value="id"
            :loading="loadingWorkers"
            required
            class="mb-4"
          >
            <template v-if="loadingWorkers" #progress>
              Loading workers...
            </template>
            <template
              v-if="availableWorkers.length === 0 && !loadingWorkers"
              #details
            >
              No workers available to assign
            </template>
          </v-select>

          <v-text-field
            v-model="form.start_date"
            label="Start Date *"
            type="date"
            required
            class="mb-4"
          ></v-text-field>

          <v-text-field
            v-model="form.end_date"
            label="End Date (Optional)"
            type="date"
            :class="{ 'has-end-date': form.end_date }"
            class="mb-2"
          ></v-text-field>
          <p class="text-caption text-medium-emphasis mb-4">
            Leave empty if the worker is currently assigned
          </p>

          <v-alert
            v-if="editingAssignment && !form.end_date"
            type="warning"
            density="compact"
            class="mb-4"
          >
            <strong>Note:</strong> This worker is currently active. Setting an
            end date will deactivate them.
          </v-alert>

          <v-card-actions class="px-0">
            <v-btn
              type="submit"
              :disabled="saving || !form.worker || !form.start_date"
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
              {{ form.end_date ? "Delete" : "End Assignment" }}
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

  return allWorkers.value
    .filter(
      (worker) => worker && worker.id && !assignedWorkerIds.includes(worker.id)
    )
    .map((worker) => ({
      ...worker,
      name: `${worker.last_name} ${worker.first_name}`,
    }));
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
    allWorkers.value = workers;
  } catch (error) {
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

    if (editingAssignment.value) {
      await updateObjectWorkerAssignment(
        props.assignment.id,
        assignmentData,
        auth.token
      );
    } else {
      await createObjectWorkerAssignment(assignmentData, auth.token);
    }

    emit("updated");
    emit("close");
  } catch (error) {
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
.has-end-date {
  border-color: #ff6b6b;
}
</style>
