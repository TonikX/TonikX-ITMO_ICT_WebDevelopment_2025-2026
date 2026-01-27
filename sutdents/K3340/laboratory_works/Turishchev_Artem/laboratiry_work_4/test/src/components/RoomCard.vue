<template>
  <v-card class="mb-4">
    <v-card-title>Номер {{ room.number }}</v-card-title>
    <v-card-text>
      <p><strong>Тип:</strong> {{ roomTypeLabel }}</p>
      <p><strong>Цена:</strong> {{ room.price }} ₽/день</p>
      <p><strong>Телефон:</strong> {{ room.phone }}</p>
      <p><strong>Этаж id:</strong> {{ floor }}</p>
    </v-card-text>
    <v-card-actions>
      <v-btn
        icon="mdi-eye"
        size="small"
        variant="text"
        :to="`/rooms/${room.id}`"
        title="Просмотр"
      ></v-btn>
      <v-btn
        icon="mdi-pencil"
        size="small"
        variant="text"
        :to="`/rooms/${room.id}/edit`"
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
  room: {
    type: Object,
    required: true,
  },
  floor: {
    type: Object,
    required: true,
  },
  disableDelete: {
    type: Boolean,
    default: false,
  },
});

const roomTypes = {
  single: 'Одноместный',
  double: 'Двухместный',
  triple: 'Трехместный',
};

const roomTypeLabel = computed(() => {
  return roomTypes[props.room.room_type] || props.room.room_type;
});

const emit = defineEmits(['delete']);
const onDelete = () => {
  emit('delete');
};
</script>