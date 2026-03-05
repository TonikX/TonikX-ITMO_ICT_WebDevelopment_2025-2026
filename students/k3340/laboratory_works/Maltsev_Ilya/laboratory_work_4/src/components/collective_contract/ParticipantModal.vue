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
  clients: {
    type: Array
  },
  categories: {
    type: Array
  },
  mode: {
    type: String,
    default: "add",
  },
});

const emits = defineEmits(["update:modelValue", "submit-participant"]);

const formData = ref({ ...props.contractData });

watch(
    () => props.contractData,
    (newVal) => {
      formData.value = { ...newVal };
    }
);

function closeModal() {
  emits("update:modelValue", false);
}

function handleSubmit() {
  emits("submit-participant", {...formData.value, collective_contract: props.contractData.id});
  closeModal();
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeModal" persistent max-width="500">
    <v-card>
      <v-card-title>Добавить участника контракта</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleSubmit">
          <v-text-field v-model="formData.collective_contract" type="text" disabled>Контракт {{ contractData.id }}</v-text-field>
          <v-select
              v-model="formData.client"
              :items="clients"
              :item-title="(item) => item.second_name + ' ' + item.first_name + ' ' + item.patronymic"
              item-value="id"
              label="Клиент"
              required
          />
          <v-select
              v-model="formData.risk_category"
              :items="categories"
              :item-title="(item) => item.title + ' ' + item.payment_amount + '  р'"
              item-value="id"
              label="Категория риска"
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
