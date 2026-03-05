<script setup>
import {ref, watch} from "vue";

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  chickenData: {
    type: Object,
  },
  cells: {
    type: Array
  },
  mode: {
    type: String,
    default: "add",
  },
});


const emits = defineEmits(["update:modelValue", "submit-chicken"]);

const formData = ref({...props.chickenData});
watch(
    () => props.chickenData,
    (newVal) => {
      formData.value = {...newVal};
    }
);


function closeModal() {
  emits("update:modelValue", false);
}

function handleSubmit() {
  emits("submit-chicken", {...formData.value, cell: formData.value.cell, breed: formData.value.breed.id});
  closeModal();
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeModal" persistent max-width="500">
    <v-card>
      <v-card-title>{{ "Перемещение курицы" }}</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleSubmit">
          <v-select
              v-model="formData.cell"
              :items="cells"
              item-title="cell_code"
              item-value="cell_code"
              label="Клетка"/>
          <v-text-field
              v-model="formData.id"
              type="text"
              disabled
          > Курица номер {{ formData.id }}</v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="secondary" @click="closeModal">Отмена</v-btn>
        <v-btn color="primary" @click="handleSubmit">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>

</style>