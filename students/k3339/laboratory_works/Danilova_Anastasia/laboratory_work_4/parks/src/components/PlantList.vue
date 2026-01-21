<template>
  <div class="plant-list">
    <div class="header">
      <h3>Plants</h3>
      <button
        @click="showCreatePlantModal = true"
        class="add-plant-btn"
        v-if="!isLoading"
      >
        + Add Plant
      </button>
    </div>

    <div v-if="isLoading" class="loading">Loading plants...</div>

    <div v-else>
      <table class="plants-table" v-if="plants.length">
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
                <button
                  @click="openEdit(placement.plant)"
                  class="edit-btn"
                  title="Edit plant"
                >
                  Edit
                </button>
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
      </table>

      <div v-else class="empty-state">
        <p>No plants found for this object</p>
        <button
          @click="showCreatePlantModal = true"
          class="add-plant-btn-empty"
        >
          + Add Your First Plant
        </button>
        <p class="empty-hint">Start by adding plants to this object</p>
      </div>

      <div v-if="count > pageSize" class="pagination">
        <button :disabled="!previous" @click="page--">Prev</button>
        <span> Page {{ page }} / {{ totalPages }} </span>
        <button :disabled="!next" @click="page++">Next</button>
      </div>
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
            <button @click="editWateringSchedule()" class="edit-btn">
              Edit
            </button>
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

    <div v-if="showCreatePlantModal" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h3>Add New Plant</h3>
          <button @click="showCreatePlantModal = false" class="close-btn">
            ×
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Species *</label>
            <select v-model="newPlant.species" class="form-control" required>
              <option value="">Select species</option>
              <option
                v-for="species in availableSpecies"
                :key="species.id"
                :value="species.id"
              >
                {{ species.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Zone *</label>
            <select v-model="newPlant.zone" class="form-control" required>
              <option value="">Select zone</option>
              <option
                v-for="zone in objectZones"
                :key="zone.id"
                :value="zone.id"
              >
                {{ zone.number }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Initial Age (years) *</label>
            <input
              v-model.number="newPlant.initial_age"
              type="number"
              min="0"
              class="form-control"
              required
              placeholder="Age when planted"
            />
          </div>
          <div class="form-group">
            <label>Unique Number in Zone *</label>
            <input
              v-model.number="newPlant.unique_number"
              type="number"
              min="1"
              class="form-control"
              required
              placeholder="Plant number in this zone"
            />
          </div>
          <div class="form-group">
            <label>Planted Date *</label>
            <input
              v-model="newPlant.planted_date"
              type="date"
              class="form-control"
              required
            />
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea
              v-model="newPlant.description"
              class="form-control"
              rows="3"
              placeholder="Additional details about the plant"
            ></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showCreatePlantModal = false" class="secondary-btn">
            Cancel
          </button>
          <button
            @click="createPlant"
            :disabled="creatingPlant"
            class="primary-btn"
          >
            {{ creatingPlant ? "Creating..." : "Create Plant" }}
          </button>
        </div>
      </div>
    </div>

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

const totalPages = computed(() => Math.ceil(count.value / pageSize.value));

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
    console.error("Error loading plants:", error);
  } finally {
    isLoading.value = false;
  }
};

const loadAdditionalData = async () => {
  try {
    const zonesData = await getObjectZones(props.objectId, auth.token);
    objectZones.value = zonesData.results || zonesData || [];
    console.log("Loaded zones:", objectZones.value);

    const speciesData = await getSpecies(auth.token);
    availableSpecies.value = speciesData.results || speciesData || [];
    console.log("Loaded species:", availableSpecies.value);
  } catch (error) {
    console.error("Error loading additional data:", error);
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
    alert("Please fill all required fields");
    return;
  }

  creatingPlant.value = true;
  try {
    const plantData = {
      species: parseInt(newPlant.species),
      initial_age: parseInt(newPlant.initial_age),
      description: newPlant.description || "",
    };

    console.log("Creating plant with data:", plantData);
    const createdPlant = await createPlantApi(plantData, auth.token);
    console.log("Created plant:", createdPlant);

    const placementData = {
      plant: createdPlant.id,
      zone: parseInt(newPlant.zone),
      unique_number: parseInt(newPlant.unique_number),
      planted_date: newPlant.planted_date,
    };

    console.log("Creating placement with data:", placementData);
    const createdPlacement = await createPlantPlacement(
      placementData,
      auth.token
    );
    console.log("Created placement:", createdPlacement);

    showCreatePlantModal.value = false;

    Object.assign(newPlant, {
      species: "",
      zone: "",
      initial_age: 1,
      unique_number: 1,
      planted_date: new Date().toISOString().split("T")[0],
      description: "",
    });

    await loadPlants();

    alert("Plant created successfully!");
  } catch (error) {
    console.error("Error creating plant:", error);
    alert(
      `Failed to create plant: ${
        error.response?.data?.detail || error.message || "Unknown error"
      }`
    );
  } finally {
    creatingPlant.value = false;
  }
};

const showPlantDetails = async (placement) => {
  console.log(`=== Showing details for plant ${placement.plant?.id} ===`);

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

  console.log(`Selected plant:`, selectedPlant.value);

  if (selectedPlant.value?.id) {
    await loadPlantSpecificData(selectedPlant.value.id);
  }
};

const loadPlantSpecificData = async (plantId) => {
  console.log(`=== Loading specific data for plant ${plantId} ===`);

  wateringSchedule.value = null;
  plantWorkerAssignments.value = [];

  loadingWatering.value = true;
  try {
    const schedule = await getPlantWateringSchedules(plantId, auth.token);
    console.log(`Schedule for plant ${plantId}:`, schedule);

    if (schedule && schedule.plant === plantId) {
      wateringSchedule.value = schedule;
      console.log(`Valid schedule found for plant ${plantId}`);
    } else if (schedule === null) {
      wateringSchedule.value = null;
      console.log(`No schedule for plant ${plantId}`);
    } else {
      console.warn(`Schedule plant mismatch: ${schedule.plant} !== ${plantId}`);
      wateringSchedule.value = null;
    }
  } catch (error) {
    console.error(`Error loading watering for plant ${plantId}:`, error);
    wateringSchedule.value = null;
  } finally {
    loadingWatering.value = false;
  }

  loadingWorkers.value = true;
  try {
    const data = await getPlantWorkerAssignments(plantId, auth.token);
    console.log(`Worker assignments API response for plant ${plantId}:`, data);

    if (data.results) {
      console.log(`Results count: ${data.results.length}`);
      data.results.forEach((assignment, index) => {
        console.log(`Assignment ${index}:`, assignment);
        console.log(`  - Plant ID: ${assignment.plant}`);
        console.log(`  - Worker:`, assignment.worker);
      });
      plantWorkerAssignments.value = data.results;
    } else if (Array.isArray(data)) {
      console.log(`Array count: ${data.length}`);
      data.forEach((assignment, index) => {
        console.log(
          `Assignment ${index}: plant=${assignment.plant}, worker=`,
          assignment.worker
        );
      });
      plantWorkerAssignments.value = data;
    } else {
      plantWorkerAssignments.value = [];
    }

    const filtered = plantWorkerAssignments.value.filter(
      (assignment) =>
        assignment.plant == plantId || assignment.plant?.id == plantId
    );

    if (filtered.length !== plantWorkerAssignments.value.length) {
      console.log(
        `Filtered: ${filtered.length} of ${plantWorkerAssignments.value.length} assignments are for plant ${plantId}`
      );
      plantWorkerAssignments.value = filtered;
    }
  } catch (error) {
    console.error(`Error loading workers for plant ${plantId}:`, error);
  } finally {
    loadingWorkers.value = false;
  }
};

const handleWateringScheduleUpdated = async () => {
  console.log(`=== Watering schedule updated, reloading data ===`);
  if (selectedPlant.value?.id) {
    await loadPlantSpecificData(selectedPlant.value.id);
  }
};

const handleWorkerAssignmentUpdated = async () => {
  console.log(`=== Worker assignment updated, reloading data ===`);
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
    console.error("Error formatting date:", error);
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
  console.log("Opening worker assignment modal...");
  console.log("Selected plant:", selectedPlant.value);
  console.log("Selected plant ID:", selectedPlant.value?.id);

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
    console.error("Error deleting worker assignment:", error);
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
</script>

<style scoped>
.plant-list {
  padding: 20px 0;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.add-plant-btn {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-plant-btn:hover {
  background-color: #218838;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(40, 167, 69, 0.3);
}

.plants-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
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

.plants-table th {
  background: #f5f5f5;
  padding: 12px;
  text-align: left;
  border-bottom: 2px solid #ddd;
  font-weight: 600;
}

.plants-table td {
  padding: 12px;
  border-bottom: 1px solid #eee;
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

.edit-btn {
  background-color: #4dabf7;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.empty-state {
  padding: 40px;
  text-align: center;
  color: #666;
  background: #f9f9f9;
  border-radius: 6px;
  margin-top: 20px;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state p {
  font-size: 1.1rem;
  color: #888;
  margin-bottom: 20px;
}

.add-plant-btn-empty {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 10px;
}

.add-plant-btn-empty:hover {
  background-color: #218838;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(40, 167, 69, 0.3);
}

.empty-hint {
  font-size: 0.9rem;
  color: #999;
  margin-top: 10px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 20px;
  padding: 20px;
}

.pagination button {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

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

.delete-btn {
  background-color: #ff6b6b;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
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

.delete-btn-small {
  background-color: #ff6b6b;
  color: white;
  border: none;
  padding: 4px 8px;
  border-radius: 3px;
  cursor: pointer;
  font-size: 11px;
}

.modal-overlay {
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

.form-group {
  margin-bottom: 15px;
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
.assignment-actions {
  display: flex;
  gap: 5px;
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

.selected-row .schedule-indicator.yes {
  background-color: #2e7d32;
  box-shadow: 0 0 0 2px #e3f2fd;
}

.selected-row .schedule-indicator.no {
  background-color: #c62828;
  box-shadow: 0 0 0 2px #e3f2fd;
}

.loading {
  padding: 40px;
  text-align: center;
  color: #666;
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }

  .add-plant-btn {
    align-self: flex-start;
  }

  .modal {
    width: 95%;
    margin: 10px;
  }
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

.plants-table td {
  vertical-align: top;
  padding-top: 12px;
  padding-bottom: 12px;
}

@media (max-width: 768px) {
  .plants-table {
    font-size: 14px;
  }

  .plant-id-subtitle,
  .unique-number,
  .planted-date,
  .schedule-hint {
    font-size: 10px;
  }

  .edit-btn,
  .details-btn {
    padding: 3px 6px;
    font-size: 10px;
  }

  .action-buttons {
    flex-direction: row;
    gap: 4px;
  }
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
