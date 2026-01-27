<template>
  <v-card class="mb-4">
    <v-card-title>Этаж №{{ floor.number }}</v-card-title>
    <v-card-text>
      {{ floor.description || 'Без описания' }}
    </v-card-text>
    <v-card-actions>
      <v-btn
        icon="mdi-eye"
        size="small"
        variant="text"
        :to="`/floors/${floor.id}`"
        title="Просмотр"
      ></v-btn>
      <v-btn
        icon="mdi-pencil"
        size="small"
        variant="text"
        :to="`/floors/${floor.id}/edit`"
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
  floor: {
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