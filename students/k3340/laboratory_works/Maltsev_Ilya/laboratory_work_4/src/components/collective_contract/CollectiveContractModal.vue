<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  contractData: {
    type: Object,
    default: () => ({}),
  },
  organizationData: {
    type: Object,
  },
  agents: {
    type: Array,
  },
  mode: {
    type: String,
    default: "add",
  },
});

const emits = defineEmits(["update:modelValue", "submit-contract"]);

const formData = ref({ ...props.contractData });

watch(
    () => props.contractData,
    (newVal) => {
      formData.value = { ...newVal };
    }
);

const contractStatuses = [
  { value: "a", text: "Активный" },
  { value: "p", text: "Приостановлен" },
  { value: "e", text: "Истёкший" },
];

const contractTypes = [
  { value: "m", text: "Медицинский" },
  { value: "l", text: "Страхование жизни и имущества" },
  { value: "a", text: "Несчастный случай" },
  { value: "g", text: "Ипотека" },
];

function closeModal() {
  emits("update:modelValue", false);
}

function handleSubmit() {
  const processedData = {
    ...formData.value,
    organization: props.organizationData.id,
    agent: typeof formData.value.agent === "object" ? formData.value.agent.id : formData.value.agent,
  };
  emits("submit-contract", processedData);
  closeModal();
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeModal" persistent max-width="500">
    <v-card>
      <v-card-title>{{ mode === "add" ? "Создать контракт" : "Редактировать контракт" }}</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleSubmit">
          <v-select
              v-model="formData.agent"
              :items="agents"
              :item-title="(item) => item.second_name + ' ' + item.first_name + ' ' + item.patronymic"
              item-value="id"
              label="Агент"
              required
          />

          <v-text-field v-model="formData.organization" type="text" disabled>{{ organizationData.full_name }}</v-text-field>
          <v-text-field v-model="formData.sign_date" label="Дата подписания" type="date" required></v-text-field>
          <v-text-field v-model="formData.start_date" label="Дата начала" type="date" required></v-text-field>
          <v-text-field v-model="formData.end_date" label="Дата окончания" type="date" required></v-text-field>

          <v-select
              v-model="formData.status"
              :items="contractStatuses"
              item-title="text"
              item-value="value"
              label="Статус контракта"
              required
          />

          <v-select
              v-model="formData.type"
              :items="contractTypes"
              item-title="text"
              item-value="value"
              label="Тип контракта"
              required
          />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="secondary" @click="closeModal">Отмена</v-btn>
        <v-btn color="primary" @click="handleSubmit">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
