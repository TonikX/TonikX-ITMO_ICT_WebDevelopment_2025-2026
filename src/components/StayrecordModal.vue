<script setup>
import { ref, watch, computed } from "vue";

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  booking: {
    type: Object,
    default: () => ({
      client: "",
      room: "",
      check_in_date: "",
      check_out_date: "",
    }),
  },
  clients: {
    type: Array,
    default: () => [],
  },
  rooms: {
    type: Array,
    default: () => [],
  },
});

const emits = defineEmits(["update:modelValue", "save-booking"]);

const formData = ref({});

// Форматирование списка клиентов для отображения полного имени
const formattedClients = computed(() =>
  props.clients.map((client) => ({
    ...client,
    full_name: `${client.last_name} ${client.first_name} ${client.middle_name || ""}`.trim(),
  }))
);

watch(
  () => props.booking,
  (newVal) => {
    formData.value = { ...newVal };
  },
  { immediate: true, deep: true }
);

function closeModal() {
  emits("update:modelValue", false);
}

function handleSubmit() {
  emits("save-booking", {
    ...formData.value,
    client: formData.value.client, 
    room: formData.value.room,
  });
  closeModal();
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeModal" max-width="500">
    <v-card>
      <v-card-title>
        {{ booking?.id ? "Редактировать бронирование" : "Добавить бронирование" }}
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleSubmit">
          <!-- Поле выбора клиента -->
          <v-select
            v-model="formData.client"
            :items="formattedClients"
            item-title="full_name"
            item-value="id"
            label="Клиент"
            required
          />

          <!-- Поле выбора комнаты -->
          <v-select
            v-model="formData.room"
            :items="rooms"
            item-title="number"
            item-value="id"
            label="Комната"
            required
          />

          <!-- Поля ввода дат -->
          <v-text-field
            v-model="formData.check_in_date"
            label="Дата заезда"
            type="date"
            required
          ></v-text-field>
          <v-text-field
            v-model="formData.check_out_date"
            label="Дата выезда"
            type="date"
            required
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
.booking-card {
  margin-bottom: 16px;
}
</style>
