<template>
  <v-dialog v-model="showModal" width="500" @click:outside="$emit('close')">
    <v-card>
      <v-card-title>Edit Plant</v-card-title>
      <v-form @submit.prevent="submit" class="pa-4">
        <v-select
          v-model="form.species"
          :items="species"
          item-title="name"
          item-value="id"
          label="Species"
          required
          :loading="loadingSpecies"
        ></v-select>

        <v-text-field
          :value="selectedLifeForm"
          label="Life Form"
          disabled
        ></v-text-field>

        <v-textarea
          v-model="form.description"
          label="Description"
          rows="3"
        ></v-textarea>

        <v-text-field
          v-model.number="form.initial_age"
          type="number"
          label="Initial Age"
          min="0"
        ></v-text-field>

        <v-text-field
          :value="plant?.current_age || 0"
          label="Current Age"
          disabled
        ></v-text-field>

        <div class="d-flex justify-space-between mt-4">
          <v-btn @click="$emit('close')" :disabled="saving">Cancel</v-btn>
          <v-btn
            type="submit"
            color="primary"
            :loading="saving"
            :disabled="!isDirty"
          >
            Save
          </v-btn>
        </div>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from "vue";
import { useAuthStore } from "@/store/auth";
import { updatePlant } from "@/services/plantService";
import { getSpecies } from "@/services/speciesService";

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
const showModal = ref(true);

const form = reactive({
  species: null,
  description: "",
  initial_age: 0,
});

const originalForm = reactive({
  species: null,
  description: "",
  initial_age: 0,
});

const loadAllSpecies = async () => {
  try {
    loadingSpecies.value = true;
    const data = await getSpecies(auth.token);
    species.value = data.results || data || [];
  } catch (error) {
    console.error("Failed to load species:", error);
  } finally {
    loadingSpecies.value = false;
  }
};

const initForm = () => {
  if (!props.plant) return;

  const speciesId = props.plant.species || props.plant.species_details?.id;

  form.species = speciesId;
  form.description = props.plant.description || "";
  form.initial_age = props.plant.initial_age || 0;

  originalForm.species = speciesId;
  originalForm.description = props.plant.description || "";
  originalForm.initial_age = props.plant.initial_age || 0;

  if (speciesId && !species.value.some((sp) => sp.id === speciesId)) {
    if (props.plant.species_details) {
      species.value.unshift(props.plant.species_details);
    }
  }
};

const isDirty = computed(() => {
  return (
    form.species !== originalForm.species ||
    form.description !== originalForm.description ||
    form.initial_age !== originalForm.initial_age
  );
});

const selectedLifeForm = computed(() => {
  if (form.species) {
    const sp = species.value.find((s) => s.id === form.species);
    return sp?.life_form?.name || "";
  }
  return "";
});

const submit = async () => {
  if (!isDirty.value) {
    emit("close");
    return;
  }

  try {
    saving.value = true;
    const updateData = {
      species: form.species,
      description: form.description,
    };

    if (form.initial_age !== originalForm.initial_age) {
      updateData.initial_age = form.initial_age;
    }

    await updatePlant(props.plant.id, updateData, auth.token);
    emit("updated");
    emit("close");
  } catch (error) {
    console.error("Failed to update plant:", error);
    alert("Failed to update plant");
  } finally {
    saving.value = false;
  }
};

onMounted(() => {
  loadAllSpecies();
  initForm();
});

watch(() => props.plant, initForm);
</script>
