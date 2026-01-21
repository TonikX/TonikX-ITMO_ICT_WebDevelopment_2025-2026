<template>
  <div class="modal-backdrop">
    <div class="modal">
      <h3>Edit plant</h3>

      <form @submit.prevent="submit">
        <label>
          Species
          <select
            v-model.number="form.species"
            required
            :disabled="loadingSpecies"
          >
            <option disabled value="">Select species</option>
            <option v-for="sp in species" :key="sp.id" :value="sp.id">
              {{ sp.name }}
            </option>
          </select>
          <small v-if="loadingSpecies">Loading species...</small>
          <div v-if="currentSpeciesName" class="current-info">
            Current: {{ currentSpeciesName }}
          </div>
        </label>

        <label>
          Life form
          <input type="text" :value="selectedLifeForm" disabled />
        </label>

        <label>
          Description
          <textarea v-model="form.description"></textarea>
        </label>

        <label>
          Initial age (years)
          <input type="number" v-model.number="form.initial_age" min="0" />
        </label>

        <label>
          Current age (years) <small>(calculated)</small>
          <input type="number" :value="plant?.current_age || 0" disabled />
        </label>

        <div class="actions">
          <button type="submit" :disabled="!isDirty || saving">
            {{ saving ? "Saving..." : "Save" }}
          </button>
          <button type="button" @click="$emit('close')" :disabled="saving">
            Cancel
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { useAuthStore } from "@/store/auth";
import { updatePlant } from "@/services/plantService";
import { getSpecies, getSpeciesById } from "@/services/speciesService";

const props = defineProps({
  plant: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["close", "updated"]);
const auth = useAuthStore();

const species = ref([]);
const loadingSpecies = ref(true);
const saving = ref(false);
const currentSpeciesDetails = ref(null);

const form = ref({
  species: null,
  description: "",
  initial_age: 0,
});

const originalForm = ref({
  species: null,
  description: "",
  initial_age: 0,
});

const loadAllSpecies = async () => {
  try {
    loadingSpecies.value = true;
    const data = await getSpecies(auth.token);
    species.value = Array.isArray(data) ? data : data.results || [];

    initForm();
  } catch (error) {
    console.error("Failed to load species:", error);
    initForm();
  } finally {
    loadingSpecies.value = false;
  }
};

const initForm = () => {
  if (!props.plant) return;

  console.log("Plant data for editing:", props.plant);
  console.log("Plant species value:", props.plant.species);
  console.log("Plant species_details:", props.plant.species_details);

  const speciesId = props.plant.species || props.plant.species_details?.id;

  if (speciesId) {
    loadCurrentSpeciesDetails(speciesId);
  }

  form.value.species = speciesId;
  form.value.description = props.plant.description || "";
  form.value.initial_age = props.plant.initial_age || 0;

  originalForm.value.species = speciesId;
  originalForm.value.description = props.plant.description || "";
  originalForm.value.initial_age = props.plant.initial_age || 0;

  if (speciesId && !species.value.some((sp) => sp.id === speciesId)) {
    if (props.plant.species_details) {
      species.value.unshift(props.plant.species_details);
    } else if (currentSpeciesDetails.value) {
      species.value.unshift(currentSpeciesDetails.value);
    } else {
      species.value.unshift({
        id: speciesId,
        name: props.plant.species_details?.name || `Species #${speciesId}`,
        life_form: props.plant.species_details?.life_form || null,
      });
    }
  }
};

const loadCurrentSpeciesDetails = async (speciesId) => {
  try {
    currentSpeciesDetails.value = await getSpeciesById(speciesId, auth.token);
    console.log("Current species details loaded:", currentSpeciesDetails.value);
  } catch (err) {
    console.warn("Could not fetch species details:", err);
    if (props.plant.species_details) {
      currentSpeciesDetails.value = props.plant.species_details;
    }
  }
};

const isDirty = computed(() => {
  return (
    form.value.species !== originalForm.value.species ||
    form.value.description !== originalForm.value.description ||
    form.value.initial_age !== originalForm.value.initial_age
  );
});

const currentSpeciesName = computed(() => {
  if (props.plant.species_details?.name) {
    return props.plant.species_details.name;
  }

  if (currentSpeciesDetails.value?.name) {
    return currentSpeciesDetails.value.name;
  }

  const speciesId = props.plant.species;
  if (speciesId) {
    const sp = species.value.find((s) => s.id === speciesId);
    return sp?.name || `Species #${speciesId}`;
  }

  return "";
});

const selectedLifeForm = computed(() => {
  if (form.value.species) {
    const sp = species.value.find((s) => s.id === form.value.species);
    if (sp) {
      return sp.life_form?.name || sp.life_form_details?.name || "";
    }
  }
  return (
    currentSpeciesDetails.value?.life_form?.name ||
    currentSpeciesDetails.value?.life_form_details?.name ||
    props.plant.species_details?.life_form?.name ||
    ""
  );
});

const submit = async () => {
  if (!isDirty.value) {
    emit("close");
    return;
  }

  try {
    saving.value = true;

    const updateData = {
      species: form.value.species,
      description: form.value.description,
    };

    if (form.value.initial_age !== originalForm.value.initial_age) {
      updateData.initial_age = form.value.initial_age;
    }

    console.log("Sending update data:", updateData);

    await updatePlant(props.plant.id, updateData, auth.token);

    emit("updated");
    emit("close");
  } catch (error) {
    console.error("Failed to update plant:", error);
    console.error("Error response:", error.response?.data);
    alert(
      "Failed to update plant: " +
        (error.response?.data?.detail || error.message)
    );
  } finally {
    saving.value = false;
  }
};

onMounted(() => {
  loadAllSpecies();
});

watch(
  () => props.plant,
  () => {
    initForm();
  },
  { immediate: true }
);
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  padding: 20px;
  width: 400px;
  max-width: 90%;
  border-radius: 8px;
  z-index: 1001;
}

label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 12px;
  font-weight: 500;
}

select,
input,
textarea {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

select:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

textarea {
  min-height: 80px;
  resize: vertical;
}

input[type="number"] {
  width: 100px;
}

.actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

button[type="submit"] {
  background-color: #4caf50;
  color: white;
}

button[type="submit"]:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

button[type="button"] {
  background-color: #f0f0f0;
  color: #333;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

small {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
}

.current-info {
  margin-top: 5px;
  font-size: 0.9rem;
  color: #666;
  font-style: italic;
}
</style>
