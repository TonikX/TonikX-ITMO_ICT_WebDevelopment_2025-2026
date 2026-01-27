<template>
  <v-card class="mb-4">
    <v-card-title>{{ staff.last_name }} {{staff.first_name }} {{ staff.patronymic }}</v-card-title>
    <v-card-text>
      <p><strong>Id:</strong> {{ staff.id }}</p>
    </v-card-text>
    <v-card-actions>
      <v-btn
        icon="mdi-eye"
        size="small"
        variant="text"
        :to="`/staff/${staff.id}`"
        title="Просмотр"
      ></v-btn>
      <v-btn
        icon="mdi-pencil"
        size="small"
        variant="text"
        :to="`/staff/${staff.id}/edit`"
        title="Редактировать"
      ></v-btn>
      <v-btn
        icon="mdi-delete"
        size="small"
        variant="text"
        color="error"
        @click="onDelete"
        :disabled="disableDelete"
        title="Удалить"
      ></v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>

const props = defineProps({
  staff: {
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