<template>
  <div>
    <v-row class="mb-4 align-center">
      <v-col cols="6">
        <h3>Plants</h3>
      </v-col>
      <v-col cols="6" class="text-right">
        <v-btn
          @click="showCreatePlantModal = true"
          color="primary"
          v-if="!isLoading"
        >
          + Add Plant
        </v-btn>
      </v-col>
    </v-row>

    <div v-if="isLoading" class="text-center py-4">
      <v-progress-circular indeterminate></v-progress-circular>
      <p>Loading plants...</p>
    </div>

    <div v-else>
      <v-card v-if="plants.length">
        <v-table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Species</th>
              <th>Zone</th>
              <th>Age</th>
              <th>Has Schedule</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="placement in plants"
              :key="placement.id"
              :class="{ 'selected-row': isPlantSelected(placement.plant?.id) }"
            >
              <td>{{ placement.id }}</td>
              <td>
                <div class="plant-info">
                  <button
                    @click="showPlantDetails(placement)"
                    class="plant-name-btn"
                  >
                    {{
                      placement.plant?.species_name ||
                      placement.plant?.species_details?.name ||
                      `Species ID: ${placement.plant?.species}` ||
                      "Unknown"
                    }}
                  </button>
                  <div class="plant-id-subtitle">
                    Plant ID: {{ placement.plant?.id || "N/A" }}
                  </div>
                  <div
                    v-if="placement.plant?.description"
                    class="plant-description"
                  >
                    {{ truncateDescription(placement.plant.description) }}
                  </div>
                </div>
              </td>
              <td>
                <div class="zone-info">
                  <div class="zone-number">
                    {{ placement.zone_number || "-" }}
                  </div>
                  <div v-if="placement.unique_number" class="unique-number">
                    #{{ placement.unique_number }}
                  </div>
                </div>
              </td>
              <td>
                <div class="age-info">
                  <div class="age-value">
                    {{ placement.plant?.current_age || 0 }} years
                  </div>
                  <div v-if="placement.planted_date" class="planted-date">
                    Planted: {{ formatShortDate(placement.planted_date) }}
                  </div>
                </div>
              </td>
              <td>
                <span
                  v-if="placement.plant?.has_watering_schedule"
                  class="schedule-indicator yes"
                  title="Has watering schedule"
                >
                  yes
                </span>
                <span
                  v-else
                  class="schedule-indicator no"
                  title="No watering schedule"
                >
                  no
                </span>
                <div
                  v-if="placement.plant?.has_watering_schedule"
                  class="schedule-hint"
                >
                  Scheduled
                </div>
                <div v-else class="schedule-hint">Not scheduled</div>
              </td>
              <td>
                <div class="action-buttons">
                  <v-btn
                    @click="openEdit(placement.plant)"
                    color="primary"
                    size="small"
                    title="Edit plant"
                  >
                    Edit
                  </v-btn>
                  <button
                    @click="showPlantDetails(placement)"
                    class="details-btn"
                    title="View details"
                  >
                    Details
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-card>

      <v-alert v-else type="info" class="my-4">
        <div class="text-center">
          <p class="mb-2">No plants found for this object</p>
          <v-btn
            @click="showCreatePlantModal = true"
            color="primary"
            class="mt-2"
          >
            + Add Your First Plant
          </v-btn>
          <p class="text-caption mt-2">Start by adding plants to this object</p>
        </div>
      </v-alert>

      <v-pagination
        v-if="count > pageSize"
        v-model="page"
        :length="totalPages"
        :total-visible="5"
        class="mt-4"
      ></v-pagination>
    </div>

    <div v-if="selectedPlant" class="plant-details-panel">
      <div class="panel-header">
        <h4>{{ selectedPlant.species?.name || "Plant Details" }}</h4>
        <button @click="selectedPlant = null" class="close-btn">×</button>
      </div>

      <div class="tabs">
        <button
          @click="activeDetailTab = 'watering'"
          :class="['tab-btn', activeDetailTab === 'watering' ? 'active' : '']"
        >
          Watering
        </button>
        <button
          @click="activeDetailTab = 'workers'"
          :class="['tab-btn', activeDetailTab === 'workers' ? 'active' : '']"
        >
          Workers ({{ plantWorkerAssignments.length }})
        </button>
      </div>

      <div v-if="activeDetailTab === 'watering'" class="tab-content">
        <div class="section-header">
          <h5>Watering Schedule</h5>
          <button
            @click="
              wateringSchedule
                ? editWateringSchedule()
                : (showWateringModal = true)
            "
            class="add-btn"
          >
            {{ wateringSchedule ? "Edit" : "Add" }}
          </button>
        </div>

        <div v-if="loadingWatering">Loading...</div>
        <div v-else-if="wateringSchedule" class="schedule-card">
          <div class="schedule-row">
            <span class="label">Frequency:</span>
            <span class="value">{{ wateringSchedule.frequency }}</span>
          </div>
          <div class="schedule-row">
            <span class="label">Time:</span>
            <span class="value">{{
              wateringSchedule.watering_time_period
            }}</span>
          </div>
          <div class="schedule-row">
            <span class="label">Current Norm:</span>
            <span class="value"
              >{{ wateringSchedule.current_water_norm_liters }} L</span
            >
          </div>
          <div class="season-grid">
            <div class="season">
              Spring: {{ wateringSchedule.water_norm_liters_spring }}L
            </div>
            <div class="season">
              Summer: {{ wateringSchedule.water_norm_liters_summer }}L
            </div>
            <div class="season">
              Fall: {{ wateringSchedule.water_norm_liters_fall }}L
            </div>
            <div class="season">
              Winter: {{ wateringSchedule.water_norm_liters_winter }}L
            </div>
          </div>
          <div class="actions">
            <!-- <button @click="editWateringSchedule()" class="edit-btn">
              Edit
            </button> -->
          </div>
        </div>
        <div v-else class="empty-schedule">No watering schedule set</div>
      </div>

      <div v-if="activeDetailTab === 'workers'" class="tab-content">
        <div class="section-header">
          <h5>Worker Assignments</h5>
          <button @click="showWorkerModal = true" class="add-btn">
            + Assign
          </button>
        </div>

        <div v-if="loadingWorkers">Loading...</div>
        <div
          v-else-if="plantWorkerAssignments.length === 0"
          class="empty-assignments"
        >
          No worker assignments
        </div>
        <table v-else class="workers-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Worker</th>
              <th>Phone</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="assignment in plantWorkerAssignments"
              :key="assignment.id"
            >
              <td>{{ formatDate(assignment.date) }}</td>
              <td>
                {{ assignment.worker?.full_name || "Unknown" }}
              </td>
              <td>{{ assignment.worker?.phone_number || "-" }}</td>
              <td>
                <div class="assignment-actions">
                  <button
                    @click="openWorkerAssignment(assignment)"
                    class="edit-btn-small"
                    title="Edit assignment"
                  >
                    Edit
                  </button>
                  <button
                    @click="deleteWorkerAssignment(assignment.id)"
                    class="delete-btn-small"
                    title="Remove assignment"
                  >
                    Remove
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <v-dialog v-model="showCreatePlantModal" max-width="500">
      <v-card>
        <v-card-title>Add New Plant</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="createPlant">
            <v-select
              v-model="newPlant.species"
              label="Species *"
              :items="availableSpecies"
              item-title="name"
              item-value="id"
              required
              :error="validationErrors.species"
              @update:model-value="clearValidationError('species')"
              class="mb-4"
            ></v-select>

            <v-select
              v-model="newPlant.zone"
              label="Zone *"
              :items="objectZones"
              item-title="number"
              item-value="id"
              required
              :error="validationErrors.zone"
              @update:model-value="
                clearValidationError('zone');
                checkUniqueNumber();
              "
              class="mb-4"
            ></v-select>

            <v-text-field
              v-model.number="newPlant.initial_age"
              label="Initial Age (years) *"
              type="number"
              min="0"
              required
              :error="validationErrors.initial_age"
              @update:model-value="clearValidationError('initial_age')"
              class="mb-4"
            ></v-text-field>

            <v-text-field
              v-model.number="newPlant.unique_number"
              label="Unique Number in Zone *"
              type="number"
              min="1"
              required
              :error="validationErrors.unique_number"
              :hint="uniqueNumberHint"
              @update:model-value="
                clearValidationError('unique_number');
                checkUniqueNumber();
              "
              class="mb-4"
            ></v-text-field>

            <v-text-field
              v-model="newPlant.planted_date"
              label="Planted Date *"
              type="date"
              required
              :error="validationErrors.planted_date"
              @update:model-value="clearValidationError('planted_date')"
              class="mb-4"
            ></v-text-field>

            <v-textarea
              v-model="newPlant.description"
              label="Description"
              rows="3"
              class="mb-4"
            ></v-textarea>

            <v-alert
              v-if="validationErrors.general"
              type="error"
              density="compact"
              class="mb-4"
            >
              {{ validationErrors.general }}
            </v-alert>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="showCreatePlantModal = false">Cancel</v-btn>
          <v-btn
            @click="createPlant"
            :disabled="creatingPlant || isUniqueNumberInvalid"
            color="primary"
          >
            {{ creatingPlant ? "Creating..." : "Create" }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <PlantEditModal
      v-if="showEditModal"
      :plant="editingPlant"
      @close="showEditModal = false"
      @updated="loadPlants"
    />

    <WateringScheduleModal
      v-if="showWateringModal"
      :plantId="selectedPlant?.id"
      :wateringSchedule="wateringSchedule"
      @close="showWateringModal = false"
      @updated="handleWateringScheduleUpdated"
    />

    <WorkerAssignmentModal
      v-if="showWorkerModal"
      :plantId="selectedPlant?.id"
      :objectId="objectId"
      :assignment="editingWorkerAssignment"
      @close="closeWorkerModal"
      @updated="handleWorkerAssignmentUpdated"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, reactive } from "vue";
import { useAuthStore } from "@/store/auth";
import { getPlantsByObject } from "@/services/plantService";
import { getPlantWateringSchedules } from "@/services/wateringService";
import {
  getPlantWorkerAssignments,
  deletePlantWorkerAssignment,
} from "@/services/plantWorkerService";
import { getObjectZones } from "@/services/objectsService";
import { getSpecies } from "@/services/speciesService";
import WateringScheduleModal from "@/components/WateringScheduleModal.vue";
import WorkerAssignmentModal from "@/components/WorkerAssignmentModal.vue";

import {
  createPlant as createPlantApi,
  createPlantPlacement,
} from "@/services/plantService";
import PlantEditModal from "@/components/PlantEditModal.vue";

const props = defineProps({ objectId: Number });
const auth = useAuthStore();

const plants = ref([]);
const isLoading = ref(false);
const page = ref(1);
const count = ref(0);
const next = ref(null);
const previous = ref(null);
const pageSize = ref(15);

const selectedPlant = ref(null);
const selectedPlantPlacement = ref(null);
const activeDetailTab = ref("watering");

const wateringSchedule = ref(null);
const plantWorkerAssignments = ref([]);
const loadingWatering = ref(false);
const loadingWorkers = ref(false);

const showEditModal = ref(false);
const editingPlant = ref(null);
const showWateringModal = ref(false);
const showWorkerModal = ref(false);
const showCreatePlantModal = ref(false);
const editingWatering = ref(null);
const editingWorkerAssignment = ref(null);

const newPlant = reactive({
  species: "",
  zone: "",
  initial_age: 1,
  unique_number: 1,
  planted_date: new Date().toISOString().split("T")[0],
  description: "",
});

const creatingPlant = ref(false);
const objectZones = ref([]);
const availableSpecies = ref([]);
const validationErrors = ref({
  species: false,
  zone: false,
  initial_age: false,
  unique_number: false,
  planted_date: false,
  general: null,
});

const totalPages = computed(() => Math.ceil(count.value / pageSize.value));

const clearValidationError = (field) => {
  validationErrors.value[field] = false;
  if (field !== "general") {
    validationErrors.value.general = null;
  }
};

const checkUniqueNumber = async () => {
  if (!newPlant.zone || !newPlant.unique_number) {
    validationErrors.value.unique_number = false;
    return;
  }

  try {
    const data = await getPlantsByObject(props.objectId, auth.token, 1, 100);
    const existingPlants = data.results || [];

    const zoneNumber = objectZones.value.find(
      (z) => z.id === newPlant.zone
    )?.number;

    const hasConflict = existingPlants.some((placement) => {
      const sameZone =
        placement.zone === newPlant.zone ||
        placement.zone_number === zoneNumber;
      const sameNumber = placement.unique_number === newPlant.unique_number;
      return sameZone && sameNumber;
    });

    validationErrors.value.unique_number = hasConflict;
  } catch (error) {
    validationErrors.value.unique_number = false;
  }
};

const uniqueNumberHint = computed(() => {
  if (!newPlant.zone) return "Select a zone first";

  if (validationErrors.value.unique_number) {
    const zone = objectZones.value.find((z) => z.id === newPlant.zone);
    const zoneName = zone ? `zone ${zone.number}` : "selected zone";
    return `This number is already used in ${zoneName}`;
  }

  return "Must be unique within the selected zone";
});

const isUniqueNumberInvalid = computed(
  () => validationErrors.value.unique_number
);

const loadPlants = async () => {
  isLoading.value = true;
  try {
    const data = await getPlantsByObject(
      props.objectId,
      auth.token,
      page.value
    );
    plants.value = data.results || [];
    count.value = data.count || 0;
    next.value = data.next;
    previous.value = data.previous;
    pageSize.value = data.results?.length || 15;
  } catch (error) {
    plants.value = [];
  } finally {
    isLoading.value = false;
  }
};

const loadAdditionalData = async () => {
  try {
    const zonesData = await getObjectZones(props.objectId, auth.token);
    objectZones.value = zonesData.results || zonesData || [];

    const speciesData = await getSpecies(auth.token);
    availableSpecies.value = speciesData.results || speciesData || [];
  } catch (error) {
    objectZones.value = [];
    availableSpecies.value = [];
  }
};

const createPlant = async () => {
  if (
    !newPlant.species ||
    !newPlant.zone ||
    !newPlant.initial_age ||
    !newPlant.unique_number ||
    !newPlant.planted_date
  ) {
    Object.keys(validationErrors.value).forEach((key) => {
      if (key !== "general" && !newPlant[key]) {
        validationErrors.value[key] = true;
      }
    });
    validationErrors.value.general = "Please fill all required fields";
    return;
  }

  if (isUniqueNumberInvalid.value) {
    validationErrors.value.general =
      "Please choose a unique number for this zone";
    return;
  }

  creatingPlant.value = true;
  validationErrors.value.general = null;

  try {
    const plantData = {
      species: parseInt(newPlant.species),
      initial_age: parseInt(newPlant.initial_age),
      description: newPlant.description || "",
    };

    const createdPlant = await createPlantApi(plantData, auth.token);

    const placementData = {
      plant: createdPlant.id,
      zone: parseInt(newPlant.zone),
      unique_number: parseInt(newPlant.unique_number),
      planted_date: newPlant.planted_date,
    };

    await createPlantPlacement(placementData, auth.token);

    showCreatePlantModal.value = false;

    Object.assign(newPlant, {
      species: "",
      zone: "",
      initial_age: 1,
      unique_number: 1,
      planted_date: new Date().toISOString().split("T")[0],
      description: "",
    });

    Object.keys(validationErrors.value).forEach((key) => {
      validationErrors.value[key] = false;
    });

    await loadPlants();
  } catch (error) {
    if (error.response?.status === 400) {
      const errorData = error.response.data;

      if (errorData.unique_number) {
        validationErrors.value.unique_number = true;
        validationErrors.value.general =
          "This number is already used in the selected zone";
      } else if (errorData.detail) {
        validationErrors.value.general = errorData.detail;
      } else if (errorData.non_field_errors) {
        validationErrors.value.general = errorData.non_field_errors.join(", ");
      } else {
        validationErrors.value.general =
          "Validation error. Please check your inputs.";
      }
    } else {
      validationErrors.value.general =
        error.response?.data?.detail ||
        error.message ||
        "Unknown error occurred";
    }
  } finally {
    creatingPlant.value = false;
  }
};

const showPlantDetails = async (placement) => {
  selectedPlant.value = null;
  selectedPlantPlacement.value = null;
  wateringSchedule.value = null;
  plantWorkerAssignments.value = [];
  loadingWatering.value = false;
  loadingWorkers.value = false;

  await new Promise((resolve) => setTimeout(resolve, 50));

  selectedPlant.value = placement.plant;
  selectedPlantPlacement.value = placement;
  activeDetailTab.value = "watering";

  if (selectedPlant.value?.id) {
    await loadPlantSpecificData(selectedPlant.value.id);
  }
};

const loadPlantSpecificData = async (plantId) => {
  wateringSchedule.value = null;
  plantWorkerAssignments.value = [];

  loadingWatering.value = true;
  try {
    const schedule = await getPlantWateringSchedules(plantId, auth.token);
    if (schedule && schedule.plant === plantId) {
      wateringSchedule.value = schedule;
    } else if (schedule === null) {
      wateringSchedule.value = null;
    } else {
      wateringSchedule.value = null;
    }
  } catch (error) {
    wateringSchedule.value = null;
  } finally {
    loadingWatering.value = false;
  }

  loadingWorkers.value = true;
  try {
    const data = await getPlantWorkerAssignments(plantId, auth.token);

    if (data.results) {
      plantWorkerAssignments.value = data.results;
    } else if (Array.isArray(data)) {
      plantWorkerAssignments.value = data;
    } else {
      plantWorkerAssignments.value = [];
    }

    const filtered = plantWorkerAssignments.value.filter(
      (assignment) =>
        assignment.plant == plantId || assignment.plant?.id == plantId
    );

    if (filtered.length !== plantWorkerAssignments.value.length) {
      plantWorkerAssignments.value = filtered;
    }
  } catch (error) {
    plantWorkerAssignments.value = [];
  } finally {
    loadingWorkers.value = false;
  }
};

const handleWateringScheduleUpdated = async () => {
  if (selectedPlant.value?.id) {
    await loadPlantSpecificData(selectedPlant.value.id);
  }
};

const handleWorkerAssignmentUpdated = async () => {
  if (selectedPlant.value?.id) {
    await loadPlantSpecificData(selectedPlant.value.id);
  }
};

const formatDate = (dateString) => {
  if (!dateString) return "-";
  return new Date(dateString).toLocaleDateString();
};

const truncateDescription = (text, maxLength = 50) => {
  if (!text) return "";
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + "...";
};

const formatShortDate = (dateString) => {
  if (!dateString) return "-";
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  } catch (error) {
    return dateString;
  }
};

const isPlantSelected = (plantId) => {
  return selectedPlant.value?.id === plantId;
};

const openEdit = (plant) => {
  editingPlant.value = plant;
  showEditModal.value = true;
};

const editWateringSchedule = () => {
  showWateringModal.value = true;
};

const openWorkerAssignment = (assignment = null) => {
  if (!selectedPlant.value?.id) {
    alert("Please select a plant first");
    return;
  }

  editingWorkerAssignment.value = assignment;
  showWorkerModal.value = true;
};

const closeWorkerModal = () => {
  showWorkerModal.value = false;
  editingWorkerAssignment.value = null;
};

const deleteWorkerAssignment = async (assignmentId) => {
  if (!confirm("Remove worker assignment?")) return;

  try {
    await deletePlantWorkerAssignment(assignmentId, auth.token);

    if (selectedPlant.value?.id) {
      await loadPlantSpecificData(selectedPlant.value.id);
    }
  } catch (error) {
    alert(`Failed to delete: ${error.response?.data?.detail || error.message}`);
  }
};

onMounted(async () => {
  await Promise.all([loadPlants(), loadAdditionalData()]);
});

watch(
  () => props.objectId,
  () => {
    page.value = 1;
    loadPlants();
    loadAdditionalData();
  }
);

watch(page, () => {
  loadPlants();
});

watch(
  () => newPlant.zone,
  () => {
    newPlant.unique_number = 1;
    checkUniqueNumber();
  }
);

watch(
  () => newPlant.unique_number,
  () => {
    checkUniqueNumber();
  }
);

watch(showCreatePlantModal, (val) => {
  if (val) {
    Object.keys(validationErrors.value).forEach((key) => {
      validationErrors.value[key] = false;
    });
    checkUniqueNumber();
  } else {
    Object.assign(newPlant, {
      species: "",
      zone: "",
      initial_age: 1,
      unique_number: 1,
      planted_date: new Date().toISOString().split("T")[0],
      description: "",
    });
  }
});
</script>

<style scoped>
.plant-details-panel {
  margin-top: 30px;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  background: #f9f9f9;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
}

.tab-btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px 4px 0 0;
  cursor: pointer;
  font-size: 14px;
}

.tab-btn.active {
  background: #4caf50;
  color: white;
  border-color: #4caf50;
}

.tab-content {
  padding: 10px 0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.add-btn {
  background-color: #4dabf7;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.schedule-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #eee;
}

.schedule-row {
  display: flex;
  margin-bottom: 10px;
}

.schedule-row .label {
  width: 140px;
  font-weight: bold;
  color: #333;
}

.schedule-row .value {
  flex: 1;
  color: #666;
}

.season-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin: 20px 0;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 6px;
}

.season {
  padding: 10px;
  background: white;
  border-radius: 4px;
  border: 1px solid #e9ecef;
  text-align: center;
  font-weight: 500;
}

.actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.empty-schedule,
.empty-assignments {
  padding: 30px;
  text-align: center;
  color: #666;
  background: white;
  border-radius: 6px;
  border: 1px solid #eee;
}

.workers-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.workers-table th {
  background: #f0f0f0;
  padding: 8px;
  text-align: left;
  font-size: 12px;
  font-weight: 600;
}

.workers-table td {
  padding: 8px;
  border-bottom: 1px solid #eee;
  font-size: 13px;
}

.edit-btn-small {
  background-color: #4dabf7;
  color: white;
  border: none;
  padding: 4px 8px;
  border-radius: 3px;
  cursor: pointer;
  font-size: 11px;
}

.edit-btn-small:hover {
  background-color: #2196f3;
}

.delete-btn-small {
  background-color: #ff6b6b;
  color: white;
  border: none;
  padding: 4px 8px;
  border-radius: 3px;
  cursor: pointer;
  font-size: 11px;
}

.delete-btn-small:hover {
  background-color: #ff5252;
}

.plant-name-btn {
  background: none;
  border: none;
  color: #4dabf7;
  text-decoration: underline;
  cursor: pointer;
  padding: 0;
  font: inherit;
}

.plant-name-btn:hover {
  color: #1a7ac7;
}

.selected-row {
  background-color: #e3f2fd !important;
  border-left: 4px solid #2196f3 !important;
}

.selected-row td {
  border-color: #bbdefb !important;
}

.selected-row:hover {
  background-color: #bbdefb !important;
}

.selected-row .plant-name-btn {
  color: #1565c0;
  font-weight: 600;
}

.plant-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.plant-id-subtitle {
  font-size: 11px;
  color: #666;
  background-color: #f5f5f5;
  padding: 2px 6px;
  border-radius: 10px;
  display: inline-block;
  align-self: flex-start;
  font-family: "Courier New", monospace;
}

.selected-row .plant-id-subtitle {
  background-color: #e3f2fd;
  color: #1565c0;
  font-weight: 500;
}

.plant-description {
  font-size: 12px;
  color: #777;
  margin-top: 4px;
  line-height: 1.3;
  font-style: italic;
}

.zone-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.zone-number {
  font-weight: 500;
  color: #333;
}

.unique-number {
  font-size: 11px;
  color: #888;
  background-color: #f0f0f0;
  padding: 1px 6px;
  border-radius: 8px;
  display: inline-block;
}

.age-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.age-value {
  font-weight: 500;
  color: #333;
}

.planted-date {
  font-size: 11px;
  color: #888;
}

.schedule-indicator {
  display: inline-block;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  text-align: center;
  line-height: 24px;
  font-weight: bold;
}

.schedule-indicator.yes {
  background-color: #4caf50;
  color: white;
}

.schedule-indicator.no {
  background-color: #f44336;
  color: white;
}

.selected-row .schedule-indicator.yes {
  background-color: #2e7d32;
  box-shadow: 0 0 0 2px #e3f2fd;
}

.selected-row .schedule-indicator.no {
  background-color: #c62828;
  box-shadow: 0 0 0 2px #e3f2fd;
}

.schedule-hint {
  font-size: 11px;
  color: #666;
  margin-top: 4px;
}

.selected-row .schedule-hint {
  color: #1565c0;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 6px;
  align-items: flex-start;
}

.details-btn {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 4px 8px;
  border-radius: 3px;
  cursor: pointer;
  font-size: 11px;
  transition: all 0.2s ease;
}

.details-btn:hover {
  background-color: #5a6268;
  transform: translateY(-1px);
}

.selected-row .details-btn {
  background-color: #2196f3;
}

.selected-row .details-btn:hover {
  background-color: #0b7dda;
}

[title] {
  position: relative;
}

[title]:hover::after {
  content: attr(title);
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background-color: #333;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  white-space: nowrap;
  z-index: 1000;
  margin-bottom: 5px;
  pointer-events: none;
}

[title]:hover::before {
  content: "";
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 5px solid transparent;
  border-top-color: #333;
  margin-bottom: -5px;
  pointer-events: none;
}
</style>
