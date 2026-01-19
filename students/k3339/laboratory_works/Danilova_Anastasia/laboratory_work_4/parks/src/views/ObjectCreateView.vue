<template>
  <v-container>
    <v-btn @click="router.push('/dashboard')" class="mb-4">
      Back to Dashboard
    </v-btn>

    <v-card class="pa-4">
      <v-card-title>Create New Object</v-card-title>
      <v-card-subtitle>Add a new park to the system</v-card-subtitle>

      <v-form @submit.prevent="handleSubmit" class="mt-4">
        <v-text-field
          v-model="formData.name"
          label="Object Name"
          required
          :error="!!errors.name"
          :error-messages="errors.name"
          class="mb-3"
        ></v-text-field>

        <v-text-field
          v-model="formData.address"
          label="Address"
          required
          :error="!!errors.address"
          :error-messages="errors.address"
          class="mb-6"
        ></v-text-field>

        <v-card class="mb-6">
          <v-card-title>Decorators</v-card-title>
          <v-card-text>
            <v-select
              v-model="selectedDecorator"
              :items="decorators"
              item-title="full_name"
              item-value="id"
              label="Select decorator"
              :disabled="formData.decorators.includes(selectedDecorator)"
              @update:model-value="addDecorator"
            >
            </v-select>

            <div v-if="formData.decorators.length > 0" class="mt-3">
              <v-chip
                v-for="decoratorId in formData.decorators"
                :key="decoratorId"
                class="mr-2 mb-2"
                closable
                @click:close="removeDecorator(decoratorId)"
              >
                {{ getDecoratorName(decoratorId) }}
              </v-chip>
            </div>
            <v-alert type="info" variant="tonal" class="mt-3">
              Optional: Select decorators responsible for this object
            </v-alert>
          </v-card-text>
        </v-card>

        <div class="d-flex justify-space-between">
          <v-btn @click="router.push('/dashboard')" :disabled="loading">
            Cancel
          </v-btn>
          <v-btn type="submit" color="primary" :loading="loading">
            Create Object
          </v-btn>
        </div>

        <v-alert v-if="error" type="error" class="mt-4">
          {{ error }}
        </v-alert>
      </v-form>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store/auth";
import { createObject } from "@/services/objectsService";
import { getDecorators } from "@/services/objectsService";

const router = useRouter();
const auth = useAuthStore();

const formData = reactive({
  name: "",
  address: "",
  decorators: [],
});

const loading = ref(false);
const error = ref("");
const errors = reactive({
  name: "",
  address: "",
});

const decorators = ref([]);
const selectedDecorator = ref("");

onMounted(async () => {
  try {
    const data = await getDecorators(auth.token);
    decorators.value = data.results || data || [];
  } catch (err) {
    console.error("Error loading decorators:", err);
  }
});

const getDecoratorName = (decoratorId) => {
  const decorator = decorators.value.find((d) => d.id === decoratorId);
  return decorator ? decorator.full_name : `Decorator #${decoratorId}`;
};

const addDecorator = () => {
  if (
    selectedDecorator.value &&
    !formData.decorators.includes(selectedDecorator.value)
  ) {
    formData.decorators.push(selectedDecorator.value);
    selectedDecorator.value = "";
  }
};

const removeDecorator = (decoratorId) => {
  const index = formData.decorators.indexOf(decoratorId);
  if (index > -1) {
    formData.decorators.splice(index, 1);
  }
};

const validateForm = () => {
  let isValid = true;

  errors.name = "";
  errors.address = "";

  if (!formData.name.trim()) {
    errors.name = "Object name is required";
    isValid = false;
  }

  if (!formData.address.trim()) {
    errors.address = "Address is required";
    isValid = false;
  }

  return isValid;
};

const handleSubmit = async () => {
  if (!validateForm()) {
    return;
  }

  error.value = "";
  const submitData = {
    name: formData.name.trim(),
    address: formData.address.trim(),
    decorators: formData.decorators,
  };

  loading.value = true;

  try {
    const response = await createObject(submitData, auth.token);
    router.push(`/objects/${response.id}`);
  } catch (err) {
    console.error("Error creating object:", err);

    if (err.response?.data) {
      const errorData = err.response.data;

      if (errorData.name) {
        errors.name = Array.isArray(errorData.name)
          ? errorData.name[0]
          : errorData.name;
      }
      if (errorData.address) {
        errors.address = Array.isArray(errorData.address)
          ? errorData.address[0]
          : errorData.address;
      }

      if (!errors.name && !errors.address && errorData.detail) {
        error.value = errorData.detail;
      } else if (errorData.non_field_errors) {
        error.value = Array.isArray(errorData.non_field_errors)
          ? errorData.non_field_errors[0]
          : errorData.non_field_errors;
      }
    } else if (err.message) {
      error.value = err.message;
    } else {
      error.value = "Failed to create object";
    }
  } finally {
    loading.value = false;
  }
};
</script>
