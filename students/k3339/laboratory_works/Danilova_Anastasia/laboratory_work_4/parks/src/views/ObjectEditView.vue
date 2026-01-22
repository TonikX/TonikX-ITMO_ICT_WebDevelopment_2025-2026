<template>
  <div v-if="!loading" class="object-edit">
    <div class="header">
      <h2>Edit Object: {{ formData.name }}</h2>
      <div class="actions">
        <button @click="goBack" class="secondary-btn">Cancel</button>
        <button @click="saveChanges" class="primary-btn" :disabled="saving">
          {{ saving ? "Saving..." : "Save Changes" }}
        </button>
      </div>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <div class="edit-form">
      <div class="form-section">
        <h3>Basic Information</h3>
        <div class="form-group">
          <label for="name">Object Name:</label>
          <input
            id="name"
            v-model="formData.name"
            type="text"
            class="form-control"
            placeholder="Enter object name"
          />
        </div>

        <div class="form-group">
          <label for="address">Address:</label>
          <input
            id="address"
            v-model="formData.address"
            type="text"
            class="form-control"
            placeholder="Enter address"
          />
        </div>
      </div>

      <div class="form-section">
        <div class="section-header">
          <h3>Zones</h3>
          <button
            @click="showAddZoneModal = true"
            type="button"
            class="add-btn"
          >
            + Add New Zone
          </button>
        </div>

        <div v-if="zones.length === 0" class="empty-state">
          No zones added yet
        </div>

        <div v-else class="zones-list">
          <div v-for="zone in zones" :key="zone.id" class="zone-item">
            <div class="zone-info">
              <span class="zone-number">Zone {{ zone.number }}</span>
              <span class="zone-id">ID: {{ zone.id }}</span>
            </div>
            <button
              @click="deleteZone(zone.id)"
              type="button"
              class="delete-btn"
            >
              Remove
            </button>
          </div>
        </div>
      </div>

      <div class="form-section">
        <div class="section-header">
          <h3>Decorators</h3>
          <button
            @click="showAddDecoratorModal = true"
            type="button"
            class="add-btn"
          >
            + Add Decorator
          </button>
        </div>

        <div v-if="currentDecorators.length === 0" class="empty-state">
          No decorators assigned
        </div>

        <div v-else class="decorators-list">
          <div
            v-for="decorator in currentDecorators"
            :key="decorator.id"
            class="decorator-item"
          >
            <div class="decorator-info">
              <span class="decorator-name">{{ decorator.name }}</span>
              <span class="decorator-details">
                <span v-if="decorator.phone">{{ decorator.phone }}</span>
                <span v-if="decorator.email && decorator.phone"> • </span>
                <span v-if="decorator.email">{{ decorator.email }}</span>
              </span>
            </div>
            <button
              @click="removeDecorator(decorator.id)"
              type="button"
              class="delete-btn"
            >
              Remove
            </button>
          </div>
        </div>
      </div>
      <div class="form-section">
        <div class="section-header">
          <h3>Assigned Workers</h3>
          <button
            @click="openWorkerAssignmentModal()"
            type="button"
            class="add-btn"
          >
            + Add Worker
          </button>
        </div>

        <div v-if="objectWorkers.length === 0" class="empty-state">
          No workers assigned to this object
        </div>

        <div v-else class="workers-list">
          <div
            v-for="assignment in objectWorkers"
            :key="assignment.id"
            class="worker-item"
            :class="{ ended: assignment.end_date }"
          >
            <div class="worker-info">
              <div class="worker-name">
                {{ assignment.worker?.full_name || "Unknown Worker" }}
              </div>
              <div class="worker-dates">
                <span class="start-date"
                  >From: {{ formatDate(assignment.start_date) }}</span
                >
                <span v-if="assignment.end_date" class="end-date">
                  To: {{ formatDate(assignment.end_date) }}
                </span>
                <span v-else class="current">Current</span>
              </div>
              <div v-if="assignment.worker?.phone_number" class="worker-phone">
                {{ assignment.worker.phone_number }}
              </div>
            </div>
            <div class="worker-actions">
              <button
                @click="editWorkerAssignment(assignment)"
                type="button"
                class="edit-btn"
              >
                {{ assignment.end_date ? "Edit" : "End" }}
              </button>
              <button
                @click="removeWorkerAssignment(assignment.id)"
                type="button"
                class="delete-btn"
              >
                Remove
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showAddZoneModal" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h3>Add New Zone</h3>
          <button @click="showAddZoneModal = false" class="close-btn">
            &times;
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="zoneNumber">Zone Number/Name:</label>
            <input
              id="zoneNumber"
              v-model="newZone.number"
              type="text"
              class="form-control"
              placeholder="e.g., Zone 1, Garden Area, etc."
            />
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showAddZoneModal = false" class="secondary-btn">
            Cancel
          </button>
          <button
            @click="addNewZone"
            class="primary-btn"
            :disabled="!newZone.number.trim()"
          >
            Add Zone
          </button>
        </div>
      </div>
    </div>

    <div v-if="showAddDecoratorModal" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h3>Add Decorator</h3>
          <button @click="showAddDecoratorModal = false" class="close-btn">
            &times;
          </button>
        </div>
        <div class="modal-body">
          <div v-if="availableDecorators.length === 0" class="empty-state">
            No decorators available to add
          </div>
          <div v-else class="decorators-select-list">
            <div
              v-for="decorator in availableDecorators"
              :key="decorator.id"
              class="decorator-select-item"
            >
              <div class="decorator-select-info">
                <div class="decorator-name">{{ decorator.name }}</div>
                <div class="decorator-details">
                  <span v-if="decorator.phone">{{ decorator.phone }}</span>
                  <span v-if="decorator.email && decorator.phone"> • </span>
                  <span v-if="decorator.email">{{ decorator.email }}</span>
                </div>
              </div>
              <button
                @click="addDecorator(decorator.id)"
                class="add-btn"
                :disabled="selectedDecorators.includes(decorator.id)"
              >
                {{
                  selectedDecorators.includes(decorator.id) ? "Added" : "Add"
                }}
              </button>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showAddDecoratorModal = false" class="primary-btn">
            Done
          </button>
        </div>
      </div>
    </div>
    <ObjectWorkerAssignmentModal
      v-if="showWorkerModal"
      :objectId="objectId"
      :assignment="editingWorkerAssignment"
      :existingAssignments="objectWorkers"
      @close="closeWorkerModal"
      @updated="loadObjectWorkers"
    />
  </div>
  <div v-else class="loading">Loading object data...</div>
</template>

<script setup>
import { ref, onMounted, reactive, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/store/auth";
import ObjectWorkerAssignmentModal from "@/components/ObjectWorkerAssignmentModal.vue";
import {
  getObjectWorkerAssignments,
  deleteObjectWorkerAssignment,
} from "@/services/plantWorkerService";

import {
  getObjectById,
  updateObject,
  getDecorators,
  getObjectZones,
  createObjectZone,
  deleteObjectZone,
} from "@/services/objectsService";

const route = useRoute();
const router = useRouter();
const auth = useAuthStore();

const loading = ref(true);
const saving = ref(false);
const error = ref(null);
const showAddZoneModal = ref(false);
const showAddDecoratorModal = ref(false);
const showWorkerModal = ref(false);
const editingWorkerAssignment = ref(null);
const objectWorkers = ref([]);

const formData = reactive({
  name: "",
  address: "",
});

const allDecorators = ref([]);
const zones = ref([]);
const selectedDecorators = ref([]);

const newZone = reactive({
  number: "",
});

const objectId = computed(() => parseInt(route.params.id));

const currentDecorators = computed(() => {
  const validIds = selectedDecorators.value.filter(
    (id) => id != null && !isNaN(id)
  );
  return allDecorators.value.filter((decorator) =>
    validIds.includes(decorator.id)
  );
});

const availableDecorators = computed(() => {
  const validIds = selectedDecorators.value.filter(
    (id) => id != null && !isNaN(id)
  );
  return allDecorators.value.filter(
    (decorator) => !validIds.includes(decorator.id)
  );
});

const loadObjectData = async () => {
  try {
    loading.value = true;

    console.log("Loading object data for ID:", objectId.value);

    const [objectData, decoratorsData, zonesData] = await Promise.all([
      getObjectById(objectId.value, auth.token),
      getDecorators(auth.token),
      getObjectZones(objectId.value, auth.token),
    ]);

    console.log("Full object data:", objectData);
    console.log("Decorators in object data:", objectData.decorators);
    console.log("Decorators response:", decoratorsData);
    console.log("Zones data:", zonesData);

    await loadObjectWorkers();
    formData.name = objectData.name || "";
    formData.address = objectData.address || "";

    zones.value = zonesData.results || zonesData || [];

    const decoratorsList = decoratorsData.results || decoratorsData || [];
    console.log("Raw decorators list:", decoratorsList);

    allDecorators.value = decoratorsList.map((decorator) => ({
      id: decorator.id,
      name:
        [decorator.first_name, decorator.last_name]
          .filter(Boolean)
          .join(" ")
          .trim() || `Decorator #${decorator.id}`,
      first_name: decorator.first_name,
      last_name: decorator.last_name,
      phone: decorator.phone_number || decorator.phone || "",
      email: decorator.email || "",
    }));

    console.log("Processed decorators:", allDecorators.value);

    if (objectData.decorators && Array.isArray(objectData.decorators)) {
      console.log("Original decorators array:", objectData.decorators);

      const decoratorIds = [];
      for (const item of objectData.decorators) {
        if (item && typeof item === "object" && item.id) {
          decoratorIds.push(item.id);
        } else if (item && typeof item === "number") {
          decoratorIds.push(item);
        } else if (item && typeof item === "string") {
          const id = parseInt(item);
          if (!isNaN(id)) decoratorIds.push(id);
        }
      }

      selectedDecorators.value = decoratorIds;
      console.log("Final selected decorator IDs:", selectedDecorators.value);
    } else {
      selectedDecorators.value = [];
      console.log("No decorators found in object data");
    }

    console.log("Final current decorators:", currentDecorators.value);
  } catch (err) {
    console.error("Failed to load data:", err);
    error.value = "Failed to load object data";
  } finally {
    loading.value = false;
  }
};

const loadObjectWorkers = async () => {
  try {
    const data = await getObjectWorkerAssignments(objectId.value, auth.token);
    console.log("Object workers assignments:", data);

    if (data.results) {
      objectWorkers.value = data.results;
    } else if (Array.isArray(data)) {
      objectWorkers.value = data;
    } else {
      objectWorkers.value = [];
    }
  } catch (error) {
    console.error("Error loading object workers:", error);
    objectWorkers.value = [];
  }
};

const openWorkerAssignmentModal = (assignment = null) => {
  editingWorkerAssignment.value = assignment;
  showWorkerModal.value = true;
};

const closeWorkerModal = () => {
  showWorkerModal.value = false;
  editingWorkerAssignment.value = null;
};

const editWorkerAssignment = (assignment) => {
  openWorkerAssignmentModal(assignment);
};

const removeWorkerAssignment = async (assignmentId) => {
  if (!confirm("Are you sure you want to remove this worker assignment?"))
    return;

  try {
    await deleteObjectWorkerAssignment(assignmentId, auth.token);
    await loadObjectWorkers();
  } catch (error) {
    console.error("Error removing worker assignment:", error);
    alert("Failed to remove worker assignment");
  }
};

const formatDate = (dateString) => {
  if (!dateString) return "-";
  return new Date(dateString).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
};
const addNewZone = async () => {
  try {
    if (!newZone.number.trim()) return;

    const zoneData = {
      object: objectId.value,
      number: newZone.number.trim(),
    };

    console.log("Creating zone:", zoneData);
    const createdZone = await createObjectZone(zoneData, auth.token);
    zones.value.push(createdZone);

    newZone.number = "";
    showAddZoneModal.value = false;
  } catch (err) {
    console.error("Failed to create zone:", err);
    alert(
      "Failed to create zone: " + (err.response?.data?.detail || err.message)
    );
  }
};

const deleteZone = async (zoneId) => {
  if (!confirm("Are you sure you want to delete this zone?")) return;

  try {
    await deleteObjectZone(zoneId, auth.token);
    zones.value = zones.value.filter((zone) => zone.id !== zoneId);
  } catch (err) {
    console.error("Failed to delete zone:", err);
    alert("Failed to delete zone");
  }
};

const addDecorator = (decoratorId) => {
  if (!selectedDecorators.value.includes(decoratorId)) {
    selectedDecorators.value.push(decoratorId);
    console.log("Added decorator ID:", decoratorId);
    console.log("Selected decorators:", selectedDecorators.value);
  }
};

const removeDecorator = (decoratorId) => {
  if (confirm("Remove this decorator from the object?")) {
    selectedDecorators.value = selectedDecorators.value.filter(
      (id) => id !== decoratorId
    );
    console.log("Removed decorator ID:", decoratorId);
  }
};

const saveChanges = async () => {
  saving.value = true;
  error.value = null;

  try {
    const validDecoratorIds = selectedDecorators.value.filter(
      (id) => id != null && !isNaN(id) && id > 0
    );

    const updateData = {
      name: formData.name,
      address: formData.address,
      decorators: validDecoratorIds,
    };

    console.log("Saving object with data:", updateData);
    await updateObject(objectId.value, updateData, auth.token);

    alert("Object updated successfully!");
    router.push(`/objects/${objectId.value}`);
  } catch (err) {
    console.error("Failed to update object:", err);
    error.value =
      err.response?.data?.message ||
      "Failed to update object. Please try again.";
    alert(error.value);
  } finally {
    saving.value = false;
  }
};

const goBack = () => {
  router.back();
};

onMounted(async () => {
  await loadObjectData();
});
</script>

<style scoped>
.object-edit {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.loading {
  text-align: center;
  padding: 40px;
  font-size: 18px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.actions {
  display: flex;
  gap: 10px;
}

.primary-btn {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.primary-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.secondary-btn {
  background-color: #f0f0f0;
  color: #333;
  border: 1px solid #ddd;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.error-message {
  background-color: #ffebee;
  color: #c62828;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.edit-form {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-section {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.form-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h3 {
  margin: 0;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.empty-state {
  padding: 20px;
  text-align: center;
  color: #666;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.zones-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.workers-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.worker-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 4px;
  border: 1px solid #eee;
}

.worker-item.ended {
  opacity: 0.7;
  background-color: #f5f5f5;
}

.worker-info {
  flex: 1;
}

.worker-name {
  font-weight: bold;
  font-size: 16px;
  margin-bottom: 5px;
}

.worker-dates {
  font-size: 14px;
  color: #666;
  margin-bottom: 5px;
}

.worker-dates .current {
  color: #4caf50;
  font-weight: 500;
}

.worker-dates .end-date {
  color: #f44336;
}

.worker-phone {
  font-size: 14px;
  color: #666;
}

.worker-actions {
  display: flex;
  gap: 8px;
}

.worker-actions .edit-btn {
  background-color: #4dabf7;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.worker-actions .edit-btn:hover {
  background-color: #2196f3;
}

.zone-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 4px;
  border: 1px solid #eee;
}

.zone-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.zone-number {
  font-weight: bold;
  font-size: 16px;
}

.zone-id {
  font-size: 12px;
  color: #666;
}

.decorators-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.decorator-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 4px;
  border: 1px solid #eee;
}

.decorator-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.decorator-name {
  font-weight: bold;
  font-size: 16px;
}

.decorator-details {
  font-size: 14px;
  color: #666;
}

.delete-btn {
  background-color: #ff6b6b;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.add-btn {
  background-color: #4dabf7;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
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

.modal-body {
  padding: 20px;
}

.modal-footer {
  padding: 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.decorators-select-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 400px;
  overflow-y: auto;
}

.decorator-select-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 4px;
  border: 1px solid #eee;
}

.decorator-select-info {
  flex: 1;
}

.decorator-select-info .decorator-name {
  font-weight: bold;
  margin-bottom: 5px;
}

.decorator-select-info .decorator-details {
  font-size: 14px;
  color: #666;
  display: flex;
  flex-direction: column;
  gap: 2px;
}
</style>
