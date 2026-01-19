<template>
  <v-form @submit.prevent="emit('submit', form)">
    <v-text-field v-model="form.name" label="Name" required></v-text-field>

    <v-text-field
      v-model="form.address"
      label="Address"
      required
    ></v-text-field>

    <v-btn type="submit" color="primary">{{ submitLabel }}</v-btn>
  </v-form>
</template>

<script setup>
import { ref, onMounted } from "vue";

const props = defineProps({
  initialData: Object,
  submitLabel: String,
});

const emit = defineEmits(["submit"]);

const form = ref({
  name: "",
  address: "",
});

onMounted(() => {
  if (props.initialData) {
    form.value = { ...props.initialData };
  }
});
</script>
