<template>
  <v-card class="mb-4">
    <v-card-title>Проживание id: {{ livingRecord.id }}</v-card-title>
    <v-card-text>
      <p><strong>Начало:</strong> {{ livingRecord.start_date }}</p>
      <p><strong>Конец:</strong> {{ livingRecord.end_date }}</p>
      <p><strong>Гость:</strong> {{ livingRecord.guest.last_name }} {{livingRecord.guest.first_name }} {{ livingRecord.guest.patronymic }}</p>
      <p><strong>Номер:</strong> {{ livingRecord.room.number }}</p>
    </v-card-text>
    <v-card-actions>
      <v-btn
        icon="mdi-eye"
        size="small"
        variant="text"
        :to="`/livingRecords/${livingRecord.id}`"
        title="Просмотр"
      ></v-btn>
      <v-btn
        icon="mdi-pencil"
        size="small"
        variant="text"
        :to="`/livingRecords/${livingRecord.id}/edit`"
        title="Редактировать"
      ></v-btn>
      <v-btn
        icon="mdi-delete"
        size="small"
        variant="text"
        color="error"
        @click="onDelete"
        title="Удалить"
      ></v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
defineProps({
  livingRecord: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(['delete']);
const onDelete = () => {
  emit('delete');
};
</script>