<script setup>
import {ref, watch} from "vue";

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  employeeData: {
    type: Object,
  },
  employees: {
    type: Array
  },
  cell: {
    type: Object
  },
  mode: {
    type: String,
    default: "add",
  },
});


const emits = defineEmits(["update:modelValue", "submit-employee"]);

const formData = ref({...props.employeeData});

watch(
    () => props.employeeData,
    (newVal) => {
      formData.value = {...newVal};
    }
);


function closeModal() {
  emits("update:modelValue", false);
}

function handleSubmit() {
  emits("submit-employee", {...formData.value, cell: props.cell.cell_code});
  closeModal();
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeModal" persistent max-width="500">
    <v-card>
      <v-card-title>{{ "Назначение сотрудника" }}</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleSubmit">
          <v-select
              v-model="formData.employee"
              :items="employees"
              :item-title="(item) => {return `${item.second_name} ${item.first_name} ${item.patronymic}`}"
              item-value="id"
              label="Сотрудник"/>
          <v-text-field v-model="formData.cell" required type="number" disabled>{{ cell.cell_code }}</v-text-field>
          <v-text-field
              label="Начало периода"
              v-model="formData.start_date"
              type="date"
          ></v-text-field>
          <v-text-field
              label="Конец периода"
              v-model="formData.end_date"
              type="date"
          ></v-text-field>
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