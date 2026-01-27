<template>
  <v-card class="mb-4">
    <v-card-text>
      <p><strong>Сотрудник:</strong> {{ cleaningRecord.staff.last_name }} {{cleaningRecord.staff.first_name }} {{ cleaningRecord.staff.patronymic }}</p>
      <p><strong>Дата:</strong> {{ cleaningRecord.cleaning_date }}</p>
      <p><strong>Этаж id:</strong> {{ cleaningRecord.floor.id }}</p>
    </v-card-text>
    <v-card-actions>
      <v-btn
        icon="mdi-eye"
        size="small"
        variant="text"
        :to="`/cleaningRecords/${cleaningRecord.id}`"
        title="Просмотр"
      ></v-btn>
      <v-btn
        icon="mdi-pencil"
        size="small"
        variant="text"
        :to="`/cleaningRecords/${cleaningRecord.id}/edit`"
        title="Редактировать"
      ></v-btn>
      <v-btn
        icon="mdi-delete"
        size="small"
        variant="text"
        color="error"
        @click="onDelete"
        title="Удалить"
        :disabled="disableDelete"
      ></v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  cleaningRecord: {
    type: Object,
    required: true,
  },
  disableDelete: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['delete']);
const onDelete = () => {
  emit('delete');
};
</script>