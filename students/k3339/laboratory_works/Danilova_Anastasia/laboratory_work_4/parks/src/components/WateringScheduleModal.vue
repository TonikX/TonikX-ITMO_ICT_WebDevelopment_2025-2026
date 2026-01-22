<template>
  <v-dialog v-model="showModal" width="500" @click:outside="$emit('close')">
    <v-card>
      <v-card-title>
        {{ wateringSchedule ? "Edit" : "Add" }} Watering Schedule
        <v-spacer></v-spacer>
        <v-btn icon @click="$emit('close')">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-form @submit.prevent="submit" class="pa-4">
        <v-text-field
          v-model="form.frequency"
          label="Frequency"
          placeholder="e.g., Once a day, Twice a week"
          required
          class="mb-3"
        ></v-text-field>

        <v-row>
          <v-col cols="6">
            <v-text-field
              v-model="form.time_watering_start"
              type="time"
              label="Watering Start Time"
              required
            ></v-text-field>
          </v-col>
          <v-col cols="6">
            <v-text-field
              v-model="form.time_watering_end"
              type="time"
              label="Watering End Time"
              required
            ></v-text-field>
          </v-col>
        </v-row>

        <v-card class="mb-4">
          <v-card-title>Water Norms (liters)</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="6">
                <v-text-field
                  v-model.number="form.water_norm_liters_spring"
                  type="number"
                  label="Spring"
                  min="0"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model.number="form.water_norm_liters_summer"
                  type="number"
                  label="Summer"
                  min="0"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model.number="form.water_norm_liters_fall"
                  type="number"
                  label="Fall"
                  min="0"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model.number="form.water_norm_liters_winter"
                  type="number"
                  label="Winter"
                  min="0"
                  required
                ></v-text-field>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <div class="d-flex justify-space-between">
          <v-btn @click="$emit('close')" :disabled="saving">Cancel</v-btn>
          <v-btn type="submit" color="primary" :loading="saving">Save</v-btn>
        </div>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { useAuthStore } from "@/store/auth";
import {
  createWateringSchedule,
  updateWateringSchedule,
} from "@/services/wateringService";

const props = defineProps({
  plantId: {
    type: Number,
    required: true,
  },
  wateringSchedule: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(["close", "updated"]);
const auth = useAuthStore();
const saving = ref(false);
const showModal = ref(true);

const form = reactive({
  frequency: "",
  time_watering_start: "08:00",
  time_watering_end: "18:00",
  water_norm_liters_spring: 0,
  water_norm_liters_summer: 0,
  water_norm_liters_fall: 0,
  water_norm_liters_winter: 0,
});

const initForm = () => {
  if (props.wateringSchedule) {
    Object.assign(form, {
      frequency: props.wateringSchedule.frequency || "",
      time_watering_start:
        props.wateringSchedule.time_watering_start || "08:00",
      time_watering_end: props.wateringSchedule.time_watering_end || "18:00",
      water_norm_liters_spring:
        props.wateringSchedule.water_norm_liters_spring || 0,
      water_norm_liters_summer:
        props.wateringSchedule.water_norm_liters_summer || 0,
      water_norm_liters_fall:
        props.wateringSchedule.water_norm_liters_fall || 0,
      water_norm_liters_winter:
        props.wateringSchedule.water_norm_liters_winter || 0,
    });
  }
};

const submit = async () => {
  saving.value = true;
  try {
    const scheduleData = {
      plant: props.plantId,
      ...form,
    };

    if (props.wateringSchedule) {
      await updateWateringSchedule(
        props.wateringSchedule.id,
        scheduleData,
        auth.token
      );
    } else {
      await createWateringSchedule(scheduleData, auth.token);
    }

    emit("updated");
    emit("close");
  } catch (error) {
    console.error("Error saving watering schedule:", error);
    alert(`Failed to save: ${error.response?.data?.detail || error.message}`);
  } finally {
    saving.value = false;
  }
};

onMounted(() => {
  initForm();
});
</script>
