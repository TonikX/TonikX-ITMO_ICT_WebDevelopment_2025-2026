<template>
  <v-dialog v-model="showModal" width="500" @click:outside="$emit('close')">
    <v-card>
      <v-card-title>
        {{ editingAssignment ? "Edit" : "Add" }} Worker to Object
      </v-card-title>
      <v-form @submit.prevent="submit" class="pa-4">
        <v-select
          v-model="form.worker"
          :items="availableWorkers"
          item-title="name"
          item-value="id"
          label="Worker"
          required
          :loading="loadingWorkers"
        >
          <template v-slot:item="{ item }">
            {{ item.title.last_name }} {{ item.title.first_name }}
          </template>
        </v-select>

        <v-text-field
          v-model="form.start_date"
          type="date"
          label="Start Date"
          required
        ></v-text-field>

        <v-text-field
          v-model="form.end_date"
          type="date"
          label="End Date"
        ></v-text-field>

        <div v-if="editingAssignment && !form.end_date" class="mb-4">
          <v-alert type="info">
            This worker is currently active. Setting an end date will deactivate
            them.
          </v-alert>
        </div>

        <div class="d-flex justify-space-between">
          <v-btn @click="$emit('close')" :disabled="saving">Cancel</v-btn>
          <v-btn
            type="submit"
            color="primary"
            :loading="saving"
            :disabled="!form.worker || !form.start_date"
          >
            {{ editingAssignment ? "Update" : "Assign" }}
          </v-btn>
        </div>

        <v-btn
          v-if="editingAssignment"
          @click="deleteAssignment"
          color="error"
          :loading="saving"
          class="mt-4"
        >
          {{ form.end_date ? "Delete" : "End Assignment" }}
        </v-btn>
      </v-form>
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
const showModal = ref(true);

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
    console.error("Error saving object worker assignment:", error);
    alert("Failed to save");
  } finally {
    saving.value = false;
  }
};

const deleteAssignment = async () => {
  if (!props.assignment?.id) return;

  const message = form.end_date
    ? "Are you sure you want to delete this assignment?"
    : "Are you sure you want to end this assignment?";

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
    alert("Failed to update/delete");
  } finally {
    saving.value = false;
  }
};

onMounted(async () => {
  initForm();
  await loadAllWorkers();
});
</script>
