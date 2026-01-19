<template>
  <v-card class="mb-6">
    <v-card-title>
      Plants
      <v-spacer></v-spacer>
      <v-btn @click="showCreatePlantModal = true" v-if="!isLoading">
        + Add Plant
      </v-btn>
    </v-card-title>

    <div v-if="isLoading" class="text-center pa-4">Loading plants...</div>

    <v-table v-else-if="plants.length">
      <thead>
        <tr>
          <th>ID</th>
          <th>Species</th>
          <th>Zone</th>
          <th>Age</th>
          <th>Schedule</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="placement in plants" :key="placement.id">
          <td>{{ placement.id }}</td>
          <td>
            <v-btn @click="showPlantDetails(placement)" variant="text">
              {{ placement.plant?.species_details?.name || "Unknown" }}
            </v-btn>
            <div class="text-caption">Plant ID: {{ placement.plant?.id }}</div>
          </td>
          <td>
            {{ placement.zone_number || "-" }}
            <div v-if="placement.unique_number" class="text-caption">
              #{{ placement.unique_number }}
            </div>
          </td>
          <td>
            {{ placement.plant?.current_age || 0 }} years
            <div v-if="placement.planted_date" class="text-caption">
              Planted: {{ formatDate(placement.planted_date) }}
            </div>
          </td>
          <td>
            <v-chip
              :color="placement.plant?.has_watering_schedule ? 'green' : 'grey'"
            >
              {{ placement.plant?.has_watering_schedule ? "yes" : "no" }}
            </v-chip>
          </td>
          <td>
            <v-btn @click="openEdit(placement.plant)" size="small" class="mr-2">
              Edit
            </v-btn>
            <v-btn @click="showPlantDetails(placement)" size="small">
              Details
            </v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>

    <div v-else class="text-center pa-4">
      <p>No plants found for this object</p>
      <v-btn @click="showCreatePlantModal = true">+ Add Your First Plant</v-btn>
    </div>

    <div v-if="count > pageSize" class="d-flex justify-center pa-4">
      <v-btn @click="prevPage" :disabled="page === 1">Prev</v-btn>
      <span class="mx-4">Page {{ page }} / {{ totalPages }}</span>
      <v-btn @click="nextPage" :disabled="page * pageSize >= count">Next</v-btn>
    </div>

    <v-dialog v-model="showCreatePlantModal" width="500">
      <v-card>
        <v-card-title>Add New Plant</v-card-title>
        <v-form @submit.prevent="createPlant" class="pa-4">
          <v-select
            v-model="newPlant.species"
            :items="availableSpecies"
            item-title="name"
            item-value="id"
            label="Species"
            required
          ></v-select>

          <v-select
            v-model="newPlant.zone"
            :items="objectZones"
            item-title="number"
            item-value="id"
            label="Zone"
            required
          ></v-select>

          <v-text-field
            v-model.number="newPlant.initial_age"
            type="number"
            label="Initial Age"
            min="0"
            required
          ></v-text-field>

          <v-text-field
            v-model.number="newPlant.unique_number"
            type="number"
            label="Unique Number"
            min="1"
            required
          ></v-text-field>

          <v-text-field
            v-model="newPlant.planted_date"
            type="date"
            label="Planted Date"
            required
          ></v-text-field>

          <v-textarea
            v-model="newPlant.description"
            label="Description"
            rows="3"
          ></v-textarea>

          <div class="d-flex justify-space-between mt-4">
            <v-btn @click="showCreatePlantModal = false">Cancel</v-btn>
            <v-btn type="submit" color="primary" :loading="creatingPlant">
              Create Plant
            </v-btn>
          </div>
        </v-form>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showPlantDetailsDialog" width="600">
      <v-card v-if="selectedPlant">
        <v-card-title>
          {{ selectedPlant.species_details?.name || "Plant Details" }}
          <v-spacer></v-spacer>
          <v-btn icon @click="showPlantDetailsDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-tabs v-model="activeDetailTab" class="mb-4">
          <v-tab value="watering">Watering</v-tab>
          <v-tab value="workers">Workers</v-tab>
        </v-tabs>

        <v-window v-model="activeDetailTab">
          <v-window-item value="watering">
            <v-card-text>
              <div class="d-flex justify-space-between align-center mb-4">
                <h4>Watering Schedule</h4>
                <v-btn @click="showWateringModal = true">
                  {{ wateringSchedule ? "Edit" : "Add" }}
                </v-btn>
              </div>

              <div v-if="wateringSchedule">
                <v-list>
                  <v-list-item>
                    <v-list-item-title>Frequency</v-list-item-title>
                    <v-list-item-subtitle>{{
                      wateringSchedule.frequency
                    }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Time Period</v-list-item-title>
                    <v-list-item-subtitle>{{
                      wateringSchedule.watering_time_period
                    }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Current Norm</v-list-item-title>
                    <v-list-item-subtitle
                      >{{
                        wateringSchedule.current_water_norm_liters
                      }}
                      L</v-list-item-subtitle
                    >
                  </v-list-item>
                </v-list>

                <v-row class="mt-4">
                  <v-col cols="6"
                    >Spring:
                    {{ wateringSchedule.water_norm_liters_spring }}L</v-col
                  >
                  <v-col cols="6"
                    >Summer:
                    {{ wateringSchedule.water_norm_liters_summer }}L</v-col
                  >
                  <v-col cols="6"
                    >Fall: {{ wateringSchedule.water_norm_liters_fall }}L</v-col
                  >
                  <v-col cols="6"
                    >Winter:
                    {{ wateringSchedule.water_norm_liters_winter }}L</v-col
                  >
                </v-row>
              </div>
              <div v-else class="text-center pa-4">
                No watering schedule set
              </div>
            </v-card-text>
          </v-window-item>

          <v-window-item value="workers">
            <v-card-text>
              <div class="d-flex justify-space-between align-center mb-4">
                <h4>Worker Assignments</h4>
                <v-btn @click="showWorkerModal = true">+ Assign</v-btn>
              </div>

              <v-table v-if="plantWorkerAssignments.length">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Worker</th>
                    <th>Phone</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="assignment in plantWorkerAssignments"
                    :key="assignment.id"
                  >
                    <td>{{ formatDate(assignment.date) }}</td>
                    <td>{{ assignment.worker?.full_name || "Unknown" }}</td>
                    <td>{{ assignment.worker?.phone_number || "-" }}</td>
                    <td>
                      <v-btn
                        @click="openWorkerAssignment(assignment)"
                        size="small"
                        class="mr-2"
                      >
                        Edit
                      </v-btn>
                      <v-btn
                        @click="deleteWorkerAssignment(assignment.id)"
                        color="error"
                        size="small"
                      >
                        Remove
                      </v-btn>
                    </td>
                  </tr>
                </tbody>
              </v-table>
              <div v-else class="text-center pa-4">No worker assignments</div>
            </v-card-text>
          </v-window-item>
        </v-window>
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
  </v-card>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from "vue";
import { useAuthStore } from "@/store/auth";
import {
  getPlantsByObject,
  createPlant,
  createPlantPlacement,
} from "@/services/plantService";
import { getPlantWateringSchedules } from "@/services/wateringService";
import {
  getPlantWorkerAssignments,
  deletePlantWorkerAssignment,
} from "@/services/plantWorkerService";
import { getObjectZones } from "@/services/objectsService";
import { getSpecies } from "@/services/speciesService";
import WateringScheduleModal from "@/components/WateringScheduleModal.vue";
import WorkerAssignmentModal from "@/components/WorkerAssignmentModal.vue";
import PlantEditModal from "@/components/PlantEditModal.vue";

const props = defineProps({ objectId: Number });
const auth = useAuthStore();

const plants = ref([]);
const isLoading = ref(false);
const page = ref(1);
const count = ref(0);
const pageSize = ref(15);

const selectedPlant = ref(null);
const activeDetailTab = ref("watering");
const wateringSchedule = ref(null);
const plantWorkerAssignments = ref([]);

const showEditModal = ref(false);
const editingPlant = ref(null);
const showWateringModal = ref(false);
const showWorkerModal = ref(false);
const showCreatePlantModal = ref(false);
const showPlantDetailsDialog = ref(false);
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

    const speciesData = await getSpecies(auth.token);
    availableSpecies.value = speciesData.results || speciesData || [];
  } catch (error) {
    console.error("Error loading additional data:", error);
  }
};

const createPlantHandler = async () => {
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

    const createdPlant = await createPlant(plantData, auth.token);

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

    await loadPlants();
  } catch (error) {
    console.error("Error creating plant:", error);
    alert("Failed to create plant");
  } finally {
    creatingPlant.value = false;
  }
};

const showPlantDetails = async (placement) => {
  selectedPlant.value = placement.plant;
  showPlantDetailsDialog.value = true;
  activeDetailTab.value = "watering";

  if (selectedPlant.value?.id) {
    try {
      const schedule = await getPlantWateringSchedules(
        selectedPlant.value.id,
        auth.token
      );
      wateringSchedule.value =
        schedule?.plant === selectedPlant.value.id ? schedule : null;
    } catch (error) {
      wateringSchedule.value = null;
    }

    try {
      const data = await getPlantWorkerAssignments(
        selectedPlant.value.id,
        auth.token
      );
      plantWorkerAssignments.value = data.results || data || [];
    } catch (error) {
      plantWorkerAssignments.value = [];
    }
  }
};

const handleWateringScheduleUpdated = async () => {
  if (selectedPlant.value?.id) {
    try {
      const schedule = await getPlantWateringSchedules(
        selectedPlant.value.id,
        auth.token
      );
      wateringSchedule.value =
        schedule?.plant === selectedPlant.value.id ? schedule : null;
    } catch (error) {
      wateringSchedule.value = null;
    }
  }
};

const handleWorkerAssignmentUpdated = async () => {
  if (selectedPlant.value?.id) {
    try {
      const data = await getPlantWorkerAssignments(
        selectedPlant.value.id,
        auth.token
      );
      plantWorkerAssignments.value = data.results || data || [];
    } catch (error) {
      plantWorkerAssignments.value = [];
    }
  }
};

const formatDate = (dateString) => {
  if (!dateString) return "-";
  return new Date(dateString).toLocaleDateString();
};

const openEdit = (plant) => {
  editingPlant.value = plant;
  showEditModal.value = true;
};

const openWorkerAssignment = (assignment = null) => {
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
      const data = await getPlantWorkerAssignments(
        selectedPlant.value.id,
        auth.token
      );
      plantWorkerAssignments.value = data.results || data || [];
    }
  } catch (error) {
    console.error("Error deleting worker assignment:", error);
    alert("Failed to delete");
  }
};

const prevPage = () => {
  if (page.value > 1) {
    page.value--;
    loadPlants();
  }
};

const nextPage = () => {
  if (page.value * pageSize.value < count.value) {
    page.value++;
    loadPlants();
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

watch(page, loadPlants);
</script>
