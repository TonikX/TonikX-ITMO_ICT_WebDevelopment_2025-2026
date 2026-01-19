<template>
  <v-container v-if="!loading">
    <v-card>
      <v-card-title>Edit Object: {{ formData.name }}</v-card-title>

      <v-form @submit.prevent="saveChanges" class="pa-4">
        <v-text-field
          v-model="formData.name"
          label="Object Name"
          required
          class="mb-3"
        ></v-text-field>

        <v-text-field
          v-model="formData.address"
          label="Address"
          class="mb-6"
        ></v-text-field>

        <v-card class="mb-6">
          <v-card-title>Zones</v-card-title>
          <v-card-text>
            <v-table v-if="zones.length > 0">
              <thead>
                <tr>
                  <th>Zone</th>
                  <th>ID</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="zone in zones" :key="zone.id">
                  <td>{{ zone.number }}</td>
                  <td>{{ zone.id }}</td>
                  <td>
                    <v-btn
                      @click="deleteZone(zone.id)"
                      color="error"
                      size="small"
                    >
                      Remove
                    </v-btn>
                  </td>
                </tr>
              </tbody>
            </v-table>
            <p v-else class="text-center">No zones added yet</p>

            <v-btn
              @click="showAddZoneModal = true"
              color="primary"
              class="mt-3"
            >
              + Add New Zone
            </v-btn>
          </v-card-text>
        </v-card>

        <v-card class="mb-6">
          <v-card-title>Decorators</v-card-title>
          <v-card-text>
            <v-table v-if="currentDecorators.length > 0">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Contact</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="decorator in currentDecorators" :key="decorator.id">
                  <td>{{ decorator.name }}</td>
                  <td>
                    <div v-if="decorator.phone">{{ decorator.phone }}</div>
                    <div v-if="decorator.email">{{ decorator.email }}</div>
                  </td>
                  <td>
                    <v-btn
                      @click="removeDecorator(decorator.id)"
                      color="error"
                      size="small"
                    >
                      Remove
                    </v-btn>
                  </td>
                </tr>
              </tbody>
            </v-table>
            <p v-else class="text-center">No decorators assigned</p>

            <v-btn
              @click="showAddDecoratorModal = true"
              color="primary"
              class="mt-3"
            >
              + Add Decorator
            </v-btn>
          </v-card-text>
        </v-card>

        <v-card class="mb-6">
          <v-card-title>Assigned Workers</v-card-title>
          <v-card-text>
            <v-table v-if="objectWorkers.length > 0">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Period</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="assignment in objectWorkers" :key="assignment.id">
                  <td>
                    {{ assignment.worker?.full_name || "Unknown Worker" }}
                  </td>
                  <td>
                    {{ formatDate(assignment.start_date) }} -
                    {{
                      assignment.end_date
                        ? formatDate(assignment.end_date)
                        : "Current"
                    }}
                  </td>
                  <td>
                    <v-chip :color="assignment.end_date ? 'grey' : 'green'">
                      {{ assignment.end_date ? "Ended" : "Active" }}
                    </v-chip>
                  </td>
                  <td>
                    <v-btn
                      @click="editWorkerAssignment(assignment)"
                      size="small"
                      class="mr-2"
                    >
                      {{ assignment.end_date ? "Edit" : "End" }}
                    </v-btn>
                    <v-btn
                      @click="removeWorkerAssignment(assignment.id)"
                      color="error"
                      size="small"
                    >
                      Remove
                    </v-btn>
                  </td>
                </tr>
              </tbody>
            </v-table>
            <p v-else class="text-center">No workers assigned</p>

            <v-btn
              @click="openWorkerAssignmentModal()"
              color="primary"
              class="mt-3"
            >
              + Add Worker
            </v-btn>
          </v-card-text>
        </v-card>

        <div class="d-flex justify-space-between mt-6">
          <v-btn @click="goBack">Cancel</v-btn>
          <v-btn type="submit" color="primary" :loading="saving">
            Save Changes
          </v-btn>
        </div>
      </v-form>
    </v-card>

    <v-dialog v-model="showAddZoneModal" width="500">
      <v-card>
        <v-card-title>Add New Zone</v-card-title>
        <v-card-text>
          <v-text-field
            v-model="newZone.number"
            label="Zone Number/Name"
            placeholder="e.g., Zone 1, Garden Area"
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="showAddZoneModal = false">Cancel</v-btn>
          <v-btn
            @click="addNewZone"
            color="primary"
            :disabled="!newZone.number.trim()"
          >
            Add Zone
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showAddDecoratorModal" width="500">
      <v-card>
        <v-card-title>Add Decorator</v-card-title>
        <v-card-text>
          <div v-if="availableDecorators.length === 0" class="text-center">
            No decorators available
          </div>
          <v-list v-else>
            <v-list-item
              v-for="decorator in availableDecorators"
              :key="decorator.id"
            >
              <v-list-item-title>{{ decorator.name }}</v-list-item-title>
              <v-list-item-subtitle>
                <span v-if="decorator.phone">{{ decorator.phone }}</span>
                <span v-if="decorator.email && decorator.phone"> • </span>
                <span v-if="decorator.email">{{ decorator.email }}</span>
              </v-list-item-subtitle>
              <template v-slot:append>
                <v-btn
                  @click="addDecorator(decorator.id)"
                  :disabled="selectedDecorators.includes(decorator.id)"
                  size="small"
                >
                  {{
                    selectedDecorators.includes(decorator.id) ? "Added" : "Add"
                  }}
                </v-btn>
              </template>
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="showAddDecoratorModal = false" color="primary">
            Done
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <ObjectWorkerAssignmentModal
      v-if="showWorkerModal"
      :objectId="objectId"
      :assignment="editingWorkerAssignment"
      :existingAssignments="objectWorkers"
      @close="closeWorkerModal"
      @updated="loadObjectWorkers"
    />
  </v-container>
  <v-container v-else class="text-center"> Loading object data... </v-container>
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

    const [objectData, decoratorsData, zonesData] = await Promise.all([
      getObjectById(objectId.value, auth.token),
      getDecorators(auth.token),
      getObjectZones(objectId.value, auth.token),
    ]);

    await loadObjectWorkers();

    formData.name = objectData.name || "";
    formData.address = objectData.address || "";

    zones.value = zonesData.results || zonesData || [];

    const decoratorsList = decoratorsData.results || decoratorsData || [];

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

    if (objectData.decorators && Array.isArray(objectData.decorators)) {
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
    } else {
      selectedDecorators.value = [];
    }
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
  }
};

const removeDecorator = (decoratorId) => {
  if (confirm("Remove this decorator from the object?")) {
    selectedDecorators.value = selectedDecorators.value.filter(
      (id) => id !== decoratorId
    );
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

    await updateObject(objectId.value, updateData, auth.token);

    alert("Object updated successfully!");
    router.push(`/objects/${objectId.value}`);
  } catch (err) {
    console.error("Failed to update object:", err);
    error.value = err.response?.data?.message || "Failed to update object";
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
