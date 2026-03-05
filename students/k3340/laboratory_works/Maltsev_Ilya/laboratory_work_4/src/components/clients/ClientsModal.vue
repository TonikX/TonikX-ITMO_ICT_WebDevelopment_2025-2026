<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  clientData: {
    type: Object,
    default: () => ({}),
  },
  mode: {
    type: String,
    default: "add",
  },
});

const emits = defineEmits(["update:modelValue", "submit-client"]);

const formData = ref({ ...props.clientData });

watch(
    () => props.clientData,
    (newVal) => {
      formData.value = { ...newVal };
    }
);

function closeModal() {
  emits("update:modelValue", false);
}

function handleSubmit() {
  emits("submit-client", formData.value);
  closeModal();
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeModal" persistent max-width="500">
    <v-card>
      <v-card-title>{{ mode === "add" ? "Добавить клиента" : "Редактировать клиента" }}</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleSubmit">
          <v-text-field v-model="formData.first_name" label="Имя" required></v-text-field>
          <v-text-field v-model="formData.second_name" label="Фамилия" required></v-text-field>
          <v-text-field v-model="formData.patronymic" label="Отчество"></v-text-field>
          <v-text-field v-model="formData.age" label="Возраст" type="number" required></v-text-field>
          <v-text-field v-model="formData.passport" label="Паспорт" required></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="secondary" @click="closeModal">Отмена</v-btn>
        <v-btn color="primary" @click="handleSubmit">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
