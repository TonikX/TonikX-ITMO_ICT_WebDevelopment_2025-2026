<template>
  <v-card class="mb-4">
    <v-card-title>{{ guest.last_name }} {{guest.first_name }} {{ guest.patronymic }}</v-card-title>
    <v-card-text>
      <p><strong>Паспорт:</strong> {{ guest.passport_number }}</p>
      <p><strong>Город:</strong> {{ guest.city }}</p>
    </v-card-text>
    <v-card-actions>
      <v-btn
        icon="mdi-eye"
        size="small"
        variant="text"
        :to="`/guests/${guest.id}`"
        title="Просмотр"
      ></v-btn>
      <v-btn
        icon="mdi-pencil"
        size="small"
        variant="text"
        :to="`/guests/${guest.id}/edit`"
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
defineProps({
  guest: {
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