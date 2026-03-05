<script setup>
import {ref, watch} from "vue";

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  organizationData: {
    type: Object
  },
  mode: {
    type: String,
    default: "add",
  },
});

const emits = defineEmits(["update:modelValue", "submit-organization"]);

const formData = ref({...props.organizationData});

watch(
    () => props.organizationData,
    (newVal) => {
      formData.value = {...newVal};
    }
);

function closeModal() {
  emits("update:modelValue", false);
}

function handleSubmit() {
  emits("submit-organization", formData.value);
  closeModal();
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeModal" persistent max-width="500">
    <v-card>
      <v-card-title>{{ mode === "add" ? "Добавить организацию" : "Редактировать организацию" }}</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleSubmit">
          <v-text-field v-model="formData.full_name" label="Полное название" required></v-text-field>
          <v-text-field v-model="formData.short_name" label="Короткое название" required></v-text-field>
          <v-text-field v-model="formData.address" label="Адрес" required></v-text-field>
          <v-text-field v-model="formData.bank_code" label="Банковский код" required></v-text-field>
          <v-text-field v-model="formData.specialization" label="Специализация" required></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="secondary" @click="closeModal">Отмена</v-btn>
        <v-btn color="primary" @click="handleSubmit">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
